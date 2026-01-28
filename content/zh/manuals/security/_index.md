---
title: 安全
description: 了解 Docker 提供的安全功能并探索最佳实践
keywords: docker, docker hub, docker desktop, security
weight: 40
params:
  sidebar:
    group: Platform
grid_admins:
- title: Settings Management
  description: 了解 Settings Management（设置管理）如何保护开发人员的工作流程。
  icon: shield_locked
  link: /security/for-admins/hardened-desktop/settings-management/
- title: Enhanced Container Isolation
  description: 了解 Enhanced Container Isolation（增强容器隔离）如何防止容器攻击。
  icon: security
  link: /security/for-admins/hardened-desktop/enhanced-container-isolation/
- title: Registry Access Management
  description: 控制开发人员在使用 Docker Desktop 时可以访问的注册表。
  icon: home_storage
  link: /security/for-admins/hardened-desktop/registry-access-management/
- title: Image Access Management
  description: 控制开发人员可以从 Docker Hub 拉取的镜像。
  icon: photo_library
  link: /security/for-admins/hardened-desktop/image-access-management/
- title: "Air-Gapped Containers"
  description: 限制容器访问不需要的网络资源。
  icon: "vpn_lock"
  link: /security/for-admins/hardened-desktop/air-gapped-containers/
- title: Enforce sign-in
  description: 为您团队和组织的成员配置登录要求。
  link: /security/for-admins/enforce-sign-in/
  icon: passkey
- title: Domain management
  description: 识别组织中未被纳管的用户。
  link: /security/for-admins/domain-management/
  icon: person_search
- title: Docker Scout
  description: 探索 Docker Scout 如何帮助您创建更安全的软件供应链。
  icon: query_stats
  link: /scout/
- title: SSO
  description: 了解如何为您的公司或组织配置 SSO（单点登录）。
  icon: key
  link: /security/for-admins/single-sign-on/
- title: SCIM
  description: 设置 SCIM 以自动配置和取消配置用户。
  icon: checklist
  link: /security/for-admins/provisioning/scim/
- title: Roles and permissions
  description: 为个人分配角色，赋予他们在组织内的不同权限。
  icon: badge
  link: /security/for-admins/roles-and-permissions/
- title: Private marketplace for Extensions (Beta)
  description: 了解如何为 Docker Desktop 用户配置和设置包含精选扩展列表的私有市场。
  icon: storefront
  link: /desktop/extensions/private-marketplace/
- title: Organization access tokens
  description: 创建组织访问令牌作为密码的替代方案。
  link: /security/for-admins/access-tokens/
  icon: password
grid_developers:
- title: Set up two-factor authentication
  description: 为您的 Docker 账户添加额外的身份验证层。
  link: /security/for-developers/2fa/
  icon: phonelink_lock
- title: Manage access tokens
  description: 创建个人访问令牌作为密码的替代方案。
  icon: password
  link: /security/for-developers/access-tokens/
- title: Static vulnerability scanning
  description: 自动对您的 Docker 镜像运行时间点扫描以检测漏洞。
  icon: image_search
  link: /docker-hub/repos/manage/vulnerability-scanning/
- title: Docker Engine security
  description: 了解如何保持 Docker Engine 的安全。
  icon: security
  link: /engine/security/
- title: Secrets in Docker Compose
  description: 了解如何在 Docker Compose 中使用密钥。
  icon: privacy_tip
  link: /compose/how-tos/use-secrets/
grid_resources:
- title: Security FAQs
  description: 探索常见的安全常见问题解答。
  icon: help
  link: /faq/security/general/
- title: Security best practices
  description: 了解您可以采取的步骤来提高容器的安全性。
  icon: category
  link: /develop/security-best-practices/
- title: Suppress CVEs with VEX
  description: 了解如何抑制在镜像中发现的不适用或已修复的漏洞。
  icon: query_stats
  link: /scout/guides/vex/
---

Docker 为管理员和开发人员提供安全保障。

如果您是管理员，您可以为开发人员在 Docker 产品中强制登录，并通过 DevOps 安全控制（如 Enhanced Container Isolation（增强容器隔离）和 Registry Access Management（注册表访问管理））来扩展、管理和保护您的 Docker Desktop 实例。

对于管理员和开发人员，Docker 提供特定于安全的产品，例如 Docker Scout，用于通过主动的镜像漏洞监控和修复策略来保护您的软件供应链。

## 管理员专区

探索 Docker 提供的安全功能，以满足您公司的安全策略。

{{< grid items="grid_admins" >}}

## 开发人员专区

了解如何在不影响生产力的情况下保护您的本地环境、基础设施和网络。

{{< grid items="grid_developers" >}}

## 更多资源

{{< grid items="grid_resources" >}}
