---
title: 安全
description: 了解 Docker 提供的安全功能并探索最佳实践
keywords: docker, docker hub, docker desktop, security, 安全
weight: 40
params:
  sidebar:
    group: 平台
grid_admins:
- title: 设置管理 (Settings Management)
  description: 了解“设置管理”如何保护开发人员的工作流。
  icon: shield_locked
  link: /security/for-admins/hardened-desktop/settings-management/
- title: 增强型容器隔离 (Enhanced Container Isolation)
  description: 了解增强型容器隔离如何防止容器攻击。
  icon: security
  link: /security/for-admins/hardened-desktop/enhanced-container-isolation/
- title: 注册表访问管理 (Registry Access Management)
  description: 控制开发人员在使用 Docker Desktop 时可以访问的注册表。
  icon: home_storage
  link: /security/for-admins/hardened-desktop/registry-access-management/
- title: 镜像访问管理 (Image Access Management)
  description: 控制开发人员可以从 Docker Hub 拉取的镜像。
  icon: photo_library
  link: /security/for-admins/hardened-desktop/image-access-management/
- title: "气隙 (Air-Gapped) 容器"
  description: 限制容器访问不需要的网络资源。
  icon: "vpn_lock"
  link: /security/for-admins/hardened-desktop/air-gapped-containers/
- title: 强制登录
  description: 为您的团队和组织成员配置登录要求。
  link: /security/for-admins/enforce-sign-in/
  icon: passkey
- title: 域名管理
  description: 识别组织中尚未纳入管理的外部用户。
  link: /security/for-admins/domain-management/
  icon: person_search
- title: Docker Scout
  description: 探索 Docker Scout 如何帮助您创建更安全的软件供应链。
  icon: query_stats
  link: /scout/
- title: SSO
  description: 了解如何为您的公司或组织配置 SSO (单点登录)。
  icon: key
  link: /security/for-admins/single-sign-on/
- title: SCIM
  description: 设置 SCIM 以自动配置和撤销用户。
  icon: checklist
  link: /security/for-admins/provisioning/scim/
- title: 角色与权限
  description: 为个人分配角色，赋予他们在组织内的不同权限。
  icon: badge
  link: /security/for-admins/roles-and-permissions/
- title: 扩展私有市场 (Beta)
  description: 了解如何为您的 Docker Desktop 用户配置和设置包含精选扩展列表的私有市场。
  icon: storefront
  link: /desktop/extensions/private-marketplace/
- title: 组织访问令牌
  description: 创建组织访问令牌作为密码的替代方案。
  link: /security/for-admins/access-tokens/
  icon: password
grid_developers:
- title: 设置双因素认证
  description: 为您的 Docker 帐户添加额外的身份验证层。
  link: /security/for-developers/2fa/
  icon: phonelink_lock
- title: 管理访问令牌
  description: 创建个人访问令牌作为密码的替代方案。
  icon: password
  link: /security/for-developers/access-tokens/
- title: 静态漏洞扫描
  description: 自动对您的 Docker 镜像进行漏洞扫描。
  icon: image_search
  link: /docker-hub/repos/manage/vulnerability-scanning/
- title: Docker Engine 安全
  description: 了解如何确保 Docker Engine 的安全。
  icon: security
  link: /engine/security/
- title: Docker Compose 中的机密 (Secrets)
  description: 了解如何在 Docker Compose 中使用机密。
  icon: privacy_tip
  link: /compose/how-tos/use-secrets/
grid_resources:
- title: 安全常见问题 (FAQ)
  description: 探索常见的安全常见问题。
  icon: help
  link: /faq/security/general/
- title: 安全最佳实践
  description: 了解您可以采取哪些步骤来提高容器的安全性。
  icon: category
  link: /develop/security-best-practices/
- title: 使用 VEX 抑制 CVE
  description: 了解如何抑制镜像中发现的不适用或已修复的漏洞。
  icon: query_stats
  link: /scout/guides/vex/
---

Docker 为管理员和开发人员都提供了安全防护措施。

如果您是管理员，您可以强制开发人员在各款 Docker 产品中登录，并使用增强型容器隔离 (Enhanced Container Isolation) 和注册表访问管理 (Registry Access Management) 等 DevOps 安全控制措施来扩展、管理和保护您的 Docker Desktop 实例。

对于管理员和开发人员，Docker 还提供了专门的安全产品，例如 Docker Scout，用于通过主动的镜像漏洞监控和修复策略来保护您的软件供应链。

## 针对管理员

探索 Docker 提供的安全功能，以满足您公司的安全政策。

{{< grid items="grid_admins" >}}

## 针对开发人员

了解如何在不影响生产力的前提下保护您的本地环境、基础设施和网络。

{{< grid items="grid_developers" >}}

## 更多资源

{{< grid items="grid_resources" >}}
