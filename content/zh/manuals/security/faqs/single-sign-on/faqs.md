---
description: 单点登录常见问题
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, administration, security
title: SSO 通用常见问题
linkTitle: 通用
weight: 10
tags: [FAQ]
aliases:
- /single-sign-on/faqs/
- /faq/security/single-sign-on/faqs/
- /single-sign-on/saml-faqs/
- /faq/security/single-sign-on/saml-faqs/
- /security/faqs/single-sign-on/saml-faqs/
---

### Docker SSO 是否对所有付费订阅可用？

Docker 单点登录 (SSO) 仅适用于 Docker Business 订阅。[升级您的现有订阅](../../../subscription/change.md)以开始使用 Docker SSO。

### Docker SSO 如何工作？

Docker SSO 允许用户使用其身份提供商 (IdP) 进行身份验证以访问 Docker。Docker 支持 Entra ID（以前称为 Azure AD）和任何 SAML 2.0 身份提供商。当您启用 SSO 时，这会将用户重定向到您提供商的身份验证页面，使用其电子邮件和密码进行身份验证。

### Docker 支持哪些 SSO 流程？

Docker 支持服务提供商发起 (SP-initiated) 的 SSO 流程。这意味着用户必须登录 Docker Hub 或 Docker Desktop 才能启动 SSO 身份验证过程。

### 在哪里可以找到如何配置 Docker SSO 的详细说明？

您首先需要与您的身份提供商建立 SSO 连接，并且需要在为用户建立 SSO 连接之前验证公司电子邮件域名。有关如何配置 Docker SSO 的详细分步说明，请参阅[单点登录](../../../security/for-admins/single-sign-on/configure/_index.md)。

### Docker SSO 是否支持多因素身份验证 (MFA)？

当组织使用 SSO 时，MFA 在 IdP 级别确定，而不是在 Docker 平台上。

### SSO 需要特定版本的 Docker Desktop 吗？

是的，您组织中的所有用户必须升级到 Docker Desktop 4.4.2 或更高版本。如果强制执行 SSO 且使用公司域名电子邮件登录或作为现有 Docker 账户关联的主要电子邮件，使用旧版本 Docker Desktop 的用户将无法登录。拥有现有账户的用户无法使用其用户名和密码登录。

### 使用 SSO 时我可以保留我的 Docker ID 吗？

对于个人 Docker ID，用户是账户所有者。Docker ID 与用户的仓库、镜像、资产的访问相关联。用户可以选择在 Docker 账户上使用公司域名电子邮件。当强制执行 SSO 时，账户将连接到组织账户。当为组织或公司强制执行 SSO 时，任何使用已验证公司域名电子邮件登录且没有现有账户的用户将自动配置账户并创建新的 Docker ID。

### SAML 身份验证是否需要额外的属性？

您必须提供电子邮件地址作为属性才能通过 SAML 进行身份验证。'Name' 属性是可选的。

### 应用程序是否识别 `SAMLResponse` 主题中的 NameID/唯一标识符？

首选格式是您的电子邮件地址，这也应该是您的 Name ID。

### 我可以将组映射与 SSO 和 Azure AD (OIDC) 身份验证方法一起使用吗？

不可以。SSO 的组映射不支持 Azure AD (OIDC) 身份验证方法，因为它需要授予 OIDC 应用程序 Directory.Read.All 权限，该权限提供对目录中所有用户、组和其他敏感数据的访问。由于潜在的安全风险，Docker 不支持此配置。相反，Docker 建议[配置 SCIM 以安全地启用组同步](/security/for-admins/provisioning/group-mapping/#use-group-mapping-with-scim)。

### SSO 配置是否需要任何防火墙规则？

不需要。配置 SSO 不需要特定的防火墙规则，只要域名 `login.docker.com` 可访问即可。该域名通常默认可访问。但是，在极少数情况下，某些组织可能有防火墙限制阻止此域名。如果您在 SSO 设置过程中遇到问题，请确保在网络的防火墙设置中允许 `login.docker.com`。

### Docker 是否使用我的 IdP 的默认会话超时？

是的，Docker 通过自定义 SAML 属性支持您的 IdP 的默认会话超时。Docker 不依赖 SAML 规范中的标准 `SessionNotOnOrAfter` 元素，而是使用自定义的 `dockerSessionMinutes` 属性来控制会话持续时间。有关更多信息，请参阅 [SSO 属性](/manuals/security/for-admins/provisioning/_index.md#sso-attributes)。
