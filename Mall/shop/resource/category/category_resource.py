from content.model.category import *
from content.model import db
from flask import current_app, request
from flask_restful import Resource, reqparse
from content.utils.data_transformer import row_list_to_list, model_list_to_list
from content.utils.shop_redis import redis_client
import json


class Shop_Category(Resource):
    def get(self):
        cache = redis_client.get('Category')  # 若每次都从客户端查询太费时，所以先看看redis里面有没有数据缓存
        if cache:
            return json.loads(cache)
        else:
            rp = reqparse.RequestParser()
            rp.add_argument('parent_id', type=int, required=True, location='args')
            args = rp.parse_args()
            data = self.getdata(args.parent_id)
            if data:
                for item in data:
                    data_2 = self.getdata(item['id'])  # 商品分类多级查询
                    if data_2:
                        item.update({'list': ''})
                        item['list'] = data_2
                        for i in data_2:
                            data_3 = self.getdata(i['id'])
                            if data_3:
                                i.update({'list': ''})
                                i['list'] = data_3
            redis_client.setex('Category', 24 * 60 * 60, json.dumps(data))  # 将列表或字典转化为字符串存储在redis
            return data

    @staticmethod  # 在类中定义的方法可用@staticmethod将其变成静态方法
    def getdata(parent_id):
        c = Category.query.with_entities(Category.id, Category.name, Category.parent_id).filter(
            Category.parent_id == parent_id).order_by(Category.sort.asc()).all()
        if c:
            data = row_list_to_list(c)
            return data
        else:
            return {'message': 'None'}


class Shop_New(Resource):
    def get(self):
        cache = redis_client.get('New_Commodity')
        if cache:
            return json.loads(cache)
        commodity = HomeNewProduct.query.join(Product, Product.id == HomeNewProduct.product_id).with_entities(
            Product.id, Product.product_name, Product.default_pic, Product.rel_category3_id).order_by(
            HomeNewProduct.sort.asc()).limit(10).all()
        if commodity:
            data = row_list_to_list(commodity)
            redis_client.setex('New_Commodity', 24 * 60 * 60, json.dumps(data))
            return data
        else:
            return {'message': 'None'}


class Shop_Recommend(Resource):
    def get(self):
        cache = redis_client.get('Recommend_Commodity')
        if cache:
            return json.loads(cache)
        commodity = HomeRecommendProduct.query.join(Product,
                                                    Product.id == HomeRecommendProduct.product_id).with_entities(
            Product.id, Product.product_name, Product.default_pic, Product.rel_category3_id).order_by(
            HomeRecommendProduct.sort.asc()).limit(10).all()
        if commodity:
            data = row_list_to_list(commodity)
            redis_client.setex('Recommend_Commodity', 24 * 60 * 60, json.dumps(data))
            return data
        else:
            return {'message': 'None'}


class Shop_Subject(Resource):
    def get(self):
        cache = redis_client.get('Recommend_subject&commodity')
        if cache:
            return json.loads(cache)
        subject = CmsSubject.query.filter(CmsSubject.show_status == 1).all()
        if subject:
            data = model_list_to_list(subject)
            for i in range(len(data)):
                commodity = CmsSubjectProductRelation.query.join(Product,
                                                                 Product.id == CmsSubjectProductRelation.product_id).filter(
                    CmsSubjectProductRelation.subject_id == data[i]['id']).with_entities(Product.id,
                                                                                         Product.product_name,
                                                                                         Product.default_pic,
                                                                                         Product.rel_category3_id).order_by(
                    Product.product_no.asc()).limit(10).all()
                if commodity:
                    data[i]['commodity_list'] = row_list_to_list(commodity)
                else:
                    data[i]['commodity_list'] = 'Blank'
            redis_client.setex('Recommend_subject&commodity', 24 * 60 * 60, json.dumps(data))
            return data
        else:
            return {'message': 'None'}
