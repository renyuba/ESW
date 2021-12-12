# 数据库操作

import pymysql
from setting import MYSQL_SETTING


def get_mysql(env):

    conn = pymysql.connect(
        host='8.141.52.175',
        user='root',
        password='yzf020305',
        db='',  # 表名
    )
    # 创建游标，默认是元组型
    cursor = conn.cursor()

    return conn, cursor


def close_mysql(cursor, conn):

    cursor.close()
    conn.close()


def select_mysql(sql, *args):
    conn, cursor = get_mysql(MYSQL_SETTING)
    try:
        cursor.execute(sql, args)
        res = cursor.fetchall()
    except Exception as err:
        print(err)
        res = err
    close_mysql(conn, cursor)
    return res


if __name__ == '__main__':

    sql = 'select * from history'
    select_mysql(sql)