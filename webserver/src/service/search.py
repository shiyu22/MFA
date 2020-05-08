import logging
from common.const import default_cache_dir
from common.config import PG_HOST, PG_PORT, PG_USER, PG_PASSWORD, PG_DATABASE, PG_TABLE
from indexer.index import milvus_client, create_table, insert_vectors, delete_table, search_vectors, create_index
from deep_speaker.encode import voc_to_vec
from face_embedding.encode import img_to_vec
import psycopg2


def connect_postgres_server():
    try:
        conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD, database=PG_DATABASE)
        print("connect the database!")
        return conn
    except:
        print("unable to connect to the database")


def search_loc_in_pg(cur, ids, table_name=PG_TABLE):
    try:
        sql = "select name from " + table_name+ " where ids = '" + str(ids) + "';"
        cur.execute(sql)
        rows = cur.fetchall()
        return str(rows[0][0])
    except:
        print("search faild!")


def do_search(img, voice):
    try:
        feats_img = img_to_vec(img)
        feats_voc = voc_to_vec(voice)
        index_client = milvus_client()

        _, re_img = search_vectors(index_client, table_name, [feats_img], 1)
        status, re_voc = search_vectors(index_client, table_name, [feats_voc], 1)
        # print(status)
        ids_img = re_img[0].id
        ids_voc = re_voc[0].id
        dis_img = re_img[0].distance

        res = ['false', -1 ,'-1']
        if dis_img[0]>0.75 and ids_img[0]==ids_voc[0]:
            conn = connect_postgres_server()
            cur = conn.cursor()
            
            index = search_loc_in_pg(cur, ids_voc[0])
            res = ['ture', ids_img, index]
        return res

    except Exception as e:
        logging.error(e)
        return "Fail with error {}".format(e)
    finally:
        if index_client:
            index_client.disconnect()
        if conn:
            cur.close()
            conn.close()
