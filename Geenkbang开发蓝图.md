技客邦 (GeekBang) 开发蓝图 🚀
V1.0
本文档旨在将《项目圣经》中的业务需求，转化为清晰、可执行的技术实现方案，指导整个开发流程。
1. 整体技术架构 (Overall Architecture) 🏛️
我们将采用经典的前后端分离架构，通过 RESTful API 进行通信。
Generated plaintext
+------------------+      +----------------------+      +---------------------+
|   微信小程序端    |      |    业务逻辑后端      |      |     数据与服务       |
| (uni-app / Vue.js) |      |     (Flask)          |      |      (MySQL, etc.)  |
+------------------+      +----------------------+      +---------------------+
| - 页面视图 (Pages) |      | - API 接口 (Controllers)|      | - 用户数据          |
| - 可复用组件 (Comps)|      | - 业务逻辑 (Services)  |      | - 技能/任务数据      |
| - 状态管理 (Pinia) |      | - 数据模型 (Models)    |      | - 订单/交易数据      |
| - API 请求 (Axios) |      | - 认证/授权 (JWT)      |      | - 评价/信用数据      |
+--------^---------+      +-----------^----------+      +----------^----------+
         |                          |                       |
         |  <-- HTTPS (RESTful API)-->|                       |
         |                          | <--- DB Connection ---> |
         |                          |                       |
