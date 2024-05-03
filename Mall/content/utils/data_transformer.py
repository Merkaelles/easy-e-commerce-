from content.model import db
from datetime import datetime, date
from decimal import Decimal


def row_list_to_list(row_list):
    l = []
    for row in row_list:
        d = dict(zip(row._fields, row))
        l.append(d)
    for i in l:
        for key in i.keys():
            if isinstance(i[key], date) or isinstance(i[key], datetime):
                i[key] = str(i[key])
            elif isinstance(i[key], Decimal):
                i[key] = float(i[key])
    return l


def model_list_to_list(model_list):
    [model.__dict__.pop('_sa_instance_state') for model in model_list]  # 去掉model中的_sa_instance_state属性
    model_x_list = [model.__dict__ for model in model_list]
    for i in model_x_list:
        for key in i.keys():
            if isinstance(i[key], date) or isinstance(i[key], datetime):
                i[key] = str(i[key])
            elif isinstance(i[key], Decimal):
                i[key] = float(i[key])
    return model_x_list
