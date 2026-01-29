---
title: Docker Build Cloud
weight: 20
description: 查找 Docker Build Cloud 文档，帮助您在本地和 CI 中更快速地构建容器镜像
keywords: build, cloud, cloud build, 远程构建器
params:
  sidebar:
    group: 产品
aliases:
  - /build/cloud/faq/
  - /build/cloud/
---

{{< summary-bar feature_name="Docker Build Cloud" >}}

Docker Build Cloud 是一项旨在让您在本地和 CI 中更快速地构建容器镜像的服务。构建运行在为您的工作负载优化配置的云基础设施上，无需任何配置。该服务使用远程构建缓存，确保任何地方、所有团队成员都能实现快速构建。

## Docker Build Cloud 的工作原理

使用 Docker Build Cloud 与运行普通构建没有区别。您像往常一样使用 `docker buildx build` 调用构建。区别在于构建执行的位置和方式。

默认情况下，当您调用构建命令时，构建运行在与 Docker 守护进程捆绑的本地 BuildKit 实例上。通过 Docker Build Cloud，您将构建请求发送到远程运行在云端的 BuildKit 实例。所有数据在传输过程中都是加密的。

远程构建器执行构建步骤，并将生成的构建输出发送到您指定的目标。例如，发送回您的本地 Docker Engine 镜像库，或发送到镜像库。

与本地构建相比，Docker Build Cloud 具有以下几项优势：

- 提高构建速度
- 共享构建缓存
- 原生多平台构建

最棒的是：您无需担心管理构建器或基础设施。只需连接到您的构建器，然后开始构建。为组织配置的每个云构建器都完全隔离在单个 Amazon EC2 实例中，并配有专门用于构建缓存的 EBS 卷，且传输过程经过加密。这意味着云构建器之间没有共享进程或数据。

> [!NOTE]
>
> Docker Build Cloud 目前仅在美国东部 (US East) 地区可用。欧洲和亚洲的用户与北美用户相比可能会感到延迟增加。
>
> 多区域构建器支持已列入路线图。

## 获取 Docker Build Cloud

要开始使用 Docker Build Cloud，请 [创建一个 Docker 账户](/accounts/create-account/)。有两种获取 Docker Build Cloud 访问权限的方式：

- 拥有免费个人（Personal）账户的用户可以选择参加 7 天免费试用，并可选择订阅以获得访问权限。要开始免费试用，请登录 [Docker Build Cloud 仪表板](https://app.docker.com/build/) 并按照屏幕上的说明进行操作。
- 所有拥有付费 Docker 订阅的用户都可以使用随 Docker 产品套件包含的 Docker Build Cloud。有关更多信息，请参阅 [Docker 订阅和功能](/manuals/subscription/details.md)。

注册并创建构建器后，请继续 [在本地环境中设置构建器](./setup.md)。

有关与 Docker Build Cloud 相关的角色和权限信息，请参阅 [角色和权限](/manuals/security/for-admins/roles-and-permissions.md#docker-build-cloud-权限)。
