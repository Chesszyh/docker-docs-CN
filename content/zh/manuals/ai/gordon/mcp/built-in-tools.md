---
title: 内置工具
description: 如何使用 Gordon 的内置工具
keywords: ai, mcp, gordon
aliases:
 - /desktop/features/gordon/mcp/built-in-tools/
---

Gordon 配备了一个集成的工具箱，提供对各种系统工具和功能的访问。这些工具通过允许 Gordon 与 Docker Engine、Kubernetes、Docker Scout 的安全扫描以及其他开发者实用程序进行交互，扩展了 Gordon 的功能。本文档涵盖了可用工具、其配置及使用模式。

## 配置

工具可以在工具箱中进行全局配置，使其在整个 Gordon 界面（包括 Docker Desktop 和 CLI）中均可访问。

配置步骤：

1. 在 Docker Desktop 的 **Ask Gordon** 视图中，选择输入区域左下角的 `Toolbox`（工具箱）按钮。

   ![带有工具箱按钮的 Gordon 页面](../images/gordon.png)

2. 要启用或禁用某个工具，请在左侧菜单中选择该工具，然后切换开关。

   ![Gordon 的工具箱](../images/toolbox.png)

   有关可用 Docker 工具的更多信息，请参阅 [参考](#参考)。

## 使用示例

本节提供了针对 Gordon 工具常用操作的任务导向型示例。

### 管理 Docker 容器

#### 列出并监控容器

```console
# 列出所有运行中的容器
$ docker ai "显示所有运行中的容器"

# 列出使用特定资源的容器
$ docker ai "列出所有内存使用超过 1GB 的容器"

# 查看特定容器的日志
$ docker ai "显示运行中的 api-container 过去一小时的日志"
```

#### 管理容器生命周期

```console
# 运行一个新容器
$ docker ai "运行一个将 80 端口映射到本地主机的 nginx 容器"

# 停止特定容器
$ docker ai "停止我的数据库容器"

# 清理未使用的容器
$ docker ai "移除所有已停止的容器"
```

### 使用 Docker 镜像

```console
# 列出可用镜像
$ docker ai "显示我所有的本地 Docker 镜像"

# 拉取特定镜像
$ docker ai "拉取最新的 Ubuntu 镜像"

# 从 Dockerfile 构建镜像
$ docker ai "从我当前目录构建一个镜像并将其标记为 myapp:latest"

# 清理未使用的镜像
$ docker ai "移除我所有未使用的镜像"
```

### 管理 Docker 卷

```console
# 列出卷
$ docker ai "列出我所有的 Docker 卷"

# 创建一个新卷
$ docker ai "创建一个名为 postgres-data 的新卷"

# 将数据从容器备份到卷
$ docker ai "将我的 postgres 容器数据备份到一个新卷"
```

### Kubernetes 操作

```console
# 创建一个部署
$ docker ai "创建一个 nginx 部署并确保它在本地暴露"

# 列出资源
$ docker ai "显示默认命名空间中的所有部署"

# 获取日志
$ docker ai "显示 auth-service pod 的日志"
```

### 安全分析


```console
# 扫描 CVE
$ docker ai "扫描我的应用程序的安全漏洞"

# 获取安全建议
$ docker ai "给我一些关于提高 nodejs-app 镜像安全性的建议"
```

### 开发工作流

```console
# 分析并提交更改
$ docker ai "查看我的本地更改，创建多个带有合理提交消息的 commit"

# 检查分支状态
$ docker ai "显示我当前分支与 main 分支相比的状态"
```

## 参考

本节提供了 Gordon 工具箱中内置工具的完整列表。

### Docker 工具

用于与您的 Docker 容器、镜像和卷进行交互的工具。

#### 容器管理

| 名称 | 说明 |
|:---|:---|
| `docker` | 访问 Docker CLI |
| `list_builds` | 列出 Docker 守护进程中的构建 |
| `build_logs` | 显示构建日志。 |

#### 卷管理

| 工具 | 说明 |
|:---|:---|
| `list_volumes` | 列出所有 Docker 卷 |
| `remove_volume` | 移除一个 Docker 卷 |
| `create_volume` | 创建一个新 Docker 卷 |

#### 镜像管理

| 工具 | 说明 |
|:---|:---|
| `list_images` | 列出所有 Docker 镜像 |
| `remove_images` | 移除 Docker 镜像 |
| `pull_image` | 从镜像库拉取镜像 |
| `push_image` | 将镜像推送到镜像库 |
| `build_image` | 构建 Docker 镜像 |
| `tag_image` | 标记 Docker 镜像 |
| `inspect` | 检查 Docker 对象 |

### Kubernetes 工具

用于与您的 Kubernetes 集群交互的工具

#### Pod

| 工具 | 说明 |
|:---|:---|
| `list_pods` | 列出集群中的所有 Pod |
| `get_pod_logs` | 获取特定 Pod 的日志 |

#### 部署管理


| 工具 | 说明 |
|:---|:---|
| `list_deployments` | 列出所有部署 |
| `create_deployment` | 创建新部署 |
| `expose_deployment` | 将部署公开为服务 |
| `remove_deployment` | 移除部署 |

#### 服务管理

| 工具 | 说明 |
|:---|:---|
| `list_services` | 列出所有服务 |
| `remove_service` | 移除服务 |

#### 集群信息

| 工具 | 说明 |
|:---|:---|
| `list_namespaces` | 列出所有命名空间 |
| `list_nodes` | 列出集群中的所有节点 |

### Docker Scout 工具

由 Docker Scout 驱动的安全分析工具。

| 工具 | 说明 |
|:---|:---|
| `search_for_cves` | 使用 Docker Scout CVE 搜索功能分析 Docker 镜像、项目目录或其他构件的漏洞。 |
| `get_security_recommendations` | 使用 Docker Scout 分析 Docker 镜像、项目目录或其他构件，以获取基础镜像更新建议。 |

### 开发者工具

通用开发实用程序。

| 工具 | 说明 |
|:---|:---|
| `fetch` | 从 URL 获取内容 |
| `get_command_help` | 获取 CLI 命令的帮助 |
| `run_command` | 执行 shell 命令 |
| `filesystem` | 执行文件系统操作 |
| `git` | 执行 git 命令 |

### AI 模型工具

| 工具 | 说明 |
|:---|:---|
| `list_models` | 列出所有可用的 Docker 模型 |
| `pull_model` | 下载 Docker 模型 |
| `run_model` | 使用提示词查询模型 |
| `remove_model` | 移除 Docker 模型 |

### Docker MCP 目录

如果您启用了 [MCP 工具包功能](../../mcp-catalog-and-toolkit/_index.md)，则您启用并配置的所有工具都可供 Gordon 使用。
