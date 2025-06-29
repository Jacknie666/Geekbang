技客邦 (GeekBang) 项目设计规划

欢迎来到“技客邦”项目！本文档旨在为所有开发者提供一个清晰、统一的设计蓝图，确保我们高效、协同地构建一个低耦合、高内聚、易于维护的P2P技能分享平台。

项目愿景：让每个学生的技能都发光 (Let Every Student's Skill Shine)

目录

技术栈 (Tech Stack)

系统架构 (System-Architecture)

后端设计 (Flask)

3.1 项目结构

3.2 核心分层设计

3.3 核心工作流示例：创建订单

前端设计 (uni-app / Vue.js)

4.1 项目结构

4.2 核心模块设计

4.3 核心工作流示例：渲染任务列表

数据库设计 (MySQL)

5.1 核心数据表 (ER)

API 与编码规范

6.1 API 设计原则

6.2 统一响应格式

6.3 命名规范

开发环境搭建 (Getting Started)

1. 技术栈 (Tech Stack)

前端: uni-app (基于 Vue.js 3) - 一套代码，多端发布（微信小程序、App等）。

后端: Flask (Python) - 轻量、灵活，快速迭代。

数据库: MySQL 8.0+

ORM: SQLAlchemy - 实现面向对象的数据库操作。

状态管理: Pinia - Vue 3 官方推荐的状态管理库。

2. 系统架构 (System-Architecture)

本项目采用前后端分离的经典架构。

Generated text
+----------------+      +-------------------------+      +----------------+
|                |      |      Backend API        |      |                |
|  微信小程序     |      |     (Flask Server)      |      |     MySQL      |
|  (uni-app)     | REST |                         | ORM  |    Database    |
|                +------>+  - API Layer            +------>+                |
|     (Client)   |  API |  - Service Layer        |      |    (Storage)   |
|                |      |  - Model Layer          |      |                |
+----------------+      +-------------------------+      +----------------+


客户端 (Client): 微信小程序作为用户交互界面，通过调用后端 API 完成所有业务操作。

后端 (Backend): Flask 应用提供无状态的 RESTful API。所有业务逻辑和数据处理都在后端完成。

数据存储 (Storage): MySQL 数据库负责持久化存储所有应用数据。

3. 后端设计 (Flask)

后端遵循分层架构思想，实现业务逻辑、数据访问和API接口的解耦。

3.1 项目结构
Generated bash
geekbang-backend/
├── run.py                 # 应用启动文件
├── config.py              # 配置文件
├── app/
│   ├── __init__.py        # 应用工厂 create_app()
│   ├── api/               # 视图层 (Blueprints)
│   │   ├── userApi.py
│   │   ├── taskApi.py
│   │   └── orderApi.py
│   ├── models/            # 模型层 (SQLAlchemy)
│   │   ├── user.py
│   │   ├── task.py
│   │   └── order.py
│   ├── services/          # 业务逻辑层 (核心)
│   │   ├── userService.py
│   │   ├── taskService.py
│   │   └── orderService.py
│   ├── utils/             # 工具类
│   │   ├── response.py    # 统一响应封装
│   │   └── decorators.py  # 装饰器 (如 @login_required)
│   └── extensions.py      # Flask 扩展实例化 (db, migrate)
└── migrations/            # Alembic 数据库迁移脚本
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
3.2 核心分层设计
API Layer (app/api/)

职责: 接收 HTTP 请求，验证请求参数，调用 Service 层处理业务，并使用 utils.response 封装返回结果。不包含任何业务逻辑。

示例 (taskApi.py):

Generated python
# 使用 camelCase 风格的路由
@task_bp.route('/tasks/<int:taskId>', methods=['GET'])
def getTaskDetail(taskId):
    task = taskService.getTaskById(taskId)
    if not task:
        return response.fail(message="Task not found")
    return response.success(data=task.toDict())
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
Service Layer (app/services/)

职责: 项目的核心，处理所有复杂的业务逻辑。它作为 API 层和 Model 层的“粘合剂”，组合不同的数据模型操作来完成一个完整的业务功能。

示例 (orderService.py):

Generated python
class OrderService:
    def createOrder(self, requesterId, taskId):
        # 1. 检查任务是否存在且可被下单
        task = taskService.getTaskById(taskId)
        if not task or task.status != 'open':
            raise Exception("Task is not available")
        
        # 2. 检查用户余额 (未来)
        
        # 3. 创建订单模型实例
        newOrder = Order(
            requesterId=requesterId,
            providerId=task.creatorId,
            taskId=taskId,
            price=task.price,
            status='pending' # 待接单
        )

        # 4. 持久化到数据库
        db.session.add(newOrder)
        # 5. 更新任务状态
        task.status = 'locked'
        db.session.commit()
        
        # 6. (未来) 发送通知给技能主
        
        return newOrder

# 实例化为单例，方便调用
orderService = OrderService()
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
Model Layer (app/models/)

职责: 定义数据结构（与数据库表一一对应），处理数据持久化。使用 SQLAlchemy ORM，以面向对象的方式操作数据库。

示例 (order.py):

Generated python
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskId = db.Column(db.Integer, db.ForeignKey('task.id'))
    requesterId = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50), default='pending')

    def toDict(self): # camelCase for JSON keys
        return {
            "orderId": self.id,
            "taskId": self.taskId,
            "requesterId": self.requesterId,
            "status": self.status
        }
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
3.3 核心工作流示例：创建订单

