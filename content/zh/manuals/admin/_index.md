---
title: 管理
description: 了解有关帐户、组织和公司管理的指南。
keywords: 管理员, 管理, 公司, 组织, 管理员控制台, 用户帐户, 帐户管理
weight: 10
params:
  sidebar:
    group: 平台
grid:
- title: 公司管理
  description: 了解如何管理公司。
  icon: apartment
  link: /admin/company/
- title: 组织管理
  description: 了解组织管理。
  icon: store
  link: /admin/organization/
- title: 入职您的组织
  description: 了解如何入职和保护您的组织。
  icon: explore
  link: /admin/organization/onboard
- title: 公司常见问题
  description: 发现有关公司的常见问题和答案。
  icon: help
  link: /faq/admin/company-faqs/
- title: 组织常见问题
  description: 探索有关组织的常见问题主题。
  icon: help
  link: /faq/admin/organization-faqs/
- title: 安全
  description: 探索管理员的安全功能。
  icon: shield_locked
  link: /security/
aliases:
- /docker-hub/admin-overview
---

管理员可以使用 Docker 管理控制台管理公司和组织。

[Docker 管理控制台](https://app.docker.com/admin) 为管理员提供对其公司和组织的集中式可观察性、访问管理和控制。为了提供这些功能，Docker 使用以下层次结构和角色。

![Docker 层次结构](./images/docker-admin-structure.webp)

- 公司：公司简化了 Docker 组织和设置的管理。创建公司是可选的，仅适用于 Docker Business 订阅者。
  - 公司所有者：一个公司可以有多个所有者。公司所有者具有公司范围的可观察性，并且可以管理适用于所有关联组织的公司范围设置。此外，公司所有者对所有关联组织具有与组织所有者相同的访问权限。
- 组织：组织是团队和仓库的集合。Docker Team 和 Business 订阅者必须至少有一个组织。
  - 组织所有者：一个组织可以有多个所有者。组织所有者可以观察其组织并管理其用户和设置。
- 团队：团队是属于组织的 Docker 成员组。组织和公司所有者可以将成员分组到其他团队中，以按团队配置仓库权限。使用团队对成员进行分组是可选的。
- 成员：成员是组织的 Docker 用户。组织和公司所有者可以为成员分配角色以定义其权限。

{{< grid >}}