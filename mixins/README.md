
## SearchMixin

### 解析url，返回搜索条件

- 两大类条件，排序和搜索
- 提取搜索结构
- 对搜索数据处理

### 定制化

Mixin 是为了提取共有服务。
具体业务中只需要实现简单配置、调用方法和参数，

##### 配置类变量 
通过配置「类变量」可以部分实现定制化，`AdapterMixin` 中就设置了大量 **类变量**。
比如：

    # 全局的查询约束，适用于 get/put/delete
    all_restriction = {}
    
    # get 的查询约束
    get_restriction = {}

##### 传递字符串 
另外大量定制化都是以 **字符串** 为媒介实现的。并不是直接传递操作实体。
比如：

- `m[self.document]` 就是通过配置字段，在 Mixin 找到具体的 Document。而并不是直接传递 Document 实体。
- `func = getattr(self, 'parse_query_conditions_for_%s' % field, None)`，
对字段进行特殊操作。这里要做的是，在搜索前对字段进行处理，对 URL 中提取的信息再处理，可能不同字段的处理细节不同，所以这里利用字段名实现定制化。 另外，我觉得使用 字段名 定制 方法名 ，很巧妙。避免了大量逻辑判断。

##### 前提判断的接口 hook

    if not self.pre_update_document(criteria, filtered_doc):
        continue



### 复用实现

复用。Don't Repeat Yourself.

写在 models 还是 MixinHandler？
这涉及到在什么层面上实现复用。
如果是对单一 Document 操作的复用，那在 Document 中实现即可。
如果是每个 handler 希望共用的逻辑，那复用可以在 MixinHandler 中实现。值得注意的是，这样的实现可以涉及多个数据库，是更上层的逻辑。
但是在 MixinHandler 中实现时，mdispatcher 就无法使用。


### 结构

search.py

    @property
    def sort(self):

    @property
    def query(self):
    
    def parse_query_conditions(self, query):
    
    def parse_query_conditions_for(self, field, value):
    
    def parse_query_conditions_for_op_id(self, value):

resource.py

    def get_documents(self):
        """
        获取资源列表
        :return:
        """
        result = m[self.document].find_by_page_with_builtin_pagination(self.criteria,
                                                                       last_id=self.last_id,
                                                                       limit=self.limit,
                                                                       sort=self.sort,
                                                                       include_fields=self.include_fields,
                                                                       **self.ref_include_fields_kwargs
                                                                       )
        return result    

    def get_relation_documents(self, _id):
        """
        获取关系文档
        :param _id:
        :return:
        """
        criteria = self.criteria or {}
        criteria.update({self.relation_field: _id})
        result = m[self.document].find_by_page_with_builtin_pagination(criteria,
                                                                       last_id=self.last_id,
                                                                       limit=self.limit,
                                                                       sort=self.sort,
                                                                       include_fields=self.include_fields,
                                                                       **self.ref_include_fields_kwargs
                                                                       )
        return result

adapter.py

    @property
    def criteria(self):
        """
        针对MongoDB的查询
        :return:
        """
        result = {}
        result.update(self.all_restriction)
        result.update(self.get_restriction)
        q = self.query
        result.update(q)
        return result


match_events.py

    get_restriction = {
        'code': {
            '$nin': [lookup.EventCode.CTRL.value],
        }
    }
    
    document = 'EventDocument'
    relation_field = 'match_id'
    
    @decorators.convert_to_object_id
    @decorators.token_required
    @decorators.resource_check(m.MatchDocument)
    def get(self, _id):
        result = self.get_relation_documents(_id)
        self.write(result)
    

