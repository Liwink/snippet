用 redis 实现 pubsub
===

## redis 自带 pubsub 不足
1. 会有数据丢失
2. 并不是串行（？）
...

## redis 实现
publish 时将数据推到 subscribe 对应的 redis 队列中。

## 问题

#### 订阅中使用 `while` 循环监听时，只能实现一个订阅（进程被锁死

将监听放在子进程中实现。

##### 怎么停止子进程？
暂时是手动kill...


[rq fork_and_perform_task](https://github.com/nvie/rq/commit/a5a89256089a5610255eb09610ed1805eee43e81#diff-e419b495cc1d73ae799a0a4c4acc4598R65)

#### redis 功耗很大

将 `LPOP` 改为 `BLPOP`。
> BLPOP 是阻塞式列表的弹出原语。 它是命令 LPOP 的阻塞版本，这是因为当给定列表内没有任何元素可供弹出的时候， 连接将被 BLPOP 命令阻塞。

30+% 的CPU使用率，直接降到0


## 新的结构

现在有三个模块：

* channel_daemon：轮询 channel，每个订阅者获取信息
* subscribe：channel 中增加订阅者
* publish：向 channel 中每个订阅者发送消息
* un_subscribe: 取消订阅

#### 阻塞式弹出 BLPOP

`r.blpop(keys, timeout)`

1. `keys` 可以是队列，由先后顺序进行 pop

2. 阻塞式的意义：
> 如果所有给定key都不存在或包含空列表，那么BLPOP命令将阻塞连接，直到等待超时，或有另一个客户端对给定key的任意一个执行LPUSH或RPUSH命令为止。

3. `timeout`，阻塞超时时间，当为0的时候表示阻塞时间无限期延长。

[REDIS BLPOP](https://redis.readthedocs.org/en/2.4/list.html#blpop)

