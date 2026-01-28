---
title: 停用账户
weight: 30
description: 了解如何停用 Docker 用户账户。
keywords: Docker Hub, delete, deactivate, account, account management
---

您可以随时停用账户。本节描述了停用用户账户的前提条件和步骤。有关停用组织的信息，请参阅[停用组织](../admin/organization/deactivate-account.md)。

>[!WARNING]
>
> 停用账户后，使用您 Docker 账户的所有 Docker 产品和服务都将无法访问。

## 前提条件

在停用您的 Docker 账户之前，请确保满足以下要求：

- 对于所有者，您必须在停用 Docker 账户之前离开您的组织或公司。
    操作步骤：
    1. 登录 [Docker Home](https://app.docker.com/admin) 并选择您的组织。
    1. 选择 **Members** 并找到您的用户名。
    1. 选择 **Actions** 菜单，然后选择 **Leave organization**。

- 如果您是组织的唯一所有者，您必须将所有者角色分配给组织的另一名成员，然后将自己从组织中移除，或者停用该组织。同样，如果您是公司的唯一所有者，要么添加其他人作为公司所有者然后移除自己，要么停用该公司。

- 如果您有活跃的 Docker 订阅，请[将其降级为 Docker Personal 订阅](../subscription/change.md)。

- 下载您想要保留的任何镜像和标签。使用 `docker pull -a <image>:<tag>`。

- 取消关联您的 [GitHub 和 Bitbucket 账户](../docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account)。

## 停用

完成上述所有步骤后，您可以停用您的账户。

> [!WARNING]
>
> 此操作无法撤销。在停用账户之前，请确保您已从账户中收集了所有需要的数据。

1. 登录 [Docker Home](https://app.docker.com/login)。
1. 选择您的头像以打开下拉菜单。
1. 选择 **Account settings**。
1. 选择 **Deactivate**。
1. 选择 **Deactivate account**。
1. 确认时，选择 **Deactivate account**。
