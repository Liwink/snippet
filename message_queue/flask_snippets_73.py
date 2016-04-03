# Connecting to Redis
from redis import Redis

redis = Redis()

# The Configuration
app.config['REDIS_QUEUE_KEY'] = 'my_queue'

# The Decorator
from flask import current_app
from pickle import loads, dumps


class DelayedResult(object):
    def __init__(self, key):
        self.key = key
        self._rv = None

    @property
    def return_value(self):
        if self._rv is None:
            rv = redis.get(self.key)
            if rv is not None:
                self._rv = loads(rv)
        return self._rv


def queuefunc(f):
    def delay(*args, **kwargs):
        qkey = current_app.config['REDIS_QUEUE_KEY']
        key = "{0}:result:{1}".format(qkey, str(uuid4()))
        s = dumps((f, key, args, kwargs))
        redis.rpush(current_app.config['REDIS_QUEUE_KEY '], s)
        return DelayedResult(key)

    f.delay = delay
    return f


# The Queue Runner
def queue_daemon(app, rv_ttl=500):
    while 1:
        msg = redis.blpop(app.config['REDIS_QUEUE_KEY'])
        func, key, args, kwargs = loads(msg[1])
        try:
            rv = func(*args, **kwargs)
        except Exception as e:
            rv = e
        if rv is not None:
            redis.set(key, dumps(rv))
            redis.expire(key, rv_ttl)


# run the daemon
queue_daemon(app)


# Running Functions through the Queue
@queuefunc
def add(a, b):
    return a + b


"""
1. 用 Redis 实现队列，消息中转
2. deamon 监听 Redis 队列，处理消息
3. 利用装饰器，函数可以进入 Redis 队列处理，而不是即时处理
4. 队列处理的结果也是放在 Redis 中，所以函数返回信息也是包装过的
5. pickle，可以将信息持久化到硬盘，对应信息存入 Redis
"""
