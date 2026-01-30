---
description: 查找通用安全相关常见问题的答案
keywords: Docker, Docker Hub, Docker Desktop 安全 FAQ, 平台, Docker Scout, 管理员, 安全
title: 通用安全常见问题 (FAQ)
linkTitle: 通用
weight: 10
tags: [FAQ]
aliases:
- /faq/security/general/
---

### 我该如何报告漏洞？

如果您在 Docker 中发现了安全漏洞，我们鼓励您以负责任的方式报告它。请将安全问题报告至 security@docker.com，以便我们的团队能够迅速处理。

### 在不使用 SSO 的情况下，密码是如何管理的？

密码是经过加密并加盐哈希 (salt-hashed) 处理的。如果您使用应用级密码而不是 SSO，您有责任确保您的员工知道如何选择强密码、不分享密码，并且不在多个系统中重复使用密码。

### 在不使用 SSO 的情况下，Docker 是否要求重置密码？

不要求定期重置密码。NIST 不再建议将强制重置密码作为最佳实践的一部分。

### Docker 是否会在登录失败后锁定用户？

Docker Hub 的系统锁定全局设置是在 5 分钟内出现 10 次登录尝试失败后进行锁定，锁定持续时间为 5 分钟。同样的全局策略也适用于经过身份验证的 Docker Desktop 用户和 Docker Scout，这两者都使用 Docker Hub 进行身份验证。

### 你们是否支持使用 YubiKeys 的物理 MFA (多因素认证)？

您可以通过 SSO 使用您的 IdP (身份提供者) 进行配置。请向您的 IdP 咨询他们是否支持物理 MFA。

### 会话是如何管理的，它们会过期吗？

默认情况下，用户登录后，Docker 使用令牌来管理会话：

- Docker Desktop 会在 90 天后或非活动状态 30 天后让您退出登录。
- Docker Hub 和 Docker Home 会在 24 小时后让您退出登录。

Docker 还支持您的 IdP 的默认会话超时。您可以通过设置 Docker 会话分钟数 (session minutes) SAML 属性来配置此项。有关更多信息，请参阅 [SSO 属性](/manuals/security/for-admins/provisioning/_index.md#sso-attributes)。

### Docker 如何将下载归因于我们，以及使用什么数据来分类或验证用户属于我们的组织？

Docker Desktop 的下载通过包含客户域名的用户电子邮件链接到特定的组织。此外，我们还使用 IP 地址来关联用户与组织。

### 如果我们的大多数工程师都在家工作且不允许使用 VPN，你们如何通过 IP 数据将下载量归因于我们？

我们使用第三方数据增强软件将用户及其 IP 地址归因于域名，我们的提供商会分析与该特定 IP 地址相关的公共和私有数据源的活动，然后利用这些活动来识别域名并将其映射到该 IP 地址。

一些用户通过登录 Docker Desktop 并加入其域名的 Docker 组织来进行身份验证，这使我们能够以更高精度进行映射，并为您报告直接的功能使用情况。我们强烈鼓励您让用户进行身份验证，以便我们为您提供最准确的数据。

### Docker 如何区分员工用户和合同工用户？

在 Docker 中设置的组织使用经过验证的域名，任何使用非验证域名电子邮件的团队成员在组织中都会被标记为 "Guest" (访客)。

### 活动日志可以保留多久？

Docker 提供各种类型的审计日志，且日志保留期各不相同。例如，Docker 活动日志可保留 90 天。您有责任导出日志或为自己的内部系统设置驱动程序。

### 我能否导出包含所有用户及其分配的角色和权限的列表？如果可以，格式是什么？

使用 [导出成员 (Export Members)](../../admin/organization/members.md#export-members) 功能，您可以将组织的用户列表连同角色和团队信息一起导出为 CSV 文件。

### Docker Desktop 如何处理和存储身份验证信息？

Docker Desktop 利用主机操作系统的安全密钥管理来处理和存储与镜像注册表进行身份验证所需的身份验证令牌。在 macOS 上是 [Keychain](https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web)；在 Windows 上是 [通过 Wincred 提供的安全与身份 API](https://learn.microsoft.com/en-us/windows/win32/api/wincred/)；在 Linux 上是 [Pass](https://www.passwordstore.org/)。

### Docker Hub 在存储和传输过程中如何保护密码？

这仅适用于使用 Docker Hub 应用级密码与 SSO/SAML 相比的情况。对于通过 SSO 即时 (Just-in-Time) 或 SCIM 配置创建的用户，Docker Hub 不存储密码。对于所有其他用户，应用级密码在存储时经过加盐哈希 (SHA-256)，并在传输过程中经过加密 (TLS)。

### 我们如何撤销不属于我们 IdP 的用户的访问权限？我们使用 SSO 但不使用 SCIM。

如果未启用 SCIM，您必须手动从组织中移除用户。如果您是在启用 SCIM 后添加的用户，SCIM 可以自动完成此操作。在启用 SCIM 之前添加到组织的任何用户都必须手动移除。

有关手动移除用户的更多信息，请参阅 [管理组织成员](/manuals/admin/organization/members.md)。

### Docker Scout 从分析的容器镜像中收集哪些元数据？

有关 Docker Scout 存储的元数据信息，请参阅 [数据处理 (Data handling)](/manuals/scout/deep-dive/data-handling.md)。

### 市场 (Marketplace) 中的扩展在发布前是否经过安全审查？

扩展的安全审查已列入我们的路线图，但目前尚未进行此类审查。

扩展不包含在 Docker 的第三方风险管理计划中。

### 我能否通过设置禁用组织中的私有仓库，以确保没人向 Docker Hub 推送镜像？

不能。通过 [注册表访问管理 (Registry Access Management, RAM)](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)，管理员可以确保使用 Docker Desktop 的开发人员仅访问被允许的注册表。这可以通过管理控制台 (Admin Console) 中的注册表访问管理面板完成。
