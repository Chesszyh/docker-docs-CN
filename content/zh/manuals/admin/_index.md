---
title: 管理
description: 探索账户、组织和公司管理的相关手册。
keywords: admin, administration, company, organization, Admin Console, user accounts, account management
weight: 10
params:
  sidebar:
    group: Platform
grid:
- title: 公司管理
  description: 探索如何管理公司。
  icon: apartment
  link: /admin/company/
- title: 组织管理
  description: 了解组织管理。
  icon: store
  link: /admin/organization/
- title: 组织入门
  description: 了解如何引导和保护您的组织。
  icon: explore
  link: /admin/organization/onboard
- title: 公司常见问题
  description: 发现有关公司的常见问题和解答。
  icon: help
  link: /faq/admin/company-faqs/
- title: 组织常见问题
  description: 探索有关组织的热门常见问题主题。
  icon: help
  link: /faq/admin/organization-faqs/
- title: 安全
  description: 探索面向管理员的安全功能。
  icon: shield_locked
  link: /security/
aliases:
- /docker-hub/admin-overview
---

管理员可以使用 Docker Admin Console（Docker 管理控制台）管理公司和组织。

[Docker Admin Console](https://app.docker.com/admin) 为管理员提供了对其公司和组织的集中可观测性、访问管理和控制功能。为了提供这些功能，Docker 使用以下层级结构和角色。

![Docker 层级结构](./images/docker-admin-structure.webp)

- 公司（Company）：公司简化了 Docker 组织和设置的管理。创建公司是可选的，仅适用于 Docker Business 订阅用户。
  - 公司所有者（Company owner）：一个公司可以有多个所有者。公司所有者拥有公司范围的可观测性，可以管理适用于所有关联组织的公司范围设置。此外，公司所有者对所有关联组织拥有与组织所有者相同的访问权限。
- 组织（Organization）：组织是团队和仓库的集合。Docker Team 和 Business 订阅用户必须至少拥有一个组织。
  - 组织所有者（Organization owner）：一个组织可以有多个所有者。组织所有者拥有对其组织的可观测性，可以管理其用户和设置。
- 团队（Team）：团队是属于某个组织的 Docker 成员群组。组织和公司所有者可以将成员分组到额外的团队中，以便按团队配置仓库权限。使用团队对成员进行分组是可选的。
- 成员（Member）：成员是属于某个组织的 Docker 用户。组织和公司所有者可以为成员分配角色以定义其权限。

{{< grid >}}
