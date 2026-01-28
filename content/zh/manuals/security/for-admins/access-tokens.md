---
title: 组织访问令牌
description: 了解如何创建和管理组织访问令牌（Organization Access Token），
  以便安全地通过程序化方式推送和拉取镜像。
keywords: docker hub, security, OAT, organization access token
linkTitle: 组织访问令牌
---

{{< summary-bar feature_name="OATs" >}}

> [!WARNING]
>
> 组织访问令牌（OAT）与 Docker Desktop、
> [镜像访问管理（IAM）](/manuals/security/for-admins/hardened-desktop/image-access-management.md)和[注册表访问管理（RAM）](/manuals/security/for-admins/hardened-desktop/registry-access-management.md)不兼容。
>
> 如果您使用 Docker Desktop、IAM 或 RAM，则必须使用个人访问令牌（Personal Access Token）。

组织访问令牌（OAT）类似于[个人访问令牌（PAT）](/security/for-developers/access-tokens/)，但 OAT 与组织关联，而不是与单个用户账户关联。使用 OAT 而非 PAT 可以让业务关键任务访问 Docker Hub 仓库，而无需将令牌绑定到单个用户。您必须拥有 [Docker Team 或 Business 订阅](/subscription/core-subscription/details/)才能使用 OAT。

OAT 具有以下优势：

- 您可以调查 OAT 的最后使用时间，如果发现任何可疑活动，可以禁用或删除它。
- 您可以限制每个 OAT 的访问权限，从而在 OAT 被泄露时降低影响。
- 所有公司或组织所有者都可以管理 OAT。如果某个所有者离开组织，其余所有者仍然可以管理这些 OAT。
- OAT 拥有独立的 Docker Hub 使用配额，不会计入您个人账户的配额。

如果您有现有的[服务账户](/docker-hub/service-accounts/)，Docker 建议您使用 OAT 替换服务账户。与服务账户相比，OAT 具有以下优势：

- 使用 OAT 更容易管理访问权限。您可以直接为 OAT 分配访问权限，而服务账户需要通过团队来管理访问权限。
- OAT 更易于管理。OAT 在管理控制台（Admin Console）中集中管理。对于服务账户，您可能需要登录该服务账户才能进行管理。如果使用单点登录（SSO）强制执行且服务账户不在您的 IdP 中，您可能无法登录服务账户进行管理。
- OAT 不与单个用户关联。如果有权访问服务账户的用户离开您的组织，您可能会失去对服务账户的访问权限。OAT 可以由任何公司或组织所有者管理。

## 创建组织访问令牌

> [!IMPORTANT]
>
> 请像对待密码一样保护访问令牌的安全。例如，将令牌安全地存储在凭据管理器中。

公司或组织所有者最多可以创建：
- Team 订阅的组织最多 10 个 OAT
- Business 订阅的组织最多 100 个 OAT

已过期的令牌也计入令牌总数。

创建 OAT 的步骤：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **Access tokens**。
1. 选择 **Generate access token**。
1. 为令牌添加标签和可选描述。使用能够表明令牌用途或目的的内容。
1. 选择令牌的过期日期。
1. 展开 **Repository** 下拉菜单以设置令牌的仓库访问权限范围。要设置仓库访问范围：
    1. 可选。选择 **Read public repositories**。
    1. 选择 **Add repository** 并从下拉菜单中选择一个仓库。
    1. 为仓库设置权限范围 &mdash; **Image Push** 或 **Image Pull**。
    1. 根据需要添加更多仓库。最多可以添加 50 个仓库。
1. 可选。展开 **Organization** 下拉菜单并选中 **Allow management access to this organization's resources** 复选框。此设置为令牌启用组织管理权限范围。以下组织管理权限范围可用：
    - **Member Edit**：编辑组织成员
    - **Member Read**：读取组织成员信息
    - **Invite Edit**：邀请成员加入组织
    - **Invite Read**：读取组织邀请信息
    - **Group Edit**：编辑组织群组
    - **Group Read**：读取组织群组信息
1. 选择 **Generate token**。复制屏幕上显示的令牌并保存。退出此页面后，您将无法再次获取该令牌。

## 使用组织访问令牌

您可以在使用 Docker CLI 登录时使用组织访问令牌。

使用以下命令从 Docker CLI 客户端登录，将 `YOUR_ORG` 替换为您的组织名称：

```console
$ docker login --username <YOUR_ORG>
```

当提示输入密码时，输入您的组织访问令牌而不是密码。

## 修改现有令牌

您可以根据需要重命名令牌、更新描述、更新仓库访问权限、停用或删除令牌。

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **Access tokens**。
1. 在令牌行中选择操作菜单，然后选择 **Deactivate**、**Edit** 或 **Delete** 来修改令牌。对于 **Inactive** 状态的令牌，您只能选择 **Delete**。
1. 如果编辑令牌，在指定修改内容后选择 **Save**。
