---
description: 单点登录身份提供商常见问题
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, IdP
title: SSO 和身份提供商常见问题
linkTitle: 身份提供商
tags: [FAQ]
aliases:
- /single-sign-on/idp-faqs/
- /faq/security/single-sign-on/idp-faqs/
---

### 是否可以在 Docker SSO 中使用多个 IdP？

是的。Docker 支持多个 IdP 配置。一个域名可以与多个 IdP 关联。Docker 支持 Entra ID（以前称为 Azure AD）和支持 SAML 2.0 的身份提供商。

### 配置 SSO 后是否可以更改我的身份提供商？

是的。您必须删除 Docker SSO 连接中现有的 IdP 配置，然后[使用新的 IdP 配置 SSO](/manuals/security/for-admins/single-sign-on/connect.md)。如果您已经启用了强制执行，您应该在更新提供商 SSO 连接之前关闭强制执行。

### 配置 SSO 需要从我的身份提供商获取哪些信息？

要在 Docker 中启用 SSO，您需要从您的 IdP 获取以下信息：

* **SAML**：Entity ID、ACS URL、Single Logout URL 和公共 X.509 证书

* **Entra ID（以前称为 Azure AD）**：Client ID、Client Secret、AD Domain。

### 如果我现有的证书过期会发生什么？

如果您现有的证书已过期，您可能需要联系您的身份提供商以获取新的 X.509 证书。然后，您需要在 Docker Hub 或 Docker Admin Console 的 [SSO 配置设置](/security/for-admins/single-sign-on/manage/#manage-sso-connections)中更新证书。

### 如果启用 SSO 时我的 IdP 宕机会发生什么？

如果强制执行了 SSO，那么当您的 IdP 宕机时将无法访问 Docker Hub。您仍然可以使用个人访问令牌从 CLI 访问 Docker Hub 镜像。

如果启用了 SSO 但未强制执行，则用户可以回退到使用用户名/密码进行身份验证并触发重置密码流程（如有必要）。

### 当 Docker Hub 作为辅助注册表时，如何处理账户？我需要机器人账户吗？

您可以将机器人账户添加到您的 IdP 并为其创建访问令牌以替换其他凭据。

### 机器人账户是否需要席位才能访问使用 SSO 的组织？

是的，机器人账户需要席位，与普通最终用户类似，需要在 IdP 中启用非别名域名电子邮件并在 Hub 中使用席位。

### SAML SSO 是否使用即时配置？

SSO 实现默认使用即时 (JIT) 配置。如果您使用 SCIM 启用自动配置，您可以选择在 Admin Console 中禁用 JIT。请参阅[即时配置](/security/for-admins/provisioning/just-in-time/)。

### IdP 发起的登录是否可用？

Docker SSO 不支持 IdP 发起的登录，仅支持服务提供商发起 (SP-initiated) 的登录。

### 是否可以将 Docker Hub 直接与 Microsoft Entra（以前称为 Azure AD）组连接？

是的，Docker Business 支持通过直接集成和 SAML 两种方式使用 Entra ID（以前称为 Azure AD）进行 SSO。

### 我与 Entra ID 的 SSO 连接无法正常工作，我收到应用程序配置错误的错误。如何排除此故障？

确认您已在 Entra ID（以前称为 Azure AD）中为您的 SSO 连接配置了必要的 API 权限。您需要在 Entra ID（以前称为 Azure AD）租户中授予管理员同意。请参阅 [Entra ID（以前称为 Azure AD）文档](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/grant-admin-consent?pivots=portal#grant-admin-consent-in-app-registrations)。
