from pymongo import MongoClient


def get_unique(field, collection="batch"):
    client = MongoClient('mongodb://localhost:27018/')
    db = client.twitter
    collection = db[collection]
    docs = collection.distinct(field)
    temp = sorted([d for d in docs])
    output = []
    for d in temp:
        output.append({"value": d, "label": d})
    return output


def get_first_nth_stream(limit=10, lang=None, group_lang=None):
    client = MongoClient('mongodb://localhost:27018/')
    pipeline = []
    group = [{'$group': {'_id': {'WINDOW_START': '$WINDOW_START',
                                 'TAG_NAME': '$TAG_NAME',
                                 'lang': '$LANG',
                                 },
                         'NB_HASH_TOTAL': {
                             '$max': '$NB_HASH'}}
              }]
    project = [{'$project': {'WINDOW_START': {'$dateFromString': {'dateString': '$_id.WINDOW_START'}},
                             'NB_HASH_TOTAL': 1,
                             'TAG_NAME': '$_id.TAG_NAME',
                             'lang': '$_id.lang', }
                }]
    sort = [{'$sort': {'WINDOW_START': -1,
                       'NB_HASH_TOTAL': -1}
             }]
    limit = [{'$limit': limit}]

    if lang:
        pipeline.append({'$match': {'LANG': lang}})
    if group_lang:
        group = [{'$group': {'_id': {'lang': '$LANG',
                                     'WINDOW_START': '$WINDOW_START'
                                     },
                             'NB_HASH_TOTAL': {
                                 '$max': '$NB_HASH'}}
                  }]
        project = [{'$project': {'WINDOW_START': {'$dateFromString': {'dateString': '$_id.WINDOW_START'}},
                                 'NB_HASH_TOTAL': 1,
                                 'lang': '$_id.lang', }
                    }]

    pipeline += group + project + sort + limit
    docs = client["twitter"]["stream"].aggregate(pipeline)
    return [d for d in docs]


def get_first_10_from_batch(start, end):
    client = MongoClient('mongodb://localhost:27018/')
    db = client.twitter
    collection = db.BatchViewAllTime
    docs = collection.aggregate([
        {'$match': {
            'WINDOW_START': {'$gte': start, '$lt': end}}},
        {'$group': {'_id': {'TAG_NAME': '$TAG_NAME', 'WINDOW_START': '$WINDOW_START'},
                    'NB_HASH': {
                        '$sum': '$NB_HASH'}}
         },
        {'$project': {
            'NB_HASH': 1,
            'TAG_NAME': '$_id.TAG_NAME',
            'WINDOW_START': '$_id.WINDOW_START',
        }},
        {'$sort': {
            'NB_HASH': -1}},
        # {'$limit': 10}
    ], allowDiskUse=True)
    return [d for d in docs]
# def get_first_10_country_from_stream():
#     client = MongoClient('mongodb://localhost:27018/')
#
#     docs = client['twitter']['stream'].aggregate([{'$group': {'_id': {'LANGUAGE': '$LANGUAGE',
#                                                                       'WINDOW_END': '$WINDOW_END',
#                                                                       'WINDOW_START': '$WINDOW_START'},
#                                                               'NB_HASH_LANG': {
#                                                                   '$sum': '$NB_HASH'}
#                                                               }
#                                                    },
#                                                   {'$sort': {'NB_HASH_LANG': -1, "_id.WINDOW_START": -1}
#                                                    },
#                                                   {'$project': {
#                                                       'WINDOW_START': {
#                                                           '$dateFromString': {
#                                                               'dateString': '$_id.WINDOW_START'
#                                                           }
#                                                       },
#                                                       'WINDOW_END': {
#                                                           '$dateFromString': {
#                                                               'dateString': '$_id.WINDOW_END'
#                                                           }
#                                                       },
#                                                       'NB_HASH_LANG': 1,
#                                                       'LANGUAGE': '$_id.LANGUAGE'
#                                                   }},
#                                                   {'$limit': 10}
#                                                   ])
#     return [d for d in docs]
