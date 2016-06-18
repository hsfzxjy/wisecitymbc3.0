## 声明

 + 所有 API 以 `/api/` 为前缀
 + 所有 API 以 `/` 结尾（否则导致 302 Redirect）
 + 所有 API 的 Payload 为 JSON 格式
 + 没有特别说明，所有 API 返回为 JSON 格式
 + API 的 URL Parameters 支持以下参数：
    + `ordering`：以 `,` 分隔的字段列表，以 `-` 开头表示倒序
    + `limit`：（请求列表时使用）每页对象数
    + 其他注明的可用于筛选的字段
 + API 遵从 REST 规范。没有特殊说明，默认（括号内为简写）：
    + `GET <basename>/`： 获取列表（list）
    + `POST <basename>/`：新增对象（create）
    + `GET <basename>/<primarykey>/`：   获取对象（retrieve）
    + `PUT <basename>/<primarykey>/`：   修改对象（**不推荐**），需提交所有字段（update）
    + `PATCH <basename>/<primarykey>/`： 部分修改对象，只对提交字段产生更改（partial）
    + `DELETE <basename>/<primarykey>/`：删除对象（delete）
 + API 以 HTTP Status Codes 的方式告知处理结果
    + `200`：请求成功
    + `201`：对象创建成功
    + `204`：对象删除成功
    + `400`：请求参数错误
    + `401`：未认证
    + `403`：没有权限
    + `404`：对象未找到
    + `405`：不支持此 HTTP 方法
    + `415`：不支持此 Media Type
    + `500`：服务器错误

## 对象定义

### Enum

以下所有 `enum` 类型已于 `front-end/consts.json` 中定义，可运行 `./manage.py constout` 自动生成。

### List<Type>

```javascript
{
    previous: (str | null) 前一页的 URL
    next: (str | null) 后一页的 URL
    results: (array of <Type>) 对象列表
}
```

### File

```javascript
{
    id: (int)
    file_name: (str)
    storage_url: (str)
    created_time: (datetime)
    mime_type: (str)
    file_type: (enum FileType = (video, image, file))
}
```

### UserData

```javascript
{
    name: (str) 名称
    industry: (str) 行业
    sector: (str) 板块
    description: (str) 介绍
    reports: (array of File) 报告
}
```

### User

```javascript
{
    id: (int)
    username: (str)
    nickname: (str)

    user_type: (enum UserType = (
        government 政府
        bureau 主席团
        company 公司/选手
    ))
    bureau_type: (enum BureauType = (
        none 无
        real_estate 房地产
        car 汽车
        electronic_technology 电子科技
        bank 银行
        energy_and_raw_materials 能源及原材料
        financial_system 金融系统
        media 媒体
    )) available when user_type = government

    user_data: (UserData)
}
```

### Tag

```javascript
{
    id: (int)
    name: (str)
}
```

### Article

```javascript
{
    id: (int)
    article_type: (enum ArticleType = (
        company
        government
        media
        finance
        energy_and_raw_materials
    ))
    author: (User)
    title: (str)
    content: (str)
    summary: (str) 摘要，HTML 转为 Text 后前 20 行
    is_top: (bool) 置顶
    created_time: (datetime)
    attachments: (array of File)
    tags: (array of tags)
}
```

### Notification

```javascript
{
    id: (int)
    message: (str)
    url: (str)
    has_read: (bool) 已读标志
    module: (str)
}
```

### Topic

```javascript
{
    id: (int)
    asker: (User)
    title: (str)
    content: (str)
    created_time: (datetime)
    updated_time: (datetime)
    is_closed: (bool) 关闭标志
    replies_count: (int)
    attachments: (array of File)
}
```

### Reply

```javascript
{
    id: (int)
    topic: (Topic) 所属帖子
    author: (User)
    created_time: (datetime)
    content: (str)
    attachments: (array of File)
}
```

### StockComment

```javascript
{
    created_time: (datetime)
    content: (str)
}
```

### Stock

```javascript
{
    id: (int)
    name: (str)
    price: (float)
    volume: (float) 成交量
    company_info: (str) 公司信息
    comments: (array of comments) 券商评价
    current_log: (StockLog)
}
```

### StockLog

```javascript
{
    id: (int)
    price: (float)
    volume: (float)
}
```

### Bond（债券）

```javascript
{
    id: (int)
    issuer: (str) 发行方
    name: (str)
    quantity: (float) 发行量
    price: (float)
    current_log: (BondLog)
}
```

### BondLog

```javascript
{
    id: (int)
    quantity: (float)
    price: (float)
}
```

### Futures（期货）

```javascript
{
    id: (int)
    price: (float)
    current_log: (FuturesLog)
}
```

### FuturesLog

```javascript
{
    id: (int)
    price: (float)
}
```

### RawMaterials（原材料）

```javascript
{
    id: (int)
    description: (str)
    mining_costs: (float) 开采成本
    processing_costs: (float) 处理成本
    price: (float)
    current_log: (RawMaterialsLog)
}
```

### RawMaterialsLog

```javascript
{
    id: (int)
    price: (float)
}
```

## API

### 用户系统

 + `filters`: `user_type`

 ---

 + `users/` (list)
    + returns List<User>
 + `POST users/login/`
    + payload
        + username
        + password
    + raises
        + 400：登录失败
    + returns
        + User
 + `GET users/logout/`
    + redirects
        + 返回至上一页面
 + `users/(<pk>|me)/` (retrieve, partial)
    + returns
        + User
 + `users/(<pk>|me)/userdata/` (retrieve, partial)
    + returns
        + UserData

 ### 文章

 + `filters`: `article_type`

---

 + `articles/` (list)
 + `articles/` (create)
    + payload
        + title
        + content
        + attachments(optional)
    + returns
        + Article
 + `articles/<pk>/` (retrieve, partial, delete)
 + `GET articles/search/`
    + params
        + keyword
    + returns
        + List<Article>

 + `tags/` (list, create)
 + `tags/<pk>/` (retrieve, partial, delete)

### 消息

 + `filters`: `module`, `has_read`

---

出于兼容性考虑，`message` 中链接写作 `[<link text>](url)`。自行解析。

---

 + `n/` (list)
 + `GET n/mark_as_read/`
    + params
        + ids 需要标为已读的id，逗号分隔
 + `n/<pk>/` (delete)

### 问答

 + `topics/` (list)
 + `topics/` (create)
    + payload
        + title
        + content
        + attachments(optional)
 + `topics/<pk>/` (retrieve, partial, delete)
 + `GET topics/<pk>/(open|close)/`
    + desc
        + 打开或关闭问题
 + `topics/<pk>/replies/` (list)
 + `topics/<pk>/replies/` (create)
    + payload
        + content
        + attachments(optional)
 + `topics/<pk>/replies/<reply_pk>/` (retrieve, partial, delete)

### 金融系统

for `<base_name>` in (`stocks`, `bonds`, `raw_materials`, `futures`)

---

 + `<base_name>/` (list)
 + `<base_name>/<pk>/` (retrieve)
 + `<base_name>/<pk>/logs/` (list)
 + `<base_name>/<pk>/logs/<log_pk>/` (retrieve)
