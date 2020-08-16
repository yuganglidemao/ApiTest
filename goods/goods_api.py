# coding: utf-8

import json
import time
from flask import request

from . import goods
from .db_handle import add_goods, search_goods

"""
	添加商品接口
"""
@goods.route("/create_goods", methods=['POST'])
def create_goods():

	result = {
		"code": "200",
		"msg" :	"请求成功",
		"result": True
	}
	try:
		data = request.json.get('goods_info')
		print(data)
		goods_name = data['goods_name']
		description = data['description']
		price = data['price']
		stock = data['stock']
		category = data['category']
		goods_img = data['goods_img']
	except KeyError:
		result['code'] = "400"
		result['msg'] = "请求参数错误"
		return json.dumps(result)

	add_goods(goods_name, description, price, goods_img, stock, category)
	result['msg'] = "添加成功"

	return result


"""
获取商品信息接口
"""
@goods.route("/get_goods", methods=['GET', 'POST'])
def get_goods():

	result = {
		"code": "200",
		"msg" :	"请求成功",
		"result": True
	}

	get_data = request.args.to_dict()
	try:
		category = get_data.get('category')
		count = int(get_data.get('count'))
		
	except KeyError:
		result['code'] = "400"
		result['msg'] = "请求参数错误"
		return json.dumps(result)

	goodses = search_goods(category, count)

	goods_data = []
	for goods in goodses:
		article = {}
		article['goods_name'] = goods.goods_name
		article['description'] = goods.description
		article['price'] = str(goods.goods_price)
		article['goods_img'] = goods.goods_img
		article['stock'] = goods.stock
		article['category_id'] = goods.category_id
		goods_data.append(article)

	result['data'] = goods_data
	result['msg'] = "查询成功"

	return json.dumps(result)