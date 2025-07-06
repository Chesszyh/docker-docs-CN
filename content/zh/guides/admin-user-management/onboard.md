---
title: 在 Docker 中引导和管理角色和权限
description: 了解如何在 Docker 中管理角色、邀请成员以及实施可扩展的访问控制，以实现安全高效的协作。
keywords: sso, scim, jit, 邀请成员, docker hub, docker admin console, 引导, 安全
weight: 20
---

本页面将指导你完成所有者和成员的引导，并使用 SSO 和 SCIM 等工具来确保未来的引导工作。

## 第 1 步：邀请所有者

当你创建一个 Docker 组织时，你将自动成为其唯一的所有者。虽然是可选的，但添加其他所有者可以通过分配管理职责来显着简化组织的引导和管理过程。它还确保了连续性，并且在主要所有者不可用时不会造成障碍。

有关所有者的详细信息，请参阅[角色和权限](/manuals/security/for-admins/roles-and-permissions.md)。

## 第 2 步：邀请成员并分配角色

成员被授予对资源的受控访问权限，并享有增强的组织权益。当你邀请成员加入你的 Docker 组织时，你会立即为他们分配一个角色。

### 邀请成员的好处

 - 增强的可见性：深入了解用户活动，从而更容易监控访问和执行安全策略。

 - 简化的协作：通过授予对共享资源和存储库的访问权限，帮助成员有效协作。

 - 改进的资源管理：在你的组织内组织和跟踪用户，确保资源的最佳分配。

 - 访问增强功能：成员可以享受组织范围内的福利，例如增加的拉取限制和对高级 Docker 功能的访问。

 - 安全控制：在组织级别应用和执行安全设置，降低与非托管帐户相关的风险。

有关详细信息，请参阅[管理组织成员](/manuals/admin/organization/members.md)。

## 第 3 步：面向未来的用户管理

一种强大的、面向未来的用户管理方法结合了自动化配置、集中式身份验证和动态访问控制。实施这些实践可确保一个可扩展、安全且高效的环境。

### 使用单点登录 (SSO) 保护用户身份验证

将 Docker 与你的身份提供商集成可简化用户访问并增强安全性。

SSO：

 - 简化登录，因为用户使用其组织凭据登录。

 - 减少与密码相关的漏洞。

 - 简化引导，因为它与 SCIM 和组映射无缝协作以实现自动化配置。

[SSO 文档](/manuals/security/for-admins/single-sign-on/_index.md)。

### 使用 SCIM 和 JIT 配置自动化引导

使用 [SCIM](/manuals/security/for-admins/provisioning/scim.md) 和[即时 (JIT) 配置](/manuals/security/for-admins/provisioning/just-in-time.md)简化用户配置和角色管理。

使用 SCIM，你可以：

 - 自动与你的身份提供商同步用户和角色。

 - 根据目录更改自动添加、更新或删除用户。

使用 JIT 配置，你可以：

 - 根据[组映射](#simplify-access-with-group-mapping)在首次登录时自动添加用户。

 - 通过消除预邀请步骤来减少开销。

### 使用组映射简化访问

组映射通过将身份提供商组链接到 Docker 角色和团队来自动化权限管理。

它还：

 - 减少角色分配中的手动错误。

 - 确保一致的访问控制策略。

 - 帮助你在团队壮大或变更时扩展权限。

有关其工作原理的更多信息，请参阅[组映射](/manuals/security/for-admins/provisioning/group-mapping.md)。
