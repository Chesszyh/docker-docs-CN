---
title: 停用帐户
weight: 30
description: 了解如何停用 Docker 用户帐户。
keywords: Docker Hub, 删除, 停用, 帐户, 帐户管理
---

您可以随时停用帐户。本节介绍停用用户帐户的先决条件和步骤。有关停用组织的信息，请参阅[停用组织](../admin/organization/deactivate-account.md)。

>[!WARNING]
>
> 停用帐户后，所有使用您的 Docker 帐户的 Docker 产品和服务都将无法访问。

## 先决条件

在停用您的 Docker 帐户之前，请确保您满足以下要求：

- 对于所有者，您必须在停用 Docker 帐户之前离开您的组织或公司。
    为此：
    1. 登录 [Docker 主页](https://app.docker.com/admin) 并选择您的组织。
    1. 选择**成员**并找到您的用户名。
    1. 选择**操作**菜单，然后选择**离开组织**。

- 如果您是组织的唯一所有者，您必须将所有者角色分配给组织的另一个成员，然后将自己从组织中删除，或者停用组织。同样，如果您是公司的唯一所有者，要么添加其他人作为公司所有者，然后将自己删除，要么停用公司。

- 如果您有有效的 Docker 订阅，请[将其降级为 Docker 个人订阅](../subscription/change.md)。

- 下载您要保留的任何镜像和标签。使用 `docker pull -a <image>:<tag>`。

- 取消链接您的 [GitHub 和 Bitbucket 帐户](../docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account)。

## 停用

完成所有前面的步骤后，您可以停用您的帐户。

> [!WARNING]
>
> 此操作无法撤消。在停用帐户之前，请确保您已从帐户中收集了所有需要的数据。

1. 登录 [Docker 主页](https://app.docker.com/login)。
1. 选择您的头像以打开下拉菜单。
1. 选择**帐户设置**。
1. 选择**停用**。
1. 选择**停用帐户**。
1. 确认，选择**停用帐户**。