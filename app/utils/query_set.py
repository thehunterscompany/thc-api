from mongoengine import QuerySet, Document
from bson.json_util import dumps
from .parser import parser_one_object

class RefQuerySet(QuerySet):
    def to_json(self):
        data = "[%s]" % (",".join([value.to_json() for value in self]))
        return data


def override_result(collection):
    data = collection.select_related()

    data = {
        key if key != 'id' else '_id': [parser_one_object(old_data) for old_data in data[key]]
        if isinstance(data[key], list) else str(data[key].id)
        if isinstance(data[key], Document) else data[key] for key in data
    }

    return dumps(data)


def pagination(page, per_page, sort_results):
    page = int(page) if page else 1
    per_page = int(per_page) if per_page else 15

    skip = (page - 1) * per_page
    limit = per_page

    paginate = [
        {
            '$facet': {
                'total': [
                    {
                        '$group': {
                            '_id': None,
                            'count': {'$sum': 1}
                        }
                    }
                ],
                'results': [
                    {'$sort': sort_results},
                    {'$skip': skip},
                    {'$limit': limit}
                ]
            }
        },
        {'$unwind': '$total'},
        {
            '$project': {
                'items': '$results',
                'page': {'$toInt': page},
                'per_page': {'$toInt': per_page},
                'total_items': '$total.count',
                'num_pages': {'$toInt': {'$ceil': {'$divide': ['$total.count', per_page]}}}
            }
        }
    ]

    return paginate


def default_paginate_schema(schema, page, per_page):
    all_schema = list(schema)
    length_schema = len(all_schema)

    default_schema = {
        'items': [],
        'page': int(page),
        'per_page': int(per_page),
        'total_items': 0,
        'num_pages': 1
    }

    return all_schema[0] if length_schema else default_schema
