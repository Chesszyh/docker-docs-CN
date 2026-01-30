---
description: 单点登录 IdP 常见问题解答
keywords: Docker, Docker Hub, SSO FAQ, 单点登录, IdP, 身份提供者
title: SSO 和身份提供者常见问题 (FAQ)
linkTitle: 身份提供者
tags: [FAQ]
aliases:
- /single-sign-on/idp-faqs/
- /faq/security/single-sign-on/idp-faqs/
---

### 是否可以在 Docker SSO 中使用多个 IdP？

可以。Docker 支持多个 IdP 配置。一个域名可以与多个 IdP 关联。Docker 支持 Entra ID (原 Azure AD) 以及支持 SAML 2.0 的身份提供者。

### 配置 SSO 后是否可以更改身份提供者？

可以。您必须删除 Docker SSO 连接中现有的 IdP 配置，然后 [使用新 IdP 配置 SSO](/manuals/security/for-admins/single-sign-on/connect.md)。如果您已经开启了强制执行，则在更新提供者的 SSO 连接之前，应先关闭强制执行。

### 配置 SSO 需要从身份提供者处获取哪些信息？

要在 Docker 中启用 SSO，您需要从 IdP 处获取以下信息：

* **SAML**: 实体 ID (Entity ID)、ACS URL、单点登出 (Single Logout) URL 以及公有 X.509 证书。

* **Entra ID (原 Azure AD)**: 客户端 ID (Client ID)、客户端密钥 (Client Secret)、AD 域名。

### 如果我现有的证书过期了会发生什么？

如果您现有的证书已过期，您可能需要联系您的身份提供者以获取新的 X.509 证书。然后，您需要在 Docker Hub 或 Docker 管理控制台的 [SSO 配置设置](/security/for-admins/single-sign-on/manage/#manage-sso-connections) 中更新证书。

### 如果启用 SSO 时我的 IdP 宕机了会发生什么？

如果强制执行了 SSO，那么当您的 IdP 宕机时，将无法访问 Docker Hub。您仍然可以使用个人访问令牌 (PAT) 从 CLI 访问 Docker Hub 镜像。

如果启用了 SSO 但未强制执行，则用户可以回退到使用用户名/密码进行身份验证，并在必要时触发重置密码流程。

### 我该如何处理将 Docker Hub 作为辅助注册表的帐户？我需要机器人帐户吗？

您可以向您的 IdP 添加一个机器人帐户，并为其创建一个访问令牌来替换其他凭据。

### 机器人帐户访问使用 SSO 的组织是否需要占用席位？

是的，机器人帐户需要一个席位，类似于普通的终端用户，需要在 IdP 中启用一个非别名的域电子邮件，并在 Hub 中占用一个席位。

### SAML SSO 是否使用即时 (Just-in-Time) 配置？

SSO 实现默认使用即时 (JIT) 配置。如果您通过 SCIM 启用了自动配置，您可以选择在管理控制台中禁用 JIT。参见 [即时配置 (Just-in-Time provisioning)](/security/for-admins/provisioning/just-in-time/)。

### 是否支持 IdP 发起的登录？

Docker SSO 不支持 IdP 发起的登录，仅支持由服务提供者发起的 (SP-initiated) 登录。

### 是否可以将 Docker Hub 直接连接到 Microsoft Entra (原 Azure AD) 组？

可以，针对 Docker Business 的 SSO 支持 Entra ID (原 Azure AD)，既可以通过直接集成，也可以通过 SAML。

### 我与 Entra ID 的 SSO 连接无法工作，收到应用程序配置错误的提示。我该如何排查？

请确认您已在 Entra ID (原 Azure AD) 中为您的 SSO 连接配置了必要的 API 权限。您需要在 Entra ID (原 Azure AD) 租户中授予管理员同意。参见 [Entra ID (原 Azure AD) 文档](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/grant-admin-consent?pivots=portal#grant-admin-consent-in-app-registrations)。
