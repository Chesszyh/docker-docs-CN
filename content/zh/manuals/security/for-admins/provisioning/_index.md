---
description: 了解如何为您的 SSO 配置预配用户。
keywords: 预配用户, 预配, provisioning, JIT, SCIM, 组映射, group mapping, sso, docker hub, hub, docker admin, admin, security, 安全
title: 预配用户
linkTitle: 预配
weight: 20
---

{{< summary-bar feature_name="SSO" >}}

配置完 SSO 连接后，下一步是预配（Provision）用户。此过程确保用户可以访问您的组织。
本指南概述了用户预配及支持的预配方法。

## 什么是预配？

预配通过根据身份提供者（IdP）的数据自动执行创建、更新和停用用户等任务，从而帮助管理用户。用户预配有三种方法，分别适用于不同的组织需求：

| 预配方法 | 描述 | Docker 中的默认设置 | 推荐用于 |
| :--- | :--- | :------------- | :--- |
| 即时预配 (Just-in-Time, JIT) | 当用户首次通过 SSO 登录时，自动创建并预配用户帐户 | 默认启用 | 最适合需要最小化设置、团队规模较小或安全要求较低的组织 |
| 跨域身份管理系统 (SCIM) | 在您的 IdP 和 Docker 之间持续同步用户数据，确保用户属性保持最新而无需手动更新 | 默认禁用 | 最适合较大型组织，或用户信息、角色频繁变更的环境 |
| 组映射 (Group mapping) | 将 IdP 中的用户组映射到 Docker 中的特定角色和权限，从而根据组数组成员身份实现精细的访问控制 | 默认禁用 | 最适合需要严格访问控制、并根据角色和权限管理用户的组织 |

## 默认预配设置

默认情况下，当您配置 SSO 连接时，Docker 会启用 JIT 预配。启用 JIT 后，用户首次使用 SSO 流程登录时会自动创建用户帐户。

JIT 预配可能无法提供某些组织所需的控制或安全级别。在这种情况下，可以配置 SCIM 或组映射，以便管理员对用户访问和属性拥有更多控制权。

## SSO 属性

当用户通过 SSO 登录时，Docker 会从您的 IdP 获取多个属性，以管理用户的身份和权限。这些属性包括：
- **Email address（电子邮件地址）**：用户的唯一标识符
- **Full name（全名）**：用户的完整姓名
- **Groups（组）**：可选。用于基于组的访问控制
- **Docker Org（Docker 组织）**：可选。指定用户所属的组织
- **Docker Team（Docker 团队）**：可选。定义用户在组织内所属的团队
- **Docker Role（Docker 角色）**：可选。决定用户在 Docker 中的权限
- **Docker session minutes（Docker 会话分钟数）**：可选。设置用户在必须重新向身份提供者（IdP）进行身份验证之前的会话持续时间。该值必须是大于 0 的正整数。
如果未提供此属性，默认情况下：
    - Docker Desktop 会在 90 天后或不活动 30 天后将您登出。
    - Docker Hub 和 Docker Home 会在 24 小时后将您登出。

如果您的组织使用 SAML 进行 SSO，Docker 会从 SAML 断言消息中检索这些属性。请记住，不同的 IdP 可能会对这些属性使用不同的名称。下表概述了 Docker 使用的可能 SAML 属性：

| SSO 属性	| SAML 断言消息属性 |
| :--- | :--- |
| Email address |	`"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"`, `email` |
| Full name	| `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"`, `name`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname"` |
| Groups (可选) |	`"http://schemas.xmlsoap.org/claims/Group"`, `"http://schemas.microsoft.com/ws/2008/06/identity/claims/groups"`, `Groups`, `groups` |
| Docker Org (可选)	| `dockerOrg` |
| Docker Team (可选) |	`dockerTeam` |
| Docker Role (可选) |	`dockerRole` |
| Docker session minutes (可选) | `dockerSessionMinutes`，必须是 > 0 的正整数 |

## 下一步

查看各预配方法指南以获取配置步骤：
- [JIT](/manuals/security/for-admins/provisioning/just-in-time.md)
- [SCIM](/manuals/security/for-admins/provisioning/scim.md)
- [组映射](/manuals/security/for-admins/provisioning/group-mapping.md)
