---
description: 组织常见问题
linkTitle: 组织
weight: 20
keywords: Docker, Docker Hub, SSO FAQs, single sign-on, organizations, administration, Admin Console, members, organization management, manage orgs
title: 组织相关常见问题
tags: [FAQ]
aliases:
- /docker-hub/organization-faqs/
- /faq/admin/organization-faqs/
---

### 如果我想要用于组织或公司的 Docker ID 已被占用怎么办？

所有 Docker ID 都是先到先得，除非公司在美国拥有该用户名的商标。如果您拥有命名空间的商标，[Docker 支持](https://hub.docker.com/support/contact/)可以为您获取该 Docker ID。

### 如何添加组织所有者？

现有所有者可以将其他团队成员添加为组织所有者。您可以在 Docker Hub 或 Docker Admin Console 中[邀请成员](../../admin/organization/members.md#invite-members)并为其分配所有者角色。

### 如何知道我的组织中有多少活跃用户？

如果您的组织使用软件资产管理工具，您可以使用它来查找有多少用户安装了 Docker Desktop。如果您的组织没有使用此类软件，您可以进行内部调查以了解谁在使用 Docker Desktop。请参阅[识别您的 Docker 用户及其 Docker 账户](../../admin/organization/onboard.md#step-1-identify-your-docker-users-and-their-docker-accounts)。使用 Docker Business 订阅，您可以在身份提供商中管理成员，并通过 [SSO](../../security/for-admins/single-sign-on/_index.md) 或 [SCIM](../../security/for-admins/provisioning/scim.md) 自动将他们配置到您的 Docker 组织。

### 用户是否需要先通过 Docker 身份验证，所有者才能将他们添加到组织？

不需要。组织所有者可以使用用户的电子邮件地址邀请用户，并在邀请过程中将他们分配到团队。

### 我可以强制要求组织成员在使用 Docker Desktop 之前进行身份验证吗？这样做有什么好处？

可以。您可以[强制登录](../../security/for-admins/enforce-sign-in/_index.md)。强制登录的一些好处包括：

- 管理员可以强制执行[镜像访问管理](/manuals/security/for-admins/hardened-desktop/image-access-management.md)和[仓库访问管理](../../security/for-admins/hardened-desktop/registry-access-management.md)等功能。
 - 管理员可以通过阻止未以组织成员身份登录的用户使用 Docker Desktop 来确保合规性。

### 如果用户在 Docker Hub 中的用户账户关联的是个人电子邮件，在受邀加入组织之前是否需要转换为使用组织的域？

是的。当您的组织启用 SSO 后，每个用户必须使用公司域登录。但是，用户可以保留其个人凭据，并创建一个与其组织域关联的新 Docker ID。

### 我可以将个人用户账户（Docker ID）转换为组织账户吗？

可以。您可以将用户账户转换为组织账户。一旦将用户账户转换为组织，就无法将其恢复为个人用户账户。有关先决条件和说明，请参阅[将账户转换为组织](convert-account.md)。

### 我们的用户通过自助服务创建 Docker Hub 账户。当达到申请的许可证总用户数时，我们如何知道？是否可以向组织添加超过许可证总数的成员？

当达到申请的许可证总用户数时，没有自动通知。但是，如果团队成员数量超过许可证数量，您将收到错误消息，提示您由于席位不足需要联系管理员。如果需要，您可以[添加席位](../../subscription/manage-seats.md)。

### 如何合并组织账户？

您可以降级次要组织，并将用户和数据转移到主要组织。请参阅[合并组织](../organization/orgs.md#merge-organizations)。

### 组织受邀者会占用席位吗？

会的。被邀请到组织的用户将占用一个已配置的席位，即使该用户尚未接受邀请。组织所有者可以通过 Docker Hub 中组织设置页面的**受邀者**选项卡或 Admin Console 中的**成员**页面管理受邀者列表。

### 组织所有者会占用席位吗？

会的。组织所有者会占用一个席位。

### 用户、受邀者、席位和成员之间有什么区别？

用户（User）是指拥有 Docker ID 的 Docker 用户。

受邀者（Invitee）是管理员已邀请加入组织但尚未接受邀请的用户。

席位（Seat）是组织内计划成员的数量。

成员（Member）可以指已收到并接受加入组织邀请的用户。成员也可以指组织内团队的成员。

### 如果有两个组织，一个用户同时属于两个组织，他们会占用两个席位吗？

会的。在用户属于两个组织的情况下，他们在每个组织中各占用一个席位。

### 是否可以为组织内的仓库设置权限？

可以。您可以按团队配置仓库访问权限。例如，您可以指定组织内的所有团队对仓库 A 和 B 拥有**读写**权限，而只有特定团队拥有**管理员**权限。组织所有者对组织内的所有仓库拥有完全管理访问权限。请参阅[为团队配置仓库权限](manage-a-team.md#configure-repository-permissions-for-a-team)。管理员还可以为成员分配编辑者角色，该角色授予对组织命名空间内仓库的管理权限。请参阅[角色和权限](../../security/for-admins/roles-and-permissions.md)。

### 我的组织需要使用 Docker 的仓库吗？

仓库（Registry）是一个托管服务，包含响应 Registry API 的镜像仓库。Docker Hub 是 Docker 的主要仓库，但您可以将 Docker 与其他容器镜像仓库一起使用。您可以通过浏览 [Docker Hub](https://hub.docker.com) 或使用 `docker search` 命令访问默认仓库。
