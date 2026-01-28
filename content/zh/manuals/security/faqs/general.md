---
description: 查找常见安全相关问题的解答
keywords: Docker, Docker Hub, Docker Desktop security FAQs, platform, Docker Scout, admin, security
title: 通用安全常见问题
linkTitle: 通用
weight: 10
tags: [FAQ]
aliases:
- /faq/security/general/
---

### 如何报告漏洞？

如果您在 Docker 中发现了安全漏洞，我们鼓励您负责任地报告它。请将安全问题报告至 security@docker.com，以便我们的团队能够迅速处理。

### 不使用 SSO 时密码是如何管理的？

密码经过加密和加盐哈希处理。如果您使用应用程序级别的密码而不是 SSO，您有责任确保您的员工知道如何选择强密码、不共享密码，以及不在多个系统中重复使用密码。

### 不使用 SSO 时 Docker 是否要求密码重置？

不要求定期重置密码。NIST 不再推荐将密码重置作为最佳实践的一部分。

### Docker 是否在登录失败后锁定用户？

Docker Hub 的系统锁定全局设置是在 5 分钟内登录失败 10 次后锁定，锁定持续时间为 5 分钟。相同的全局策略适用于经过身份验证的 Docker Desktop 用户和 Docker Scout，两者都使用 Docker Hub 进行身份验证。

### 你们是否支持使用 YubiKeys 的物理 MFA？

您可以通过您的 IdP 使用 SSO 进行配置。请向您的 IdP 确认他们是否支持物理 MFA。

### 会话是如何管理的，它们会过期吗？

默认情况下，Docker 在用户登录后使用令牌来管理会话：

- Docker Desktop 在 90 天后或 30 天不活动后将您登出。
- Docker Hub 和 Docker Home 在 24 小时后将您登出。

Docker 还支持您的 IdP 的默认会话超时。您可以通过设置 Docker 会话分钟数 SAML 属性来配置此项。有关更多信息，请参阅 [SSO 属性](/manuals/security/for-admins/provisioning/_index.md#sso-attributes)。

### Docker 如何将下载归属于我们，以及使用哪些数据来分类或验证用户是我们组织的一部分？

Docker Desktop 下载通过用户的包含客户域名的电子邮件链接到特定组织。此外，我们使用 IP 地址将用户与组织关联。

### 如果我们的大多数工程师在家工作且不允许使用 VPN，你们如何通过 IP 数据将下载数量归属于我们？

我们使用第三方数据丰富软件将用户及其 IP 地址归属于域名，我们的提供商分析与该特定 IP 地址相关的公共和私有数据源的活动，然后使用该活动来识别域名并将其映射到 IP 地址。

某些用户通过登录 Docker Desktop 并加入其域名的 Docker 组织进行身份验证，这使我们能够以更高的准确度映射他们，并为您报告直接功能使用情况。我们强烈建议您让用户进行身份验证，以便我们能够为您提供最准确的数据。

### Docker 如何区分员工用户和承包商用户？

在 Docker 中设置的组织使用已验证的域名，任何电子邮件域名与已验证域名不同的团队成员在该组织中被标记为"访客"。

### 活动日志可保留多长时间？

Docker 提供各种类型的审计日志，日志保留时间各不相同。例如，Docker 活动日志可保留 90 天。您有责任将日志导出或设置驱动程序到您自己的内部系统。

### 我可以导出包含所有用户及其分配角色和权限的列表吗？如果可以，是什么格式？

使用[导出成员](../../admin/organization/members.md#export-members)功能，您可以将组织用户的列表及其角色和团队信息导出为 CSV 格式。

### Docker Desktop 如何处理和存储身份验证信息？

Docker Desktop 利用主机操作系统的安全密钥管理来处理和存储用于向镜像注册表进行身份验证所需的身份验证令牌。在 macOS 上，这是 [Keychain](https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web)；在 Windows 上，这是[通过 Wincred 的安全和身份 API](https://learn.microsoft.com/en-us/windows/win32/api/wincred/)；在 Linux 上，这是 [Pass](https://www.passwordstore.org/)。

### Docker Hub 如何在存储和传输中保护密码？

这仅适用于使用 Docker Hub 的应用程序级别密码而非 SSO/SAML 的情况。对于通过 SSO 即时配置或 SCIM 配置创建的用户，Docker Hub 不存储密码。对于所有其他用户，应用程序级别的密码在存储中进行加盐哈希（SHA-256），在传输中进行加密（TLS）。

### 对于不属于我们 IdP 的用户，我们如何取消他们的配置？我们使用 SSO 但不使用 SCIM

如果未启用 SCIM，您必须手动从组织中删除用户。如果您的用户是在启用 SCIM 后添加的，SCIM 可以自动执行此操作。在启用 SCIM 之前添加到组织的任何用户必须手动删除。

有关手动删除用户的更多信息，请参阅[管理组织成员](/manuals/admin/organization/members.md)。

### Scout 分析的容器镜像收集了哪些元数据？

有关 Docker Scout 存储的元数据的信息，请参阅[数据处理](/manuals/scout/deep-dive/data-handling.md)。

### Marketplace 中的扩展在上架前是如何进行安全审查的？

扩展的安全审查在我们的路线图上，但目前尚未完成此审查。

扩展不在 Docker 的第三方风险管理计划范围内。

### 我可以通过设置在组织中禁用私有仓库，以确保没有人将镜像推送到 Docker Hub 吗？

不可以。使用 [Registry Access Management](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)（注册表访问管理，RAM），管理员可以确保使用 Docker Desktop 的开发人员只能访问允许的注册表。这可以通过 Admin Console 中的 Registry Access Management 仪表板完成。
