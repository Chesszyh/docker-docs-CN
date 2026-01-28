---
description: 了解单点登录的工作原理、如何设置以及所需的 SSO 属性。
keywords: Single Sign-On, SSO, sign-on, admin, docker hub, admin console, security
title: 单点登录概述
linkTitle: 单点登录
aliases:
- /single-sign-on/
- /admin/company/settings/sso/
- /admin/organization/security-settings/sso-management/
weight: 10
---

{{< summary-bar feature_name="SSO" >}}

单点登录（Single sign-on，SSO）允许用户通过其身份提供商（Identity Providers，IdPs）进行身份验证来访问 Docker。SSO 可用于整个公司及该公司下的所有关联组织，或者用于拥有 Docker Business 订阅的单个组织。要将您现有的账户升级到 Docker Business 订阅，请参阅[升级您的订阅](/subscription/upgrade/)。

## SSO 工作原理

当您启用 SSO 时，Docker 支持非 IdP 发起的 SSO 流程进行用户登录。用户不再使用其 Docker 用户名和密码进行身份验证，而是被重定向到您的身份提供商的身份验证页面进行登录。用户必须登录到 Docker Hub 或 Docker Desktop 才能启动 SSO 身份验证流程。

下图展示了 SSO 在 Docker Hub 和 Docker Desktop 中的运作和管理方式。此外，它还提供了有关如何在您的 IdP 之间进行身份验证的信息。

![SSO 架构](images/SSO.png)

## 如何设置

SSO 的配置包括以下步骤：
1. 通过在 Docker 中创建和验证域来[配置 SSO](../single-sign-on/configure.md)。
2. 在 Docker 和您的 IdP 中[创建您的 SSO 连接](../single-sign-on/connect.md)。
3. 交叉连接 Docker 和您的 IdP。
4. 测试您的连接。
5. 配置用户。
6. 可选。[强制登录](../enforce-sign-in/_index.md)。
7. [管理您的 SSO 配置](../single-sign-on/manage.md)。

完成 SSO 配置后，首次用户可以使用其公司的域电子邮件地址登录 Docker Hub 或 Docker Desktop。一旦登录，他们将被添加到您的公司，分配到一个组织，如有必要，还会分配到一个团队。

## 前提条件

在配置 SSO 之前，请确保满足以下前提条件：
* 通知您的公司有关新的 SSO 登录程序。
* 验证所有用户都已安装 Docker Desktop 4.4.2 或更高版本。
* 如果您的组织计划[强制执行 SSO](/manuals/security/for-admins/single-sign-on/connect.md#optional-enforce-sso)，使用 Docker CLI 的成员需要[创建个人访问令牌（PAT）](/docker-hub/access-tokens/)。PAT 将用于代替他们的用户名和密码。Docker 计划在未来弃用使用密码登录 CLI 的方式，因此使用 PAT 将是防止身份验证问题的必要条件。有关更多详细信息，请参阅[安全公告](/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced)。
* 确保您的所有 Docker 用户在您的 IdP 上都有一个有效用户，其电子邮件地址与其唯一主体标识符（Unique Primary Identifier，UPN）相同。
* 确认所有 CI/CD 流水线已将其密码替换为 PAT。
* 对于您的服务账户，请添加您的其他域或在您的 IdP 中启用它。

## 下一步

- 开始在 Docker 中[配置 SSO](../../for-admins/single-sign-on/configure.md)
- 查看[常见问题解答](../../../security/faqs/single-sign-on/_index.md)
