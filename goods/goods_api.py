# coding: utf-8

import json, hashlib
from flask import request

from tools.db_tools import redis_cli

from . import goods
from .db_handle import add_goods, search_goods, get_goods_info, get_goods_all

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
		token = request.json.get("token")

		if not token:
			result['code'] = "403"
			result['msg'] = "请登录账号"
			return json.dumps(result)

		if redis_cli.get_value(token):
			data = request.json.get('goods_info')
			goods_name = data['goods_name']
			description = data['description']
			price = data['price']
			stock = data['stock']
			category = data['category']
			goods_img = data['goods_img']
		else:
			result['code'] = "403"
			result['msg'] = "请检查账号"
			return json.dumps(result)

	except KeyError:
		result['code'] = "400"
		result['msg'] = "请求参数错误"
		return json.dumps(result)

	add_goods(goods_name, description, price, goods_img, stock, category)
	result['msg'] = "添加成功"

	return result


# 获取商品信息接口
@goods.route("/get_goods", methods=['GET'])
def get_goods():

	result = {
		"code": "200",
		"msg" :	"请求成功",
		"result": True
	}

	get_data = request.args.to_dict()
	try:
		token = get_data.get('token')

		if not token:
			result['code'] = "403"
			result['msg'] = "请登录账号"
			return json.dumps(result)
		if redis_cli.get_value(token):
			category = get_data.get('category')
			count = int(get_data.get('count'))
		else:
			result['code'] = "403"
			result['msg'] = "请检查账号"
			return json.dumps(result)
		
	except KeyError:
		result['code'] = "400"
		result['msg'] = "请求参数错误"
		return json.dumps(result)

	goodses = search_goods(category, count)

	goods_data = []
	for goods in goodses:
		article = {}
		article['id'] = goods.goods_id
		article['goods_name'] = goods.goods_name
		article['description'] = goods.description
		article['price'] = str(goods.goods_price)
		article['goods_img'] = goods.goods_img
		article['category_id'] = goods.category_id
		goods_data.append(article)

	result['data'] = goods_data
	result['msg'] = "查询成功"

	return json.dumps(result)


# 商品信息详情接口
@goods.route("/goods_info", methods=['GET'])
def goods_info():

	result = {
		"code": "200",
		"msg" :	"请求成功",
		"result": True
	}

	get_data = request.args.to_dict()
	try:
		token = get_data.get('token')

		if not token:
			result['code'] = "403"
			result['msg'] = "请登录账号"
			return json.dumps(result)
		if redis_cli.get_value(token):
			goods_id = get_data.get('goods_id')
		else:
			result['code'] = "403"
			result['msg'] = "请检查账号"
			return json.dumps(result)
		
	except KeyError:
		result['code'] = "400"
		result['msg'] = "请求参数错误"
		return json.dumps(result)

	goods_info = get_goods_info(goods_id)[0]
	article = {}
	article['id'] = goods_info.goods_id
	article['goods_name'] = goods_info.goods_name
	article['description'] = goods_info.description
	article['price'] = str(goods_info.goods_price)
	article['goods_img'] = goods_info.goods_img
	article['stock'] = goods_info.stock

	result['data'] = article
	result['msg'] = "查询成功"

	return json.dumps(result)



# 获取全部商品信息接口
@goods.route("/all_goods", methods=['GET'])
def all_goods():

	result = {
		"code": "200",
		"msg" :	"请求成功",
		"result": True
	}

	get_data = request.args.to_dict()
	try:
		token = get_data.get('token')

		if not token:
			result['code'] = "403"
			result['msg'] = "请登录账号"
			return json.dumps(result)
		if not redis_cli.get_value(token):
			result['code'] = "403"
			result['msg'] = "请检查账号"
			return json.dumps(result)
		
	except KeyError:
		result['code'] = "400"
		result['msg'] = "请求参数错误"
		return json.dumps(result)

	goodses = get_goods_all()

	goods_data = []
	for goods in goodses:
		article = {}
		article['id'] = goods.goods_id
		article['goods_name'] = goods.goods_name
		article['description'] = goods.description
		article['price'] = str(goods.goods_price)
		article['goods_img'] = goods.goods_img
		article['category_id'] = goods.category_id
		goods_data.append(article)

	result['data'] = goods_data
	result['msg'] = "查询成功"

	return json.dumps(result)
