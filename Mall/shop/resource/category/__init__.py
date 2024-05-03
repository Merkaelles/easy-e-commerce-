from flask import Blueprint
from flask_restful import Api
from content.utils.output import output_json

category_bp = Blueprint('shop', __name__, url_prefix='/shop')
category_api = Api(category_bp)
category_api.representation('application/json')(output_json)

from .category_resource import *
category_api.add_resource(Shop_Category, '/category', endpoint='category')
category_api.add_resource(Shop_New, '/new', endpoint='new')
category_api.add_resource(Shop_Recommend, '/recommend', endpoint='recommend')
category_api.add_resource(Shop_Subject, '/subject', endpoint='subject')
