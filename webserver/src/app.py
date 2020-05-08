import os
import os.path as path
import logging
from common.config import IMG_TABLE,VOC_TABLE
from common.const import UPLOAD_PATH
from service.search import do_search
from service.insert import do_insert
from service.count import do_count
from indexer.index import milvus_client, create_table, insert_vectors, delete_table, search_vectors, create_index
from flask_cors import CORS
from flask import Flask, request, send_file, jsonify
from flask_restful import reqparse
from werkzeug.utils import secure_filename
import numpy as np
from numpy import linalg as LA
import datetime


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['JSON_SORT_KEYS'] = False
CORS(app)

model = None

@app.route('/api/v1/count', methods=['POST'])
def do_count_api():
    args = reqparse.RequestParser(). \
        add_argument('Table', type=str). \
        parse_args()
    table_name = args['Table']
    rows = do_count(table_name)
    return "{}".format(rows)


@app.route('/api/v1/insert', methods=['POST'])
def do_insert_api():
    args = reqparse.RequestParser(). \
        add_argument("Name", type=str). \
        parse_args()

    name = args['Name']
    file_img = request.files.get('img', "")
    file_voc = request.files.get('voc', "")
    print(name)
    if file_img and file_voc:
        ids = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], ids[:-1] + '.jpg')
        file_img.save(img_path)
        voc_path = os.path.join(app.config['UPLOAD_FOLDER'], ids[:-1] + '.wav')
        file_voc.save(voc_path)
        print(name, ids, file_img, voc_path)
        try:
            status = do_insert(name, ids[:-1], img_path, voc_path)
        except:
            return "fileed insert", 400
        return "{}".format(status), 200
    else:
        return "no file data", 400


@app.route('/data/<image_name>')
def image_path(image_name):
    file_name = UPLOAD_FOLDER + '/' + image_name
    if path.exists(file_name):
        return send_file(file_name)
    return "file not exist"


@app.route('/api/v1/search', methods=['POST'])
def do_search_api():
    file_img = request.files.get('img', "")
    file_voc = request.files.get('voc', "")
    if file_img and file_voc:
        try:
            res = do_search(table_name, molecular_name, top_k)
            res[1] = request.url_root + "data/" +res[1]
        except:
            return "There has no results, please make sure there is only one face in the video."

        return res, 200
    return "not found", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
