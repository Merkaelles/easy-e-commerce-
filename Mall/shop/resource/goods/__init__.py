from flask import Blueprint
from flask_restful import Api
from content.utils.output import output_json

goods_bp = Blueprint('goods', __name__, url_prefix='/goods')
goods_api = Api(goods_bp)
goods_api.representation('application/json')(output_json)

from .goods_resource import *
goods_api.add_resource(Goods_List, '/goodslist', endpoint='goodslist')
goods_api.add_resource(Goods_Specification, '/specification', endpoint='specification')