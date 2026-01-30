---
description: 单点登录常见问题解答
keywords: Docker, Docker Hub, SSO FAQ, 单点登录, 管理, 安全
title: SSO 通用常见问题 (FAQ)
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

### Docker SSO 是否对所有付费订阅都可用？

Docker 单点登录 (SSO) 仅包含在 Docker Business 订阅中。请 [升级您现有的订阅](../../../subscription/change.md) 以开始使用 Docker SSO。

### Docker SSO 是如何工作的？

Docker SSO 允许用户使用其身份提供者 (IdP) 进行身份验证以访问 Docker。Docker 支持 Entra ID (原 Azure AD) 以及任何符合 SAML 2.0 规范的身份提供者。启用 SSO 后，用户将被重定向到您的提供者的身份验证页面，使用其电子邮件和密码进行身份验证。

### Docker 支持哪些 SSO 流程？

Docker 支持由服务提供者发起的 (SP-initiated) SSO 流程。这意味着用户必须登录 Docker Hub 或 Docker Desktop 来发起 SSO 身份验证过程。

### 我在哪里可以找到关于如何配置 Docker SSO 的详细说明？

您首先需要与您的身份提供者建立 SSO 连接，并且在为您的用户建立 SSO 连接之前，需要先验证公司电子邮件域名。有关如何配置 Docker SSO 的详细分步说明，请参阅 [单点登录 (SSO)](../../../security/for-admins/single-sign-on/configure/_index.md)。

### Docker SSO 是否支持多因素认证 (MFA)？

当组织使用 SSO 时，MFA 由 IdP 级别决定，而不是由 Docker 平台决定。

### 我是否需要特定版本的 Docker Desktop 才能使用 SSO？

是的，您组织中的所有用户都必须升级到 Docker Desktop 4.4.2 或更高版本。如果使用公司域名电子邮件登录，或者该邮件作为现有 Docker 帐户关联的主要电子邮件，那么在使用旧版本 Docker Desktop 的用户在强制执行 SSO 后将无法登录。拥有现有帐户的用户将无法使用其用户名和密码登录。

### 在使用 SSO 时，我能否保留我的 Docker ID？

对于个人的 Docker ID，用户是该帐户的所有者。Docker ID 与用户对仓库、镜像和资产的访问权限相关联。用户可以选择在 Docker 帐户中绑定公司域名电子邮件。当强制执行 SSO 时，该帐户将连接到组织帐户。当为组织或公司强制执行 SSO 时，任何使用经过验证的公司域名电子邮件登录且没有现有帐户的用户，都将自动预置一个帐户，并创建一个新的 Docker ID。

### SAML 身份验证是否需要额外的属性？

您必须提供电子邮件地址作为属性才能通过 SAML 进行身份验证。“Name (姓名)”属性是可选的。

### 应用程序是否识别 `SAMLResponse` 主体中的 NameID/唯一标识符？

首选格式是您的电子邮件地址，该地址也应作为您的 Name ID。

### 我能否将组映射 (group mapping) 与 SSO 和 Azure AD (OIDC) 身份验证方法结合使用？

不能。SSO 的组映射功能不支持 Azure AD (OIDC) 身份验证方法，因为它需要授予 OIDC 应用程序 `Directory.Read.All` 权限，这会提供对目录中所有用户、组和其他敏感数据的访问权限。出于潜在的安全风险考虑，Docker 不支持此配置。相反，Docker 建议 [配置 SCIM 以启用安全的组同步](/security/for-admins/provisioning/group-mapping/#use-group-mapping-with-scim)。

### 配置 SSO 是否需要任何防火墙规则？

不需要。配置 SSO 不需要特定的防火墙规则，只要能够访问 `login.docker.com` 域名即可。此域名通常默认是可访问的。然而，在极少数情况下，某些组织可能有防火墙限制屏蔽了该域名。如果您在 SSO 设置期间遇到问题，请确保在您的网络防火墙设置中允许访问 `login.docker.com`。

### Docker 是否使用我的 IdP 的默认会话超时设置？

是的，Docker 支持通过自定义 SAML 属性使用您的 IdP 的默认会话超时设置。Docker 不依赖于 SAML 规范中标准的 `SessionNotOnOrAfter` 元素，而是使用自定义的 `dockerSessionMinutes` 属性来控制会话持续时间。有关更多信息，请参阅 [SSO 属性](/manuals/security/for-admins/provisioning/_index.md#sso-attributes)。
