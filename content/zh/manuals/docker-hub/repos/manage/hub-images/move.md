---
description: 了解如何在仓库之间移动镜像。
keywords: Docker Hub, Hub, repository content, move
title: 在仓库之间移动镜像
linkTitle: 移动镜像
weight: 40
---

整合和组织跨仓库的 Docker 镜像可以简化您的工作流程，无论您是管理个人项目还是为组织做贡献。本主题介绍了如何在 Docker Hub 仓库之间移动镜像，确保您的内容在正确的账户或命名空间下保持可访问和有序。

## 个人账户到个人账户

在整合个人仓库时，您可以从初始仓库拉取私有镜像，并将它们推送到您拥有的另一个仓库。为避免丢失私有镜像，请执行以下步骤：

1. 使用个人订阅[注册](https://app.docker.com/signup)一个新的 Docker 账户。
2. 使用您的原始 Docker 账户登录 [Docker](https://app.docker.com/login)。
3. 拉取您的镜像：

   ```console
   $ docker pull namespace1/docker101tutorial
   ```

4. 使用新创建的 Docker 用户名为您的私有镜像打标签，例如：

   ```console
   $ docker tag namespace1/docker101tutorial new_namespace/docker101tutorial
   ```
5. 使用 CLI 的 `docker login` 命令，使用新创建的 Docker 账户登录，并将新打标签的私有镜像推送到您的新 Docker 账户命名空间：

   ```console
   $ docker push new_namespace/docker101tutorial
   ```

之前存在于您原账户中的私有镜像现在可以在您的新账户中使用了。

## 个人账户到组织

为避免丢失私有镜像，您可以从个人账户拉取私有镜像，并将它们推送到您拥有的组织。

1. 导航到 [Docker Hub](https://hub.docker.com) 并选择 **My Hub**。
2. 选择适用的组织，并验证您的用户账户是该组织的成员。
3. 使用您的原始 Docker 账户登录 [Docker Hub](https://hub.docker.com)，并拉取您的镜像：

   ```console
   $ docker pull namespace1/docker101tutorial
   ```
4. 使用新的组织命名空间为您的镜像打标签：

   ```console
   $ docker tag namespace1/docker101tutorial <new_org>/docker101tutorial
   ```
5. 将新打标签的镜像推送到您的新组织命名空间：

   ```console
   $ docker push new_org/docker101tutorial
   ```

之前存在于您用户账户中的私有镜像现在可供您的组织使用了。
