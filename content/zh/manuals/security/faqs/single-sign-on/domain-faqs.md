---
description: 单点登录域名常见问题
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, domains, domain verification, domain management
title: SSO 和域名常见问题
linkTitle: 域名
tags: [FAQ]
aliases:
- /single-sign-on/domain-faqs/
- /faq/security/single-sign-on/domain-faqs/
---

### 我可以添加子域名吗？

是的，您可以将子域名添加到您的 SSO 连接中，但是所有电子邮件地址也应该在该域名上。请验证您的 DNS 提供商是否支持同一域名的多个 TXT 记录。

### DNS 提供商可以配置一次用于一次性验证，之后删除它，还是永久需要它？

您可以一次性验证以将域名添加到连接中。如果您的组织更换 IdP 并需要重新设置 SSO，您的 DNS 提供商将需要再次验证。

### 配置 SSO 需要添加域名吗？我应该添加哪些域名？如何添加？

添加和验证域名是启用和强制执行 SSO 所必需的。有关更多信息，请参阅[配置单点登录](/manuals/security/for-admins/single-sign-on/configure.md)。这应该包括用户将用于访问 Docker 的所有电子邮件域名。不允许使用公共域名，例如 `gmail.com` 或 `outlook.com`。此外，电子邮件域名应设置为主要电子邮件。

### 是否支持 IdP 发起的身份验证？

Docker SSO 不支持 IdP 发起的身份验证。用户必须通过 Docker Desktop 或 Hub 发起登录。

### 我可以在多个组织上验证同一个域名吗？

您不能在组织级别为多个组织验证同一个域名。如果您想为多个组织验证一个域名，您必须拥有 Docker Business 订阅，并[创建公司](/manuals/admin/company/new-company.md)。公司可以对组织进行集中管理，并允许在公司级别进行域名验证。
