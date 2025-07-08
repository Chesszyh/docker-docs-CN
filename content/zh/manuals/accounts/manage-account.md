---
title: 管理帐户
weight: 20
description: 了解如何管理您的 Docker 帐户设置。
keywords: 帐户, docker ID, 帐户设置, 帐户管理, docker 主页
---

您可以使用 Docker Home 集中管理您的 Docker 帐户设置。在这里，您还可以对您的帐户执行管理操作并管理您的帐户安全。

> [!TIP]
>
> 如果您的帐户与强制单点登录 (SSO) 的组织关联，您可能没有权限更新您的帐户设置。
> 您必须联系您的管理员更新您的设置。

## 更新常规设置

1. 登录您的 [Docker 帐户](https://app.docker.com/login)。
2. 选择右上角的头像，然后选择**帐户设置**。

在“帐户设置”页面中，您可以执行以下任何操作。

### 更新帐户信息

帐户信息在您的 Docker Hub 帐户资料中可见。您可以更新以下帐户信息：

- 全名
- 公司
- 位置
- 网站
- Gravatar 电子邮件：要为您的 Docker 帐户添加头像，请创建 [Gravatar 帐户](https://gravatar.com/) 并创建您的头像。接下来，将您的 Gravatar 电子邮件添加到您的 Docker 帐户设置中。您的头像可能需要一些时间才能在 Docker 中更新。

在此处进行更改，然后选择**保存**以保存您的设置。

### 更新电子邮件地址

要更新您的电子邮件地址，请选择**电子邮件**：

1. 输入您的新电子邮件地址。
2. 输入您的密码以确认更改。
3. 选择**发送验证电子邮件**以向您的新电子邮件地址发送验证电子邮件。

验证您的电子邮件地址后，您的帐户信息将更新。

### 更改密码

您可以通过电子邮件启动密码重置来更改密码。

要更改密码，请选择**密码**，然后选择**重置密码**。
按照密码重置电子邮件中的说明进行操作。

## 管理安全设置

要更新您的双因素认证 (2FA) 设置，请选择 **2FA**。
有关您帐户的双因素认证 (2FA) 的信息，请参阅
[启用双因素认证](../security/for-developers/2fa/_index.md) 以开始使用。

要管理个人访问令牌，请选择**个人访问令牌**。
有关个人访问令牌的信息，请参阅
[创建和管理访问令牌](../security/for-developers/access-tokens.md)。

## 管理已连接的帐户

您可以使用“帐户设置”页面取消链接与您的 Docker 帐户关联的 Google 或 GitHub 帐户：

1. 选择**已连接的帐户**。
2. 在您已连接的帐户上选择**断开连接**。
3. 要完全取消链接您的 Docker 帐户，您还必须从 Google 或 GitHub 取消链接 Docker。有关更多信息，请参阅 Google 或 GitHub 的文档：
    - [管理您的 Google 帐户与第三方之间的连接](https://support.google.com/accounts/answer/13533235?hl=zh-Hans)
    - [审查和撤销 GitHub Apps 的授权](https://docs.github.com/zh-cn/apps/using-github-apps/reviewing-and-revoking-authorization-of-github-apps)

## 帐户管理

要将您的帐户转换为组织，请选择**转换**。
有关转换帐户的更多信息，请参阅
[将帐户转换为组织](../admin/organization/convert-account.md)。

要停用您的帐户，请选择**停用**。
有关停用帐户的信息，请参阅
[停用用户帐户](./deactivate-user-account.md)。