Client -> API Layer -> Service Layer -> Model Layer -> DB

前端: 用户点击“立即求助”按钮，发送请求 POST /api/orders，body 为 {"taskId": 123}。

orderApi.py: 接收请求，从 token 中解析出 userId，调用 orderService.createOrder(userId, 123)。

orderService.py: 执行 createOrder 方法中的业务逻辑（校验任务、创建订单、更新任务状态等）。

models: Order 和 Task 对象被创建和修改，db.session.commit() 将变更写入数据库。

orderService.py: 返回成功创建的 newOrder 对象。

orderApi.py: 将 newOrder 对象序列化为字典，并用 response.success() 包装后返回给前端。

4. 前端设计 (uni-app / Vue.js)

前端采用组件化和模块化思想，提升代码复用性和可维护性。

4.1 项目结构
Generated bash
geekbang-frontend/
├── pages/                  # 主包页面
│   ├── home/index.vue      # 首页
│   └── user/profile.vue    # 个人中心
├── subPackages/            # 业务分包 (按需加载)
│   ├── task/
│   │   ├── pages/taskDetail.vue
│   │   └── pages/publishTask.vue
│   └── order/
│       └── pages/orderList.vue
├── components/             # 全局可复用组件
│   ├── TaskCard/TaskCard.vue
│   └── UserAvatar/UserAvatar.vue
├── static/                 # 静态资源
├── api/                    # API 请求模块
│   ├── userApi.js
│   └── taskApi.js
├── store/                  # 全局状态管理 (Pinia)
│   └── user.js             # 用户信息模块
└── utils/                  # 工具函数
    └── request.js          # 封装的请求库
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
4.2 核心模块设计
API Client (api/)

职责: 集中管理所有对后端 API 的请求。每个模块对应一个文件，方法名与业务操作对应。

示例 (taskApi.js):

Generated javascript
import request from '@/utils/request';

// 使用 camelCase
export function getTaskList(params) {
  return request({
    url: '/tasks',
    method: 'GET',
    params // e.g., { page: 1, pageSize: 10, type: 'skill' }
  });
}
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
JavaScript
IGNORE_WHEN_COPYING_END
Request Util (utils/request.js)

职责: 封装 uni.request，实现请求拦截（自动添加 token）、响应拦截（处理统一响应格式、全局错误提示）等。

State Management (store/)

职责: 使用 Pinia 管理全局共享状态，如用户信息、登录状态（token）等。

示例 (store/user.js):

Generated javascript
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: uni.getStorageSync('token') || '',
    userInfo: {}
  }),
  actions: {
    async login(code) {
      // 调用 userApi.login, 保存 token 和 userInfo
    }
  }
});
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
JavaScript
IGNORE_WHEN_COPYING_END
Components (components/)

职责: 将 UI 拆分为独立的、可复用的组件，如任务卡片、用户头像、星级评分等。组件通过 props 接收数据，通过 emits 与父组件通信。

