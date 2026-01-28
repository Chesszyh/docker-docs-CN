---
title: 管理
description: 发现关于账户、组织和公司管理的指南。
keywords: 管理, 行政, 公司, 组织, 管理控制台, 用户账户, 账户管理
weight: 10
params:
  sidebar:
    group: 平台
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
  description: 了解如何引导并保护您的组织。
  icon: explore
  link: /admin/organization/onboard
- title: 公司 FAQ
  description: 发现关于公司的常见问题及解答。
  icon: help
  link: /faq/admin/company-faqs/
- title: 组织 FAQ
  description: 探索关于组织的常见问题。
  icon: help
  link: /faq/admin/organization-faqs/
- title: 安全
  description: 探索面向管理员的安全功能。
  icon: shield_locked
  link: /security/
aliases:
- /docker-hub/admin-overview
---

管理员可以使用 Docker 管理控制台管理公司和组织。

[Docker 管理控制台](https://app.docker.com/admin) 为管理员提供了对其公司和组织的集中可观测性、访问管理和控制。为了提供这些功能，Docker 使用了以下层级结构和角色。

![Docker 层级结构](./images/docker-admin-structure.webp)

- 公司（Company）：公司简化了对 Docker 组织和设置的管理。创建公司是可选的，且仅对 Docker Business 订阅者可用。
  - 公司所有者（Company owner）：一个公司可以有多个所有者。公司所有者具有全公司的可观测性，并可以管理适用于所有关联组织的全公司设置。此外，公司所有者对所有关联组织具有与组织所有者相同的访问权限。
- 组织（Organization）：组织是团队和存储库的集合。Docker Team 和 Business 订阅者必须至少拥有一个组织。
  - 组织所有者（Organization owner）：一个组织可以有多个所有者。组织所有者对其实施可观测性，并可以管理其用户和设置。
- 团队（Team）：团队是属于某个组织的一组 Docker 成员。组织和公司所有者可以将成员分为额外的团队，以便按团队配置存储库权限。使用团队对成员进行分组是可选的。
- 成员（Member）：成员是身为组织成员的 Docker 用户。组织和公司所有者可以向成员分配角色，以定义其权限。

{{< grid >}}
