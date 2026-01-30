---
title: 组织访问令牌 (OAT)
description: 了解如何创建和管理组织访问令牌，以便通过编程方式安全地推送和拉取镜像。
keywords: docker hub, security, OAT, organization access token, 组织访问令牌
linkTitle: 组织访问令牌
---

{{< summary-bar feature_name="OATs" >}}

> [!WARNING]
>
> 组织访问令牌 (OAT) 与 Docker Desktop、[镜像访问管理 (IAM)](/manuals/security/for-admins/hardened-desktop/image-access-management.md) 以及 [注册表访问管理 (RAM)](/manuals/security/for-admins/hardened-desktop/registry-access-management.md) 不兼容。
>
> 如果您使用 Docker Desktop、IAM 或 RAM，则必须改用个人访问令牌 (PAT)。

组织访问令牌 (OAT) 类似于 [个人访问令牌 (PAT)](/security/for-developers/access-tokens/)，但 OAT 与组织相关联，而不是与单个用户帐户相关联。使用 OAT 代替 PAT 可以让业务关键型任务访问 Docker Hub 仓库，而无需将令牌连接到单个用户。您必须拥有 [Docker Team 或 Business 订阅](/subscription/core-subscription/details/) 才能使用 OAT。

OAT 提供以下优势：

- 您可以调查 OAT 的最后使用时间，如果发现任何可疑活动，可以禁用或删除它。
- 您可以限制每个 OAT 的访问权限，从而在 OAT 泄露时限制影响。
- 所有公司或组织所有者都可以管理 OAT。如果一个所有者离开组织，其余所有者仍可以管理 OAT。
- OAT 拥有自己的 Docker Hub 使用限制，不会计入您的个人帐户限制。

如果您已拥有 [服务帐户 (service accounts)](/docker-hub/service-accounts/)，Docker 建议您使用 OAT 替换这些服务帐户。与服务帐户相比，OAT 具有以下优势：

- 使用 OAT 更容易管理访问权限。您可以直接为 OAT 分配访问权限，而服务帐户需要通过团队 (teams) 来分配权限。
- OAT 更容易管理。OAT 在管理控制台中进行集中管理。对于服务帐户，您可能需要登录该服务帐户才能进行管理。如果强制执行单点登录 (SSO) 且服务帐户不在您的 IdP 中，您可能无法登录该服务帐户进行管理。
- OAT 不与单个用户关联。如果拥有服务帐户访问权限的用户离开了您的组织，您可能会失去对该服务帐户的访问权限。OAT 可由任何公司或组织所有者管理。

## 创建组织访问令牌

> [!IMPORTANT]
>
> 请像对待密码一样对待访问令牌并保持其私密。例如，将您的令牌安全地存储在凭据管理器中。

公司或组织所有者最多可以创建：
- 拥有 Team 订阅的组织可创建 10 个 OAT
- 拥有 Business 订阅的组织可创建 100 个 OAT

已过期的令牌也会计入令牌总数。

创建 OAT 的步骤：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Admin Console** (管理控制台)，然后选择 **Access tokens** (访问令牌)。
3. 选择 **Generate access token** (生成访问令牌)。
4. 为您的令牌添加标签和可选描述。使用能够指示令牌用途或目的的内容。
5. 选择令牌的过期日期。
6. 展开 **Repository** (仓库) 下拉菜单，为您的令牌设置访问权限范围。设置仓库访问范围：
    1. (可选) 选择 **Read public repositories** (读取公共仓库)。
    2. 选择 **Add repository** (添加仓库) 并从下拉菜单中选择一个仓库。
    3. 为您的仓库设置范围 &mdash; **Image Push** (推送镜像) 或 **Image Pull** (拉取镜像)。
    4. 根据需要添加更多仓库。您最多可以添加 50 个仓库。
7. (可选) 展开 **Organization** (组织) 下拉菜单并勾选 **Allow management access to this organization's resources** (允许对该组织资源的管理访问) 复选框。此设置将为您的令牌启用组织管理范围。提供以下组织管理范围：
    - **Member Edit**: 编辑组织成员
    - **Member Read**: 读取组织成员
    - **Invite Edit**: 邀请成员加入组织
    - **Invite Read**: 读取对组织的邀请
    - **Group Edit**: 编辑组织的分组
    - **Group Read**: 读取组织的分组
8. 选择 **Generate token** (生成令牌)。复制屏幕上显示的令牌并妥善保存。一旦退出该屏幕，您将无法再次找回该令牌。

## 使用组织访问令牌

当您使用 Docker CLI 登录时，可以使用组织访问令牌。

在您的 Docker CLI 客户端中使用以下命令登录，将 `YOUR_ORG` 替换为您的组织名称：

```console
$ docker login --username <YOUR_ORG>
```

当提示输入密码时，输入您的组织访问令牌而不是密码。

## 修改现有令牌

您可以根据需要重命名、更新描述、更新仓库访问权限、停用或删除令牌。

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Admin Console**，然后选择 **Access tokens**。
3. 选择令牌行中的操作菜单，然后选择 **Deactivate** (停用)、**Edit** (编辑) 或 **Delete** (删除) 来修改令牌。对于 **Inactive** (非活跃) 令牌，您只能选择 **Delete**。
4. 如果编辑令牌，在指定修改后选择 **Save** (保存)。
