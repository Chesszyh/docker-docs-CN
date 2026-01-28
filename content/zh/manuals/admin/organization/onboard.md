---
title: 组织入门
weight: 20
description: 开始引导您的 Docker Team 或 Business 组织。
keywords: 业务, 团队, 组织, 入门, 引导
toc_min: 1
toc_max: 3
aliases:
- /docker-hub/onboard/
- /docker-hub/onboard-team/
- /docker-hub/onboard-business/
---

{{< summary-bar feature_name="管理组织" >}}

学习如何使用 Docker Hub 或 Docker 管理控制台（Admin Console）引导您的组织。

引导您的组织入门可以让管理员获得用户活动的可见性并强制执行安全设置。此外，您的组织成员还将获得更高的拉取限制和其他组织范围内的福利。有关更多详情，请参阅 [Docker 订阅和功能](../../subscription/details.md)。

在本指南中，您将学习如何执行以下操作：

- 识别您的用户，以帮助您高效分配订阅席位
- 邀请成员和所有者加入您的组织
- 使用单点登录 (SSO) 和跨域身份管理系统 (SCIM) 保护您组织的身份验证和授权
- 为 Docker Desktop 强制执行登录，以确保安全最佳实践

## 前提条件

在开始引导您的组织之前，请确保您：

- 拥有 Docker Team 或 Business 订阅。详情请参阅 [Docker 定价](https://www.docker.com/pricing/)。

  > [!NOTE]
  >
  > 购买自助服务订阅时，屏幕上的说明将引导您创建组织。如果您是通过 Docker 销售人员购买的订阅且尚未创建组织，请参阅 [创建组织](/admin/organization/orgs)。

- 熟悉 [管理概览](../_index.md) 和 [FAQ](/faq/admin/general-faqs/) 中的 Docker 概念和术语。

## 通过引导式设置入门

管理控制台提供引导式设置，帮助您轻松引导组织。引导式设置步骤由基本的入门任务组成。如果您想在引导式设置之外进行引导，请参阅 [推荐的入门步骤](/manuals/admin/organization/onboard.md#recommended-onboarding-steps)。

要使用引导式设置进行引导，请导航至 [管理控制台](https://app.docker.com) 并在左侧导航栏中选择 **Guided setup**（引导式设置）。

引导式设置将引导您完成以下入门步骤：

- **邀请您的团队**：邀请所有者和成员。
- **管理用户访问**：添加并验证域名，使用 SSO 管理用户，并强制执行 Docker Desktop 登录。
- **Docker Desktop 安全**：配置镜像访问管理、镜像库访问管理和设置管理。

## 推荐的入门步骤

### 第一步：识别您的 Docker 用户

识别您的用户有助于您高效分配席位，并确保他们获得 Docker 订阅福利。

1. 识别您组织中的 Docker 用户。
   - 如果您的组织使用设备管理软件（如 MDM 或 Jamf），您可以使用该软件来帮助识别 Docker 用户。详情请参阅您的设备管理软件文档。您可以通过检查每个用户的机器上是否在以下位置安装了 Docker Desktop 来识别 Docker 用户：
      - Mac: `/Applications/Docker.app`
      - Windows: `C:\Program Files\Docker\Docker`
      - Linux: `/opt/docker-desktop`
   - 如果您的组织不使用设备管理软件，或者您的用户尚未安装 Docker Desktop，您可以对用户进行调查。
2. 要求用户将其 Docker 账户电子邮件更新为组织域名的邮件，或使用该邮件创建一个新账户。
   - 要更新账户的电子邮件地址，请指示您的用户登录 [Docker Hub](https://hub.docker.com)，并将电子邮件地址更新为组织域名的邮件地址。
   - 要创建一个新账户，请指示您的用户前往 [注册页面](https://hub.docker.com/signup) 并使用组织域名的邮件地址进行注册。
3. 要求您的 Docker 销售代表或 [联系销售人员](https://www.docker.com/pricing/contact-sales/) 获取使用您组织域名电子邮件地址的 Docker 账户列表。

### 第二步：邀请所有者

创建组织时，您是唯一的所有者。您可以选择添加其他所有者。所有者可以帮助您引导并管理组织。

要添加所有者，请邀请一名用户并为其分配所有者（owner）角色。有关更多详情，请参阅 [邀请成员](/admin/organization/members/)。

### 第三步：邀请成员

当您向组织添加用户时，您可以获得其活动的可见性，并可以强制执行安全设置。此外，您的组织成员还将获得更高的拉取限制和其他组织范围内的福利。

要添加成员，请邀请一名用户并为其分配成员（member）角色。有关更多详情，请参阅 [邀请成员](/admin/organization/members/)。

### 第四步：使用 SSO 和 SCIM 管理用户访问

配置 SSO 和 SCIM 是可选的，且仅对 Docker Business 订阅者可用。要将 Docker Team 订阅升级为 Docker Business 订阅，请参阅 [升级您的订阅](/subscription/upgrade/)。

使用您的身份提供商 (IdP) 来管理成员，并通过 SSO 和 SCIM 自动将他们配置到 Docker。详情请参阅以下内容：

   - [配置 SSO](/manuals/security/for-admins/single-sign-on/configure.md) 以便在成员通过您的身份提供商登录 Docker 时对其进行身份验证并添加成员。
   - 可选：[强制执行 SSO](/manuals/security/for-admins/single-sign-on/connect.md) 以确保用户在登录 Docker 时必须使用 SSO。

     > [!NOTE]
     >
     > 强制执行单点登录 (SSO) 与强制执行 Docker Desktop 登录是不同的功能。有关更多详情，请参阅 [强制执行登录与强制执行单点登录 (SSO) 的区别](/security/for-admins/enforce-sign-in/#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。

   - [配置 SCIM](/security/for-admins/provisioning/scim/) 以便通过您的身份提供商在 Docker 中自动配置、添加和取消配置成员。

### 第五步：为 Docker Desktop 强制执行登录

默认情况下，您的组织成员可以在不登录的情况下使用 Docker Desktop。当用户未作为组织成员登录时，他们无法获得 [组织订阅带来的福利](../../subscription/details.md) 并且可以规避 [Docker 的安全功能](/security/for-admins/hardened-desktop/)。

有多种方法可以强制执行登录，具体取决于您公司的设置和偏好：
- [注册表项方法（仅限 Windows）](/security/for-admins/enforce-sign-in/methods/#registry-key-method-windows-only)
- [`.plist` 方法（仅限 Mac）](/security/for-admins/enforce-sign-in/methods/#plist-method-mac-only)
- [`registry.json` 方法（通用）](/security/for-admins/enforce-sign-in/methods/#registryjson-method-all)

### 第六步：管理 Docker Desktop 安全

Docker 提供以下安全功能来管理您组织的安全状况：

- [镜像访问管理](/manuals/security/for-admins/hardened-desktop/image-access-management.md)：控制您的开发人员可以从 Docker Hub 拉取哪些类型的镜像。
- [镜像库访问管理](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)：定义您的开发人员可以访问哪些镜像库。
- [设置管理](/manuals/security/for-admins/hardened-desktop/settings-management.md)：为您组织的用户设置和控制 Docker Desktop 设置。

## 下一步

- [管理 Docker 产品](./manage-products.md) 以配置访问权限并查看使用情况。
- 配置 [强化的 Docker Desktop](/desktop/hardened-desktop/) 以改善您组织在容器化开发方面的安全状况。
- [管理您的域名](/manuals/security/for-admins/domain-management.md) 以确保您域名下的所有 Docker 用户都属于您的组织。

您的 Docker 订阅还提供了许多其他功能。要了解更多信息，请参阅 [Docker 订阅和功能](/subscription/details/)。
