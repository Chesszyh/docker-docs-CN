---
title: 公司相关常见问题
linkTitle: 公司
weight: 30
description: 公司常见问题
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, company, administration, company management
tags: [FAQ]
aliases:
- /docker-hub/company-faqs/
- /faq/admin/company-faqs/
---

### 创建公司并将组织添加到公司时，现有订阅会受影响吗？

您可以在组织级别管理订阅和相关的计费详情。

### 我的一些组织没有 Docker Business 订阅。我还能使用父公司吗？

可以，但您只能将拥有 Docker Business 订阅的组织添加到公司中。

### 如果我的某个组织从 Docker Business 降级，但我仍然需要以公司所有者身份进行访问，会发生什么？

要访问和管理子组织，该组织必须拥有 Docker Business 订阅。如果组织不包含在此订阅中，组织的所有者必须在公司之外管理该组织。

### 我的组织在迁移过程中需要准备停机时间吗？

不需要，您可以照常进行业务操作。

### 我可以添加多少个公司所有者？

您最多可以为单个公司账户添加 10 个公司所有者。

### 公司所有者会占用订阅席位吗？

公司所有者不会占用席位，除非以下情况之一为真：

- 他们被添加为您公司下某个组织的成员
- SSO 已启用

虽然公司所有者在公司内的所有组织中拥有与组织所有者相同的访问权限，但没有必要将他们添加到任何组织中。这样做会导致他们占用一个席位。

当您首次创建公司时，您的账户既是公司所有者也是组织所有者。在这种情况下，只要您仍然是组织所有者，您的账户就会占用一个席位。

为避免占用席位，请[将另一个用户指派为组织所有者](/manuals/admin/organization/members.md#update-a-member-role)并将您自己从组织中移除。作为公司所有者，您将保留完整的管理访问权限，而无需使用订阅席位。

### 公司所有者在关联/嵌套组织中有哪些权限？

公司所有者可以导航到**组织**页面，在单一位置查看所有嵌套组织。他们还可以查看或编辑组织成员，以及更改单点登录（SSO）和跨域身份管理系统（SCIM，System for Cross-domain Identity Management）设置。对公司设置的更改会影响公司下每个组织中的所有用户。有关更多信息，请参阅[角色和权限](../../security/for-admins/roles-and-permissions.md)。

### 公司级别支持哪些功能？

您可以在公司级别管理域验证、SSO 和 SCIM。以下功能在公司级别不受支持，但您可以在组织级别管理它们：

- 镜像访问管理（Image Access Management）
- 仓库访问管理（Registry Access Management）
- 用户管理
- 计费

要查看和管理公司下所有组织的用户，您可以在使用 [Admin Console](https://app.docker.com/admin) 时[在公司级别管理用户](../../admin/company/users.md)。

公司或公司内的组织不支持域审计功能。

### 创建公司名称有什么要求？

公司名称必须与其子组织的名称不同。如果子组织需要与公司相同的名称，您应该稍作修改。例如，**Docker Inc**（父公司），**Docker**（子组织）。

### 公司所有者如何将组织添加到公司？

您可以在 Admin Console 中将组织添加到公司。有关更多信息，请参阅[将组织添加到公司](../../admin/company/organizations.md#add-organizations-to-a-company.md)。

### 公司所有者如何管理公司的 SSO/SCIM 设置？

请参阅您的 [SCIM](scim.md) 和 [SSO](../../security/for-admins/single-sign-on/configure/_index.md) 设置。

### 公司所有者如何在 IdP 中启用组映射？

有关更多信息，请参阅 [SCIM](scim.md) 和[组映射](../../security/for-admins/provisioning/group-mapping.md)。

### 公司与组织的定义有什么区别？

公司是一起管理的组织集合。组织是一起管理的仓库和团队的集合。
