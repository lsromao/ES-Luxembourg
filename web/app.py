from flask import Flask, jsonify
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from models.city import City
from elasticsearch_dsl import Search

import os
import logging
import utils.data_cleaning as dat
import utils.elastic_documents as ed


app = Flask(__name__)

@app.before_first_request
def init_elasticsearch():
    global es

    es = Elasticsearch([os.environ['ELASTICSEARCH_URL']])

    if es.ping():
        logging.info('ElasticSearch connected.')
        City.init(using=es)
    else:
        logging.error('ElasticSearch not connected.')

@app.route('/<city>', methods=['GET'])
def get_info(city):
    city_search = Search(using=es, index='city').query("match", commune=city).extra(size=1000)
    response = city_search.execute()
    
    records = []
    for hit in response['hits']['hits']:
        records.append(hit['_source'].to_dict())
    
    logging.warning(len(records))
    return jsonify(records)

@app.route('/start', methods=['PUT'])
def start():
    
    data = dat.get_data()

    docs = ed.get_city_records(data)

    return jsonify(bulk(es,docs))

if __name__ == '__main__':
    logging.basicConfig(
        level = logging.INFO, 
        format = '%(asctime)s:%(levelname)s: %(message)s',
        datefmt = '%m/%d/%Y %I:%M:%S %p'
    )

    app.run(debug=True, host='0.0.0.0')
