---
title: Docker 订阅和功能
linkTitle: 订阅和功能
description: 了解 Docker 订阅层级及其功能
keywords: subscription, personal, pro, team, business, features, docker subscription
aliases:
- /subscription/core-subscription/details/
weight: 10
---

Docker 订阅通过提供团队快速交付安全、高质量应用所需的工具来增强开发团队的能力。这些计划包括访问 Docker 的产品套件：

- [Docker Desktop](../desktop/_index.md)：业界领先的容器优先开发解决方案，包括 Docker Engine、Docker CLI、Docker Compose、Docker Build/BuildKit 和 Kubernetes。
- [Docker Hub](../docker-hub/_index.md)：全球最大的基于云的容器镜像仓库。
- [Docker Build Cloud](../build-cloud/_index.md)：强大的基于云的构建器，可将构建时间加速高达 39 倍。
- [Docker Scout](../scout/_index.md)：软件供应链安全工具，让您快速评估镜像健康状况并加速安全改进。
- [Testcontainers Cloud](https://testcontainers.com/cloud/docs)：基于容器的测试自动化，提供更快的测试、统一的开发者体验等。

以下部分描述了 Docker 订阅或旧版 Docker 订阅（Legacy Docker subscription）中包含的一些关键功能。

> [!NOTE]
>
> 旧版 Docker 计划适用于最后一次购买或续订订阅在 2024 年 12 月 10 日之前的 Docker 订阅者。这些订阅者将保持其当前订阅和定价，直到其下一个续订日期在 2024 年 12 月 10 日或之后。要查看购买或续订历史记录，请查看您的[账单历史记录](../billing/history.md)。有关旧版 Docker 订阅的更多详情，请参阅[宣布升级 Docker 计划](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

## Docker Personal

**Docker Personal** 非常适合开源社区、个人开发者、教育和小型企业。它包括免费使用基本的 Docker 工具，以及强大工具的试用版，这些工具将提升您的开发循环。

Docker Personal 包括：

- Docker Scout 中包含 1 个具有持续漏洞分析的仓库
- 无限的公共 Docker Hub 仓库
- 认证用户每 6 小时 200 次 Docker Hub 镜像拉取限制
- 7 天 Docker Build Cloud 试用
- 7 天 Testcontainers Cloud 试用

希望在试用期后继续使用 Docker Build Cloud 或 Docker Testcontainers Cloud 的 Docker Personal 用户可以随时升级到 Docker Pro 订阅。

所有未认证用户，包括未认证的 Docker Personal 用户，每个 IPv4 地址或 IPv6 /64 子网每 6 小时可获得 100 次拉取。

有关每个层级可用功能的列表，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

## Docker Pro

**Docker Pro** 使个人开发者能够更好地控制其开发环境，并提供集成且可靠的开发者体验。它减少了开发者在繁琐和重复任务上花费的时间，使开发者能够花更多时间为客户创造价值。Docker Pro 订阅包括访问所有工具，包括 Docker Desktop、Docker Hub、Docker Scout、Docker Build Cloud 和 Testcontainers Cloud。

Docker Pro 包括：

- 每月 200 分钟 Docker Build Cloud 构建时间。Docker Build Cloud 分钟数不会逐月累积。
- Docker Scout 中包含 2 个具有持续漏洞分析的仓库。
- 每月 100 分钟 Testcontainers Cloud 运行时间，可在 Docker Desktop 或 CI 中使用。Testcontainers Cloud 运行时分钟数不会逐月累积。
- 无 Docker Hub 镜像拉取速率限制。

有关每个层级可用功能的列表，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

## Docker Team

**Docker Team** 为组织提供协作、生产力和安全功能。它使开发者团队能够释放协作和共享的全部力量，并结合基本的安全功能和团队管理功能。Docker Team 订阅包括 Docker 组件商业使用的许可，包括 Docker Desktop、Docker Hub、Docker Scout、Docker Build Cloud 和 Testcontainers Cloud。

Docker Team 包括：

- 每月 500 分钟 Docker Build Cloud 构建时间。Docker Build Cloud 分钟数不会逐月累积。
- Docker Scout 中无限仓库的持续漏洞分析。
- 每月 500 分钟 Testcontainers Cloud 运行时间，可在 Docker Desktop 或 CI 中使用。Testcontainers Cloud 运行时分钟数不会逐月累积。
- 无 Docker Hub 镜像拉取速率限制。

还有高级协作和管理工具，包括具有[基于角色的访问控制 (RBAC)](/security/for-admins/roles-and-permissions/) 的组织和团队管理、[活动日志](/admin/organization/activity-logs/)等。

有关每个层级可用功能的列表，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

## Docker Business

**Docker Business** 为大规模使用 Docker 的企业提供集中管理和高级安全功能。它使领导者能够管理其 Docker 开发环境并加速其安全软件供应链计划。Docker Business 订阅包括 Docker 组件商业使用的许可，包括 Docker Desktop、Docker Hub、Docker Scout、Docker Build Cloud 和 Testcontainers Cloud。

Docker Business 包括：

- 每月 1500 分钟 Docker Build Cloud 构建时间。Docker Build Cloud 分钟数不会逐月累积。
- Docker Scout 中无限仓库的持续漏洞分析。
- 每月 1500 分钟 Testcontainers Cloud 运行时间，可在 Docker Desktop 或 CI 中使用。Testcontainers Cloud 运行时分钟数不会逐月累积。
- 无 Docker Hub 镜像拉取速率限制。

此外，您还可以获得企业级功能，例如：
- [加固的 Docker Desktop](../security/for-admins/hardened-desktop/_index.md)
- [镜像访问管理](../security/for-admins/hardened-desktop/image-access-management.md)，让管理员控制开发者可以访问的内容
- [镜像仓库访问管理](../security/for-admins/hardened-desktop/registry-access-management.md)，让管理员控制开发者可以访问的镜像仓库
- [公司层](/admin/company/)用于管理多个组织和设置
- [单点登录](/security/for-admins/single-sign-on/)
- [跨域身份管理系统](/security/for-admins/provisioning/scim/)

有关每个层级可用功能的列表，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

## 自助服务

自助服务 Docker 订阅是指所有事项都由您自己设置。您可以：

- 管理您自己的发票
- 添加或移除席位
- 更新账单和付款信息
- 随时降级您的订阅

## 销售协助

销售协助订阅是指由专门的 Docker 客户经理设置和管理一切的 Docker Business 或 Team 订阅。

{{< /tab >}}
{{< tab name="Legacy Docker plans" >}}

> [!IMPORTANT]
>
> 自 2024 年 12 月 10 日起，Docker Core、Docker Build Cloud 和 Docker Scout 订阅不再可用，已被提供所有工具访问权限的 Docker 订阅计划所取代。如果您在 2024 年 12 月 10 日之前订阅或续订了订阅，您的旧版 Docker 计划在续订之前仍适用于您的账户。有关更多详情，请参阅[宣布升级 Docker 计划](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

以下描述了旧版 Docker 计划中包含的一些关键功能：

![Docker Core 订阅图示](./images/subscription-diagram.webp)

## 旧版 Docker 计划

### 旧版 Docker Pro

**旧版 Docker Pro** 使个人开发者能够更好地控制其开发环境，并提供集成且可靠的开发者体验。它减少了开发者在繁琐和重复任务上花费的时间，使开发者能够花更多时间为客户创造价值。

旧版 Docker Pro 包括：
- 无限的公共仓库
- 无限的[作用域访问令牌](/security/for-developers/access-tokens/)
- 公共仓库的无限[协作者](/docker-hub/repos/manage/access/#collaborators)，每月免费。
- 访问[旧版 Docker Scout Free](#legacy-docker-scout-free) 以开始使用软件供应链安全。
- 无限的私有仓库
- 每天 5000 次镜像[拉取](/manuals/docker-hub/usage/pulls.md)
- [自动构建](/docker-hub/builds/)，支持 5 个并发构建
- 300 次[漏洞扫描](/docker-hub/vulnerability-scanning/)

有关每个旧版层级可用功能的列表，请参阅[旧版 Docker 定价](https://www.docker.com/legacy-pricing/)。

#### 升级您的旧版 Docker Pro 订阅

当您将旧版 Docker Pro 订阅升级为 Docker Pro 订阅时，您的订阅包括以下变更：

- Docker Build Cloud 构建分钟数从 100/月增加到 200/月，且无月费。Docker Build Cloud 分钟数不会逐月累积。
- Docker Scout 中包含 2 个具有持续漏洞分析的仓库。
- 现在包含 100 分钟 Testcontainers Cloud 运行时间，可在 Docker Desktop 或 CI 中使用。Testcontainers Cloud 运行时分钟数不会逐月累积。
- 移除 Docker Hub 镜像拉取速率限制。

有关每个层级可用功能的列表，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

### 旧版 Docker Team

**旧版 Docker Team** 为组织提供协作、生产力和安全功能。它使开发者团队能够释放协作和共享的全部力量，并结合基本的安全功能和团队管理功能。Docker Team 订阅包括 Docker 组件商业使用的许可，包括 Docker Desktop 和 Docker Hub。

旧版 Docker Team 包括：
- 旧版 Docker Pro 中包含的所有内容
- 无限的团队
- [自动构建](/docker-hub/builds/)，支持 15 个并发构建
- 无限[漏洞扫描](/docker-hub/vulnerability-scanning/)
- 每个团队成员每天 5000 次镜像[拉取](/manuals/docker-hub/usage/pulls.md)

还有高级协作和管理工具，包括具有[基于角色的访问控制 (RBAC)](/security/for-admins/roles-and-permissions/) 的组织和团队管理、[活动日志](/admin/organization/activity-logs/)等。

有关每个旧版层级可用功能的列表，请参阅[旧版 Docker 定价](https://www.docker.com/legacy-pricing/)。

#### 升级您的旧版 Docker Team 订阅

当您将旧版 Docker Team 订阅升级为 Docker Team 订阅时，您的订阅包括以下变更：

- 不再需要支付额外的每席位费用，Docker Build Cloud 现在可供 Docker 订阅中的所有用户使用。
- Docker Build Cloud 构建分钟数从 400/月增加到 500/月。Docker Build Cloud 分钟数不会逐月累积。
- Docker Scout 现在包含无限仓库的持续漏洞分析，从 3 个增加。
- 现在包含 500 分钟 Testcontainers Cloud 运行时间，可在 Docker Desktop 或 CI 中使用。Testcontainers Cloud 运行时分钟数不会逐月累积。
- 移除 Docker Hub 镜像拉取速率限制。
- 最小用户数为 1（从 5 降低）。

有关每个层级可用功能的列表，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

### 旧版 Docker Business

**旧版 Docker Business** 为大规模使用 Docker 的企业提供集中管理和高级安全功能。它使领导者能够管理其 Docker 开发环境并加速其安全软件供应链计划。Docker Business 订阅包括 Docker 组件商业使用的许可，包括 Docker Desktop 和 Docker Hub。

旧版 Docker Business 包括：
- 旧版 Docker Team 中包含的所有内容
- [加固的 Docker Desktop](../security/for-admins/hardened-desktop/_index.md)
- [镜像访问管理](../security/for-admins/hardened-desktop/image-access-management.md)，让管理员控制开发者可以访问的内容
- [镜像仓库访问管理](../security/for-admins/hardened-desktop/registry-access-management.md)，让管理员控制开发者可以访问的镜像仓库
- [公司层](/admin/company/)用于管理多个组织和设置
- [单点登录](/security/for-admins/single-sign-on/)
- [跨域身份管理系统](/security/for-admins/provisioning/scim/)等。

有关每个层级可用功能的列表，请参阅[旧版 Docker 定价](https://www.docker.com/legacy-pricing/)。

#### 升级您的旧版 Docker Business 订阅

当您将旧版 Docker Business 订阅升级为 Docker Business 订阅时，您的订阅包括以下变更：

- 不再需要支付额外的每席位费用，Docker Build Cloud 现在可供 Docker 订阅中的所有用户使用。
- Docker Build Cloud 包含分钟数从 800/月增加到 1500/月。Docker Build Cloud 分钟数不会逐月累积。
- Docker Scout 现在包含无限仓库的持续漏洞分析，从 3 个增加。
- 现在包含 1500 分钟 Testcontainers Cloud 运行时间，可在 Docker Desktop 或 CI 中使用。Testcontainers Cloud 运行时分钟数不会逐月累积。
- 移除 Docker Hub 镜像拉取速率限制。

有关每个层级可用功能的列表，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

#### 自助服务

自助服务 Docker Business 订阅是指所有事项都由您自己设置。您可以：

- 管理您自己的发票
- 添加或移除席位
- 更新账单和付款信息
- 随时降级您的订阅

#### 销售协助

销售协助 Docker Business 订阅是指由专门的 Docker 客户经理设置和管理一切。

## 旧版 Docker Scout 订阅

本节概述了 Docker Scout 的旧版订阅。

> [!IMPORTANT]
>
> 自 2024 年 12 月 10 日起，Docker Scout 订阅不再可用，已被提供所有工具访问权限的 Docker 订阅所取代。如果您在 2024 年 12 月 10 日之前订阅或续订了订阅，您的旧版 Docker 订阅在续订之前仍适用于您的账户。有关更多详情，请参阅[宣布升级 Docker 计划](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

### 旧版 Docker Scout Free

旧版 Docker Scout Free 可供组织使用。如果您有旧版 Docker 订阅，您将自动获得旧版 Docker Scout Free 的访问权限。

旧版 Docker Scout Free 包括：

- 无限的本地镜像分析
- 最多 3 个启用 Docker Scout 的仓库
- SDLC 集成，包括策略评估和工作负载集成
- 本地和云容器镜像仓库集成
- 安全态势报告

### 旧版 Docker Scout Team

旧版 Docker Scout Team 包括：

- 旧版 Docker Scout Free 中可用的所有功能
- 除了 3 个启用 Docker Scout 的仓库外，购买订阅时可添加最多 100 个仓库

### 旧版 Docker Scout Business

旧版 Docker Scout Business 包括：

- 旧版 Docker Scout Team 中可用的所有功能
- 无限启用 Docker Scout 的仓库

### 升级您的旧版 Docker Scout 订阅

当您将旧版 Docker Scout 订阅升级为 Docker 订阅时，您的订阅包括以下变更：

- Docker Business：无限仓库的持续漏洞分析，从 3 个增加。
- Docker Team：无限仓库的持续漏洞分析，从 3 个增加。
- Docker Pro：包含 2 个具有持续漏洞分析的仓库。
- Docker Personal：包含 1 个具有持续漏洞分析的仓库。

有关每个层级可用功能的列表，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

## 旧版 Docker Build Cloud 订阅

本节描述了不同旧版 Docker Build Cloud 订阅层级可用的功能。

> [!IMPORTANT]
>
> 自 2024 年 12 月 10 日起，Docker Build Cloud 仅在新的 Docker Pro、Team 和 Business 计划中可用。当您的订阅在 2024 年 12 月 10 日或之后续订时，您每月包含的 Build Cloud 分钟数将增加。有关更多详情，请参阅[宣布升级 Docker 计划](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

### 旧版 Docker Build Cloud Starter

如果您有旧版 Docker 订阅，则包含基础级别的 Build Cloud 分钟数和缓存。可用的功能因您的旧版 Docker 订阅层级而异。

#### 旧版 Docker Pro

- 每月 100 分钟构建时间
- 可供一个用户使用
- 4 个并行构建

#### 旧版 Docker Team

- 每月 400 分钟构建时间，在组织内共享
- 可选择加入最多 100 名成员
- 可购买额外席位以添加更多分钟数

#### 旧版 Docker Business

- Docker Team 列出的所有功能
- 每月 800 分钟构建时间，在组织内共享

### 旧版 Docker Build Cloud Team

旧版 Docker Build Cloud Team 提供以下功能：

- 每席位额外 200 分钟构建时间
- 可选择购买预留分钟数
- 增加的共享缓存

旧版 Docker Build Cloud Team 订阅与 Docker [组织](/admin/organization/)绑定。要使用旧版 Docker Build Cloud Team 订阅的构建分钟数或共享缓存，用户必须是与订阅关联的组织的成员。请参阅管理席位和邀请。

### 旧版 Docker Build Cloud Enterprise

有关企业订阅的更多详情，请[联系销售](https://www.docker.com/products/build-cloud/#contact_sales)。

### 升级您的旧版 Docker Build Cloud 订阅

您不再需要订阅单独的 Docker Build Cloud 订阅来访问 Docker Build Cloud 或扩展您的分钟数。当您将旧版 Docker 订阅升级为 Docker 订阅时，您的订阅包括以下变更：

- Docker Business：包含分钟数从 800/月增加到 1500/月，可选择扩展更多分钟数。
- Docker Team：包含分钟数从 400/月增加到 500/月，可选择扩展更多分钟数。
- Docker Pro：包含分钟数从 100/月增加到 200/月，可选择扩展更多分钟数。
- Docker Personal：您将获得 7 天试用。

{{< /tab >}}
{{< /tabs >}}

## 订阅支持

所有 Docker Pro、Team 和 Business 订阅者都可获得其订阅的电子邮件支持。
