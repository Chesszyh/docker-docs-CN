---
title: Docker Hub 发布说明
linkTitle: 发布说明
weight: 999
description: 了解 Docker Hub 的新功能、错误修复和重大变更
keywords: docker hub, whats new, release notes
toc_min: 1
toc_max: 2
tags: [Release notes]
---

在这里，您可以了解每个 Docker Hub 版本的最新变更、新功能、错误修复和已知问题。

## 2025-02-18

### 新功能

- 您可以使用[镜像管理](./repos/manage/hub-images/manage.md)删除镜像和镜像索引。

## 2024-12-12

### 新功能

- Docker Hub 中的 AI 目录现在可以直接通过 Docker Desktop 访问。

## 2024-03-23

### 新功能

 - 您现在可以使用[类别](./repos/manage/information.md#repository-categories)为 Docker Hub 仓库添加标签。

## 2023-12-11

- 高级镜像管理功能以及相应的 API 端点已停用。
  请参阅 [docker/roadmap#534](https://github.com/docker/roadmap/issues/534)。

  以下 API 端点已被移除：

  ```text
  /namespaces/{namespace}/repositories/{repository}/images
  /namespaces/{namespace}/repositories/{repository}/images/{digest}/tags
  /namespaces/{namespace}/repositories/{repository}/images-summary
  /namespaces/{namespace}/delete-images
  ```

## 2023-08-28

- 启用了 SSO 的组织可以使用 [SCIM 角色映射](scim.md#set-up-role-mapping)将成员分配到角色、组织和团队。

## 2023-07-26

### 新功能

- 组织可以将[编辑者角色](roles-and-permissions.md)分配给成员，以授予额外权限而无需完全管理员访问权限。

## 2023-05-09

### 新功能

- Docker Business 订阅用户现在可以在 Docker Hub 中[创建公司](new-company.md)来管理组织和设置。

## 2023-03-07

### 新功能

-  您现在可以通过 SSO 和 SCIM 配置的[组映射](group-mapping.md)自动同步用户更新到您的 Docker 组织和团队。

## 2022-12-12

### 新功能

- 新的域名审计功能让您可以审计您的域名，查找不属于您组织成员的用户。


## 2022-09-26

### 新功能

- 新的[自动构建功能](../docker-hub/repos/manage/builds/manage-builds.md#check-your-active-builds)让您可以每 30 秒查看正在进行的日志，而不是等到构建完成时才能查看。

## 2022-09-21

### 错误修复和增强

- 在 Docker Hub 中，您现在可以下载 [registry.json](../security/for-admins/enforce-sign-in/_index.md) 文件或复制命令来创建 registry.json 文件，以强制您的组织用户登录。

## 2022-09-19

### 错误修复和增强

- 您现在可以从您拥有的组织中[导出成员的 CSV 文件](../admin/organization//members.md#export-members)。

## 2022-07-22

### 错误修复和增强

- 您现在可以使用包含成员电子邮件地址的 CSV 文件邀请成员加入您的组织。CSV 文件可以是您专门为此目的创建的文件，也可以是从其他内部系统导出的文件。

## 2022-07-19

### 错误修复和增强

- SCIM 现在可用于使用 Entra ID（以前称为 Azure AD）身份提供商的 Docker Business 订阅组织。

## 2022-06-23

### 新功能

- 使用 [SCIM](scim.md)，您可以在 Okta 身份提供商（IdP）中管理用户。此外，您可以在属于 Docker Business 订阅的组织上启用 SCIM。

## 2022-05-24

### 新功能

- [注册表访问管理](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)现在可用于所有 Docker Business 订阅。启用后，您的用户可以访问 Docker Hub 中的特定注册表。

## 2022-05-03

### 新功能

- 组织所有者可以通过 Docker ID 或电子邮件地址[邀请新成员](members.md#invite-members)加入组织。

## 2021-11-15

### 新功能

- 您现在可以使用信用卡购买或升级到 Docker Business 订阅。要了解更多信息，请参阅[升级您的订阅](../subscription//change.md)。

## 2021-08-31

### 新功能

Docker [宣布](https://www.docker.com/blog/updating-product-subscriptions/)了产品订阅的更新和扩展，以提高开发人员和企业的生产力、协作性和安全性。Docker 订阅层级现在包括 Personal、Pro、Team 和 Business。

更新后的 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)包含对 **Docker Desktop** 条款的更改。

- 对于小型企业（员工少于 250 人且年收入低于 1000 万美元）、个人使用、教育和非商业开源项目，Docker Desktop **仍然免费**。
- 对于大型企业的专业使用，需要付费订阅（**Pro、Team 或 Business**），最低每月 5 美元。
- 这些条款的生效日期为 2021 年 8 月 31 日。对于需要付费订阅才能使用 Docker Desktop 的用户，有一个宽限期直到 2022 年 1 月 31 日。
- Docker Pro 和 Docker Team 订阅现在**包含 Docker Desktop 的商业使用**。
- 现有的 Docker Free 订阅已更名为 **Docker Personal**。
- Docker Engine 或任何其他上游**开源** Docker 或 Moby 项目**没有变化**。

    要了解这些变化如何影响您，请阅读[常见问题解答](https://www.docker.com/pricing/faq)。有关更多信息，请参阅 [Docker 订阅概述](../subscription/_index.md)。

## 2021-05-05

### 增强

在管理仓库内容时，您现在可以根据标签的时效性过滤结果，并更容易识别未标记的镜像。

有关 Docker Hub API 文档，请参阅 [Docker Hub API 参考](/reference/api/hub/latest.md#operation/GetNamespacesRepositoriesImages)。

## 2021-04-13

### 增强

**账单详情**页面现在除了显示您的个人账户外，还显示您拥有的任何组织。这使您可以清楚地识别所选命名空间的账单详情，并允许您在个人账户和组织账户之间切换以查看或更新详情。

## 2021-04-09

### 增强

您现在可以指定任何电子邮件地址来接收组织的账单相关电子邮件。该电子邮件地址不必与组织所有者账户关联。您必须是组织的所有者才能更新任何账单详情。

要更改接收账单相关电子邮件的电子邮件地址，请登录 Docker Hub 并导航到组织的 **Billing**（账单）选项卡。选择 **Payment Methods**（付款方式）> **Billing Information**（账单信息）。在 **Email**（电子邮件）字段中输入您想要使用的新电子邮件地址。点击 **Update**（更新）使更改生效。

有关如何更新账单信息的详细信息，请参阅[更新账单信息](../billing/_index.md)。

## 2021-03-22

### 新功能

**高级镜像管理仪表板**

Docker 推出了高级镜像管理仪表板，使您能够查看和管理仓库中的 Docker 镜像。

## 2021-01-25

### 新功能

Docker 推出了审计日志，这是一项新功能，允许团队所有者查看在组织和仓库级别发生的活动列表。此功能从发布日期开始跟踪活动，即**从 2021 年 1 月 25 日起**。

有关此功能的更多信息以及使用说明，请参阅[活动日志](../admin/organization/activity-logs.md)。

## 2020-11-10

### 新功能

**Repositories**（仓库）视图现在显示哪些镜像因为最近没有被拉取或推送而变得陈旧。有关更多信息，请参阅[仓库标签](repos/manage/access/_index.md#view-repository-tags)。

## 2020-10-07

### 新功能

Docker 推出了 Hub 漏洞扫描功能，使您能够使用 Snyk 自动扫描 Docker 镜像的漏洞。有关更多信息，请参阅 [Hub 漏洞扫描](vulnerability-scanning.md)。

## 2020-05-14

### 新功能

* Docker 宣布了新的按席位定价模式，以加速云原生开发的开发人员工作流程。以前基于私有仓库/并发自动构建的计划已被新的 **Pro** 和 **Team** 计划取代，这些计划包含无限的私有仓库。有关更多信息，请参阅 [Docker 订阅](../subscription/_index.md)。

* Docker 已对 Docker Hub 上的下载和拉取请求启用下载速率限制。这限制了用户在指定时间范围内可以下载的对象数量。有关更多信息，请参阅[使用量和限制](/manuals/docker-hub/usage/_index.md)。

## 2019-11-04

### 增强

* [仓库页面](repos/_index.md)及所有相关设置和选项卡已更新并从 `cloud.docker.com` 迁移到 `hub.docker.com`。您可以通过新 URL 访问该页面：[https://hub.docker.com/repositories](https://hub.docker.com/repositories)。

### 已知问题

* 某些官方镜像的扫描结果不显示。

## 2019-10-21

### 新功能

* **Beta：** Docker Hub 现在支持双因素认证（2FA）。在您的账户设置中的 **[Security](https://hub.docker.com/settings/security)**（安全）部分启用它。

    > 如果您同时丢失了 2FA 认证设备和恢复代码，您可能无法恢复您的账户。

### 增强

* 作为安全措施，当启用双因素认证时，Docker CLI 需要使用个人访问令牌而不是密码来登录。

### 已知问题

* 某些官方镜像的扫描结果不显示。


## 2019-10-02

### 增强

* 您现在可以直接从[组织页面](https://hub.docker.com/orgs)管理团队和成员。
每个组织页面现在分为以下选项卡：
  * **新增：** Members（成员）- 直接从此页面管理您的成员（删除、添加或打开他们的团队）
  * **新增：** Teams（团队）- 按团队或用户名搜索，并打开任何团队页面来管理团队
  * **新增：** Invitees（受邀者）（条件选项卡，仅在存在邀请时显示）- 从此选项卡重新发送或删除邀请
  * Repositories（仓库）
  * Settings（设置）
  * Billing（账单）

### 错误修复

* 修复了 Kinematic 无法连接和登录 Docker Hub 的问题。

### 已知问题

* 某些官方镜像的扫描结果不显示。


## 2019-09-19

### 新功能

* 您现在可以在 Docker Hub 中[创建个人访问令牌](/security/for-developers/access-tokens/)，并使用它们从 Docker CLI 进行认证。在您的账户设置中新的 **[Security](https://hub.docker.com/settings/security)**（安全）部分可以找到它们。

### 已知问题

* 某些官方镜像的扫描结果不显示。


## 2019-09-16

### 增强

* 个人账户的[账单页面](../subscription/change.md)已更新。您可以通过新 URL 访问该页面：[https://hub.docker.com/billing/plan](https://hub.docker.com/billing/plan)。

### 已知问题

* 某些官方镜像的扫描结果不显示。

## 2019-09-05

### 增强

* 镜像页面上的 `Tags`（标签）选项卡现在为每个标签提供额外信息：
  * 与标签关联的摘要列表
  * 构建时使用的架构
  * 操作系统
  * 最近更新特定标签镜像的用户
* Docker 官方镜像的安全扫描摘要已更新。

### 已知问题

* 某些官方镜像的扫描结果不显示。
