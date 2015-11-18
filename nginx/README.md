

### upstream
    
    upstream openplay_api_stats.backend {
    #upstream的负载均衡，weight是权重，可以根据机器配置定义权重。weigth参数表示权值，权值越高被分配到的几率越大。
            server localhost:8200 weight=1;
            server localhost:8201 weight=1;
            server localhost:8202 weight=1;
            server localhost:8203 weight=1;
    }

### location

       location ~ ^/v1/  {
            [ configuration ] 
        }

* 以`=`开头表示精确匹配
* `^~` 开头表示uri以某个常规字符串开头，不是正则匹配
* `~` 开头表示区分大小写的正则匹配
* `~*` 开头表示不区分大小写的正则匹配
* `/` 通用匹配, 如果没有其它匹配,任何请求都会匹配到

### if

condition 判断

* -f和!-f用来判断是否存在文件
* -d和!-d用来判断是否存在目录
* -e和!-e用来判断是否存在文件或目录
* -x和!-x用来判断文件是否可执行

全局变量

* `$args` ： 这个变量等于请求行中的参数，同$query_string
* `$content_length` ： 请求头中的Content-length字段。
* `$content_type` ： 请求头中的Content-Type字段。
* `$document_root` ： 当前请求在root指令中指定的值。
* `$host` ： 请求主机头字段，否则为服务器名称。
* `$http_user_agent` ： 客户端agent信息
* `$http_cookie` ： 客户端cookie信息
* `$limit_rate` ： 这个变量可以限制连接速率。
* `$request_method` ： 客户端请求的动作，通常为GET或POST。
* `$remote_addr` ： 客户端的IP地址。
* `$remote_port` ： 客户端的端口。
* `$remote_user` ： 已经经过Auth Basic Module验证的用户名。
* `$request_filename` ： 当前请求的文件路径，由root或alias指令与URI请求生成。
* `$scheme` ： HTTP方法（如http，https）。
* `$server_protocol` ： 请求使用的协议，通常是HTTP/1.0或HTTP/1.1。
* `$server_addr` ： 服务器地址，在完成一次系统调用后可以确定这个值。
* `$server_name` ： 服务器名称。
* `$server_port` ： 请求到达服务器的端口号。
* `$request_uri` ： 包含请求参数的原始URI，不包含主机名，如：”/foo/bar.php?arg=baz”。
* `$uri` ： 不带请求参数的当前URI，$uri不包含主机名，如”/foo/bar.html”。
* `document_uri` ： 与$uri相同。


[nginx配置location总结及rewrite规则写法](http://seanlook.com/2015/05/17/nginx-location-rewrite/)
