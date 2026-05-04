# FRP Controller

FRP 内网穿透隧道管理工具。管理多个 frp 客户端的启动、停止和监控。

## 功能

- 支持多隧道并行管理
- 自动扫描 `config/` 目录下的配置文件
- 使用 `screen` 会话管理隧道进程
- 支持隧道的启动、停止、列表查看

## 环境要求

- **Linux 系统**（screen 命令在 Linux 上原生支持）
- **`screen`** — 用于后台会话管理（`apt install screen` 或 `yum install screen`）
- **`frpc`** — FRP 客户端程序，[前往 frp 发布页下载](https://github.com/fatedier/frp/releases)

## 快速开始

### 1. 安装 frpc

从 [frp Releases](https://github.com/fatedier/frp/releases) 下载对应系统的版本，将 `frpc` 放到项目根目录：

```
frp_controller/
└── frp/
    ├── frpc          # frp 客户端程序
    └── frprun.sh     # 断线自动重连脚本
```

> 或者放到任意位置后在配置中指定路径。

### 2. 添加配置文件

在 `config/` 目录下放置 `.toml` 格式的 frp 配置文件：

```
config/
├── web.toml          # 直接放 config/ 下
└── mc/
    └── server.toml   # 子目录里也会自动识别
```

配置文件示例（`config/web.toml`）：
```toml
[common]
server_addr = your.server.com
server_port = 7000
auth.token = your-token

[web]
type = http
local_port = 8080
custom_domains = web.your.com
```

### 3. 初始化配置

```bash
# 将 config/ 下的配置文件展开到 config_root/（处理子目录结构）
python3 copy_configs.py
```

### 4. 管理隧道

```bash
# 启动所有隧道
python3 start.py

# 查看运行中的隧道
python3 list.py

# 停止所有隧道
python3 stop.py

# 测试单个隧道
python3 frptest.py
```

## 配置文件智能识别

`lib.py` 中的 `get_config()` 会自动扫描 `config/` 目录，按规则生成配置名：

| 文件位置 | 生成的配置名 |
|---------|-------------|
| `config/web.toml` | `FRPAUTO_web` |
| `config/mc/server.toml` | `FRPAUTO_mc.server` |

每个配置会以 `FRPAUTO_` 前缀的 screen 会话运行。

## 目录结构

```
frp_controller/
├── lib.py          # 核心库：配置扫描、screen 会话管理
├── start.py        # 启动所有隧道
├── stop.py         # 停止所有隧道
├── list.py         # 列出运行中的隧道
├── copy_configs.py # 配置初始化工具
├── sfz.py          # 身份证号生成工具（辅助用途）
├── config/         # 隧道配置文件目录（敏感信息，已 .gitignore）
├── config_root/    # 展开后的配置（自动生成，已 .gitignore）
└── frp/            # frp 二进制程序（已 .gitignore）
```

## 注意事项

- `config/` 目录中的 .toml 文件包含服务器地址、token 等敏感信息，已加入 `.gitignore`，**不会被提交到 GitHub**
- 运行前请确保 `frpc` 已放置到 `frp/` 目录下
- screen 会话名为 `FRPAUTO_xxx` 格式，方便识别
