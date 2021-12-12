# 视图文件
from models import select_mysql
from setting import HTML_ROOT_DIR
# 传递的参数是字典格式

# def handle_request(path):
#     for url in PATH_URLS:
#         if path == url[0]:
#             status, response_heard, body = url[1]()
#             return status, response_heard, body
#     status = '404 NOT FOUNT'
#     response_heard = 'Server: EasyWebSever'
#     body = ''
#     return status, response_heard, body


def index(kargs):
    try:
        with open(HTML_ROOT_DIR + '/index.html', 'rb') as file:
            body = file.read()
            status = '200 OK'
            response_heard = 'Server: EasyWebSever'
            # 操作数据库
            # sql 语句
            '''
            sql = ''
            result = select_mysql(sql)
            '''

    except Exception as err:
        status = '404 NOT FOUNT'
        response_heard = 'Server: EasyWebSever'

        body = err
    return status, response_heard, body


def member(kargs):
    ...