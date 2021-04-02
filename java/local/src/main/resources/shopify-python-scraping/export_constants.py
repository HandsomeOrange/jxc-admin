#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   export_constants.py
@Contact :   douniwan@douniwan.com
@License :   (C)Copyright 2021-2031, Dou-Ni-Wan

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2021/3/17 15:59   yqz        1.0         None
"""

shopify_headers = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type',
                   'Tags', 'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name',
                   'Option2 Value', 'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams',
                   'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price',
                   'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src',
                   'Image Position', 'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
                   'Google Shopping / Google Product Category', 'Google Shopping / Gender', 'Google Shopping / Age Group', 'Google Shopping / MPN', 'Google Shopping / AdWords Grouping',
                   'Google Shopping / AdWords Labels', 'Google Shopping / Condition', 'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1',
                   'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image', 'Variant Weight Unit',
                   'Variant Tax Code', 'Cost per item']
# 47

append_headers = ['product_id','商品属性*']

shoplazza_headers = ['商品ID', '商品标题*', '商品副标题', '链接', '商品描述',
                     'seo标题', 'seo描述', 'seo关键词', '商品上架*', '需要物流*',
                     '商品收税*', '虚拟销量', '跟踪库存*', '库存规则*', '专辑名称',
                     '标签', '供应商名称', '供应商URL', '商品属性*', '款式1',
                     '款式2', '款式3', '商品售价*', '商品原价*', '商品SKU',
                     '商品重量', '重量单位', '商品条形码', '商品库存', '商品主图*',
                     '商品副图', '款式图片', '商品备注', '款式备注', '商品spu']
shoplazza_second_row = ['（此行导入时不可删除 ）商品 ID 是系统生成的唯一标识符，新增商品无需填写'
                        '请确保款式部分的标题与商品主体的标题一致，且保持连续排列（中间请勿插入其他商品）\n最多255字符'
                        '仅商品主体及单商品（无款式）填写即可\n最多255字符' '商品链接不支持导出（该字段仅用于商品导出后查看商品链接）\n'
                        '仅商品主体及单商品（无款式）填写即可，上传不带样式，若需要样式，请用html代码上传'
                        '仅商品主体及单商品（无款式）填写即可\n最多5000字符' '仅商品主体及单商品（无款式）填写即可\n最多5000字符'
                        '仅商品主体及单商品（无款式）填写即可' '商品上传完成后直接上架则输入Y，反之则填N。\n仅商品主体及单商品（无款式）填写即可'
                        '商品需要物流配送则输入Y，反之则填N。\n仅主商品及单商品（无子产品）填写即可'
                        '商品需要收税则输入Y，反之则填N。\n仅商品主体及单商品（无款式）填写即可' '仅商品主体及单商品（无款式）填写即可，最多输入六位数的自然数'
                        '需要跟踪商品库存则填Y，反之则填N。\n仅商品主体及单商品（无款式）填写即可'
                        '若跟踪库存为Y，则该项必填：\n填入「1」表示：库存为0允许购买\n填入「2」表示：库存为0不允许购买\n填入「3」表示：库存为0自动下架\n仅商品主体及单商品需要填写该项'
                        '请填入已有专辑名称，若专辑不存在，则不添加。\n多个专辑请用「英文逗号」隔开。\n仅商品主体及单商品（无款式）填写即可'
                        '仅商品主体及单商品（无款式）填写即可，多个标签请用「英文逗号」隔开。\n最多输入250个标签，每个不得超过500字符'
                        '仅商品主体及单商品（无款式）填写即可' '仅商品主体及单商品（无款式）填写即可'
                        '商品主体（Main）：填入M\n款式部分（Part）：填入P\n单商品（Single）：填入S'
                        '商品主体填写款式名称，款式部分填写款式信息，单商品无需填写' '商品主体填写款式名称，款式部分填写款式信息，单商品无需填写'
                        '商品主体填写款式名称，款式部分填写款式信息，单商品无需添加' '单商品（无款式）及款式需要填入该项，商品主体无需填写'
                        '单商品（无款式）及款式部分需要填入该项，商品主体无需填写' '单商品（无款式）及款式部分填入该项即可，商品主体无需填写'
                        '单商品（无款式）及款式部分填入该项即可，商品主体无需填写'
                        '仅款式部分及单商品需要填写\n可选单位有：kg, lb, g, oz\n如不填写，则默认为kg'
                        '单商品（无款式）及款式部分填入该项即可，商品主体无需填写' '单商品（无款式）及款式部分填入该项即可，商品主体无需填写'
                        '仅能一张图片（图片URL）\n仅商品主体及单商品需要填写该项'
                        '可多张图片（图片URL），URL用「英文逗号」隔开\n仅商品主体和单商品需要填写该项'
                        '仅能一张图片（图片URL），若不填入，则默认不需要图片。若产品其中一个款式上传图片，则其余款式也需要上传图片，否则默认填入商品主图\n仅款式部分需要填写该项'
                        '最多输入50个字' '单个款式备注需不超过20个字' '仅商品主体及单商品（无款式）填写即可']

item_handler = 'handler'
item_href = 'href'

shopify_product_thread = 10
dict_row_data = 'row_data'
dict_product_number = 'product_number'
