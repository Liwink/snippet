
### RESTful

> 1. 每个 URI 代表一种资源（ `URI` 中不应该有动词，表现实体的，应该是名词）；
> 2. 客户端和服务端之间，传递这种资源的某种表现层；
> 3. 客户端通过四个 HTTP 动词，对服务器端资源进行操作，时间「表现层状态转化」；


### Problem

1. URI 中频繁动词
    - /invitation/send_phone/
    - /invitation/send_user/
    - /invitation/remove_user/

2. 资源最好用复数：/invitation/ -> /invitations/

3. 抽象不足，像问题 `1` 中列出了三个动作，但都可以抽象到/invitation/下面，用 `POST`, `DELETE` 完成

4. 不够表意，资源命名不合适，例如：`/v1/organizer/seasons/([0-9a-z]{24,})/invitation/send_phone/?`，实际完成的功能是「邀请球队加入赛季」，
我取义时重在 `invitation` 上面，在这里使用 `organizer` 表示资源更好。  
`/v1/organizer/seasons/([0-9a-z]{24,})/invitation/send_phone/?`  
->  
`/v1/organizer/seasons/([0-9a-z]{24,})/teams/?`  
使用后一个链接时，`POST` 和 `DELETE` 分别表示添加球队和移除球队，发送邀请只是实现上的操作。
第一个 `URI` 最大的问题是不够表意，「看起来」说的是「赛季的邀请信息」

5. 要充分利用 `method`，比如今天吃饭的时候，关于「点赞」的设计，`GET` 获取点赞的信息，`POST` 表示点赞，`DELETE` 取消点赞。这样的功能分配就比较合理
