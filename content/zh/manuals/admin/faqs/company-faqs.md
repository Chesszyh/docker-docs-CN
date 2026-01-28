---
title: 公司常见问题 (FAQ)
linkTitle: 公司
weight: 30
description: 公司 FAQ
keywords: Docker, Docker Hub, SSO FAQ, 单点登录, 公司, 管理, 公司管理
tags: [FAQ]
aliases:
- /docker-hub/company-faqs/
- /faq/admin/company-faqs/
---

### 创建公司并添加组织后，现有的订阅是否会受到影响？

您可以在组织级别管理订阅和相关的账单详情。

### 我的一些组织没有 Docker Business 订阅。我还能使用母公司吗？

可以，但您只能将具有 Docker Business 订阅的组织添加到公司。

### 如果我的一个组织从 Docker Business 降级，但我仍需要作为公司所有者进行访问，会发生什么？

要访问和管理子组织，该组织必须拥有 Docker Business 订阅。如果该组织未包含在次订阅中，则组织所有者必须在公司之外管理该组织。

### 我的组织在迁移过程中需要准备停机吗？

不需要，您可以照常开展业务。

### 我可以添加多少个公司所有者？

一个公司账户最多可以添加 10 个公司所有者。

### 公司所有者是否占用订阅席位？

公司所有者不占用席位，除非满足以下条件之一：

- 他们被添加为您公司旗下某个组织的成员
- 启用了 SSO

虽然公司所有者在公司内的所有组织中具有与组织所有者相同的访问权限，但没有必要将他们添加到任何组织中。这样做会导致他们占用席位。

当您第一次创建公司时，您的账户既是公司所有者又是组织所有者。在这种情况下，只要您仍然是组织所有者，您的账户就会占用一个席位。

为了避免占用席位，请 [指定另一名用户为组织所有者](/manuals/admin/organization/members.md#update-a-member-role) 并将您自己从组织中移除。作为公司所有者，您将保留完整的管理访问权限，且不占用订阅席位。

### 公司所有者在关联/嵌套组织中拥有哪些权限？

公司所有者可以导航到 **Organizations**（组织）页面，在同一个位置查看其所有嵌套组织。他们还可以查看或编辑组织成员，并更改单点登录 (SSO) 和跨域身份管理系统 (SCIM) 设置。对公司设置的更改会影响公司下属各组织中的所有用户。有关更多信息，请参阅 [角色和权限](../../security/for-admins/roles-and-permissions.md)。

### 公司层级支持哪些功能？

您可以在公司层级管理域名验证、SSO 和 SCIM。公司层级不支持以下功能，但您可以在组织层级管理它们：

- 镜像访问管理
- 镜像库访问管理
- 用户管理
- 账单

要查看和管理您公司旗下所有组织的用户，当您使用 [管理控制台](https://app.docker.com/admin) 时，可以 [在公司层级管理用户](../../admin/company/users.md)。

公司或公司内的组织不支持域名审计。

### 创建公司名称有什么要求？

公司名称必须与子组织的名称唯一。如果子组织需要与公司相同的名称，您应该稍微修改一下。例如，**Docker Inc**（母公司），**Docker**（子组织）。

### 公司所有者如何将组织添加到公司？

您可以在管理控制台中将组织添加到公司。有关更多信息，请参阅 [将组织添加到公司](../../admin/company/organizations.md#add-organizations-to-a-company.md)。

### 公司所有者如何管理公司的 SSO/SCIM 设置？

参阅您的 [SCIM](scim.md) 和 [SSO](../../security/for-admins/single-sign-on/configure/_index.md) 设置。

### 公司所有者如何在 IdP 中启用组映射？

有关更多信息，请参阅 [SCIM](scim.md) 和 [组映射](../../security/for-admins/provisioning/group-mapping.md)。

### 公司与组织的定义区别是什么？

公司是共同管理的一组组织的集合。组织是共同管理的一组存储库和团队的集合。
