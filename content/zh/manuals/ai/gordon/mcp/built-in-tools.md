---
title: 内置工具
description: 如何使用 Gordon 的内置工具
keywords: ai, mcp, gordon
aliases:
 - /desktop/features/gordon/mcp/built-in-tools/
---

Gordon 配备了一个集成工具箱，提供对各种系统工具和功能的访问。这些工具通过允许 Gordon 与 Docker Engine、Kubernetes、Docker Scout 的安全扫描以及其他开发者实用工具进行交互来扩展其功能。本文档涵盖了可用的工具、它们的配置和使用模式。

## 配置

工具可以在工具箱中全局配置，使它们可以在整个 Gordon 界面中访问，包括 Docker Desktop 和 CLI。

配置方法：

1. 在 Docker Desktop 的 **Ask Gordon** 视图中，选择输入区域左下角的 `Toolbox` 按钮。

   ![带有工具箱按钮的 Gordon 页面](../images/gordon.png)

2. 要启用或禁用工具，请在左侧菜单中选择它并选择切换开关。

   ![Gordon 的工具箱](../images/toolbox.png)

   有关可用 Docker 工具的更多信息，请参阅[参考](#参考)。

## 使用示例

本节提供了使用 Gordon 工具进行常见操作的面向任务的示例。

### 管理 Docker 容器

#### 列出和监控容器

```console
# List all running containers
$ docker ai "Show me all running containers"

# List containers using specific resources
$ docker ai "List all containers using more than 1GB of memory"

# View logs from a specific container
$ docker ai "Show me logs from my running api-container from the last hour"
```

#### 管理容器生命周期

```console
# Run a new container
$ docker ai "Run a nginx container with port 80 exposed to localhost"

# Stop a specific container
$ docker ai "Stop my database container"

# Clean up unused containers
$ docker ai "Remove all stopped containers"
```

### 处理 Docker 镜像

```console
# List available images
$ docker ai "Show me all my local Docker images"

# Pull a specific image
$ docker ai "Pull the latest Ubuntu image"

# Build an image from a Dockerfile
$ docker ai "Build an image from my current directory and tag it as myapp:latest"

# Clean up unused images
$ docker ai "Remove all my unused images"
```

### 管理 Docker 卷

```console
# List volumes
$ docker ai "List all my Docker volumes"

# Create a new volume
$ docker ai "Create a new volume called postgres-data"

# Backup data from a container to a volume
$ docker ai "Create a backup of my postgres container data to a new volume"
```

### Kubernetes 操作

```console
# Create a deployment
$ docker ai "Create an nginx deployment and make sure it's exposed locally"

# List resources
$ docker ai "Show me all deployments in the default namespace"

# Get logs
$ docker ai "Show me logs from the auth-service pod"
```

### 安全分析


```console
# Scan for CVEs
$ docker ai "Scan my application for security vulnerabilities"

# Get security recommendations
$ docker ai "Give me recommendations for improving the security of my nodejs-app image"
```

### 开发工作流程

```console
# Analyze and commit changes
$ docker ai "Look at my local changes, create multiple commits with sensible commit messages"

# Review branch status
$ docker ai "Show me the status of my current branch compared to main"
```

## 参考

本节提供了 Gordon 工具箱中内置工具的完整列表。

### Docker 工具

用于与 Docker 容器、镜像和卷交互的工具。

#### 容器管理

| 名称          | 描述                            |
|---------------|----------------------------------------|
| `docker`      | 访问 Docker CLI               |
| `list_builds` | 列出 Docker 守护进程中的构建   |
| `build_logs`  | 显示构建日志。                   |

#### 卷管理

| 工具 | 描述 |
|------|-------------|
| `list_volumes` | 列出所有 Docker 卷 |
| `remove_volume` | 删除 Docker 卷 |
| `create_volume` | 创建新的 Docker 卷 |

#### 镜像管理

| 工具 | 描述 |
|------|-------------|
| `list_images` | 列出所有 Docker 镜像 |
| `remove_images` | 删除 Docker 镜像 |
| `pull_image` | 从注册表拉取镜像 |
| `push_image` | 推送镜像到注册表 |
| `build_image` | 构建 Docker 镜像 |
| `tag_image` | 标记 Docker 镜像 |
| `inspect` | 检查 Docker 对象 |

### Kubernetes 工具

用于与 Kubernetes 集群交互的工具

#### Pod

| 工具 | 描述 |
|------|-------------|
| `list_pods` | 列出集群中的所有 Pod |
| `get_pod_logs` | 获取特定 Pod 的日志 |

#### 部署管理


| 工具 | 描述 |
|------|-------------|
| `list_deployments` | 列出所有部署 |
| `create_deployment` | 创建新部署 |
| `expose_deployment` | 将部署暴露为服务 |
| `remove_deployment` | 删除部署 |

#### 服务管理

| 工具 | 描述 |
|------|-------------|
| `list_services` | 列出所有服务 |
| `remove_service` | 删除服务 |

#### 集群信息

| 工具 | 描述 |
|------|-------------|
| `list_namespaces` | 列出所有命名空间 |
| `list_nodes` | 列出集群中的所有节点 |

### Docker Scout 工具

由 Docker Scout 提供支持的安全分析工具。

| 工具 | 描述 |
|------|-------------|
| `search_for_cves` | 使用 Docker Scout CVEs 分析 Docker 镜像、项目目录或其他制品的漏洞，搜索 CVE |
| `get_security_recommendations` | 使用 Docker Scout 分析 Docker 镜像、项目目录或其他制品，获取基础镜像更新建议。 |

### 开发者工具

通用开发实用工具。

| 工具 | 描述 |
|------|-------------|
| `fetch` | 从 URL 获取内容 |
| `get_command_help` | 获取 CLI 命令的帮助 |
| `run_command` | 执行 shell 命令 |
| `filesystem` | 执行文件系统操作 |
| `git` | 执行 git 命令 |

### AI 模型工具

| 工具 | 描述 |
|------|-------------|
| `list_models` | 列出所有可用的 Docker 模型 |
| `pull_model` | 下载 Docker 模型 |
| `run_model` | 使用提示词查询模型 |
| `remove_model` | 删除 Docker 模型 |

### Docker MCP Catalog

如果你启用了 [MCP Toolkit 功能](../../mcp-catalog-and-toolkit/_index.md)，你已启用和配置的所有工具都可供 Gordon 使用。
