---
title: Docker 账户通用常见问题
linkTitle: 通用
weight: 10
description: Docker 账户和管理常见问题
keywords: onboarding, docker, teams, orgs, user accounts, organization accounts
tags: [FAQ]
aliases:
- /docker-hub/general-faqs/
- /docker-hub/onboarding-faqs/
- /faq/admin/general-faqs/
---

### 什么是 Docker ID？

Docker ID 是您 Docker 账户的用户名，用于访问 Docker 产品。要创建 Docker ID，您需要一个电子邮件地址，或者您可以使用社交账户或 GitHub 账户注册。您的 Docker ID 必须在 4 到 30 个字符之间，只能包含数字和小写字母。您不能使用任何特殊字符或空格。

有关更多信息，请参阅 [Docker ID](/accounts/create-account/)。如果您的管理员启用了[单点登录（SSO）](../../security/for-admins/single-sign-on/_index.md)，这将为新用户自动配置 Docker ID。

开发人员可能拥有多个 Docker ID，以便将与拥有 Docker Business 或 Team 订阅的组织关联的 Docker ID 与个人使用的 Docker ID 分开。

### 我可以更改我的 Docker ID 吗？

不可以。Docker ID 一旦创建就无法更改。如果您需要不同的 Docker ID，您必须使用新的 Docker ID 创建新的 Docker 账户。

此外，如果您停用账户，将来也无法重用该 Docker ID。

### 如果我想要的 Docker ID 已被占用怎么办？

所有 Docker ID 都是先到先得，除非公司在美国拥有该用户名的商标。如果您拥有命名空间的商标，[Docker 支持](https://hub.docker.com/support/contact/)可以为您获取该 Docker ID。

### 什么是组织？

Docker 中的组织（Organization）是一起管理的团队和仓库的集合。一旦 Docker 用户被组织所有者关联到该组织，他们就成为该组织的成员。[组织所有者](#who-is-an-organization-owner)是对组织拥有管理访问权限的用户。有关创建组织的更多信息，请参阅[创建您的组织](orgs.md)。

### 什么是组织名称或命名空间？

组织名称，有时也称为组织命名空间或组织 ID，是 Docker 组织的唯一标识符。组织名称不能与现有的 Docker ID 相同。

### 什么是角色？

角色（Role）是授予成员的权限集合。角色定义了在 Docker Hub 中执行操作的访问权限，例如创建仓库、管理标签或查看团队。请参阅[角色和权限](roles-and-permissions.md)。

### 什么是团队？

团队（Team）是属于组织的一组 Docker 用户。一个组织可以有多个团队。组织所有者可以创建新团队，并使用 Docker ID 或电子邮件地址将成员添加到现有团队，并选择用户应加入的团队。请参阅[创建和管理团队](manage-a-team.md)。

### 什么是公司？

公司（Company）是一个管理层，用于集中管理多个组织。管理员可以将拥有 Docker Business 订阅的组织添加到公司，并为公司下的所有组织配置设置。请参阅[设置您的公司](/admin/company/)。

### 谁是组织所有者？

组织所有者是拥有管理仓库、添加成员和管理成员角色权限的管理员。他们对私有仓库、所有团队、计费信息和组织设置拥有完全访问权限。组织所有者还可以为组织中的每个团队指定[仓库权限](manage-a-team.md#configure-repository-permissions-for-a-team)。只有组织所有者才能为组织启用 SSO。当您的组织启用 SSO 后，组织所有者还可以管理用户。

Docker 可以通过 SSO 强制执行为新终端用户或希望拥有单独公司用 Docker ID 的用户自动配置 Docker ID。

组织所有者还可以添加其他所有者来帮助他们管理组织中的用户、团队和仓库。

### 我可以配置多个 SSO 身份提供商（IdP）来认证用户到单个组织吗？

可以。Docker SSO 支持多个 IdP 配置。有关更多信息，请参阅[配置 SSO](../../security/for-admins/single-sign-on/configure/_index.md) 和 [SSO 常见问题](../../security/faqs/single-sign-on/faqs.md)。

### 什么是服务账户？

> [!IMPORTANT]
>
> 自 2024 年 12 月 10 日起，服务账户不再可用。现有的服务账户协议将在当前期限到期前继续有效，但新购买或续订服务账户已不再可用，客户必须在新订阅下续订。建议过渡到组织访问令牌（OAT，Organization Access Tokens），它可以提供类似的功能。有关更多信息，请参阅[组织访问令牌（Beta）](/manuals/security/for-admins/access-tokens.md)。

[服务账户](../../docker-hub/service-accounts.md)是用于容器镜像或容器化应用程序自动化管理的 Docker ID。服务账户通常用于自动化工作流程，不与 Team 或 Business 订阅中的成员共享 Docker ID。服务账户的常见用例包括在 Docker Hub 上镜像内容，或将镜像拉取与您的 CI/CD 流程关联。

### 我可以为其他用户删除或停用 Docker 账户吗？

只有能够访问 Docker 账户的人才能停用该账户。有关更多详细信息，请参阅[停用账户](../../admin/organization/deactivate-account.md)。

如果用户是您组织的成员，您可以从组织中移除该用户。有关更多详细信息，请参阅[移除成员或受邀者](../../admin/organization/members.md#remove-a-member-from-a-team)。

### 如何管理用户账户的设置？

您可以在登录 [Docker 账户](https://app.docker.com/login)时随时管理账户设置。在右上角导航中选择您的头像，然后选择**我的账户**。

当您登录账户时，您也可以从任何 Docker 网页应用程序访问此菜单。请参阅[管理您的 Docker 账户](/accounts/manage-account)。如果您的账户与使用 SSO 的组织关联，您可能对可控制的设置访问权限有限。

### 如何为我的 Docker 账户添加头像？

要为您的 Docker 账户添加头像，请创建一个 [Gravatar 账户](https://gravatar.com/)并创建您的头像。然后，将您的 Gravatar 电子邮件添加到 Docker 账户设置中。

请注意，您的头像可能需要一些时间才能在 Docker 中更新。
