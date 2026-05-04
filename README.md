# FRP Controller

FRP 内网穿透隧道管理工具。管理多个 frp 客户端的启动、停止和监控。

## 功能

- 支持多隧道并行管理
- 自动扫描 `config/` 目录下的配置文件
- 使用 `screen` 会话管理隧道进程
- 支持隧道的启动、停止、列表查看

## 使用方法

### 1. 添加配置文件

在 `config/` 目录下放置 `.toml` 配置文件：

```
config/
├── web.toml          # 直接放 config/ 下
└── mc/
    └── server.toml   # 子目录里也会自动识别
```

### 2. 初始化配置

```bash
python3 copy_configs.py
```

### 3. 管理隧道

```bash
# 启动所有隧道
python3 lib.py

# 查看运行中的隧道
python3 list.py
```

## 目录结构

```
frp_controller/
├── lib.py          # 核心库：隧道管理、screen 会话控制
├── list.py         # 列出运行中的隧道
├── copy_configs.py # 初始化配置文件
├── config/         # 隧道配置文件目录 (已 gitignore)
└── frp/            # frp 客户端程序 (已 gitignore)
```

## 依赖

- Linux 系统
- `screen` 命令
- `frpc` 客户端
