---
title: 入职您的组织
weight: 20
description: 开始入职您的 Docker Team 或 Business 组织。
keywords: 业务, 团队, 组织, 入门, 入职
toc_min: 1
toc_max: 3
aliases:
- /docker-hub/onboard/
- /docker-hub/onboard-team/
- /docker-hub/onboard-business/
---

{{< summary-bar feature_name="管理员组织" >}}

了解如何使用 Docker Hub 或 Docker 管理控制台入职您的组织。

入职您的组织使管理员能够了解用户活动并强制执行安全设置。此外，您的组织成员将获得更高的拉取限制和其他组织范围的福利。有关更多详细信息，请参阅 [Docker 订阅和功能](../../subscription/details.md)。

在本指南中，您将学习如何执行以下操作：

- 识别您的用户，以帮助您高效分配订阅席位
- 邀请成员和所有者加入您的组织
- 使用单点登录 (SSO) 和跨域身份管理系统 (SCIM) 保护您的组织的认证和授权
- 强制 Docker Desktop 登录以确保安全最佳实践

## 先决条件

在开始入职您的组织之前，请确保您：

- 拥有 Docker Team 或 Business 订阅。有关详细信息，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

  > [!NOTE]
  >
  > 购买自助服务订阅时，屏幕上的说明会引导您创建组织。如果您通过 Docker Sales 购买了订阅但尚未创建组织，请参阅[创建组织](/admin/organization/orgs)。

- 熟悉[管理概述](../_index.md)和[常见问题](/faq/admin/general-faqs/)中的 Docker 概念和术语。

## 通过引导式设置入职

管理控制台具有引导式设置，可帮助您轻松入职您的组织。引导式设置步骤包括基本的入职任务。如果您想在引导式设置之外入职，请参阅[推荐的入职步骤](/manuals/admin/organization/onboard.md#recommended-onboarding-steps)。

要使用引导式设置入职，请导航到 [管理控制台](https://app.docker.com) 并选择左侧导航栏中的**引导式设置**。

引导式设置将引导您完成以下入职步骤：

- **邀请您的团队**：邀请所有者和成员。
- **管理用户访问**：添加和验证域，使用 SSO 管理用户，并强制 Docker Desktop 登录。
- **Docker Desktop 安全**：配置镜像访问管理、注册表访问管理和设置管理。

## 推荐的入职步骤

### 第一步：识别您的 Docker 用户

识别您的用户有助于您高效分配席位，并确保他们获得 Docker 订阅福利。

1. 识别您组织中的 Docker 用户。
   - 如果您的组织使用设备管理软件，例如 MDM 或 Jamf，您可以使用设备管理软件来帮助识别 Docker 用户。有关详细信息，请参阅您的设备管理软件文档。您可以通过检查每个用户机器上以下位置是否安装了 Docker Desktop 来识别 Docker 用户：
      - Mac：`/Applications/Docker.app`
      - Windows：`C:\Program Files\Docker\Docker`
      - Linux：`/opt/docker-desktop`
   - 如果您的组织不使用设备管理软件或您的用户尚未安装 Docker Desktop，您可以调查您的用户。
2. 要求用户将其 Docker 帐户电子邮件更新为组织域中的电子邮件，或使用该电子邮件创建新帐户。
   - 要更新帐户的电子邮件地址，请指示您的用户登录 [Docker Hub](https://hub.docker.com)，并将电子邮件地址更新为组织域中的电子邮件地址。
   - 要创建新帐户，请指示您的用户使用组织域中的电子邮件地址[注册](https://hub.docker.com/signup)。
3. 要求您的 Docker 销售代表或[联系销售](https://www.docker.com/pricing/contact-sales/)以获取使用您组织域中电子邮件地址的 Docker 帐户列表。

### 第二步：邀请所有者

当您创建组织时，您是唯一的所有者。添加其他所有者是可选的。所有者可以帮助您入职和管理您的组织。

要添加所有者，请邀请用户并为其分配所有者角色。有关更多详细信息，请参阅[邀请成员](/admin/organization/members/)。

### 第三步：邀请成员

当您将用户添加到组织时，您可以了解他们的活动并强制执行安全设置。此外，您的组织成员将获得更高的拉取限制和其他组织范围的福利。

要添加成员，请邀请用户并为其分配成员角色。有关更多详细信息，请参阅[邀请成员](/admin/organization/members/)。

### 第四步：使用 SSO 和 SCIM 管理用户访问

配置 SSO 和 SCIM 是可选的，并且仅适用于 Docker Business 订阅者。要将 Docker Team 订阅升级到 Docker Business 订阅，请参阅[升级您的订阅](/subscription/upgrade/)。

使用您的身份提供商 (IdP) 通过 SSO 和 SCIM 自动管理成员并将其配置到 Docker。有关更多详细信息，请参阅：

   - [配置 SSO](/manuals/security/for-admins/single-sign-on/configure.md) 以在成员通过您的身份提供商登录 Docker 时进行认证和添加成员。
   - 可选。[强制 SSO](/manuals/security/for-admins/single-sign-on/connect.md) 以确保用户登录 Docker 时必须使用 SSO。

     > [!NOTE]
     >
     > 强制单点登录 (SSO) 和强制 Docker Desktop 登录是不同的功能。有关更多详细信息，请参阅
     > [强制登录与强制单点登录 (SSO)](/security/for-admins/enforce-sign-in/#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。

   - [配置 SCIM](/security/for-admins/provisioning/scim/) 以通过您的身份提供商自动配置、添加和取消配置成员到 Docker。

### 第五步：强制 Docker Desktop 登录

默认情况下，您的组织成员无需登录即可使用 Docker Desktop。当用户未登录为您的组织成员时，他们不会获得[组织订阅的福利](../../subscription/details.md)，并且他们可以规避 [Docker 的安全功能](/security/for-admins/hardened-desktop/)。

根据您公司的设置和偏好，有多种方法可以强制登录：
- [注册表键方法（仅限 Windows）](/security/for-admins/enforce-sign-in/methods/#registry-key-method-windows-only)
- [`.plist` 方法（仅限 Mac）](/security/for-admins/enforce-sign-in/methods/#plist-method-mac-only)
- [`registry.json` 方法（所有）](/security/for-admins/enforce-sign-in/methods/#registryjson-method-all)

### 第六步：管理 Docker Desktop 安全

Docker 提供以下安全功能来管理您组织的安全态势：

- [镜像访问管理](/manuals/security/for-admins/hardened-desktop/image-access-management.md)：控制您的开发人员可以从 Docker Hub 拉取哪些类型的镜像。
- [注册表访问管理](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)：定义您的开发人员可以访问哪些注册表。
- [设置管理](/manuals/security/for-admins/hardened-desktop/settings-management.md)：为您的用户设置和控制 Docker Desktop 设置。

## 接下来

- [管理 Docker 产品](./manage-products.md) 以配置访问和查看使用情况。
- 配置 [强化 Docker Desktop](/desktop/hardened-desktop/) 以提高您组织容器化开发的安全态势。
- [管理您的域](/manuals/security/for-admins/domain-management.md) 以确保您域中的所有 Docker 用户都是您组织的一部分。

您的 Docker 订阅提供了更多附加功能。要了解更多信息，请参阅 [Docker 订阅和功能](/subscription/details/)。