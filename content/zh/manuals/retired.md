---
title: 已弃用和已退役的 Docker 产品与特性
linkTitle: 已弃用产品与特性
description: |
  探索已弃用和已退役的 Docker 特性、产品以及开源项目，包括有关过渡工具和存档计划的详细信息。
params:
  sidebar:
    group: 产品 (Products)
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

本文档概述了已弃用、退役或发生转型的 Docker 特性、产品以及开源项目。

> [!NOTE]
>
> 本页不涵盖已弃用和已移除的 Docker Engine 特性。有关已弃用 Docker Engine 特性的详细列表，请参阅 [Docker Engine 已弃用特性文档](/manuals/engine/deprecated.md)。

## 产品与特性

Docker, Inc. 不再为这些已弃用或退役的特性提供支持。已移交给第三方的项目将继续由其新维护者进行更新。

### Docker Machine

Docker Machine 曾是用于在各种平台（包括虚拟机和云提供商）上预配和管理 Docker 宿主机的工具。它目前已不再维护，建议用户在受支持的平台上直接使用 [Docker Desktop](/manuals/desktop/_index.md) 或 [Docker Engine](/manuals/engine/_index.md)。Machine 创建和配置宿主机的方法已被与 Docker Desktop 集成更紧密的现代化工作流所取代。

### Docker Toolbox

Docker Toolbox 曾用于无法运行 Docker Desktop 的旧版系统。它将 Docker Machine、Docker Engine 和 Docker Compose 捆绑在一个安装程序中。Toolbox 现已不再维护，在当前系统中已被 [Docker Desktop](/manuals/desktop/_index.md) 有效替代。尽管在旧文档或社区教程中偶尔还会出现 Docker Toolbox 的引用，但不建议用于新安装。

### Docker Cloud 集成 (Docker Cloud integrations)

Docker 之前曾为 Amazon 的 Elastic Container Service (ECS) 和 Azure Container Instances (ACI) 提供集成，以简化容器工作流。这些集成现已弃用，用户现在应依赖原生云工具或第三方解决方案来管理其工作负载。向特定平台或通用编排工具的转型，减少了对专门的 Docker Cloud 集成的需求。

您仍然可以在 [Compose CLI 存储库](https://github.com/docker-archive/compose-cli/tree/main/docs) 中查看这些集成的相关文档。

### Docker 企业版 (Docker Enterprise Edition)

Docker 企业版 (EE) 曾是 Docker 用于部署和管理大规模容器环境的商业平台。它于 2019 年被 Mirantis 收购，寻求企业级功能的用户现在可以探索 Mirantis Kubernetes Engine 或 Mirantis 提供的其他产品。Docker EE 中包含的大部分技术和特性已被吸收进 Mirantis 产品线中。

> [!NOTE]  
> 有关 Docker 目前提供的企业级特性的信息，请参阅 [Docker Business 订阅](/manuals/subscription/details.md#docker-business)。

### Docker Data Center 和 Docker Trusted Registry

Docker Data Center (DDC) 是一个涵盖 Docker Universal Control Plane (UCP) 和 Docker Trusted Registry (DTR) 的总称。这些组件为企业环境中的容器管理、安全和注册表服务提供了全栈解决方案。在 Docker 企业版被收购后，它们现在属于 Mirantis 的产品组合。仍遇到 DDC、UCP 或 DTR 引用的用户应参考 Mirantis 的文档以获取现代替代方案的指导。

### 开发环境 (Dev Environments)

开发环境是 Docker Desktop 中引入的一项特性，允许开发人员快速启动开发环境。它已在 Docker Desktop 4.42 及更高版本中被弃用并移除。类似的工作流可以通过 Docker Compose 或根据特定项目要求创建自定义配置来实现。

## 开源项目

最初由 Docker 维护的几个开源项目已被存档、停止或移交给其他维护者或组织。

### Registry (现为 CNCF Distribution)

Docker Registry 曾作为容器镜像注册表的开源实现。它于 2019 年捐赠给了云原生计算基金会 (CNCF)，并以 "Distribution" 的名称进行维护。它仍然是管理和分发容器镜像的基石。

[CNCF Distribution](https://github.com/distribution/distribution)

### Docker Compose v1 (已被 Compose v2 取代)

Docker Compose v1 (`docker-compose`) 是一款基于 Python 的用于定义多容器应用程序的工具，现已被 Compose v2 (`docker compose`) 取代。Compose v2 使用 Go 语言编写，并与 Docker CLI 集成。Compose v1 不再维护，用户应迁移到 Compose v2。

[Compose v2 文档](/manuals/compose/_index.md)

### InfraKit

InfraKit 曾是一款开源工具包，旨在管理声明式基础设施并自动化容器部署。它已被存档，建议用户探索如 Terraform 之类的工具进行基础设施预配和编排。

[InfraKit GitHub 仓库](https://github.com/docker/infrakit)

### Docker Notary (现为 CNCF Notary)

Docker Notary 曾是一个用于签署和验证容器内容真实性的系统。它于 2017 年捐赠给了 CNCF，并以 "Notary" 的名称继续开发。寻求安全内容验证的用户应参考 CNCF Notary 项目。

[CNCF Notary](https://github.com/notaryproject/notary)

### SwarmKit

SwarmKit 通过为容器部署提供编排能力来驱动 Docker Swarm 模式。虽然 Swarm 模式仍可运行，但其开发速度已放缓，取而代之的是基于 Kubernetes 的解决方案。在评估容器编排选项时，应考察 SwarmKit 是否能满足现代工作负载的需求。

[SwarmKit GitHub 仓库](https://github.com/docker/swarmkit)