# !/usr/bin/python3

import pymysql
import re

from _ast import Tuple


def get_data_from_mysql():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "test")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("select * from biu_b_ask_zhihu")

    # 使用 fetchone() 方法获取单条数据.
    # word2vec_mysql = cursor.fetchone()

    #每次获取100条数据
    dr = re.compile(r'<[^>]+>',re.S)

    list = []
    results = cursor.fetchall()
    for data in results:
        tmp = []
        tmp.append(data[0])
        tmp.append(data[1])
        tmp.append(dr.sub('',data[2]))
        list.append(tmp)

    for tt in list :
        print(tt)

    # 关闭数据库连接
    db.close()
    return list


def updata(data):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "test")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    try:
        for line in data:
            sql = "update biu_b_ask_zhihu set lda_indx=%d, lda_key_words='%s' where id='%s'" % (line[0], line[1], line[2])
            print(sql)
            cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()


if __name__ == '__main__':
    # 100000
    data = [[ '1,2', u'dfdfasdf', '100000'], [ '1,2, 3', u'adfadsfadsf', '300000']]
    updata(data)
