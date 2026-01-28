---
title: 管理账户
weight: 20
description: 了解如何管理您的 Docker 账户设置。
keywords: 账户, docker ID, 账户设置, 账户管理, docker home
---

您可以使用 Docker Home 集中管理您的 Docker 账户设置。在这里，您还可以对账户执行管理操作并管理账户安全。

> [!TIP]
>
> 如果您的账户与强制执行单点登录 (SSO) 的组织相关联，您可能没有权限更新账户设置。您必须联系您的管理员来更新设置。

## 更新常规设置

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 选择右上角的头像，然后选择 **Account settings**（账户设置）。

在账户设置页面，您可以执行以下任何操作。

### 更新账户信息

账户信息在 Docker Hub 的账户个人资料中可见。您可以更新以下账户信息：

- 全名
- 公司
- 位置
- 网站
- Gravatar 电子邮件：要为您的 Docker 账户添加头像，请创建一个 [Gravatar 账户](https://gravatar.com/) 并创建您的头像。接下来，将您的 Gravatar 电子邮件添加到您的 Docker 账户设置中。头像在 Docker 中更新可能需要一些时间。

在此处进行更改，然后选择 **Save**（保存）以保存设置。

### 更新电子邮件地址

要更新您的电子邮件地址，请选择 **Email**（电子邮件）：

1. 输入您的新电子邮件地址。
2. 输入您的密码以确认更改。
3. 选择 **Send verification email**（发送验证邮件）向您的新电子邮件地址发送验证邮件。

验证电子邮件地址后，您的账户信息将更新。

### 更改密码

您可以通过电子邮件发起密码重置来更改密码。

要更改密码，请选择 **Password**（密码），然后选择 **Reset password**（重置密码）。按照密码重置邮件中的说明进行操作。

## 管理安全设置

要更新您的双重身份验证 (2FA) 设置，请选择 **2FA**。有关账户双重身份验证 (2FA) 的信息，请参阅 [启用双重身份验证](../security/for-developers/2fa/_index.md) 开始使用。

要管理个人访问令牌，请选择 **Personal access tokens**（个人访问令牌）。有关个人访问令牌的信息，请参阅 [创建和管理访问令牌](../security/for-developers/access-tokens.md)。

## 管理关联账户

您可以使用账户设置页面取消关联已链接到 Docker 账户的 Google 或 GitHub 账户：

1. 选择 **Connected accounts**（关联账户）。
2. 在已关联的账户上选择 **Disconnect**（断开连接）。
3. 要完全取消 Docker 账户的关联，您还必须在 Google 或 GitHub 端取消与 Docker 的关联。有关更多信息，请参阅 Google 或 GitHub 的文档：
    - [管理您的 Google 账号与第三方之间的连接](https://support.google.com/accounts/answer/13533235?hl=zh-Hans)
    - [查看并撤销 GitHub App 的授权](https://docs.github.com/zh/apps/using-github-apps/reviewing-and-revoking-authorization-of-github-apps)

## 账户管理

要将您的账户转换为组织，请选择 **Convert**（转换）。有关转换账户的更多信息，请参阅 [将账户转换为组织](../admin/organization/convert-account.md)。

要停用您的账户，请选择 **Deactivate**（停用）。有关停用账户的信息，请参阅 [停用用户账户](./deactivate-user-account.md)。
