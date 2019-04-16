import pymysql
import json

try:
    f = open('config.json', 'r')
    config = json.load(f)
    conn = pymysql.connect(host=config['db']['host'], user=config['db']['user'], password=config['db']['password'],
                           db=config['db']['db'], charset=config['db']['charset'], port=config['db']['port'])
    cur = conn.cursor()


except :
    print('資料庫未正確設定')




def exec(cmd, parameter = None):
    try:
        if parameter is None:
            cur.execute(cmd)
        else :
            cur.execute(cmd,parameter)

    except Exception as e:
        raise e
        conn.rollback()

    # conn.commit()

    result = cur.fetchall()
    return result

def commit():
    conn.commit()


def fetch_one(cmd, parameter = None):
    try:
        if parameter is None:
            cur.execute(cmd)
        else :
            cur.execute(cmd,parameter)

        conn.commit()


    except Exception as e:
        raise e
        conn.rollback()

    result = cur.fetchall()
    return result[0][0]