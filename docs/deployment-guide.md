# DiResearchStudio 部署指南

## 架构概览

```
浏览器 (3000) ──► 前端 Next.js
                    │
                    ▼
              网关 FastAPI (8001) ──► SQLite / PostgreSQL
                    │
                    ├── /api/admin/*     用户管理、登录认证、可见性规则
                    ├── /api/threads/*   对话线程、运行流、SSE 流式响应
                    ├── /api/models      模型列表
                    ├── /api/mcp         MCP 配置
                    ├── /api/skills      技能管理
                    └── /health          健康检查
```

## 前置要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | 3.12+ | 后端运行时 |
| uv | latest | Python 包管理器 |
| Node.js | 20+ | 前端运行时（推荐 22+） |
| pnpm | 10.26+ | 前端包管理器 |
| Git | 2.x | 版本控制 |

数据库可选：
- **SQLite**（开发/测试环境，无需额外安装）
- **PostgreSQL**（生产环境推荐）

## 快速开始

### 1. 克隆代码

```bash
git clone https://github.com/chenbg123/researchstudio.git
cd researchstudio
git checkout diresearchstudio-enterprise
```

### 2. 安装依赖

```bash
# 后端
cd backend && uv sync && cd ..

# 前端
cd frontend && pnpm install && cd ..
```

或使用根目录 Makefile：

```bash
make install
```

### 3. 配置文件

#### 3.1 创建 `config.yaml`

从示例文件复制：

```bash
cp config.example.yaml config.yaml
```

#### 3.2 配置模型

在 `config.yaml` 的 `models:` 部分取消注释并配置你的模型，示例：

```yaml
models:
  # Anthropic Claude
  - name: claude-sonnet-4-6
    display_name: Claude Sonnet 4.6
    use: langchain_anthropic:ChatAnthropic
    model: claude-sonnet-4-6
    api_key: $ANTHROPIC_AUTH_TOKEN          # 引用 .env 中的环境变量
    anthropic_api_url: https://api.anthropic.com/  # 如有代理可替换
    default_request_timeout: 600.0
    max_retries: 2
    max_tokens: 8192
    supports_vision: true

  # OpenAI GPT-4
  # - name: gpt-4
  #   display_name: GPT-4
  #   use: langchain_openai:ChatOpenAI
  #   model: gpt-4
  #   api_key: $OPENAI_API_KEY
  #   request_timeout: 600.0
  #   max_tokens: 4096
```

#### 3.3 配置数据库

在 `config.yaml` 末尾添加 `gateway:` 部分：

**SQLite（开发环境）：**

```yaml
gateway:
  # 注意：SQLite 需要使用绝对路径，4个斜杠
  database_url: sqlite:////absolute/path/to/your/project/diresearchstudio.db
```

**PostgreSQL（生产环境）：**

```yaml
gateway:
  database_url: postgresql+psycopg://user:password@localhost:5432/diresearchstudio
```

#### 3.4 创建 `.env`

```bash
# 项目根目录创建 .env 文件
cat > .env << 'EOF'
ANTHROPIC_AUTH_TOKEN=your-api-key-here
# OPENAI_API_KEY=your-openai-key
EOF
```

### 4. 初始化数据库

```bash
cd backend

# 创建表结构
PYTHONPATH=. uv run python -c "
from app.db.base import Base
from app.db.models.user import User
from app.db.models.chat_thread import ChatThread
from app.db.models.chat_message import ChatMessage
from app.db.models.chat_element import ChatElement
from app.db.models.admin_visibility import AdminVisibility
from app.db.session import _get_engine
engine = _get_engine()
Base.metadata.create_all(engine)
print('Tables created:', list(Base.metadata.tables.keys()))
"

# 创建管理员用户（必须）
PYTHONPATH=. uv run python -c "
from app.db.session import get_session_factory
from app.services.auth import AuthService
factory = get_session_factory()
db = factory()
auth = AuthService(db)
user = auth.create_local_user(
    username='admin',
    password='admin123!',
    display_name='Admin',
    role='admin',
)
print(f'Admin user created: {user.id}')
db.close()
"

cd ..
```

### 5. 启动服务

#### 方式一：手动启动（推荐开发环境）

**终端 1 — 启动网关：**

```bash
cd backend
source ../.env
PYTHONPATH=. uv run uvicorn app.gateway.app:app \
  --host 0.0.0.0 --port 8001 --reload
```

**终端 2 — 启动前端：**

```bash
cd frontend
SKIP_ENV_VALIDATION=1 \
NEXT_PUBLIC_BACKEND_BASE_URL=http://localhost:8001 \
NEXT_PUBLIC_LANGGRAPH_BASE_URL=http://localhost:8001/api \
npx next dev --port 3000
```

#### 方式二：后台启动

