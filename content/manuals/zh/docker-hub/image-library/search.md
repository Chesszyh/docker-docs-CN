---
description: 了解如何浏览和搜索 Docker Hub 的丰富资源。
keywords: Docker Hub, Hub, explore, search, image library
title: Docker Hub 搜索
linkTitle: 搜索
weight: 10
---

[Docker Hub 搜索界面](https://hub.docker.com/search)让您可以探索数百万资源。为了帮助您找到所需的内容，它提供了各种过滤器，让您可以缩小结果范围或发现不同类型的内容。

## 过滤器

搜索功能包括根据您的需求缩小结果范围的过滤器，例如产品、类别和可信内容。这确保您可以快速找到和访问最适合您项目的资源。

### 产品

Docker Hub 的内容库包含三种产品，每种产品旨在满足开发人员和组织的特定需求。这些产品包括镜像、插件和扩展。

#### 镜像

Docker Hub 托管数百万个容器镜像，使其成为容器化应用程序和解决方案的首选仓库。这些镜像包括：

- 操作系统镜像：Linux 发行版的基础镜像，如 Ubuntu、Debian 和 Alpine，或 Windows Server 镜像。
- 数据库和存储镜像：预配置的数据库，如 MySQL、PostgreSQL 和 MongoDB，以简化应用程序开发。
- 语言和框架镜像：流行的 Java、Python、Node.js、Ruby、.NET 等镜像，提供预构建的环境以加快开发速度。

Docker Hub 中的镜像通过提供预构建、可重用的构建块来简化开发过程，减少从头开始的需要。无论您是构建第一个容器的初学者还是管理复杂架构的企业，Docker Hub 镜像都提供了可靠的基础。

#### 插件

Docker Hub 中的插件让您可以扩展和自定义 Docker Engine 以满足特殊需求。插件直接与 Docker Engine 集成，提供以下功能：

- 网络插件：增强网络功能，支持与复杂网络基础设施的集成。
- 卷插件：提供高级存储选项，支持跨各种后端的持久化和分布式存储。
- 授权插件：提供细粒度的访问控制以保护 Docker 环境。

通过利用 Docker 插件，团队可以定制 Docker Engine 以满足其特定的运营需求，确保与现有基础设施和工作流程的兼容性。

要了解更多关于插件的信息，请参阅 [Docker Engine 托管插件系统](/manuals/engine/extend/_index.md)。

#### 扩展

Docker Hub 为 Docker Desktop 提供扩展，增强其核心功能。这些扩展专门用于简化软件开发生命周期。扩展提供以下工具：

- 系统优化和监控：管理资源并优化 Docker Desktop 的性能。
- 容器管理：简化容器部署和监控。
- 数据库管理：在容器内促进高效的数据库操作。
- Kubernetes 和云集成：连接本地环境与云原生和 Kubernetes 工作流程。
- 可视化工具：通过图形表示获得容器资源使用情况的洞察。

扩展通过减少上下文切换并将基本工具引入 Docker Desktop 界面，帮助开发人员和团队创建更高效和统一的工作流程。

要了解更多关于扩展的信息，请参阅 [Docker 扩展](/manuals/extensions/_index.md)。

### 可信内容

Docker Hub 的可信内容提供精心策划的高质量、安全镜像选择，旨在让开发人员对其使用的资源的可靠性和安全性充满信心。这些镜像稳定、定期更新，并遵循行业最佳实践，使其成为构建和部署应用程序的坚实基础。Docker Hub 的可信内容包括 Docker 官方镜像、经过验证的发布商镜像和 Docker 赞助的开源软件镜像。

有关更多详细信息，请参阅[可信内容](./trusted-content.md)。

### 类别

Docker Hub 通过类别使查找和探索容器镜像变得容易。类别根据主要用例对镜像进行分组，帮助您快速找到构建、部署和运行应用程序所需的工具和资源。

{{% include "hub-categories.md" %}}

### 操作系统

**Operating systems**（操作系统）过滤器让您可以将搜索范围缩小到与特定主机操作系统兼容的容器镜像。此过滤器确保您使用的镜像与目标环境一致，无论您是为基于 Linux 的系统、Windows 还是两者开发。

- **Linux**：访问为 Linux 环境定制的各种镜像。这些镜像为在容器中构建和运行基于 Linux 的应用程序提供基础环境。
- **Windows**：探索 Windows 容器镜像。

> [!NOTE]
>
> **Operating systems**（操作系统）过滤器仅适用于镜像。如果您选择 **Extensions**（扩展）或 **Plugins**（插件）过滤器，则 **Operating systems**（操作系统）过滤器不可用。

### 架构

**Architectures**（架构）过滤器让您可以找到为支持特定 CPU 架构而构建的镜像。这确保了与您的硬件环境的兼容性，从开发机器到生产服务器。

- **ARM**：选择与 ARM 处理器兼容的镜像，常用于物联网设备和嵌入式系统。
- **ARM 64**：查找与现代 ARM 处理器兼容的 64 位 ARM 镜像，如 AWS Graviton 或 Apple Silicon 中的处理器。
- **IBM POWER**：查找为 IBM Power Systems 优化的镜像，为企业工作负载提供性能和可靠性。
- **PowerPC 64 LE**：访问为小端序 PowerPC 64 位架构设计的镜像。
- **IBM Z**：发现为 IBM Z 大型机定制的镜像，确保与企业级硬件的兼容性。
- **x86**：选择与 32 位 x86 架构兼容的镜像，适用于较旧的系统或轻量级环境。
- **x86-64**：过滤现代 64 位 x86 系统的镜像，广泛用于桌面、服务器和云基础设施。

> [!NOTE]
>
> **Architectures**（架构）过滤器仅适用于镜像。如果您选择 **Extensions**（扩展）或 **Plugins**（插件）过滤器，则 **Architectures**（架构）过滤器不可用。

### Docker 审核

**Reviewed by Docker**（Docker 审核）过滤器在选择扩展时提供额外的保证层。此过滤器帮助您识别 Docker Desktop 扩展是否已经过 Docker 的质量和可靠性审核。

- **Reviewed**（已审核）：经过 Docker 审核流程的扩展，确保它们符合高标准。
- **Not Reviewed**（未审核）：未经过 Docker 审核的扩展。

> [!NOTE]
>
> **Reviewed by Docker**（Docker 审核）过滤器仅适用于扩展。要使此过滤器可用，您必须在 **Products**（产品）中仅选择 **Extensions**（扩展）过滤器。
