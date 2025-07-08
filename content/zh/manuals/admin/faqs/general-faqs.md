---
title: Docker 帐户通用常见问题
linkTitle: 通用
weight: 10
description: 常见 Docker 帐户和管理问题
keywords: 入职, docker, 团队, 组织, 用户帐户, 组织帐户
tags: [FAQ]
aliases:
- /docker-hub/general-faqs/
- /docker-hub/onboarding-faqs/
- /faq/admin/general-faqs/
---

### 什么是 Docker ID？

Docker ID 是您的 Docker 帐户的用户名，可让您访问 Docker 产品。要创建 Docker ID，您需要一个电子邮件地址，或者您可以使用您的社交或 GitHub 帐户注册。您的 Docker ID 必须介于 4 到 30 个字符之间，并且只能包含数字和小写字母。您不能使用任何特殊字符或空格。

有关更多信息，请参阅 [Docker ID](/accounts/create-account/)。如果您的管理员强制执行[单点登录 (SSO)](../../security/for-admins/single-sign-on/_index.md)，这将为新用户配置 Docker ID。

开发人员可以拥有多个 Docker ID，以便将与具有 Docker Business 或 Team 订阅的组织关联的 Docker ID 与其个人使用的 Docker ID 分开。

### 我可以更改我的 Docker ID 吗？

不可以。一旦创建，您就无法更改您的 Docker ID。如果您需要不同的 Docker ID，您必须使用新的 Docker ID 创建一个新的 Docker 帐户。

此外，如果您停用帐户，将来就不能再重复使用 Docker ID。

### 如果我的 Docker ID 被占用怎么办？

所有 Docker ID 都是先到先得，但拥有美国商标的用户除外。如果您拥有命名空间的商标，[Docker 支持](https://hub.docker.com/support/contact/) 可以为您检索 Docker ID。

### 什么是组织？

Docker 中的组织是团队和仓库的集合，它们共同管理。Docker 用户一旦通过组织所有者与该组织关联，就成为该组织的成员。[组织所有者](#who-is-an-organization-owner) 是对组织具有管理访问权限的用户。有关创建组织的更多信息，请参阅[创建您的组织](orgs.md)。

### 什么是组织名称或命名空间？

组织名称，有时称为组织命名空间或组织 ID，是 Docker 组织的唯一标识符。组织名称不能与现有 Docker ID 相同。

### 什么是角色？

角色是授予成员的权限集合。角色定义了在 Docker Hub 中执行操作的访问权限，例如创建仓库、管理标签或查看团队。请参阅[角色和权限](roles-and-permissions.md)。

### 什么是团队？

团队是属于组织的 Docker 用户组。一个组织可以有多个团队。组织所有者可以创建新团队，并使用 Docker ID 或电子邮件地址将成员添加到现有团队，并通过选择用户应属于的团队。请参阅[创建和管理团队](manage-a-team.md)。

### 什么是公司？

公司是集中管理多个组织的管理层。管理员可以将具有 Docker Business 订阅的组织添加到公司，并为公司下的所有组织配置设置。请参阅[设置您的公司](/admin/company/)。

### 谁是组织所有者？

组织所有者是具有管理仓库、添加成员和管理成员角色权限的管理员。他们拥有对私有仓库、所有团队、账单信息和组织设置的完全访问权限。
组织所有者还可以为组织中的每个团队指定[仓库权限](manage-a-team.md#configure-repository-permissions-for-a-team)。只有组织所有者才能为组织启用 SSO。
当为您的组织启用 SSO 时，组织所有者还可以管理用户。

Docker 可以通过 SSO 强制执行为新最终用户或希望拥有单独 Docker ID 以供公司使用的用户自动配置 Docker ID。

组织所有者还可以添加其他所有者，以帮助他们管理组织中的用户、团队和仓库。

### 我可以配置多个 SSO 身份提供商 (IdP) 来认证单个组织的用户吗？

可以。Docker SSO 支持多个 IdP 配置。有关更多信息，请参阅[配置 SSO](../../security/for-admins/single-sign-on/configure/_index.md) 和 [SSO 常见问题](../../security/faqs/single-sign-on/faqs.md)。

### 什么是服务帐户？

> [!IMPORTANT]
>
> 截至 2024 年 12 月 10 日，服务帐户不再可用。现有服务帐户协议将履行至当前期限届满，但不再提供服务帐户的新购买或续订，客户必须在新订阅下续订。建议过渡到组织访问令牌 (OAT)，它可以提供类似的功能。有关更多信息，请参阅[组织访问令牌（Beta 版）](/manuals/security/for-admins/access-tokens.md)。

[服务帐户](../../docker-hub/service-accounts.md) 是用于自动化管理容器镜像或容器化应用程序的 Docker ID。服务帐户通常用于自动化工作流中，并且不与团队或商业订阅中的成员共享 Docker ID。服务帐户的常见用例包括在 Docker Hub 上镜像内容，或将镜像拉取与您的 CI/CD 流程关联。

### 我可以删除或停用其他用户的 Docker 帐户吗？

只有有权访问 Docker 帐户的人才能停用该帐户。有关更多详细信息，请参阅[停用帐户](../../admin/organization/deactivate-account.md)。

如果用户是您组织的成员，您可以将该用户从您的组织中删除。有关更多详细信息，请参阅[从团队中删除成员或受邀者](../../admin/organization/members.md#remove-a-member-from-a-team)。

### 如何管理用户帐户设置？

登录您的 [Docker 帐户](https://app.docker.com/login) 后，您可以随时管理您的帐户设置。选择右上角导航栏中的头像，然后选择**我的帐户**。

登录帐户后，您还可以从任何 Docker Web 应用程序访问此菜单。请参阅[管理您的 Docker 帐户](/accounts/manage-account)。如果您的帐户与使用 SSO 的组织关联，您可能对可以控制的设置具有有限的访问权限。

### 如何为我的 Docker 帐户添加头像？

要为您的 Docker 帐户添加头像，请创建一个 [Gravatar 帐户](https://gravatar.com/) 并创建您的头像。接下来，将您的 Gravatar 电子邮件添加到您的 Docker 帐户设置中。

请注意，您的头像可能需要一些时间才能在 Docker 中更新。