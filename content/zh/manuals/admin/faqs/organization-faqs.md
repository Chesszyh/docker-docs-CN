---
description: 组织常见问题 (FAQ)
linkTitle: 组织
weight: 20
keywords: Docker, Docker Hub, SSO FAQ, 单点登录, 组织, 管理, 管理控制台, 成员, 组织管理, 管理组织
title: 组织常见问题 (FAQ)
tags: [FAQ]
aliases:
- /docker-hub/organization-faqs/
- /faq/admin/organization-faqs/
---

### 如果我想要用于组织或公司的 Docker ID 被占用了怎么办？

所有的 Docker ID 均遵循先到先得的原则，除非是拥有美国注册商标的公司。如果您拥有该命名空间的商标，[Docker 支持](https://hub.docker.com/support/contact/) 可以为您找回该 Docker ID。

### 如何添加组织所有者？

现有的所有者可以将其他团队成员添加为组织所有者。您可以 [邀请成员](../../admin/organization/members.md#invite-members) 并在 Docker Hub 或 Docker 管理控制台中为他们分配所有者角色。

### 我如何知道我的组织中有多少活跃用户？

如果您的组织使用软件资产管理工具，您可以使用它来查找有多少用户安装了 Docker Desktop。如果您的组织不使用此类软件，您可以进行内部调查以了解谁在使用 Docker Desktop。请参阅 [识别您的 Docker 用户及其 Docker 账户](../../admin/organization/onboard.md#step-1-identify-your-docker-users-and-their-docker-accounts)。拥有 Docker Business 订阅后，您可以在身份提供商中管理成员，并通过 [SSO](../../security/for-admins/single-sign-on/_index.md) 或 [SCIM](../../security/for-admins/provisioning/scim.md) 将他们自动配置到您的 Docker 组织。

### 在所有者将用户添加到组织之前，用户是否需要先通过 Docker 身份验证？

不需要。组织所有者可以使用用户的电子邮件地址邀请他们，并在邀请过程中将他们分配到团队。

### 我可以强制我的组织成员在访问 Docker Desktop 之前进行身份验证吗？这样做有什么好处？

可以。您可以 [强制登录](../../security/for-admins/enforce-sign-in/_index.md)。强制登录的一些好处包括：

- 管理员可以强制执行 [镜像访问管理](/manuals/security/for-admins/hardened-desktop/image-access-management.md) 和 [镜像库访问管理](../../security/for-admins/hardened-desktop/registry-access-management.md) 等功能。
- 管理员可以通过阻止未作为组织成员登录的用户使用 Docker Desktop 来确保合规性。

### 如果用户的个人电子邮件与 Docker Hub 中的用户账户关联，他们在受邀加入组织之前是否必须转换为使用组织的域名？

是的。当为您的组织启用 SSO 时，每位用户必须使用公司的域名登录。但是，用户可以保留其个人凭据，并创建一个与其组织域名关联的新 Docker ID。

### 我可以将我的个人用户账户（Docker ID）转换为组织账户吗？

可以。您可以将用户账户转换为组织账户。一旦将用户账户转换为组织，就无法再将其恢复为个人用户账户。有关前提条件和说明，请参阅 [将账户转换为组织](convert-account.md)。

### 我们的用户通过自助服务创建 Docker Hub 账户。我们如何知道所申请许可证的用户总数何时已达到上限？是否可以向组织添加超过许可证总数的成员？

当所申请许可证的用户总数达到上限时，没有任何自动通知。但是，如果团队成员人数超过许可证数量，您将收到一条错误提示，告知您由于缺少席位请联系管理员。如果需要，您可以 [添加席位](../../subscription/manage-seats.md)。

### 我该如何合并组织账户？

您可以降级次要组织，并将用户和数据迁移到主要组织。请参阅 [合并组织](../organization/orgs.md#merge-organizations)。

### 组织受邀者是否占用席位？

是的。受邀加入组织的开发人员将占用一个已配置的席位，即使该用户尚未接受邀请。组织所有者可以通过 Docker Hub 中组织设置页面的 **Invitees**（受邀者）选项卡，或者通过管理控制台中的 **Members**（成员）页面来管理受邀者名单。

### 组织所有者是否占用席位？

是的。组织所有者会占用一个席位。

### 用户 (User)、受邀者 (Invitee)、席位 (Seat) 和成员 (Member) 之间的区别是什么？

用户指的是拥有 Docker ID 的 Docker 用户。

受邀者是管理员已邀请加入组织但尚未接受邀请的用户。

席位是组织内计划的成员数量。

成员可以指代收到并接受邀请加入组织的用户。成员也可以指代组织内某个团队的成员。

### 如果有两个组织，且一个用户同时属于这两个组织，他们是否占用两个席位？

是的。在用户属于两个组织的情况下，他们在每个组织中各占用一个席位。

### 是否可以为组织内的存储库设置权限？

可以。您可以按团队配置存储库访问权限。例如，您可以指定组织内的所有团队对存储库 A 和 B 具有 **Read and Write**（读写）访问权限，而只有特定团队具有 **Admin**（管理）访问权限。组织所有者对组织内的所有存储库具有完全的管理访问权限。请参阅 [为团队配置存储库权限](manage-a-team.md#configure-repository-permissions-for-a-team)。管理员还可以为成员分配编辑者角色，该角色授予对组织命名空间下所有存储库的管理权限。请参阅 [角色和权限](../../security/for-admins/roles-and-permissions.md)。

### 我的组织是否需要使用 Docker 的镜像库？

镜像库（Registry）是一个托管服务，包含镜像存储库并响应 Registry API。Docker Hub 是 Docker 的主要镜像库，但您可以将 Docker 与其他容器镜像库配合使用。您可以通过访问 [Docker Hub](https://hub.docker.com) 或使用 `docker search` 命令来访问默认镜像库。
