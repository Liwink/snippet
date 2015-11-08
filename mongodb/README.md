这个 snippet 主要讨论 MongoDB 使用
===


#### 配置
1. 用 `mongokit` 的 `Connection` 建立连接；
2. 构建 `Document`，`structure` 构建表的字段结构；
3. 在连接中注册表。


#### structure
MongoKit 中 Document 会搜索父类中的 structure，来构成完整的字段。

实例的 structure，会按照继承类的搜索优先顺序找到字段，所以如果只用实例的 structure，是不会读取到父层的数据。

```
class DocumentProperties(SchemaProperties):
    def __new__(cls, name, bases, attrs):
        for base in bases:
            parent = base.__mro__[0]
            if hasattr(parent, 'structure'):
                if parent.structure is not None:
                    #parent = parent()
                    if parent.indexes:
                        if 'indexes' not in attrs:
                            attrs['indexes'] = []
                        for index in attrs['indexes']+parent.indexes:
                            if index not in attrs['indexes']:
                                attrs['indexes'].append(index)
        return SchemaProperties.__new__(cls, name, bases, attrs)
```


