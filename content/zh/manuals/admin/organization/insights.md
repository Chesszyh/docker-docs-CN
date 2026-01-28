---
description: 获取关于组织用户及其 Docker 使用情况的洞察。
keywords: organization, insights
title: 洞察
---

{{< summary-bar feature_name="Insights" >}}

洞察（Insights）帮助管理员可视化和了解 Docker 在其组织内的使用情况。通过洞察，管理员可以确保其团队充分配备以发挥 Docker 的最大潜力，从而提高整个组织的生产力和效率。

主要优势包括：

- 统一的工作环境。在团队之间建立和维护标准化配置。
- 最佳实践。推广和执行使用指南以确保最佳性能。
- 提高可见性。监控和推动组织配置和策略的采用。
- 优化许可证使用。确保开发人员能够访问 Docker 订阅提供的高级功能。

## 前提条件

- [Docker Business 订阅](../../subscription/details.md#docker-business)
- 管理员必须为用户[强制登录](/security/for-admins/enforce-sign-in/)
- 由您的客户成功经理启用洞察功能

## 查看组织用户的洞察

要访问洞察，您必须联系您的客户成功经理以启用该功能。功能启用后，使用以下步骤访问洞察：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Insights**，然后选择数据的时间段。

> [!NOTE]
>
> 洞察数据不是实时的，每天更新一次。在洞察页面的右上角，查看 **Last updated** 日期以了解数据的最后更新时间。

您可以在以下图表中查看数据：

 - [Docker Desktop 用户](#docker-desktop-用户)
 - [构建](#构建)
 - [容器](#容器)
 - [Docker Desktop 使用情况](#docker-desktop-使用情况)
 - [Docker Hub 镜像](#docker-hub-镜像)
 - [扩展](#扩展)

### Docker Desktop 用户

跟踪您域中的活跃 Docker Desktop 用户，按许可证状态区分。此图表帮助您了解组织内的参与程度，提供关于有多少用户正在积极使用 Docker Desktop 的洞察。请注意，选择退出分析的用户不包括在活跃计数中。

该图表包含以下数据：

| 数据 | 描述 |
|:-----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Active user（活跃用户） | 积极使用 Docker Desktop 并且使用在您组织中拥有许可证的 Docker 帐户登录或使用与您组织关联的域名电子邮件地址登录 Docker 帐户的用户数量。<br><br>未使用与您组织关联的帐户登录的用户不会在数据中显示。要确保用户使用与您组织关联的帐户登录，您可以[强制登录](/security/for-admins/enforce-sign-in/)。 |
| Total organization members（组织成员总数） | 使用过 Docker Desktop 的用户数量，无论其洞察活动如何。 |
| Users opted out of analytics（选择退出分析的用户） | 您组织中选择退出发送分析的成员数量。<br><br>当用户选择退出发送分析时，您将无法在洞察中看到他们的任何数据。要确保数据包括所有用户，您可以使用[设置管理](/desktop/hardened-desktop/settings-management/)为所有用户设置 `analyticsEnabled`。 |
| Active users (graph)（活跃用户图表） | 总活跃用户的时间视图。 |


### 构建

使用此图表监控开发效率和您团队在构建上投入的时间。它提供了构建活动的清晰视图，帮助您识别模式、优化构建时间并提高整体开发生产力。

该图表包含以下数据：

| 数据                   | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|:-----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Average build per user（每用户平均构建数） | 每个活跃用户的平均构建数量。构建包括用户运行以下任一命令的任何时候：<ul><li>`docker build`</li><li>`docker buildx b`</li><li>`docker buildx bake`</li><li>`docker buildx build`</li><li>`docker buildx f`</li><li>`docker builder b`</li><li>`docker builder bake`</li><li>`docker builder build`</li><li>`docker builder f`</li><li>`docker compose build`</li><li>`docker compose up --build`</li><li>`docker image build`</li></ul> |
| Average build time（平均构建时间）     | 每次构建的平均构建时间。                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Build success rate（构建成功率）     | 成功构建占总构建数量的百分比。成功构建包括任何正常退出的构建。                                                                                                                                                                                                                          |
| Total builds (graph)（总构建数图表）   | 总构建数量，分为成功构建和失败构建。成功构建包括任何正常退出的构建。失败构建包括任何异常退出的构建。                                                                                                                                                                                   |

### 容器

使用此图表查看用户运行的容器总数和平均数量。它让您了解整个组织的容器使用情况，帮助您了解使用趋势并有效管理资源。

该图表包含以下数据：

| 数据                                   | 描述                                                                                                                                                                |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Total containers run（运行的容器总数）                   | 活跃用户运行的容器总数。运行的容器包括使用 Docker Desktop 图形用户界面、`docker run` 或 `docker compose` 运行的容器。 |
| Average number of containers run（运行的容器平均数量）       | 每个活跃用户运行的容器平均数量。                                                                                                                      |
| Containers run by active users (graph)（活跃用户运行的容器图表） | 活跃用户随时间运行的容器数量。                                                                                                                    |

### Docker Desktop 使用情况

使用此图表探索 Docker Desktop 使用模式，以优化您团队的工作流程并确保兼容性。它提供了关于 Docker Desktop 如何被使用的宝贵洞察，使您能够简化流程并提高效率。

该图表包含以下数据：

| 数据                              | 描述                                                                                                                                                                                                                                                                       |
|:----------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Most used version（最常用版本）                 | 您组织中用户最常使用的 Docker Desktop 版本。                                                                                                                                                                                                            |
| Most used OS（最常用操作系统）                      | 用户最常使用的操作系统。                                                                                                                                                                                                                          |
| Versions by active users (graph)（按活跃用户划分的版本图表）  | 使用每个 Docker Desktop 版本的活跃用户数量。<br><br>要了解更多关于每个版本和发布日期的信息，请参阅 [Docker Desktop 发行说明](/desktop/release-notes/)。                                                                                     |
| Interface by active users (graph)（按活跃用户划分的界面图表） | 按用户与 Docker Desktop 交互的界面类型分组的活跃用户数量。<br><br>CLI 用户是任何运行过 `docker` 命令的活跃用户。GUI 用户是任何与 Docker Desktop 图形用户界面交互过的活跃用户。 |

### Docker Hub 镜像

使用此图表分析镜像分发活动，并查看您域中最常使用的 Docker Hub 镜像。此信息帮助您管理镜像使用，确保最关键的资源随时可用并被有效使用。

> [!NOTE]
>
> 镜像数据仅适用于 Docker Hub。不包括第三方注册表和镜像的数据。

该图表包含以下数据：

| 数据                 | 描述                                                                                                     |
|:---------------------|:----------------------------------------------------------------------------------------------------------------|
| Total pulled images（拉取的镜像总数）  | 用户从 Docker Hub 拉取的镜像总数。                                                     |
| Total pushed images（推送的镜像总数）  | 用户推送到 Docker Hub 的镜像总数。                                                       |
| Top 10 pulled images（前 10 个拉取的镜像） | 用户从 Docker Hub 拉取的前 10 个镜像列表以及每个镜像被拉取的次数。 |

### 扩展

使用此图表监控扩展安装活动。它提供了您团队正在使用的 Docker Desktop 扩展的可见性，让您跟踪采用情况并识别提高生产力的流行工具。

该图表包含以下数据：

| 数据                                           | 描述                                                                                                                                      |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| Percentage of org with extensions installed（组织中安装扩展的百分比）    | 您组织中至少安装了一个 Docker Desktop 扩展的用户百分比。                                               |
| Top 5 extensions installed in the organization（组织中安装的前 5 个扩展） | 您组织中用户安装的前 5 个 Docker Desktop 扩展列表以及安装每个扩展的用户数量。 |

## 导出 Docker Desktop 用户数据

您可以将 Docker Desktop 用户数据导出为 CSV 文件：

1. 打开 [Docker Home](https://app.docker.com) 并在 **Choose profile** 页面上选择您的组织。
1. 在左侧导航菜单中选择 **Admin Console**。
1. 选择 **Desktop insights**。
1. 选择洞察数据的时间范围：**1 Week**、**1 Month** 或 **3 Months**。
1. 选择 **Export** 并从下拉菜单中选择 **Docker Desktop users**。

您的导出将自动下载。打开文件以查看导出数据。

### 了解导出数据

Docker Desktop 用户导出文件包含以下数据点：

- Name：用户姓名
- Username：用户的 Docker ID
- Email：与用户 Docker ID 关联的电子邮件地址
- Type：用户类型
- Role：用户[角色](/manuals/security/for-admins/roles-and-permissions.md)
- Teams：用户所属的组织内的团队
- Date Joined：用户加入您组织的日期
- Last Logged-In Date：用户最后一次使用网络浏览器登录 Docker 的日期（包括 Docker Hub 和 Docker Home）
- Docker Desktop Version：用户安装的 Docker Desktop 版本
- Last Seen Date：用户最后一次使用 Docker Desktop 应用程序的日期
- Opted Out Analytics：用户是否选择退出 Docker Desktop 中的[发送使用统计信息](/manuals/security/for-admins/hardened-desktop/settings-management/settings-reference.md#send-usage-statistics)设置

## 洞察故障排除

如果您在洞察中遇到数据问题，请考虑以下解决方案来解决常见问题。

- 将用户更新到最新版本的 Docker Desktop。

   使用 Docker Desktop 4.16 或更低版本的用户不会显示数据。此外，较旧版本可能无法提供所有数据。确保所有用户都安装了最新版本的 Docker Desktop。

- 为所有用户启用 Docker Desktop 中的 **Send usage statistics**。

   如果用户选择退出发送 Docker Desktop 的使用统计信息，则他们的使用数据将不会成为洞察的一部分。要为所有用户大规模管理该设置，您可以使用[设置管理](/desktop/hardened-desktop/settings-management/)并启用 `analyticsEnabled` 设置。

- 确保用户使用 Docker Desktop 而不是独立版本的 Docker Engine。

   只有 Docker Desktop 才能为洞察提供数据。如果用户在 Docker Desktop 之外安装 Docker Engine，Docker Engine 将不会为该用户提供数据。

- 确保用户登录到与您组织关联的帐户。

   未登录到与您组织关联的帐户的用户不会在数据中显示。要确保用户使用与您组织关联的帐户登录，您可以[强制登录](/security/for-admins/enforce-sign-in/)。
