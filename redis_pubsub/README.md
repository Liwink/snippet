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

[rq fork_and_perform_task](https://github.com/nvie/rq/commit/a5a89256089a5610255eb09610ed1805eee43e81#diff-e419b495cc1d73ae799a0a4c4acc4598R65)

#### redis 功耗很大


