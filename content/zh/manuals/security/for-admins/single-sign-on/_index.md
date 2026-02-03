---
description: 了解单点登录的工作原理、如何进行设置以及所需的 SSO 属性。
keywords: 单点登录, Single Sign-On, SSO, 登录, 管理, docker hub, admin console, 管理控制台, security, 安全
title: 单点登录概览
linkTitle: 单点登录
aliases:
- /single-sign-on/
- /admin/company/settings/sso/
- /admin/organization/security-settings/sso-management/
weight: 10
---

{{< summary-bar feature_name="SSO" >}}

单点登录 (Single sign-on, SSO) 允许用户通过其身份提供者 (IdP) 进行身份验证来访问 Docker。SSO 可用于整个公司及其关联的所有组织，或者拥有 Docker Business 订阅的单个组织。要将您现有的帐户升级到 Docker Business 订阅，请参阅[升级您的订阅](/subscription/upgrade/)。

## SSO 的工作原理

当您启用 SSO 时，Docker 支持用于用户登录的非 IdP 发起的 SSO 流程。用户不再使用其 Docker 用户名和密码进行身份验证，而是被重定向到身份提供者的身份验证页面进行登录。用户必须登录 Docker Hub 或 Docker Desktop 才能启动 SSO 身份验证过程。

下图显示了 SSO 在 Docker Hub 和 Docker Desktop 中的运行和管理方式。此外，它还提供了有关如何在 IdP 之间进行身份验证的信息。

![SSO 架构](images/SSO.png)

## 如何进行设置

通过以下步骤配置 SSO：
1. 通过在 Docker 中创建并验证域名来[配置 SSO](../single-sign-on/configure.md)。
2. 在 Docker 和您的 IdP 中[创建您的 SSO 连接](../single-sign-on/connect.md)。
3. 交叉连接 Docker 和您的 IdP。
4. 测试您的连接。
5. 预配用户。
6. （可选）[强制登录](../enforce-sign-in/_index.md)。
7. [管理您的 SSO 配置](../single-sign-on/manage.md)。

SSO 配置完成后，首次登录的用户可以使用其公司的域名电子邮件地址登录 Docker Hub 或 Docker Desktop。登录后，他们将被添加到您的公司，并被分配到一个组织，必要时还会被分配到一个团队。

## 前提条件

在配置 SSO 之前，请确保满足以下前提条件：
* 向您的公司通报新的 SSO 登录程序。
* 验证所有用户是否都安装了 Docker Desktop 4.4.2 或更高版本。
* 如果您的组织计划[强制执行 SSO](/manuals/security/for-admins/single-sign-on/connect.md#optional-enforce-sso)，则使用 Docker CLI 的成员需要[创建个人访问令牌 (PAT)](/docker-hub/access-tokens/)。PAT 将用于代替其用户名和密码。Docker 计划在未来弃用使用密码登录 CLI 的方式，因此为了防止身份验证问题，将需要使用 PAT。有关更多详细信息，请参阅[安全公告](/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced)。
* 确保您所有的 Docker 用户在 IdP 上都有一个有效的用户，其电子邮件地址与其唯一主要标识符 (UPN) 相同。
* 确认所有 CI/CD 流水线都已用 PAT 替换了密码。
* 对于您的服务帐户，请在 IdP 中添加您的其他域名或启用它。

## 下一步

- 开始在 Docker 中 [配置 SSO](../../for-admins/single-sign-on/configure.md)
- 浏览 [常见问题解答 (FAQs)](../../../security/faqs/single-sign-on/_index.md)
