# 来源端设置：Google Ads、官网表单、Gmail 和百度爱番番

先确认用户在哪里提交：**在你的网站填表走 Gmail 路线；在百度的咨询或表单组件留资走爱番番推送。** 如果用户直接在 Google 广告里的「潜在客户表单」填写，那是另一种来源，见文末。用自己控制的测试表单或咨询组件造一条虚构询盘，再连飞书测试表。

## Google Ads → 官网表单 → Gmail

### 1. 在 Google Ads 配广告落地页

1. 从 [Google Ads 中国官网](https://business.google.com/cn/google-ads/) 登录，打开对应广告，在「最终到达网址」填有询盘表单的官网落地页，而不是 Gmail 或飞书地址。[最终到达网址说明](https://support.google.com/google-ads/answer/6080568?hl=zh-Hans)
2. 如果业务需要广告归因，按 [Google Ads 自动标记说明](https://support.google.com/google-ads/answer/3095550?hl=zh-Hans) 在「管理 → 帐号设置 → 自动标记」核对开关，并验证跳转不会丢掉点击参数。网站能否将来源记录到通知邮件，要在表单系统里另行配置并验证；单凭邮箱或发件人不能判断每一条都是广告询盘。广告归因和转化跟踪都不是 Gmail 入表的前置条件。

### 2. 在官网表单后台设置通知

1. 打开自己建站系统的表单编辑器，在「通知」「提交后动作」或对应设置里添加邮件通知。把收件人设为用于接入的 Gmail 地址，设置固定且能区分站点的邮件主题，例如 `[网站 A] 新询盘`。这一步在**建站后台**操作，不在 Google Ads 里设置；菜单以实际建站工具为准。
2. 让通知正文包含可用的表单字段，比如 `Email`（可选）、`Product`（可选）、`Inquiry`（必填留言）。用于归因的站点或表单标识建议固定；明确验证过的广告来源信息才作为广告标记。把系统发件人与访客填写的邮箱分开，访客邮箱放正文，必要时也可设为 Reply-To。
3. 从官网直接提交一条虚构询盘。打开 [Gmail](https://mail.google.com/)，确认实际收到邮件，核对主题、字段、正文换行及来源值。访客能提交成功，但 Gmail 没收到时，先查表单邮件通知、发件配置和垃圾邮件文件夹，再排查飞书。

### 3. 在 Gmail 和 Google Cloud 配只读接入

- **可选：用 Gmail 过滤器标记官网通知。** 在 Gmail 的搜索栏打开「显示搜索选项」，按发件人和主题试搜，创建过滤器并应用专用标签。[Gmail 过滤器官方说明](https://support.google.com/mail/answer/6579?hl=zh-Hans) 标签只帮助筛选，不等于授权范围；`gmail.readonly` 能读取该账号中的邮件，建议使用专用收件邮箱。
- **使用现有连接器**：按连接器的授权页面接入专用邮箱，核对实际权限。只做入表时不需要发信、删信或写 Gmail 标签。若需自行管理 OAuth，则继续下列操作。
- **自行配置 Gmail API**：在 [Google Cloud Console](https://console.cloud.google.com/) 选择或新建项目，打开 [Gmail API 启用页](https://console.cloud.google.com/apis/enableflow;apiid=gmail.googleapis.com)。在 Google Auth Platform 配置「品牌宣传」「受众群体」「数据访问权限」，按组织内或外部受众配置，外部测试模式添加获准的测试用户。[OAuth 同意页官方说明](https://developers.google.com/workspace/guides/configure-oauth-consent) · [Gmail 权限范围](https://developers.google.com/workspace/gmail/api/auth/scopes)
- **创建与运行方式匹配的 OAuth 客户端**：本地手动测试可按 [Gmail API Python 快速入门](https://developers.google.com/workspace/gmail/api/quickstart/python) 创建「桌面应用」客户端。服务端部署按 [Google Web Server OAuth 指引](https://developers.google.com/identity/protocols/oauth2/web-server) 配置自己的合法回调地址，保存授权凭据和刷新令牌时使用受保护的存储。外部 OAuth 项目若维持在 Testing，Gmail 只读的刷新令牌通常在 7 天后失效；长期轮询前核对 [Google 的令牌有效期和发布要求](https://developers.google.com/identity/protocols/oauth2#expiration)。
- **验收**：以实际用于轮询的授权读取那封测试邮件，确认读取到 Gmail API 的消息 ID 和完整正文，再核对飞书中的来源、编号和留言。收到邮件只验证通知环节，写入成功还要回查飞书。

## 百度爱番番 → HTTPS 接收端 → 飞书

### 1. 找到推送规则页面

- 打开 [百度营销中心](https://yingxiao.baidu.com/) 或 [爱番番入口](https://aifanfan.baidu.com/)，用有权限的推广账号进入对应的爱番番业务。公开对接资料展示的路径是「营销服务 → 爱番番 → 设置 → 线索设置 → API 导出 → 推送接口配置 → 新建规则」。部分界面从「线索设置」直接显示「推送接口配置」。可对照第三方的[爱番番后台操作截图](https://app.msgbox.chat/docs/zh-Hans/EKZ9wSYFTikoBZkE5RccIOwwnfq/YPcnwd2s6idJsRk4srYc2KNxnfd/)，只参考百度侧步骤。
- 找不到菜单时，先核对登录的推广账户、爱番番版本和管理员权限，再请百度营销支持确认该账号是否开放推送。以上是导航参考，不保证每个账户都有相同菜单。爱番番用于**导入**线索的 OpenAPI 与这里的向外**推送**是不同功能。

### 2. 填通知 URL、条件和字段

1. 先准备能接收并鉴权的 HTTPS 服务。选阿里云函数计算时，参照 [配置 HTTP 触发器](https://help.aliyun.com/zh/functioncompute/configure-an-http-trigger-for-a-function-and-invoke-the-function-by-using-http-requests) 创建对应入口。通知 URL 填接收服务的 HTTPS 地址；飞书网页链接和普通群机器人 URL 不能代替这个接收服务。
2. 设置规则名。界面如提供 CRM 类型，可选择与你实际接收服务匹配的类型（自建服务界面若有「自研」，可选该项）。生效条件选实际需要的组件来源，例如只接在线咨询或只接指定表单；有多个服务站点时分别用测试询盘核对来源映射。
3. 在「字段映射／数据格式」中，通过界面的变量插入功能分别配置唯一线索 ID、询盘摘要、完整会话和必要的联系字段。包内示例对应 `clueId`、`additionalContent`、`formDetail`、`emailAccount`；真实字段和变量语法以界面为准。若自定义表单字段需要填写用户在页面看到的名称，请使用实际表单字段名称。校验推送鉴权，记录测试状态和字段是否到齐；不记录密钥、鉴权值或完整客户报文。

### 3. 先送测试，再用受控来源验证

1. 点击「发送测试数据」并确认接收端收到。若编号仍显示 `${clueId}` 等占位符，只说明推送能到达；这条不进入询盘表。
2. 保存规则。只为测试所需的组件或受控来源启用规则，由操作者从自己的咨询入口或表单提交一条虚构询盘，确认「推送历史 → 接收端 → 飞书测试表」三处证据一致，且编号、摘要和会话是实际值。
3. 在测试环境重放同一条，飞书只留一行。两个站点共用端点时，各发一条并核对渠道。确认这几项后再扩大到生产来源。

## Google Ads 原生潜在客户表单

如果访客直接在广告内填表，而不是跳自己的网站，本 Skill 的 Gmail 示例不适用。使用 Google Ads 官方的[潜在客户表单 Webhook 设置](https://support.google.com/google-ads/answer/16729613?hl=zh-Hans)，或者先[下载潜在客户表单 CSV](https://support.google.com/google-ads/answer/10089020?hl=zh-Hans)核对字段。原生表单接入需要独立的适配器，本包不包含。
