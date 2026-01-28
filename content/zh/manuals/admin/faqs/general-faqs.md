---
title: Docker 账户常规 FAQ
linkTitle: 常规
weight: 10
description: 关于 Docker 账户和管理的常见问题
keywords: 入门, docker, 团队, 组织, 用户账户, 组织账户
tags: [FAQ]
aliases:
- /docker-hub/general-faqs/
- /docker-hub/onboarding-faqs/
- /faq/admin/general-faqs/
---

### 什么是 Docker ID？

Docker ID 是您 Docker 账户的用户名，让您可以访问 Docker 产品。要创建 Docker ID，您需要一个电子邮件地址，或者可以使用社交账号或 GitHub 账号进行注册。您的 Docker ID 长度必须在 4 到 30 个字符之间，且只能包含数字和小写字母。不能使用任何特殊字符或空格。

有关更多信息，请参阅 [Docker ID](/accounts/create-account/)。如果您的管理员强制执行 [单点登录 (SSO)](../../security/for-admins/single-sign-on/_index.md)，这将为新用户自动配置 Docker ID。

开发人员可能会拥有多个 Docker ID，以便将与拥有 Docker Business 或 Team 订阅的组织关联的 Docker ID 与其个人使用的 Docker ID 分开。

### 我可以更改我的 Docker ID 吗？

不可以。一旦创建，您就无法更改 Docker ID。如果您需要不同的 Docker ID，则必须使用新的 Docker ID 创建一个新的 Docker 账户。

此外，如果您停用了账户，将来也无法再次使用该 Docker ID。

### 如果我的 Docker ID 被占用了怎么办？

所有的 Docker ID 均遵循先到先得的原则，除非是拥有美国注册商标的公司。如果您拥有该命名空间的商标，[Docker 支持](https://hub.docker.com/support/contact/) 可以为您找回该 Docker ID。

### 什么是组织？

Docker 中的组织是共同管理的一组团队和存储库的集合。一旦 Docker 用户被组织所有者与该组织关联，他们就成为了该组织的成员。[组织所有者](#who-is-an-organization-owner) 是对组织拥有管理访问权限的用户。有关创建组织的更多信息，请参阅 [创建您的组织](orgs.md)。

### 什么是组织名称或命名空间？

组织名称，有时被称为组织命名空间或组织 ID，是 Docker 组织的唯一标识符。组织名称不能与现有的 Docker ID 相同。

### 什么是角色？

角色是授予成员的权限集合。角色定义了在 Docker Hub 中执行操作的访问权限，例如创建存储库、管理标签或查看团队。请参阅 [角色和权限](roles-and-permissions.md)。

### 什么是团队？

团队是属于某个组织的一组 Docker 用户。一个组织可以拥有多个团队。组织所有者可以通过使用 Docker ID 或电子邮件地址并选择用户所属的团队，来创建新团队或将成员添加到现有团队中。请参阅 [创建和管理团队](manage-a-team.md)。

### 什么是公司？

公司是一个管理层，用于集中管理多个组织。管理员可以将拥有 Docker Business 订阅的组织添加到公司，并为公司旗下的所有组织配置设置。请参阅 [设置您的公司](/admin/company/)。

### 谁是组织所有者？

组织所有者是拥有管理存储库、添加成员和管理成员角色权限的管理员。他们可以完全访问私有存储库、所有团队、账单信息和组织设置。组织所有者还可以为组织中的每个团队指定 [存储库权限](manage-a-team.md#configure-repository-permissions-for-a-team)。只有组织所有者才能为组织启用 SSO。当为您的组织启用 SSO 时，组织所有者还可以管理用户。

Docker 可以通过 SSO 强制执行，为新的最终用户或希望拥有单独公司用途 Docker ID 的用户自动配置 Docker ID。

组织所有者还可以添加额外的所有者，以协助管理组织中的用户、团队和存储库。

### 我可以配置多个 SSO 身份提供商 (IdP) 来对单个组织的用户进行身份验证吗？

可以。Docker SSO 支持多种 IdP 配置。有关更多信息，请参阅 [配置 SSO](../../security/for-admins/single-sign-on/configure/_index.md) 和 [SSO FAQ](../../security/faqs/single-sign-on/faqs.md)。

### 什么是服务账号？

> [!IMPORTANT]
>
> 截至 2024 年 12 月 10 日，服务账号已不再提供。现有的服务账号协议将在其当前期限届满前继续履行，但不再提供服务账号的新购买或续订，客户必须根据新的订阅进行续订。建议转型为组织访问令牌 (OAT)，它可以提供类似的功能。有关更多信息，请参阅 [组织访问令牌 (Beta)](/manuals/security/for-admins/access-tokens.md)。

[服务账号](../../docker-hub/service-accounts.md) 是一个用于自动化管理容器镜像或容器化应用程序的 Docker ID。服务账号通常用于自动化工作流中，且不与 Team 或 Business 订阅中的成员共享 Docker ID。服务账号的常见用例包括在 Docker Hub 上镜像内容，或将镜像拉取与您的 CI/CD 流程挂钩。

### 我可以删除或停用其他用户的 Docker 账户吗？

只有拥有该 Docker 账户访问权限的人才能停用该账户。有关更多详情，请参阅 [停用账户](../../admin/organization/deactivate-account.md)。

如果该用户是您组织的成员，您可以将该用户从组织中移除。有关更多详情，请参阅 [移除成员或受邀者](../../admin/organization/members.md#remove-a-member-from-a-team)。

### 如何管理用户账户的设置？

您可以在登录 [Docker 账户](https://app.docker.com/login) 后随时管理您的账户设置。选择右上角导航栏中的头像，然后选择 **My Account**（我的账户）。

登录账户后，您也可以从任何 Docker Web 应用程序访问此菜单。请参阅 [管理您的 Docker 账户](/accounts/manage-account)。如果您的账户与使用 SSO 的组织关联，您对可控制设置的访问权限可能会受到限制。

### 如何为我的 Docker 账户添加头像？

要为您的 Docker 账户添加头像，请创建一个 [Gravatar 账户](https://gravatar.com/) 并创建您的头像。接下来，将您的 Gravatar 电子邮件添加到您的 Docker 账户设置中。

请注意，您的头像在 Docker 中更新可能需要一些时间。
