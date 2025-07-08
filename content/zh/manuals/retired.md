---
title: 已弃用和已停用的 Docker 产品和功能
linkTitle: 已弃用和已停用的产品和功能
description: |
  探索已弃用和已停用的 Docker 功能、产品和开源项目，包括有关已转换工具和已归档计划的详细信息。
params:
  sidebar:
    group: 产品
aliases:
  - /cloud/
  - /cloud/aci-compose-features/
  - /cloud/aci-container-features/
  - /cloud/aci-integration/
  - /cloud/ecs-architecture/
  - /cloud/ecs-compose-examples/
  - /cloud/ecs-compose-features/
  - /cloud/ecs-integration/
  - /engine/context/aci-integration/
  - /engine/context/ecs-integration/
  - /machine/
  - /machine/drivers/hyper-v/
  - /machine/get-started/
  - /machine/install-machine/
  - /machine/overview/
  - /registry/
  - /registry/compatibility/
  - /registry/configuration/
  - /registry/deploying/
  - /registry/deprecated/
  - /registry/garbage-collection/
  - /registry/help/
  - /registry/insecure/
  - /registry/introduction/
  - /registry/notifications/
  - /registry/recipes/
  - /registry/recipes/apache/
  - /registry/recipes/nginx/
  - /registry/recipes/osx-setup-guide/
  - /registry/spec/
  - /registry/spec/api/
  - /registry/spec/auth/
  - /registry/spec/auth/jwt/
  - /registry/spec/auth/oauth/
  - /registry/spec/auth/scope/
  - /registry/spec/auth/token/
  - /registry/spec/deprecated-schema-v1/
  - /registry/spec/implementations/
  - /registry/spec/json/
  - /registry/spec/manifest-v2-1/
  - /registry/spec/manifest-v2-2/
  - /registry/spec/menu/
  - /registry/storage-drivers/
  - /registry/storage-drivers/azure/
  - /registry/storage-drivers/filesystem/
  - /registry/storage-drivers/gcs/
  - /registry/storage-drivers/inmemory/
  - /registry/storage-drivers/oss/
  - /registry/storage-drivers/s3/
  - /registry/storage-drivers/swift/
  - /toolbox/
  - /toolbox/overview/
  - /toolbox/toolbox_install_mac/
  - /toolbox/toolbox_install_windows/
  - /desktop/features/dev-environments/
  - /desktop/features/dev-environments/create-dev-env/
  - /desktop/features/dev-environments/set-up/
  - /desktop/features/dev-environments/share/
  - /desktop/features/dev-environments/dev-cli/
---

本文档概述了已弃用、已停用或已转换的 Docker 功能、产品和开源项目。

> [!NOTE]
>
> 本文档不涵盖已弃用和已移除的 Docker 引擎功能。
> 有关已弃用的 Docker 引擎功能的详细列表，请参阅
> [Docker 引擎已弃用功能文档](/manuals/engine/deprecated.md)。

## 产品和功能

Docker, Inc. 不再为这些已弃用或已停用的功能提供支持。已移交给第三方的项目将继续由其新的维护者提供更新。

### Docker Machine

Docker Machine 是一种用于在各种平台（包括虚拟机和云提供商）上配置和管理 Docker 主机的工具。它已不再维护，建议用户直接在支持的平台上使用 [Docker Desktop](/manuals/desktop/_index.md) 或 [Docker Engine](/manuals/engine/_index.md)。Machine 创建和配置主机的方法已被更现代的工作流程所取代，这些工作流程与 Docker Desktop 的集成更紧密。

### Docker Toolbox

Docker Toolbox 用于无法运行 Docker Desktop 的旧系统。它将 Docker Machine、Docker Engine 和 Docker Compose 捆绑到一个安装程序中。Toolbox 已不再维护，在当前系统上已被 [Docker Desktop](/manuals/desktop/_index.md) 有效取代。在较旧的文档或社区教程中偶尔会看到对 Docker Toolbox 的引用，但不建议用于新安装。

### Docker Cloud 集成

Docker 以前为亚马逊的弹性容器服务 (ECS) 和 Azure 容器实例 (ACI) 提供集成，以简化容器工作流程。这些集成已被弃用，用户现在应依赖本机云工具或第三方解决方案来管理其工作负载。向平台特定或通用编排工具的转变减少了对专门的 Docker Cloud 集成的需求。

您仍然可以在 [Compose CLI 存储库](https://github.com/docker-archive/compose-cli/tree/main/docs)中查看这些集成的相关文档。

### Docker 企业版

Docker 企业版 (EE) 是 Docker 用于部署和管理大规模容器环境的商业平台。它于 2019 年被 Mirantis 收购，寻求企业级功能的用户现在可以探索 Mirantis Kubernetes Engine 或 Mirantis 提供的其他产品。Docker EE 中的许多技术和功能已被吸收到 Mirantis 产品线中。

> [!NOTE]
> 有关 Docker 今天提供的企业级功能的信息，请参阅 [Docker Business 订阅](/manuals/subscription/details.md#docker-business)。

### Docker 数据中心和 Docker 受信注册表

Docker 数据中心 (DDC) 是一个总称，包括 Docker 通用控制平面 (UCP) 和 Docker 受信注册表 (DTR)。这些组件为在企业环境中管理容器、安全性和注册表服务提供了全栈解决方案。在 Docker Enterprise 被收购后，它们现在属于 Mirantis 产品组合。仍然遇到对 DDC、UCP 或 DTR 的引用的用户应参阅 Mirantis 的文档以获取有关现代等效项的指导。

### 开发环境

开发环境是 Docker Desktop 中引入的一项功能，允许开发人员快速启动开发环境。它已在 Docker Desktop 4.42 及更高版本中被弃用和移除。可以通过 Docker Compose 或创建针对特定项目需求量身定制的自定义配置来实现类似的工作流程。

## 开源项目

最初由 Docker 维护的几个开源项目已被归档、终止或移交给其他维护者或组织。

### 注册表（现为 CNCF 发行版）

Docker 注册表是容器镜像注册表的开源实现。它于 2019 年捐赠给云原生计算基金会 (CNCF)，并以“发行版”的名称进行维护。它仍然是管理和分发容器镜像的基石。

[CNCF 发行版](https://github.com/distribution/distribution)

### Docker Compose v1（由 Compose v2 取代）

Docker Compose v1 (`docker-compose`) 是一个用于定义多容器应用程序的基于 Python 的工具，已被用 Go 编写并与 Docker CLI 集成的 Compose v2 (`docker compose`) 取代。Compose v1 已不再维护，用户应迁移到 Compose v2。

[Compose v2 文档](/manuals/compose/_index.md)

### InfraKit

InfraKit 是一个开源工具包，旨在管理声明性基础架构并自动化容器部署。它已被归档，建议用户探索 Terraform 等工具进行基础架构配置和编排。

[InfraKit GitHub 存储库](https://github.com/docker/infrakit)

### Docker Notary（现为 CNCF Notary）

Docker Notary 是一个用于签名和验证容器内容真实性的系统。它于 2017 年捐赠给 CNCF，并继续作为“Notary”进行开发。寻求安全内容验证的用户应查阅 CNCF Notary 项目。

[CNCF Notary](https://github.com/notaryproject/notary)

### SwarmKit

SwarmKit 通过为容器部署提供编排来支持 Docker Swarm 模式。虽然 Swarm 模式仍然可用，但为了支持基于 Kubernetes 的解决方案，开发速度已经放缓。评估容器编排选项的个人应调查 SwarmKit 是否满足现代工作负载要求。

[SwarmKit GitHub 存储库](https://github.com/docker/swarmkit)
