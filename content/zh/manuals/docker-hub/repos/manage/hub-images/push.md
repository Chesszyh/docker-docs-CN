---
description: 了解如何向 Docker Hub 上的仓库添加内容。
keywords: Docker Hub, Hub, repository content, push
title: 推送镜像到仓库
linkTitle: 推送镜像
weight: 30
---

要向 Docker Hub 上的仓库添加内容，您需要为 Docker 镜像打标签，然后将其推送到您的仓库。此过程使您可以与他人共享您的镜像或在不同环境中使用它们。

1. 为您的 Docker 镜像打标签。

   `docker tag` 命令为您的 Docker 镜像分配一个标签，其中包括您的 Docker Hub 命名空间和仓库名称。一般语法是：

   ```console
   $ docker tag [SOURCE_IMAGE[:TAG]] [NAMESPACE/REPOSITORY[:TAG]]
   ```

   示例：

   如果您的本地镜像名为 `my-app`，并且您想使用标签 `v1.0` 将其标记为仓库 `my-namespace/my-repo`，请运行：

   ```console
   $ docker tag my-app my-namespace/my-repo:v1.0
   ```

2. 将镜像推送到 Docker Hub。

   使用 `docker push` 命令将您打好标签的镜像上传到 Docker Hub 上指定的仓库。

   示例：

   ```console
   $ docker push my-namespace/my-repo:v1.0
   ```

   此命令将标记为 `v1.0` 的镜像推送到 `my-namespace/my-repo` 仓库。

3. 在 Docker Hub 上验证镜像。