+--------v--------------------------v-----------------------v----------+
|                         云服务基础设施 (腾讯云/阿里云)                  |
| 🖥️ 服务器 (CVM)          🗄️ 数据库 (TencentDB for MySQL)              |
| 🖼️ 对象存储 (COS) for portfolios/images                          |
| 💳 微信支付 API         🎓 学校学籍认证接口 (if available)             |
+--------------------------------------------------------------------+
Use code with caution.
2. 项目结构 (Project Structure) 📁
为了实现低耦合和模块化，我们建议采用以下目录结构。
2.1 前端 (uni-app with Vue 3) 📱
Generated bash
geekbang-miniprogram/
├── src/
│   ├── api/                # API 请求模块 (按业务划分)
│   │   ├── userApi.js
│   │   ├── skillApi.js
│   │   └── orderApi.js
│   ├── assets/             # 静态资源 (图片, 字体)
│   ├── components/         # 全局可复用组件
│   │   ├── SkillCard.vue   # 技能卡片
│   │   ├── TaskItem.vue    # 任务列表项
│   │   └── RatingStars.vue # 星级评分
│   ├── pages/              # 主包页面
│   │   ├── home/           # 首页 (技能市场)
│   │   ├── tasks/          # 任务广场
│   │   ├── messages/       # 消息/IM
│   │   └── profile/        # 个人中心
│   ├── static/             # 静态资源 (不会被编译)
│   ├── store/              # 状态管理 (Pinia)
│   │   ├── index.js
│   │   └── userStore.js    # 用户信息、登录状态
│   ├── styles/             # 全局样式
│   ├── utils/              # 工具函数 (日期格式化, 请求封装)
│   └── main.js             # Vue 应用入口
├── App.vue                 # 应用配置
├── manifest.json           # uni-app 配置文件
└── pages.json              # 页面路由配置
Use code with caution.
Bash
2.2 后端 (Flask) ⚙️
我们将使用 Flask Blueprints 来实现模块化。
Generated bash
geekbang-backend/
├── app/
│   ├── __init__.py         # 应用工厂函数
│   ├── api/                # API 蓝图 (按模块划分)
│   │   ├── authController.py
│   │   ├── userController.py
│   │   ├── skillController.py
│   │   └── orderController.py
│   ├── models/             # 数据模型 (SQLAlchemy ORM)
│   │   ├── user.py
│   │   ├── skill.py
│   │   ├── task.py
│   │   └── order.py
│   ├── services/           # 业务逻辑层 (核心)
│   │   ├── userService.py
│   │   ├── skillService.py
│   │   ├── matchingService.py
│   │   └── paymentService.py
│   ├── utils/              # 工具/辅助函数
│   │   ├── decorators.py
│   │   └── response.py
│   └── extensions.py       # Flask 扩展实例化 (db, jwt, etc.)
├── migrations/             # 数据库迁移脚本 (Flask-Migrate)
├── tests/                  # 单元测试/集成测试
├── config.py               # 配置文件
└── run.py                  # 应用启动脚本
Use code with caution.
Bash
3. 数据库设计 (MySQL Schema) 💾
采用 camelCase 命名法用于 JSON 交互，snake_case 用于数据库字段。
users 表 (用户) 👤
字段名	类型	描述
id	INT (PK)	用户唯一ID
openId	VARCHAR	微信 OpenID (唯一)
unionId	VARCHAR	微信 UnionID
nickName	VARCHAR	昵称
avatarUrl	VARCHAR	头像链接
isVerified	BOOLEAN	是否已学籍认证
creditScore	INT	信用分 (初始100)
balance	DECIMAL	账户余额
createdAt	DATETIME	创建时间
skills 表 (技能服务) 🛠️
字段名	类型	描述
id	INT (PK)	技能唯一ID
userId	INT (FK)	技能主ID
title	VARCHAR	技能标题
description	TEXT	详细描述
category	VARCHAR	分类 (设计, 编程, ...)
tags	JSON	技能标签数组
price	DECIMAL	价格
portfolio	JSON	作品集 (图片/链接)
status	ENUM	状态 (active, inactive)
averageRating	FLOAT	平均评分
tasks 表 (悬赏任务) 🎯
字段名	类型	描述
id	INT (PK)	任务唯一ID
userId	INT (FK)	发布者ID
title	VARCHAR	任务标题
description	TEXT	任务描述
budget	DECIMAL	预算
deadline	DATETIME	截止日期
status	ENUM	状态 (open, in_progress, ...)
assigneeId	INT (FK)	承接者ID
orders 表 (订单) 🧾
字段名	类型	描述
id	INT (PK)	订单唯一ID
orderNumber	VARCHAR	订单号 (唯一)
requesterId	INT (FK)	需求方ID
providerId	INT (FK)	供给方ID
sourceId	INT	来源ID (skillId 或 taskId)
sourceType	ENUM	来源类型 (skill, task)
amount	DECIMAL	订单金额
status	ENUM	状态 (pending, paid, completed, ...)
reviews 表 (双向评价) ⭐
字段名	类型	描述
id	INT (PK)	评价唯一ID
orderId	INT (FK)	关联订单ID
reviewerId	INT (FK)	评价者ID
revieweeId	INT (FK)	被评价者ID
rating	TINYINT	星级 (1-5)
comment	TEXT	评价内容
4. 核心 API 接口设计 (RESTful API) 🔌
认证 (Auth)
POST /api/auth/login
描述: 微信小程序登录，用 code 换取自定义登录态 (JWT Token)。
请求: { "code": "wx_login_code" }
响应: { "token": "jwt_token", "isNewUser": true/false }
用户 (User)
GET /api/users/me
描述: 获取当前登录用户的详细信息 (需要 Token)。
PUT /api/users/me
描述: 更新用户信息 (昵称、头像等)。
技能 (Skill)
POST /api/skills
描述: 发布一个新技能。
GET /api/skills
描述: 获取技能列表，支持搜索和排序。
GET /api/skills/{skillId}
描述: 获取单个技能的详细信息。
任务 (Task)
POST /api/tasks
描述: 发布一个悬赏任务。
GET /api/tasks
描述: 获取任务广场列表。
订单 (Order)
POST /api/orders
描述: 根据技能创建订单。
POST /api/orders/{orderId}/pay
描述: 请求支付，返回支付参数给小程序。
POST /api/orders/{orderId}/confirm-completion
描述: 需求方确认服务完成。
5. 核心业务流程实现 🚶‍♂️
示例：用户小明购买小艺的 "PPT 美化" 服务
📱 前端 (小明): 在小艺的技能详情页点击 "立即求助"，调用 POST /api/orders，请求体为 { "skillId": 小艺的技能ID }。
⚙️ 后端 (OrderController):
验证用户登录状态。
调用 OrderService 创建一个状态为 pending 的订单。
返回新创建的 orderId。
📱 前端: 跳转到订单确认页，用户点击 "去支付"，调用 POST /api/orders/{orderId}/pay。
⚙️ 后端 (PaymentService):
与微信支付 API 交互，生成预支付订单。
将支付参数返回给前端。
📱 前端: 调用 wx.requestPayment，拉起微信支付。
⚙️ 后端: 在支付回调接口中，接收微信支付成功通知，将订单状态更新为 paid，并通知小艺。
(...服务进行中...)
📱 前端 (小明): 服务完成后，点击 "确认完成"，调用 POST /api/orders/{orderId}/confirm-completion。
⚙️ 后端 (OrderService):
将订单状态更新为 completed。
将款项划转到小艺的余额。
触发双方可进行评价的状态。
6. 开发路线图 (Roadmap) 🗺️
Phase 1: MVP - 验证核心闭环 (0-1) 🎯
目标: 跑通 "发布 → 查找 → 交易 → 完成" 的核心流程。
功能:
✅ 用户模块：微信登录、基本信息。
✅ 技能/任务模块：发布、列表、详情。
✅ 交易模块：创建订单、微信支付、确认完成。
Phase 2: 信用与体验增强 (1-100) ✨
目标: 建立信任体系，优化匹配效率和用户体验。
功能:
⭐ 信用体系：双向评价、信用分。
🎓 认证体系：学生认证。
💬 沟通模块：内置 IM。
🔍 搜索筛选：高级搜索。
👤 个人主页：技能图谱。
Phase 3: 社区与智能化 (100+) 🧠
目标: 提升社区粘性，实现智能匹配，探索增值服务。
功能:
🤖 智能匹配：推荐算法。
⚡ “即时帮”：在线抢单。
👨‍👩‍👧‍👦 社群功能：技能交流群。
💎 增值服务：“大神”认证、排名推广。
