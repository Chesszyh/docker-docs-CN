---
description: 单点登录强制执行常见问题
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, enforce SSO, SSO enforcement
title: SSO 和强制执行常见问题
linkTitle: 强制执行
tags: [FAQ]
aliases:
- /single-sign-on/enforcement-faqs/
- /faq/security/single-sign-on/enforcement-faqs/
---

### 我目前有 Docker Team 订阅。如何启用 SSO？

SSO 可用于 Docker Business 订阅。要启用 SSO，您必须首先将订阅升级到 Docker Business 订阅。要了解如何升级现有账户，请参阅[升级您的订阅](../../../subscription/change.md)。

### 启用 SSO 需要 DNS 验证吗？

是的。您必须先验证域名，然后才能将其与 SSO 连接一起使用。

### Docker SSO 是否支持通过命令行进行身份验证？

当强制执行 SSO 时，[密码无法访问 Docker CLI](/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced)。您仍然可以使用个人访问令牌 (PAT) 进行身份验证来访问 Docker CLI。

每个用户必须创建一个 PAT 才能访问 CLI。要了解如何创建 PAT，请参阅[管理访问令牌](/security/for-developers/access-tokens/)。在 SSO 强制执行之前已经使用 PAT 登录的用户仍然可以使用该 PAT 进行身份验证。

### SSO 如何影响自动化系统和 CI/CD 管道？

在强制执行 SSO 之前，您必须[创建 PAT](/security/for-developers/access-tokens/)。这些 PAT 用于代替密码登录自动化系统和 CI/CD 管道。

### 在强制执行之前使用个人电子邮件进行身份验证的组织用户会发生什么？

确保您的用户在其账户上拥有组织电子邮件，以便账户将迁移到使用 SSO 进行身份验证。

### 我可以启用 SSO 但暂不强制执行吗？

是的，您可以选择不强制执行，用户可以选择在登录屏幕上使用 Docker ID（标准电子邮件和密码）或域名验证的电子邮件地址（SSO）。

### SSO 已强制执行，但用户可以使用用户名和密码登录。为什么会这样？

不属于您已注册域名但已被邀请加入您组织的访客用户不会通过您的 SSO 身份提供商登录。SSO 强制执行仅要求属于您域名的用户必须通过 SSO IdP。

### 是否有办法在生产之前使用 Okta 测试租户测试此功能？

是的，您可以创建一个测试组织。公司可以在新组织上设置一个新的 5 席位 Business 订阅进行测试。为此，请确保只启用 SSO，不要强制执行，否则所有域名电子邮件用户将被强制登录到该测试租户。

### 登录要求是在运行时还是安装时跟踪的？

对于 Docker Desktop，如果它被配置为需要对组织进行身份验证，则它在运行时跟踪。

### 强制执行 SSO 与强制登录有什么区别？

强制执行 SSO 和强制登录 Docker Desktop 是不同的功能，您可以单独使用或一起使用。

强制执行 SSO 确保用户使用其 SSO 凭据而不是其 Docker ID 登录。好处之一是 SSO 使您能够更好地管理用户凭据。

强制登录 Docker Desktop 确保用户始终登录到作为您组织成员的账户。好处是您组织的安全设置始终应用于用户的会话，并且您的用户始终享受您订阅的好处。有关更多详细信息，请参阅[强制 Desktop 登录](../../../security/for-admins/enforce-sign-in/_index.md#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。
