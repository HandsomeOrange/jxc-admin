import argparse
import csv
import json
import re
import sys
import threading
import time
import traceback
import urllib.request
import uuid
from urllib.error import HTTPError
import export_constants
import requests
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
ELLIOT_TEMPLATE = 2


def get_page(url, page, collection_handle=None):
    full_url = url
    if collection_handle:
        full_url += '/collections/{}'.format(collection_handle)
    full_url += '/products.json'
    req = urllib.request.Request(
        full_url + '?sort_by=best-selling&page={}'.format(page),
        data=None,
        headers={
            'User-Agent': USER_AGENT
        }
    )
    while True:
        try:
            data = urllib.request.urlopen(req).read()
            break
        except HTTPError:
            print('Blocked! Sleeping...')
            time.sleep(180)
            print('Retrying')

    products = json.loads(data.decode())['products']
    return products


def get_page_collections(url):
    full_url = url + '/collections.json'
    page = 1
    while True:
        req = urllib.request.Request(
            full_url + '?page={}'.format(page),
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        while True:
            try:
                data = urllib.request.urlopen(req).read()
                break
            except HTTPError:
                print('Blocked! Sleeping...')
                time.sleep(180)
                print('Retrying')

        cols = json.loads(data.decode())['collections']
        if not cols:
            break
        for col in cols:
            yield col
        page += 1


def check_shopify(url):
    try:
        get_page(url, 1)
        return True
    except Exception:
        return False


def fix_url(url):
    fixed_url = url.strip()
    if not fixed_url.startswith('http://') and \
            not fixed_url.startswith('https://'):
        fixed_url = 'https://' + fixed_url

    return fixed_url.rstrip('/')


def extract_products_collection(url, col):
    page = 1
    products = get_page(url, page, col)
    total_pages = []
    total_pages += products
    while products and len(products):
        page += 1
        products = get_page(url, page, col)
        total_pages += products
    return total_pages


def extract_shopify_products(url, path, collections=None, delimiter=","):
    try:
        rows_data = []
        seen_variants = set()
        product_num = 1
        for col in get_page_collections(url):
            if collections and col['handle'] not in collections:
                continue
            handle = col['handle']
            title = col['title']
            for product in extract_products_collection(url, handle):
                p_id = product['id']
                if p_id in seen_variants:
                    continue
                seen_variants.add(p_id)
                ret = format_row_data(product)
                for i in ret:
                    rows_data.append(i)
                product_num += 1
        __write_output_file(rows_data, path, delimiter, product_num)
    except Exception as e:
        traceback.print_exc()


def __write_output_file(rows_data, path, delimiter=",", product_num=0):
    if not rows_data or not len(rows_data):
        return
        # utf - 8 - sig
    with open(path, 'w', encoding='utf-8', newline='') as f:
        # f.write(str(codecs.BOM_UTF8))
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(get_headers())
        for row in rows_data:
            writer.writerow(row)
    print(f'save {path} success end.... product_num{product_num}')


def get_headers():
    csv_headers = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published']
    for i in range(1, 4):
        csv_headers += [f'Option{i} Name', f'Option{i} Value']
    csv_headers += ['Variant SKU',
                    'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy',
                    'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price',
                    'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position',
                    'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
                    'Google Shopping / Google Product Category', 'Google Shopping / Gender',
                    'Google Shopping / Age Group', 'Google Shopping / MPN', 'Google Shopping / AdWords Grouping',
                    'Google Shopping / AdWords Labels', 'Google Shopping / Condition',
                    'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0',
                    'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2',
                    'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image',
                    'Variant Weight Unit', 'Variant Tax Code', 'Cost per item']
    return csv_headers


def format_row_data(product):
    variants = []
    # metafields = []
    if 'variants' in product:
        variants = product['variants']
    # if 'metafields' in product['product'] and len(product['product']['metafields']):
    #     metafields = product['product']['metafields']
    _images = []
    if 'images' in product and len(product['images']):
        _images = product['images']
    option_names = []
    for op in product['options']:
        option_names.insert(int(op['position']) - 1, op['name'])
    #  'Base Price(USD)', 'Sale Price(USD)', 'Quantity', 'Unit of Weight', 'Weight', 'Unit of Dimensions', 'Height', 'Width', 'Length', 'SEO Title', 'SEO Description']
    products = []
    index = 1
    weight = ''
    unit_of_weight = ''
    for i in variants:
        if 'weight_unit' in i:
            unit_of_weight = i['weight_unit']
            weight = i['weight']
        if 'grams' in i:
            unit_of_weight = 'grams'
            weight = i['grams']
        # for meta in metafields:
        #     if meta == 'metafields_global_title_tag':
        #         seo_title = metafields[meta]
        #     if meta == 'metafields_global_description_tag':
        #         seo_desc = metafields[meta]
        #     if 'name' in meta and meta['name'] == 'metafields_global_title_tag':
        #         if 'value' in meta:
        #             seo_title = meta['value']
        #         else:
        #             seo_title = str(meta)
        #     if 'name' in meta and meta['name'] == 'metafields_global_description_tag':
        #         if 'value' in meta:
        #             seo_desc = meta['value']
        #         else:
        #             seo_desc = str(meta)
        # print(i)
        pic_url = ''
        if 'featured_image' in i:
            pic_url = i['featured_image']['src'].split('?')[0] if i['featured_image'] and i[
                'featured_image']['src'] else ''
        elif len(_images) and index <= len(_images):
            pic_url = _images[index - 1]['src'] if 'src' in _images[index - 1] else ''
        products.append([product['handle'], product['title'], product['body_html'],
                         product['vendor'], product['product_type'],
                         ','.join(product['tags']) if type(product['tags']) == list else product['tags'],
                         product['published_at'], option_names[0] if len(option_names) >= 1 else '', i['option1'],
                         option_names[1] if len(option_names) >= 2 else '', i['option2'],
                         option_names[2] if len(option_names) >= 3 else '', i['option3'],
                         i['sku'], weight, 'shopify', '', '',
                         "", i['price'], i['compare_at_price'], i['requires_shipping'], i['taxable'],
                         '', pic_url, index, '', '', product['title'], product['title'],
                         '', '', '', '', '', '', '', '', '', '', '', '', '', pic_url,
                         format_unit_weight(unit_of_weight), '', ''
                         # ,quantity,format_unit_weight(unit_of_weight), weight, "IN", "3", "3","3", seo_title, seo_desc
                         ])
        index += 1
    if len(products) == 0:
        products.append([product['handle'], product['title'], product['body_html'],
                         product['vendor'], product['product_type'], ','.join(product['tags']),
                         product['published_at'], option_names[0] if len(option_names) >= 1 else '', '',
                         option_names[1] if len(option_names) >= 2 else '', '',
                         option_names[2] if len(option_names) >= 3 else '', '',
                         '', weight, 'shopify', '', '',
                         '', '', '', '', '',
                         '', '', index, '', '', product['title'], product['title'],
                         '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                         format_unit_weight(unit_of_weight), '', ''
                         # ,quantity,format_unit_weight(unit_of_weight), weight, "IN", "3", "3","3", seo_title, seo_desc
                         ])
    return products


def format_unit_weight(w):
    if w.lower() == "ounces" or w.lower() == "oz":
        return "OZ"
    if w.lower() == "grams" or w.lower() == "g":
        return "G"
    if w.lower() == "pounds" or w.lower() == "lb":
        return "LB"
    if w.lower() == "kilograms" or w.lower() == "kg":
        return "KG"
    else:
        return "LB"


def get_product_row(i, metafields):
    quantity = i['inventory_quantity'] if 'inventory_quantity' in i else '1'
    weight = ''
    unit_of_weight = ''
    seo_title = ''
    seo_desc = ''
    if 'grams' in i:
        unit_of_weight = 'grams'
        weight = i['grams']
    if 'weight_unit' in i:
        unit_of_weight = i['weight_unit']
        weight = i['weight']
    for meta in metafields:
        if meta == 'metafields_global_title_tag':
            seo_title = metafields[meta]
        if meta == 'metafields_global_description_tag':
            seo_desc = metafields[meta]
        if 'name' in meta and meta['name'] == 'metafields_global_title_tag':
            if 'value' in meta:
                seo_title = meta['value']
            else:
                seo_title = str(meta)
        if 'name' in meta and meta['name'] == 'metafields_global_description_tag':
            if 'value' in meta:
                seo_desc = meta['value']
            else:
                seo_desc = str(meta)
    if 'variants' in i:
        if len(i['variants']) >= 1:
            k = i['variants'][0]
            if 'grams' in k:
                unit_of_weight = 'grams'
                weight = k['grams']
            if 'weight_unit' in k:
                unit_of_weight = k['weight_unit']
                weight = k['weight']
        base_price = k['compare_at_price'] if 'compare_at_price' in k else ''
        if (base_price == '' or base_price == None): base_price = k['price'] if 'price' in k else ''
        sale_price = k['price'] if base_price != '' else ''
        try:
            if (base_price != '' and sale_price != '' and float(base_price) < float(sale_price)):
                tmp_var = sale_price
                sale_price = base_price
                base_price = tmp_var
        except Exception as e:
            pass
        if sale_price == base_price:
            sale_price = ''
        return [base_price, sale_price, quantity, format_unit_weight(unit_of_weight), weight if weight else '1', "IN",
                "3", "3", "3", seo_title, seo_desc]
    else:
        base_price = i['compare_at_price'] if 'compare_at_price' in i else ''
        if (base_price == '' or base_price == None): base_price = i['price'] if 'price' in i else ''
        sale_price = i['price'] if base_price != '' else ''
        try:
            if (base_price != '' and sale_price != '' and float(base_price) < float(sale_price)):
                tmp_var = sale_price
                sale_price = base_price
                base_price = tmp_var
        except Exception as e:
            pass
        if sale_price == base_price:
            sale_price = ''
        return [base_price, sale_price, quantity, format_unit_weight(unit_of_weight), weight if weight else '1', "IN",
                "3", "3", "3", seo_title, seo_desc]


def old_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list-collections', dest="list_collections", action="store_true",
                        help="List collections in the site")
    parser.add_argument("--collections", "-c", dest="collections", default="",
                        help="Download products only from the given collections")
    parser.add_argument("--csv", dest="csv", action="store_true", help="Output format CSV ")
    parser.add_argument("--tsv", dest="tsv", action="store_true", help="Output format TSV")
    parser.add_argument("--google-manufacturer", action="store_true", help="Output google-manufacturer template")
    parser.add_argument("--elliot-template-1", action="store_true", help="Output in Elliot's products old template")
    parser.add_argument("--elliot-template", action="store_true", help="Output in Elliot's products template")
    parser.add_argument("--base-feed", action="store_true", help="Output original Shopify template")
    # constants to avoid string literal comparison 
    (options, args) = parser.parse_known_args()
    delimiter = "\t" if options.tsv else ','
    if len(args) > 0:
        url = fix_url(args[0])
        print(f'url : {url}')
        print(f'options.list_collections : {options.list_collections}')
        print(f'options.collections : {options.collections}')
        if options.list_collections:
            for col in get_page_collections(url):
                print(col['handle'])
        else:
            collections = []
            if options.collections:
                collections = options.collections.split(',')
            filename = 'products.tsv' if options.tsv else 'products.csv'
            extract_shopify_products(url, filename, collections, delimiter)
            # if (options.elliot_template):
            #     extract_products(url, filename, collections, delimiter, ELLIOT_TEMPLATE_1)
            # elif options.google_manufacturer:
            #     extract_products(url, filename, collections, delimiter, GOOGLE_TEMPLATE)
            # elif options.elliot_template_1:
            #     extract_products(url, filename, collections, delimiter, ELLIOT_TEMPLATE)
            # elif not options.base_feed:
            #     extract_products(url, filename, collections, delimiter, GOOGLE_TEMPLATE)
            # else:
            #     extract_products(url, filename, collections, delimiter, BASE_TEMPLATE)


