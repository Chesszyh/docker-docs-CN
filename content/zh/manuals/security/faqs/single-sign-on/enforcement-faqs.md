---
description: 单点登录强制执行常见问题解答
keywords: Docker, Docker Hub, SSO FAQ, 单点登录, 强制执行 SSO, SSO 强制执行
title: SSO 和强制执行常见问题 (FAQ)
linkTitle: 强制执行
tags: [FAQ]
aliases:
- /single-sign-on/enforcement-faqs/
- /faq/security/single-sign-on/enforcement-faqs/
---

### 我目前拥有 Docker Team 订阅。我该如何启用 SSO？

SSO 包含在 Docker Business 订阅中。要启用 SSO，您必须首先将您的订阅升级为 Docker Business 订阅。要了解如何升级现有帐户，请参阅 [升级您的订阅](../../../subscription/change.md)。

### 启用 SSO 是否需要 DNS 验证？

是的。在将域名用于 SSO 连接之前，您必须先验证该域名。

### Docker SSO 是否支持通过命令行进行身份验证？

当强制执行 SSO 时，[密码将被禁止访问 Docker CLI](/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced)。您仍然可以使用个人访问令牌 (PAT) 进行身份验证来访问 Docker CLI。

每个用户都必须创建一个 PAT 才能访问 CLI。要了解如何创建 PAT，请参阅 [管理访问令牌](/security/for-developers/access-tokens/)。在强制执行 SSO 之前已使用 PAT 登录的用户仍可以使用该 PAT 进行身份验证。

### SSO 对自动化系统和 CI/CD 管道有何影响？

在强制执行 SSO 之前，您必须 [创建 PAT](/security/for-developers/access-tokens/)。这些 PAT 用于代替密码登录自动化系统和 CI/CD 管道。

### 在强制执行之前使用个人电子邮件进行身份验证的组织用户可以期待什么？

确保您的用户在其帐户中绑定了其组织电子邮件，以便这些帐户能够迁移到 SSO 进行身份验证。

### 我能否在启用 SSO 的同时暂不启用强制执行选项？

可以，您可以选择不强制执行，这样用户在登录界面可以选择使用 Docker ID (标准电子邮件和密码) 或经过域名验证的电子邮件地址 (SSO)。

### SSO 已强制执行，但用户仍可以使用用户名和密码登录。为什么会这样？

不属于您注册域名但已被邀请加入您组织的访客 (Guest) 用户不通过您的 SSO 身份提供者登录。SSO 强制执行仅要求属于您域名的用户必须通过 SSO IdP 登录。

### 是否有办法在正式投入生产之前，先在 Okta 的测试租户中测试此功能？

有，您可以创建一个测试组织。公司可以为一个新的组织设置一个包含 5 个席位的 Business 订阅来进行测试。在执行此操作时，请确保仅启用 SSO 而不强制执行，否则所有域电子邮件用户都将被迫登录到该测试租户。

### 登录要求是在运行时还是安装时进行跟踪的？

对于 Docker Desktop，如果配置为需要组织身份验证，它会在运行时进行跟踪。

### 强制执行 SSO 与强制登录 (enforce sign-in) 有什么区别？

强制执行 SSO 和强制登录到 Docker Desktop 是不同的功能，您可以单独使用或结合使用。

强制执行 SSO 确保用户使用其 SSO 凭据而不是 Docker ID 登录。其好处之一是 SSO 使您能够更好地管理用户凭据。

强制登录到 Docker Desktop 确保用户始终登录到一个属于您组织的帐户。其好处是您组织的安全性设置始终应用于用户的会话，且您的用户始终能享受到您订阅的权益。有关更多细节，请参阅 [强制执行 Docker Desktop 登录](../../../security/for-admins/enforce-sign-in/_index.md#enforcing-sign-in-versus-enforcing-single-sign-on-sso)。
