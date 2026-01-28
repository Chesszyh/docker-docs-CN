---
title: 组织入门
weight: 20
description: 开始为您的 Docker Team 或 Business 组织入门。
keywords: business, team, organizations, get started, onboarding
toc_min: 1
toc_max: 3
aliases:
- /docker-hub/onboard/
- /docker-hub/onboard-team/
- /docker-hub/onboard-business/
---

{{< summary-bar feature_name="Admin orgs" >}}

了解如何使用 Docker Hub 或 Docker Admin Console 为您的组织入门。

组织入门让管理员能够了解用户活动并执行安全设置。此外，组织成员可获得增加的拉取限制和其他组织范围的优势。有关更多详细信息，请参阅 [Docker 订阅和功能](../../subscription/details.md)。

在本指南中，您将学习如何：

- 识别您的用户以帮助您高效分配订阅席位
- 邀请成员和所有者加入您的组织
- 使用单点登录（SSO）和跨域身份管理系统（SCIM）保护组织的身份验证和授权
- 强制 Docker Desktop 登录以确保安全最佳实践

## 前提条件

在开始组织入门之前，请确保您：

- 拥有 Docker Team 或 Business 订阅。有关详细信息，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

  > [!NOTE]
  >
  > 购买自助服务订阅时，屏幕上的说明会指导您创建组织。如果您通过 Docker 销售购买了订阅但尚未创建组织，请参阅[创建组织](/admin/organization/orgs)。

- 在[管理概述](../_index.md)和[常见问题](/faq/admin/general-faqs/)中熟悉 Docker 概念和术语。

## 使用引导式设置入门

Admin Console 提供引导式设置来帮助您轻松完成组织入门。引导式设置步骤包含基本的入门任务。如果您想在引导式设置之外入门，请参阅[推荐的入门步骤](/manuals/admin/organization/onboard.md#推荐的入门步骤)。

要使用引导式设置入门，请导航到 [Admin Console](https://app.docker.com) 并在左侧导航中选择 **Guided setup**。

引导式设置将引导您完成以下入门步骤：

- **Invite your team**：邀请所有者和成员。
- **Manage user access**：添加和验证域名，使用 SSO 管理用户，并强制 Docker Desktop 登录。
- **Docker Desktop security**：配置镜像访问管理、注册表访问管理和设置管理。

## 推荐的入门步骤

### 第一步：识别您的 Docker 用户

识别您的用户有助于您高效分配席位并确保他们获得 Docker 订阅的优势。

1. 识别您组织中的 Docker 用户。
   - 如果您的组织使用设备管理软件（如 MDM 或 Jamf），您可以使用设备管理软件帮助识别 Docker 用户。有关详细信息，请参阅您的设备管理软件文档。您可以通过检查每个用户机器上以下位置是否安装了 Docker Desktop 来识别 Docker 用户：
      - Mac：`/Applications/Docker.app`
      - Windows：`C:\Program Files\Docker\Docker`
      - Linux：`/opt/docker-desktop`
   - 如果您的组织不使用设备管理软件或您的用户尚未安装 Docker Desktop，您可以调查您的用户。
2. 要求用户将其 Docker 帐户电子邮件更新为您组织域中的电子邮件，或使用该电子邮件创建新帐户。
   - 要更新帐户的电子邮件地址，请指导您的用户登录 [Docker Hub](https://hub.docker.com)，并将电子邮件地址更新为您组织域中的电子邮件地址。
   - 要创建新帐户，请指导您的用户使用其组织域中的电子邮件地址[注册](https://hub.docker.com/signup)。
3. 询问您的 Docker 销售代表或[联系销售](https://www.docker.com/pricing/contact-sales/)以获取使用您组织域中电子邮件地址的 Docker 帐户列表。

### 第二步：邀请所有者

创建组织时，您是唯一的所有者。添加其他所有者是可选的。所有者可以帮助您入门和管理您的组织。

要添加所有者，请邀请用户并为其分配所有者角色。有关更多详细信息，请参阅[邀请成员](/admin/organization/members/)。

### 第三步：邀请成员

当您将用户添加到组织时，您可以了解他们的活动并可以执行安全设置。此外，组织成员可获得增加的拉取限制和其他组织范围的优势。

要添加成员，请邀请用户并为其分配成员角色。有关更多详细信息，请参阅[邀请成员](/admin/organization/members/)。

### 第四步：使用 SSO 和 SCIM 管理用户访问

配置 SSO 和 SCIM 是可选的，仅适用于 Docker Business 订阅者。要将 Docker Team 订阅升级到 Docker Business 订阅，请参阅[升级您的订阅](/subscription/upgrade/)。

使用您的身份提供商（IdP）管理成员并通过 SSO 和 SCIM 自动配置到 Docker。有关更多详细信息，请参阅以下内容：

   - [配置 SSO](/manuals/security/for-admins/single-sign-on/configure.md) 以在用户通过您的身份提供商登录 Docker 时进行身份验证并添加成员。
   - 可选。[强制执行 SSO](/manuals/security/for-admins/single-sign-on/connect.md) 以确保用户登录 Docker 时必须使用 SSO。

     > [!NOTE]
     >
     > 强制执行单点登录（SSO）和强制 Docker Desktop 登录是不同的功能。有关更多详细信息，请参阅[强制登录与强制执行单点登录（SSO）](/security/for-admins/enforce-sign-in/#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。

   - [配置 SCIM](/security/for-admins/provisioning/scim/) 以通过您的身份提供商自动配置、添加和取消配置 Docker 成员。

### 第五步：强制 Docker Desktop 登录

默认情况下，组织成员可以在不登录的情况下使用 Docker Desktop。当用户不以组织成员身份登录时，他们不会获得[组织订阅的优势](../../subscription/details.md)，并且可以绕过 [Docker 的安全功能](/security/for-admins/hardened-desktop/)。

根据您公司的设置和偏好，有多种方式可以强制登录：
- [注册表密钥方法（仅限 Windows）](/security/for-admins/enforce-sign-in/methods/#registry-key-method-windows-only)
- [`.plist` 方法（仅限 Mac）](/security/for-admins/enforce-sign-in/methods/#plist-method-mac-only)
- [`registry.json` 方法（全部）](/security/for-admins/enforce-sign-in/methods/#registryjson-method-all)

### 第六步：管理 Docker Desktop 安全

Docker 提供以下安全功能来管理您组织的安全态势：

- [镜像访问管理](/manuals/security/for-admins/hardened-desktop/image-access-management.md)：控制开发人员可以从 Docker Hub 拉取哪些类型的镜像。
- [注册表访问管理](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)：定义开发人员可以访问哪些注册表。
- [设置管理](/manuals/security/for-admins/hardened-desktop/settings-management.md)：为用户设置和控制 Docker Desktop 设置。

## 后续步骤

- [管理 Docker 产品](./manage-products.md)以配置访问权限和查看使用情况。
- 配置[强化的 Docker Desktop](/desktop/hardened-desktop/)以改善组织容器化开发的安全态势。
- [管理您的域名](/manuals/security/for-admins/domain-management.md)以确保您域中的所有 Docker 用户都是组织的一部分。

您的 Docker 订阅提供了更多附加功能。要了解更多信息，请参阅 [Docker 订阅和功能](/subscription/details/)。
