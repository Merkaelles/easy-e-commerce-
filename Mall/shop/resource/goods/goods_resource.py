from flask_restful import Resource, reqparse, request
from content.model.goods import *
from content.model.category import *
from content.utils.data_transformer import row_list_to_list, model_list_to_list
import json


class Goods_List(Resource):
    def post(self):
        rp = reqparse.RequestParser()
        rp.add_argument('page', required=True, type=int, location='args')
        rp.add_argument('size', required=True, type=int, location='args')
        args = rp.parse_args()
        self.page = args.page
        self.size = args.size
        self.search_word = request.form.get('productName')
        self.relCategory1ID = request.form.get('relCategory1ID')
        self.relCategory2ID = request.form.get('relCategory2ID')
        self.relCategory3ID = request.form.get('relCategory3ID')

        res = self.select_search()
        if res:
            data = {}
            data['has_next'] = res.has_next
            data['has_prev'] = res.has_prev
            data['next_num'] = res.next_num
            data['page'] = res.page
            data['pages'] = res.pages
            data['total'] = res.total
            data['content'] = row_list_to_list(res.items)
            return data
        else:
            return {'message': 'None'}

    def select_search(self):
        res_filter = None

        if self.relCategory1ID:
            res_filter = Product.query.filter(Product.rel_category1_id == self.relCategory1ID)
        if self.relCategory2ID:
            res_filter = Product.query.filter(Product.rel_category2_id == self.relCategory2ID)
        if self.relCategory3ID:
            res_filter = Product.query.filter(Product.rel_category3_id == self.relCategory3ID)
        if self.search_word:
            res_filter = Product.query.filter(Product.product_name.like("%" + self.search_word + "%"))
        if res_filter:
            res = res_filter.with_entities(Product.id, Product.default_pic, Product.price, Product.product_name,
                                           Product.rel_category3_id).paginate(page=self.page, per_page=self.size,
                                                                              error_out=False)
            return res
        else:
            return None


class Goods_Specification(Resource):  # 商品规格
    def post(self):
        self.search_word = request.form.get('productName')
        self.relCategory1ID = request.form.get('relCategory1ID')
        self.relCategory2ID = request.form.get('relCategory2ID')
        self.relCategory3ID = request.form.get('relCategory3ID')
        res = self.get_spec_list()
        return res or {'message': 'None', 'code': 200}

    def get_spec_list(self):
        res_filter = None

        if self.relCategory1ID:
            res_filter = Product.query.filter(Product.rel_category1_id == self.relCategory1ID)
        if self.relCategory2ID:
            res_filter = Product.query.filter(Product.rel_category2_id == self.relCategory2ID)
        if self.relCategory3ID:
            res_filter = Product.query.filter(Product.rel_category3_id == self.relCategory3ID)
        if self.search_word:
            res_filter = Product.query.filter(Product.product_name.like("%" + self.search_word + "%"))
        res_with_entities = res_filter.with_entities(Product.spec_options).first()
        if not res_with_entities:
            return None
        product_spec = res_with_entities.spec_options.split(',')
        spec_list = []

        for spec in product_spec:
            spec_name = Specification.query.filter(Specification.id == int(spec)).with_entities(Specification.name,
                                                                                                Specification.id).first()
            spec_info = SpecificationOption.query.filter(SpecificationOption.rel_spec_id == int(spec)).with_entities(
                SpecificationOption.name, SpecificationOption.id, SpecificationOption.enabled,
                SpecificationOption.rel_spec_id).all()
            optionlist = row_list_to_list(spec_info)
            spec_list.append({'specID': spec_name.id,
                              'specName': spec_name.name,
                              'optionlist': optionlist})
        return spec_list