```bash
# 启动网关（后台）
cd backend
source ../.env
PYTHONPATH=. nohup uv run uvicorn app.gateway.app:app \
  --host 0.0.0.0 --port 8001 --reload > ../logs/gateway.log 2>&1 &
echo "Gateway PID: $!"

# 启动前端（后台）
cd ../frontend
SKIP_ENV_VALIDATION=1 \
NEXT_PUBLIC_BACKEND_BASE_URL=http://localhost:8001 \
NEXT_PUBLIC_LANGGRAPH_BASE_URL=http://localhost:8001/api \
nohup npx next dev --port 3000 > ../logs/frontend.log 2>&1 &
echo "Frontend PID: $!"
```

> **远程访问（非 localhost）**：如果你从其他机器通过 IP 访问（如 `http://192.168.1.100:3000`），
> 需要将环境变量中的 `localhost` 替换为服务器实际 IP，并在 `config.yaml` 中配置 CORS：
>
> ```bash
> # 前端环境变量使用服务器 IP
> NEXT_PUBLIC_BACKEND_BASE_URL=http://192.168.1.100:8001 \
> NEXT_PUBLIC_LANGGRAPH_BASE_URL=http://192.168.1.100:8001/api \
> npx next dev --hostname 0.0.0.0 --port 3000
> ```
>
> ```yaml
> # config.yaml - 添加前端 origin 到 CORS 白名单
> gateway:
>   cors_origins:
>     - http://localhost:3000
>     - http://192.168.1.100:3000    # 替换为你的服务器 IP
> ```
>
> 也可以通过环境变量设置 CORS：`CORS_ORIGINS=http://localhost:3000,http://192.168.1.100:3000`

#### 方式三：`make dev`（需要 nginx + Node.js 22+）

```bash
make dev
```

> 此方式会同时启动 LangGraph Server + Gateway + Frontend + Nginx。
> 需要 Node.js 22+ 和系统安装 nginx。

### 6. 验证服务

```bash
# 健康检查
curl http://localhost:8001/health
# 期望: {"status":"healthy","service":"diresearchstudio-gateway"}

# 查看模型列表
curl http://localhost:8001/api/models
# 期望: {"models":[{"name":"claude-sonnet-4-6",...}]}
```

### 7. 访问应用

浏览器打开 `http://localhost:3000`

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123!`

---

## 常用命令

### 服务管理

```bash
# 查看服务状态
curl http://localhost:8001/health                 # 网关健康检查
lsof -i :8001                                    # 查看网关进程
lsof -i :3000                                    # 查看前端进程

# 查看日志
tail -f logs/gateway.log                          # 网关日志
tail -f logs/frontend.log                         # 前端日志

# 停止服务
kill $(lsof -t -i :8001)                          # 停止网关
kill $(lsof -t -i :3000)                          # 停止前端
make stop                                         # 停止所有（如果用 make dev 启动的）
```

### 用户管理（API）

```bash
# 登录（获取 session cookie）
curl -X POST http://localhost:8001/api/admin/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123!"}' \
  -c cookies.txt

# 查看当前会话
curl http://localhost:8001/api/admin/auth/session -b cookies.txt

# 列出所有用户
curl http://localhost:8001/api/admin/users -b cookies.txt

# 创建用户
curl -X POST http://localhost:8001/api/admin/users \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"alice123!","display_name":"Alice","role":"user"}' \
  -b cookies.txt

# 禁用用户
curl -X POST http://localhost:8001/api/admin/users/{user_id}/disable -b cookies.txt

# 重置密码
curl -X POST http://localhost:8001/api/admin/users/{user_id}/reset-password \
  -H 'Content-Type: application/json' \
  -d '{"password":"newpassword!"}' \
  -b cookies.txt

# 注销
curl -X POST http://localhost:8001/api/admin/auth/logout -b cookies.txt
```

### 数据库操作

```bash
cd backend

# 查看数据库中的用户
PYTHONPATH=. uv run python -c "
from app.db.session import get_session_factory
from app.db.models.user import User
db = get_session_factory()()
for u in db.query(User).all():
    print(f'{u.identifier:15} role={u.role:6} status={u.status}')
db.close()
"

# 添加用户（脚本方式）
PYTHONPATH=. uv run python -c "
from app.db.session import get_session_factory
from app.services.auth import AuthService
db = get_session_factory()()
auth = AuthService(db)
user = auth.create_local_user(
    username='newuser',
    password='password123!',
    display_name='New User',
    role='user',
)
print(f'User created: {user.identifier} ({user.id})')
db.close()
"

# SQLite 直接查看（如果用 SQLite）
sqlite3 diresearchstudio.db ".tables"
sqlite3 diresearchstudio.db "SELECT identifier, role, status FROM users;"
```

### 代码质量

```bash
# 后端
cd backend
make lint                    # 代码检查
make format                  # 代码格式化
make test                    # 运行测试

