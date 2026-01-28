---
title: Docker Build Cloud
weight: 20
description: 查找 Docker Build Cloud 文档，帮助您在本地和 CI 中更快地构建容器镜像
keywords: build, cloud, cloud build, remote builder
params:
  sidebar:
    group: Products
aliases:
  - /build/cloud/faq/
  - /build/cloud/
---

{{< summary-bar feature_name="Docker Build Cloud" >}}

Docker Build Cloud 是一项服务，可让您在本地和 CI 中更快地构建容器镜像。构建在针对您的工作负载进行优化配置的云基础设施上运行，无需配置。该服务使用远程构建缓存，确保所有团队成员在任何地方都能快速构建。

## Docker Build Cloud 的工作原理

使用 Docker Build Cloud 与运行常规构建没有区别。您以通常的方式调用构建，使用 `docker buildx build`。区别在于构建的执行位置和方式。

默认情况下，当您调用构建命令时，构建在与 Docker 守护进程捆绑的本地 BuildKit 实例上运行。使用 Docker Build Cloud，您将构建请求发送到在云端远程运行的 BuildKit 实例。所有数据在传输过程中都是加密的。

远程构建器执行构建步骤，并将生成的构建输出发送到您指定的目标。例如，返回到您本地的 Docker Engine 镜像存储，或发送到镜像仓库。

Docker Build Cloud 相比本地构建提供了多项优势：

- 提升构建速度
- 共享构建缓存
- 原生多平台构建

最棒的是：您无需担心管理构建器或基础设施。只需连接到您的构建器，即可开始构建。每个为组织配置的云构建器都完全隔离在单独的 Amazon EC2 实例上，具有专用的 EBS 卷用于构建缓存，并在传输过程中加密。这意味着云构建器之间没有共享的进程或数据。

> [!NOTE]
>
> Docker Build Cloud 目前仅在美国东部区域可用。与北美用户相比，欧洲和亚洲的用户可能会遇到较高的延迟。
>
> 多区域构建器的支持已在路线图中。

## 获取 Docker Build Cloud

要开始使用 Docker Build Cloud，请[创建一个 Docker 账户](/accounts/create-account/)。有两种方式可以获取 Docker Build Cloud 的访问权限：

- 拥有免费 Personal 账户的用户可以选择 7 天免费试用，并可选择订阅以继续访问。要开始免费试用，请登录 [Docker Build Cloud Dashboard](https://app.docker.com/build/) 并按照屏幕上的说明操作。
- 所有拥有付费 Docker 订阅的用户都可以访问 Docker Build Cloud，作为其 Docker 产品套件的一部分。有关更多信息，请参阅 [Docker 订阅和功能](/manuals/subscription/details.md)。

注册并创建构建器后，继续[在本地环境中设置构建器](./setup.md)。

有关 Docker Build Cloud 相关角色和权限的信息，请参阅[角色和权限](/manuals/security/for-admins/roles-and-permissions.md#docker-build-cloud-permissions)。
