用 redis 实现 pubsub
===

### redis 自带 pubsub 不足
1. 会有数据丢失
2. 并不是串行（？）
...

### redis 实现
publish 时将数据推到 subscribe 对应的 redis 队列中。

### 问题

#### 订阅中使用 `while` 循环监听时，只能实现一个订阅（进程被锁死

将监听放在子进程中实现。

##### 怎么停止子进程？
暂时是手动kill...


[rq fork_and_perform_task](https://github.com/nvie/rq/commit/a5a89256089a5610255eb09610ed1805eee43e81#diff-e419b495cc1d73ae799a0a4c4acc4598R65)

#### redis 功耗很大

将 `LPOP` 改为 `BLPOP`。
> BLPOP 是阻塞式列表的弹出原语。 它是命令 LPOP 的阻塞版本，这是因为当给定列表内没有任何元素可供弹出的时候， 连接将被 BLPOP 命令阻塞。

30+% 的CPU使用率，直接降到0