# 前端
cd frontend
pnpm lint                    # ESLint 检查
pnpm typecheck               # TypeScript 类型检查
pnpm check                   # lint + typecheck
```

---

## 环境变量参考

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ANTHROPIC_AUTH_TOKEN` | — | Anthropic API Key |
| `OPENAI_API_KEY` | — | OpenAI API Key |
| `DATABASE_URL` | 读取 config.yaml | 数据库连接 URL（覆盖 config.yaml） |
| `GATEWAY_HOST` | `0.0.0.0` | 网关绑定地址 |
| `GATEWAY_PORT` | `8001` | 网关端口 |
| `CORS_ORIGINS` | config.yaml 或 `http://localhost:3000` | CORS 允许的源（逗号分隔，覆盖 config.yaml） |
| `SKIP_ENV_VALIDATION` | — | 设为 `1` 跳过前端环境变量验证 |
| `NEXT_PUBLIC_BACKEND_BASE_URL` | — | 网关 API 地址 |
| `NEXT_PUBLIC_LANGGRAPH_BASE_URL` | — | LangGraph API 地址（需带 `/api`） |

---

## 目录结构（关键文件）

```
researchstudio/
├── .env                           # 环境变量（API Keys，不提交）
├── config.yaml                    # 应用配置（模型、数据库，不提交）
├── config.example.yaml            # 配置模板
├── Makefile                       # 根命令
├── backend/
│   ├── Makefile                   # 后端命令
│   ├── app/
│   │   ├── gateway/
│   │   │   ├── app.py             # FastAPI 应用入口
│   │   │   ├── config.py          # 网关配置（读 config.yaml + 环境变量）
│   │   │   └── routers/
│   │   │       ├── admin.py       # 认证 + 用户管理 + 可见性
│   │   │       ├── models.py      # 模型列表
│   │   │       ├── threads.py     # 线程管理
│   │   │       ├── thread_runs.py # 对话运行
│   │   │       └── ...
│   │   ├── db/
│   │   │   ├── base.py            # SQLAlchemy Base
│   │   │   ├── session.py         # 数据库会话工厂
│   │   │   └── models/            # ORM 模型
│   │   │       ├── user.py
│   │   │       ├── chat_thread.py
│   │   │       ├── chat_message.py
│   │   │       └── admin_visibility.py
│   │   └── services/
│   │       ├── auth.py            # 认证服务（密码哈希/验证）
│   │       └── visibility.py      # 可见性规则服务
│   └── packages/harness/deerflow/ # 核心框架包
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── login/page.tsx     # 登录页
│   │   │   └── workspace/         # 工作区
│   │   │       ├── admin/         # 管理控制台
│   │   │       └── chats/         # 聊天页
│   │   └── core/
│   │       ├── auth/              # 认证 hooks/api/types
│   │       ├── admin/             # 管理 hooks/api/types
│   │       ├── config/            # URL 配置
│   │       └── threads/           # 对话 hooks
│   └── package.json
└── logs/                          # 日志目录
```

---

## 常见问题

### Q: 登录后跳转回 /login

检查 `frontend/src/app/workspace/page.tsx` 是否还在使用 `better-auth` 的 `getSession()`。应该直接 `redirect("/workspace/chats/new")` 而不检查 better-auth session。

### Q: 前端请求报 CORS 错误

当浏览器通过非 `localhost` 地址（如 `http://192.168.1.100:3000`）访问时，需要确保：

1. **`NEXT_PUBLIC_BACKEND_BASE_URL`** 使用与浏览器相同的 IP（不能用 `localhost`，否则 cookie 跨域丢失）
2. **CORS 白名单** 包含浏览器的 origin

在 `config.yaml` 中配置：

```yaml
gateway:
  cors_origins:
    - http://localhost:3000
    - http://192.168.1.100:3000   # 替换为你的实际 IP
```

或通过环境变量：`CORS_ORIGINS=http://localhost:3000,http://192.168.1.100:3000`

> **原理**：前端 JS 使用 `credentials: "include"` 发送 cookie，浏览器要求 CORS 响应中
> `Access-Control-Allow-Origin` 必须是精确的 origin（不能是 `*`），且需要 `Access-Control-Allow-Credentials: true`。

### Q: SQLite 报 `pool_pre_ping` 错误

`backend/app/db/session.py` 中需要跳过 SQLite 的 `pool_pre_ping`：

```python
kwargs = {"future": True}
if not config.database_url.startswith("sqlite"):
    kwargs["pool_pre_ping"] = True
```

### Q: 聊天显示 404 Not Found

确保前端启动时 `NEXT_PUBLIC_LANGGRAPH_BASE_URL` 设为 `http://localhost:8001/api`（注意末尾的 `/api`）。LangGraph SDK 调用 `/threads` 等路径时，会拼接为 `http://localhost:8001/api/threads`。

### Q: `make dev` 失败提示 Node.js 版本

`scripts/check.py` 要求 Node.js 22+。可绕过 `make dev`，改为手动启动服务（参见"方式一"）。

### Q: config.yaml 的 gateway 配置不生效

确认 `config.yaml` 在项目���目录或 `backend/` 目录下，且格式正确：

```yaml
gateway:
  database_url: sqlite:////absolute/path/diresearchstudio.db
```

`get_gateway_config()` 读取优先级：**环境变量 > config.yaml > 默认值**。
