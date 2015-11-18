
## WebServer1

Socket 监听端口
    （accept 是阻塞式的吗
telnet 向端口发送请求

当 telnet 建立连接时，listen_socket.accept() 接收到响应。（之前都阻塞）
当 telnet 未发送消息的时候，client_connection 没有响应

所以这样看，`listen_socket.listen(1)` 和 `client_connection.recv(1024)` 都是阻塞式的。



[gunicorn](https://github.com/benoitc/gunicorn/commit/52b950945fb1a399d171d42234b74afaba7eb579)

## WebServer2

这个项目就可以看出些结构化的东西

* WSGIServer类
    * `__init__`
    * `set_app`
    * `server_forever`
    * `handle_one_request`
        * `parse_request`
        * `get_environ`
        * `start_response`
    * `finish_response`

WSGIServer 是一个实现了 WSGI 的 Server。
Server 直接通过 `socket` 和客户端实现 `TCP` 连接，同时解析 `HTTP` 数据。
Server 依据 WSGI 中间件协议，将解析后的 HTTP 信息包装，传递给实现 WSGI 协议的 App。

这里主要参数信息都在 `env` 中，但 `self.start_response` 的作用是什么。（实现回调？