4.3 核心工作流示例：渲染任务列表

pages/home/index.vue: 在 onLoad 生命周期中，调用 api/taskApi.js 中的 getTaskList 方法。

taskApi.js: 调用 utils/request.js 发送 GET 请求到 /api/tasks。

request.js: 添加请求头 Authorization: Bearer <token> (如果已登录)。

后端: 处理请求并返回任务列表数据（JSON 格式）。

request.js: 响应拦截器解析出 data 字段。

pages/home/index.vue: 获取到任务列表数组，将其赋值给页面的响应式变量 taskList。

Template: 使用 v-for 指令遍历 taskList，将每个 task 对象作为 prop 传递给 <TaskCard> 组件进行渲染。

5. 数据库设计 (MySQL)
5.1 核心数据表 (ER)

user (用户表)
id (PK), openId, nickName, avatarUrl, schoolName, studentId, verificationStatus, creditScore, createdAt

task (技能/任务表)
id (PK), creatorId (FK to user.id), taskType ('skill', 'bounty'), title, description, price, currencyType ('cny', 'virtual'), status ('open', 'locked', 'completed', 'closed'), tags, createdAt

order (订单表)
id (PK), taskId (FK to task.id), requesterId (FK to user.id), providerId (FK to user.id), price, status ('pending', 'inProgress', 'completed', 'cancelled', 'disputed'), createdAt, completedAt

review (评价表)
id (PK), orderId (FK to order.id), reviewerId (FK to user.id), revieweeId (FK to user.id), rating, comment, createdAt

message (聊天消息表)
id (PK), conversationId, senderId (FK to user.id), receiverId (FK to user.id), content, messageType, createdAt

6. API 与编码规范
6.1 API 设计原则

RESTful 风格: 使用名词表示资源 (e.g., /users, /tasks)，使用 HTTP 方法表示操作 (GET, POST, PUT, DELETE)。

无状态: 每个请求都应包含所有必要信息，服务器不保存客户端会话状态。

版本控制: (可选) 在 URL 中加入版本号，如 /api/v1/tasks。

6.2 统一响应格式

所有 API 响应都应遵循以下 JSON 结构，便于前端统一处理。

Generated json
{
  "code": 0,
  "message": "Success",
  "data": {}
}
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Json
IGNORE_WHEN_COPYING_END

code: 0 表示成功, 其他非零值表示失败 (可自定义错误码)。

message: 响应消息，成功时为 "Success" 或具体信息，失败时为错误描述。

data: 响应数据，成功时为具体数据对象，失败时可为 null。

6.3 命名规范

统一使用 camelCase (小驼峰命名法) 作为前后端数据交换的黄金标准，其他场景遵循各自语言的最佳实践。

前后端交互的 JSON 字段: camelCase

{ "userId": 1, "taskTitle": "帮我带杯咖啡" }

JavaScript / TypeScript:

变量和函数名: camelCase (e.g., let taskList, function getUserInfo())

类名: PascalCase (e.g., class ApiClient)

Python:

变量和函数名: snake_case (e.g., task_list, get_user_info) (遵循 PEP8)

类名: PascalCase (e.g., class UserService)

数据库:

表名和字段名: snake_case (e.g., task_title, user_id)

文件名:

Python: snake_case.py (e.g., user_service.py)

Vue/JS: PascalCase.vue 或 camelCase.js (e.g., TaskCard.vue, taskApi.js)

7. 开发环境搭建 (Getting Started)
后端
Generated bash
# 1. 克隆仓库
git clone <repo_url>
cd geekbang-backend

# 2. 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置数据库
#    编辑 config.py 中的 SQLALCHEMY_DATABASE_URI

# 5. 执行数据库迁移
flask db upgrade

# 6. 启动服务
flask run
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
前端
Generated bash
# 1. 克隆仓库
git clone <repo_url>
cd geekbang-frontend

# 2. 安装依赖
npm install

# 3. 运行
#    使用 HBuilderX 打开项目，配置 manifest.json 中的微信小程序 AppID。
#    点击菜单栏的 "运行" -> "运行到小程序模拟器" -> "微信开发者工具"。
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
