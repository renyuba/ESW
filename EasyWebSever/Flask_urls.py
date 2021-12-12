# 装饰器路由匹配

PATH_URLS = [

]


# def c(path):
# 调用有装饰器的函数时只执行一次
#     def a(func):
#         # 调用有装饰器的函数时只执行一次
#         print('============================')
#
#         def b():
#             # 调用一次执行一次
#             return func(path)
#         return b
#     return a
#
#
# @c('/')
# def hello(path):
#     print('hello')
#     print(path)
#
#
# hello()


def route(path):

    def i_route(func):
        PATH_URLS.append((path, func))

        def core():
            return func(path)

        return core

    return i_route


@route('/')
def func(path):
    print('hello')


@route('/1/')
def func1(path):
    print('hello')
