---
description: 了解即时预配（Just-in-Time provisioning）如何与您的 SSO 连接协同工作。
keywords: 用户预配, 即时预配, JIT, 自动预配, autoprovision, Docker Hub, Docker Admin, 管理, 安全, security
title: 即时预配 (Just-in-Time)
linkTitle: 即时预配
---

{{< summary-bar feature_name="SSO" >}}

即时预配 (Just-in-Time, JIT) 在每次成功的单点登录 (SSO) 身份验证后自动创建和更新用户帐户。JIT 会验证登录的用户是否属于该组织以及身份提供者 (IdP) 分配给他们的团队。当您[创建 SSO 连接](../single-sign-on/_index.md)时，JIT 预配默认处于开启状态。

## 启用 JIT 预配时的 SSO 身份验证

当用户使用 SSO 登录且您的 SSO 配置启用了 JIT 预配时，会自动执行以下步骤：

1. 系统检查是否存在与该用户电子邮件地址关联的 Docker 帐户。

    - 如果帐户已存在：系统使用现有帐户，并在必要时更新用户的全名。
    - 如果帐户不存在：使用基本用户属性（电子邮件、名字和姓氏）创建一个新的 Docker 帐户。系统会根据用户的电子邮件、姓名和随机数字生成一个唯一的用户名，以确保全平台用户名的唯一性。

2. 系统检查是否有待处理的 SSO 组织邀请。

    - 发现邀请：邀请将自动被接受。
    - 邀请包含特定组：用户将被添加到 SSO 组织内的该组中。

3. 系统验证 IdP 在身份验证期间是否共享了组映射。

    - 提供了组映射：用户被分配到相关的组织和团队。
    - 未提供组映射：系统检查用户是否已经是该组织的成员。如果不是，用户将被添加到 SSO 连接中配置的默认组织和团队中。

下图概述了启用 JIT 时的 SSO 身份验证流程：

   ![启用 JIT 预配](../../images/jit-enabled-flow.svg)

## 禁用 JIT 预配时的 SSO 身份验证

当您的 SSO 连接中禁用了 JIT 预配时，身份验证期间会发生以下操作：

1. 系统检查是否存在与该用户电子邮件地址关联的 Docker 帐户。

    - 如果帐户已存在：系统使用现有帐户，并在必要时更新用户的全名。
    - 如果帐户不存在：使用基本用户属性（电子邮件、名字和姓氏）创建一个新的 Docker 帐户。系统会根据用户的电子邮件、姓名和随机数字生成一个唯一的用户名，以确保全平台用户名的唯一性。

2. 系统检查是否有待处理的 SSO 组织邀请。

   - 发现邀请：如果用户是组织成员或有待处理的邀请，登录成功，且邀请自动被接受。
   - 未发现邀请：如果用户不是组织成员且没有待处理的邀请，登录失败，并显示 `Access denied`（访问被拒绝）错误。用户必须联系管理员以获取组织邀请。

在禁用 JIT 的情况下，只有在[启用了 SCIM](/security/for-admins/provisioning/scim/#enable-scim-in-docker) 时组映射才可用。如果未启用 SCIM，用户将不会自动预配到组中。

下图概述了禁用 JIT 时的 SSO 身份验证流程：

![禁用 JIT 预配](../../images/jit-disabled-flow.svg)

## 禁用 JIT 预配

> [!WARNING]
>
> 禁用 JIT 预配可能会中断用户的访问和工作流。禁用 JIT 后，用户将不会被自动添加到您的组织中。用户必须已经是该组织的成员或拥有待处理的邀请，才能通过 SSO 成功登录。要在禁用 JIT 的情况下自动预配用户，请[使用 SCIM](./scim.md)。

您可能出于以下原因想要禁用 JIT 预配：

- 您有多个组织，已启用 SCIM，并希望 SCIM 作为预配的唯一事实来源（Source of Truth）。
- 您希望根据组织的安全配置来控制和限制使用，并希望使用 SCIM 来预配访问权限。

默认情况下，用户是通过 JIT 预配的。如果您启用了 SCIM，则可以禁用 JIT：

1. 在 [Docker Home](https://app.docker.com/) 中，选择您的组织。
2. 选择 **Admin Console（管理控制台）**，然后选择 **SSO and SCIM**。
3. 在 SSO 连接表中，选择 **Action（操作）** 图标，然后选择 **Disable JIT provisioning（禁用 JIT 预配）**。
4. 选择 **Disable（禁用）** 进行确认。