def __get_product_json_url(product_url):
    p_url = re.sub(r'/collections/[^/]+/', '/', product_url)
    return f'{p_url}/products.json'


def __get_collection_from_full_url(full_collection_url):
    __base_url = full_collection_url.rsplit('collections/', 1)[0]
    __collection = full_collection_url.rsplit('collections/', 1)[1].split('/')[0].split('?')[0]
    return __base_url, __collection


def extract_single_product(product_url_list, save_path):
    threads = []
    thread_cnt = export_constants.shopify_product_thread
    data_spice = [product_url_list[i::thread_cnt] for i in range(thread_cnt)]
    result_dict = {}
    for i in range(thread_cnt):
        threads.append(
            threading.Thread(target=__extract_single_product_thread, args=(data_spice[i], result_dict,)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    all_row_data = []
    product_number = 0
    for k in result_dict:
        all_row_data += result_dict[k][export_constants.dict_row_data]
        product_number += result_dict[k][export_constants.dict_product_number]
    __write_output_file(all_row_data, save_path, ',', product_number)


def __extract_single_product_thread(product_url_list, result_dict):
    if not len(product_url_list):
        return
    rows_data = []
    product_number = 0
    for p_url in product_url_list:
        try:
            res = requests.get(__get_product_json_url(p_url), headers={'User-Agent': USER_AGENT})
            res.raise_for_status()
            res_json = json.loads(res.text)
            if 'product' not in res_json:
                continue
            product = res_json['product']
            ret = format_row_data(product)
            for i in ret:
                rows_data.append(i)
            product_number += 1
        except:
            pass
    if len(rows_data):
        result_dict[str(uuid.uuid4())] = {export_constants.dict_row_data: rows_data,
                                          export_constants.dict_product_number: product_number}


if __name__ == '__main__':
    a = []
    for i in range(1, len(sys.argv)):
        a.append((str(sys.argv[i])))
    full_url = str(a[0])
    out_file = str(a[1])
    if a[2] == '0':
        # 按类别采集
        base_url, collection = __get_collection_from_full_url(full_url)
        extract_shopify_products(base_url, out_file, [collection])
    else:
        # 按商品采集
        extract_single_product(full_url.split(','), out_file)
