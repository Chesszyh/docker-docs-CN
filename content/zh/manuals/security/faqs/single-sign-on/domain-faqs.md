---
description: 单点登录域名常见问题解答
keywords: Docker, Docker Hub, SSO FAQ, 单点登录, 域名, 域名验证, 域名管理
title: SSO 和域名常见问题 (FAQ)
linkTitle: 域名
tags: [FAQ]
aliases:
- /single-sign-on/domain-faqs/
- /faq/security/single-sign-on/domain-faqs/
---

### 我能否添加子域名？

可以，您可以向您的 SSO 连接添加子域名，但所有的电子邮件地址也应位于该域名下。请验证您的 DNS 提供商是否支持同一域名的多个 TXT 记录。

### DNS 提供商能否仅配置一次用于单次验证，稍后再将其移除，还是需要永久保留？

您可以执行一次操作将域名添加到连接中。如果您组织更改了 IdP (身份提供者) 且必须重新设置 SSO，您的 DNS 提供商将需要再次进行验证。

### 配置 SSO 是否必须添加域名？我应该添加哪些域名？以及如何添加？

启用和强制执行 SSO 需要添加并验证域名。有关更多信息，请参阅 [配置单点登录 (SSO)](/manuals/security/for-admins/single-sign-on/configure.md)。这应包括用户访问 Docker 将使用的所有电子邮件域名。不允许使用公共域名，例如 `gmail.com` 或 `outlook.com`。此外，电子邮件域名应设置为主要电子邮件地址。

### 是否支持 IdP 发起的身份验证？

Docker SSO 不支持 IdP 发起的身份验证。用户必须通过 Docker Desktop 或 Docker Hub 发起登录。

### 我能否在多个组织中验证同一个域名？

您无法在组织级别为多个组织验证同一个域名。如果您想为多个组织验证同一个域名，您必须拥有 Docker Business 订阅，并 [创建一个公司 (Company)](/manuals/admin/company/new-company.md)。公司可以实现组织的集中管理，并允许在公司级别进行域名验证。
