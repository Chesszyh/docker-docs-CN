---
title: 停用账户
weight: 30
description: 了解如何停用 Docker 用户账户。
keywords: Docker Hub, 删除, 停用, 账户, 账户管理
---

您可以随时停用账户。本节介绍了停用用户账户的前提条件和步骤。有关停用组织的信息，请参阅 [停用组织](../admin/organization/deactivate-account.md)。

>[!WARNING]
>
> 停用账户后，所有使用您 Docker 账户的 Docker 产品和服务都将无法访问。

## 前提条件

在停用您的 Docker 账户之前，请确保您满足以下要求：

- 对于所有者，您必须在停用 Docker 账户之前退出您的组织或公司。
    步骤如下：
    1. 登录 [Docker Home](https://app.docker.com/admin) 并选择您的组织。
    2. 选择 **Members**（成员）并找到您的用户名。
    3. 选择 **Actions**（操作）菜单，然后选择 **Leave organization**（退出组织）。

- 如果您是组织的唯一所有者，您必须将所有者角色分配给组织的其他成员，然后将自己从组织中移除，或者停用该组织。同样，如果您是公司的唯一所有者，要么添加其他人作为公司所有者然后移除自己，要么停用该公司。

- 如果您有活跃的 Docker 订阅，请将其 [降级为 Docker Personal 订阅](../subscription/change.md)。

- 下载任何您想保留的镜像和标签。使用 `docker pull -a <image>:<tag>`。

- 取消关联您的 [GitHub 和 Bitbucket 账户](../docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account)。

## 停用

完成上述所有步骤后，您可以停用账户。

> [!WARNING]
>
> 此操作不可撤销。请务必在停用账户之前收集好您需要的所有数据。

1. 登录 [Docker Home](https://app.docker.com/login)。
2. 选择您的头像以打开下拉菜单。
3. 选择 **Account settings**（账户设置）。
4. 选择 **Deactivate**（停用）。
5. 选择 **Deactivate account**（停用账户）。
6. 选择 **Deactivate account**（停用账户）进行确认。
