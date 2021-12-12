# coding:utf-8
import socket
from multiprocessing import Process
from list_urls import PATH_URLS
from setting import HTML_ROOT_DIR, STATIC_ROOT_DIR


class REWS(object):

    def __init__(self, port):
        sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sever_socket.bind(("", port))
        sever_socket.listen(128)
        self.sever_socket = sever_socket

    @staticmethod
    def handle_cli(cli_socket):
        request_data = cli_socket.recv(1024)
        request_start_line = request_data.splitlines()[0]
        # 解析请求方式
        # 解析请求路径
        path = request_start_line.decode("utf-8").split(" ", maxsplit=2)[1]
        # 解析请求参数
        args = path.split("?")
        path = args[0]
        kargs = 0
        if len(args) == 2:
            kargs = {}
            args = args[1]
            args = args.split("&")
            for arg in args:
                key = arg.split("=")[0]
                value = arg.split("=")[1]
                kargs[key] = value

        flag = 0
        for url in PATH_URLS:
            if url[0] == path:
                flag = 1
                func = url[1]
                break

        if flag:
            try:
                status, response_heard, body = func(kargs)
                flag = 0
            except IOError:
                with open(HTML_ROOT_DIR + '/500.html', 'rb') as file:
                    body = file.read()
                    status = '500 Internal Server Error'
                    response_heard = 'Server: EasyWebSever'
                    flag = 0
        else:
            try:
                with open(STATIC_ROOT_DIR + path, 'rb') as file:
                    body = file.read()
                    status = '200 OK'
                    response_heard = 'Server: EasyWebSever'
            except IOError:
                with open(HTML_ROOT_DIR + '/404.html', 'rb') as file:
                    body = file.read()
                status = '404 NOT FOUNT'
                response_heard = 'Server: EasyWebSever'

        '''
            匹配url路径，其余一致认为是静态请求
        '''
        # if '/' == path:
        #     path = '/index.html'
        #
        # # 动态请求
        # try:
        #     # 尝试取html后缀， 获取失败则跳转到静态请求处理
        #     re.search(f'\.html$', path).group(0)
        #     try:
        #         status, response_heard, body = handle_request(path)
        #         # with open(HTML_ROOT_DIR + path, 'rb') as file:
        #         #     data = file.read()
        #         #     status = '200 OK'
        #     except IOError:
        #         with open(HTML_ROOT_DIR + '/404.html', 'rb') as file:
        #             data = file.read()
        #             status = '404 NOT FOUNT'
        #             response_heard = 'Server: EasyWebSever'
        
        response_start_line = 'HTTP/1.1 ' + status + '\r\n'
        response_heard = response_heard + '\r\n'
        response_body = body.decode('utf-8')

        response_data = response_start_line + response_heard + '\r\n' + response_body
        cli_socket.send(bytes(response_data, 'utf-8'))
        cli_socket.close()

    def runserver(self):
        while 1:
            cli_socket, cli_address = self.sever_socket.accept()
            handle_cli_process = Process(target=self.handle_cli, args=(cli_socket,))
            handle_cli_process.start()
            cli_socket.close()


if __name__ == '__main__':
    sever = REWS(8000)
    sever.runserver()