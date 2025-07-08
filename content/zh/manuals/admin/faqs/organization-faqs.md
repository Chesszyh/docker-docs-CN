---
description: 组织常见问题
linkTitle: 组织
weight: 20
keywords: Docker, Docker Hub, SSO 常见问题, 单点登录, 组织, 管理, 管理员控制台, 成员, 组织管理, 管理组织
title: 组织常见问题
tags: [FAQ]
aliases:
- /docker-hub/organization-faqs/
- /faq/admin/organization-faqs/
---

### 如果我想要的组织或公司 Docker ID 被占用怎么办？

所有 Docker ID 都是先到先得，但拥有美国商标的用户除外。如果您拥有命名空间的商标，[Docker 支持](https://hub.docker.com/support/contact/) 可以为您检索 Docker ID。

### 如何添加组织所有者？

现有所有者可以将其他团队成员添加为组织所有者。您可以通过 [邀请成员](../../admin/organization/members.md#invite-members) 并在 Docker Hub 或 Docker 管理控制台中为他们分配所有者角色。

### 我如何知道我的组织中有多少活跃用户？

如果您的组织使用软件资产管理工具，您可以使用它来查找有多少用户安装了 Docker Desktop。如果您的组织不使用此软件，您可以进行内部调查以找出谁在使用 Docker Desktop。请参阅[识别您的 Docker 用户及其 Docker 帐户](../../admin/organization/onboard.md#step-1-identify-your-docker-users-and-their-docker-accounts)。通过 Docker Business 订阅，您可以在身份提供商中管理成员，并通过 [SSO](../../security/for-admins/single-sign-on/_index.md) 或 [SCIM](../../security/for-admins/provisioning/scim.md) 自动将其配置到您的 Docker 组织。

### 用户是否需要先通过 Docker 认证，然后所有者才能将他们添加到组织中？

不需要。组织所有者可以使用他们的电子邮件地址邀请用户，并在邀请过程中将他们分配给团队。

### 我可以强制我的组织成员在使用 Docker Desktop 之前进行认证吗？这样做有什么好处？

可以。您可以[强制登录](../../security/for-admins/enforce-sign-in/_index.md)。强制登录的一些好处是：

- 管理员可以强制执行诸如 [镜像访问管理](/manuals/security/for-admins/hardened-desktop/image-access-management.md) 和 [注册表访问管理](../../security/for-admins/hardened-desktop/registry-access-management.md) 等功能。
 - 管理员可以通过阻止未登录为组织成员的用户使用 Docker Desktop 来确保合规性。

### 如果用户将其个人电子邮件与 Docker Hub 中的用户帐户关联，他们是否必须先转换为使用组织的域，然后才能被邀请加入组织？

是的。当为您的组织启用 SSO 时，每个用户都必须使用公司的域登录。但是，用户可以保留其个人凭据并创建与组织域关联的新 Docker ID。

### 我可以将我的个人用户帐户 (Docker ID) 转换为组织帐户吗？

可以。您可以将您的用户帐户转换为组织帐户。一旦您将用户帐户转换为组织，就无法将其恢复为个人用户帐户。有关先决条件和说明，请参阅[将帐户转换为组织](convert-account.md)。

### 我们的用户通过自助服务创建 Docker Hub 帐户。我们如何知道何时已达到所请求许可证的用户总数？是否可以向组织添加比许可证总数更多的成员？

当达到所请求许可证的用户总数时，不会有任何自动通知。但是，如果团队成员数量超过许可证数量，您将收到一条错误消息，通知您由于席位不足而联系管理员。如果需要，您可以[添加席位](../../subscription/manage-seats.md)。

### 如何合并组织帐户？

您可以降级辅助组织，并将您的用户和数据转移到主组织。请参阅[合并组织](../organization/orgs.md#merge-organizations)。

### 组织受邀者是否占用席位？

是的。被邀请加入组织的用户将占用一个已配置的席位，即使该用户尚未接受邀请。组织所有者可以通过 Docker Hub 中的**邀请者**选项卡或管理控制台中的**成员**页面管理受邀者列表。

### 组织所有者是否占用席位？

是的。组织所有者将占用一个席位。

### 用户、受邀者、席位和成员之间有什么区别？

用户是指拥有 Docker ID 的 Docker 用户。

受邀者是指管理员已邀请加入组织但尚未接受邀请的用户。

席位是组织中计划的成员数量。

成员可以指已收到并接受邀请加入组织的用户。成员也可以指组织内团队的成员。

### 如果有两个组织，并且一个用户同时属于这两个组织，他们会占用两个席位吗？

是的。在用户属于两个组织的情况下，他们将在每个组织中占用一个席位。

### 是否可以设置组织内仓库的权限？

是的。您可以按团队配置仓库访问权限。例如，您可以指定组织内的所有团队对仓库 A 和 B 具有**读写**访问权限，而只有特定团队具有**管理员**访问权限。组织所有者对组织内的所有仓库具有完全管理访问权限。请参阅[为团队配置仓库权限](manage-a-team.md#configure-repository-permissions-for-a-team)。管理员还可以为成员分配编辑者角色，该角色授予对组织命名空间中仓库的管理权限。请参阅[角色和权限](../../security/for-admins/roles-and-permissions.md)。

### 我的组织需要使用 Docker 的注册表吗？

注册表是包含镜像仓库并响应注册表 API 的托管服务。Docker Hub 是 Docker 的主要注册表，但您可以将 Docker 与其他容器镜像注册表一起使用。您可以通过浏览 [Docker Hub](https://hub.docker.com) 或使用 `docker search` 命令访问默认注册表。