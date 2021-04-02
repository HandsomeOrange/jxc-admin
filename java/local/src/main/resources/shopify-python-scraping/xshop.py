#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   xshop.py    
@Contact :   douniwan@douniwan.com
@License :   (C)Copyright 2021-2031, Dou-Ni-Wan

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/3/25 12:23   yqz        1.0         None
"""

# import lib
import json
import logger

import requests, export_constants
from bs4 import BeautifulSoup


def get_product_id(detail_href):
    try:
        detail_res = requests.get(detail_href)
        detail_res.raise_for_status()
        detail_soup = BeautifulSoup(detail_res.text, features='lxml')
        tag = detail_soup.find('input', class_='product-id')
        if tag and tag.has_attr('value'):
            return tag['value']
    except:
        print(f'{detail_href} get product id error')
    return None


class XShop:

    def __init__(self, url):
        self.__collection_url = url
        self.__product_list = []
        self.__visited_product = {}

    def __extract_products(self):
        page = 1
        res = requests.get(f'{self.__collection_url}&page={page}')
        res.raise_for_status()
        page_soup = BeautifulSoup(res.text, features='lxml')
        a_list = page_soup.select('li.classify-item a')
        while a_list:
            for i in a_list:
                handler = str(i['href']).rsplit('/', 1)[1]
                data_item = {export_constants.item_handler: handler,
                             export_constants.item_href: 'https://www.brahmhn.com' + str(i['href'])}
                self.__product_list.append(data_item)
                # print('https://www.brahmhn.com' + i['href'])
            page += 1
            res = requests.get(f'{self.__collection_url}&page={page}')
            page_soup = BeautifulSoup(res.text, features='lxml')
            a_list = page_soup.select('li.classify-item a')

    def __get_item_detail(self):
        for d in self.__product_list:
            product_id = get_product_id(d[export_constants.item_href])
            if not product_id:
                continue
            self.__get_item_recommend(product_id)

    def __get_item_recommend(self, product_id):
        url = 'https://www.brahmhn.com/buyer/product/recommend'
        request_body = {'product_id': product_id, 'refresh': True}
        res = requests.post(f'{url}', data=json.dumps(request_body))
        res.raise_for_status()
        res_js = json.loads(res.text)
        recommend_list = []
        if res_js['data'] and 'products' in res_js['data']:
            for d in res_js['data']['products']:
                recommend_list.append(d['id'])
                # if len(self.__visited_product.keys()) >= len(self.__product_list):
                #     logger.info('recommend search end')
                #     return
                self.__visited_product[d['id']] = d
            recommend_list.sort()
            logger.info(f'{product_id} recommend list {recommend_list}')
        return recommend_list[-4]

    def test(self):
        # self.__extract_products()
        # # print(self.__product_list)
        # self.__get_item_detail()
        # for d in self.__visited_product:
        #     logger.info(d)
        id = '159945009'
        for i in range(10):
            id = self.__get_item_recommend(id)

        # self.__get_item_recommend('159945009')


if __name__ == '__main__':
    x = XShop('https://www.brahmhn.com/products?handler=bags')
    x.test()
