---
description: 了解如何在 Docker Hub 上管理仓库标签。
keywords: Docker Hub, Hub, repository content, tags
title: Docker Hub 上的标签
linkTitle: 标签
weight: 10
---

标签允许您在单个 Docker Hub 仓库中管理多个版本的镜像。通过为每个镜像添加特定的 `:<tag>`，例如 `docs/base:testing`，您可以为各种用例组织和区分镜像版本。如果未指定标签，镜像默认使用 `latest` 标签。

## 为本地镜像打标签

要为本地镜像打标签，请使用以下方法之一：

- 构建镜像时，使用 `docker build -t <org-or-user-namespace>/<repo-name>[:<tag>`。
- 使用 `docker tag <existing-image> <org-or-user-namespace>/<repo-name>[:<tag>]` 为现有本地镜像重新打标签。
- 提交更改时，使用 `docker commit <existing-container> <org-or-user-namespace>/<repo-name>[:<tag>]`。

然后，您可以将此镜像推送到由其名称或标签指定的仓库：

```console
$ docker push <org-or-user-namespace>/<repo-name>:<tag>
```

镜像随后被上传并可在 Docker Hub 中使用。

## 查看仓库标签

您可以查看可用的标签以及相关镜像的大小。

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   将显示您的仓库列表。

3. 选择一个仓库。

   将显示该仓库的 **General** 页面。

4. 选择 **Tags** 标签页。

您可以选择标签的摘要以查看更多详细信息。

## 删除仓库标签

只有仓库所有者或具有授权权限的其他团队成员才能删除标签。

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   将显示您的仓库列表。

3. 选择一个仓库。

   将显示该仓库的 **General** 页面。

4. 选择 **Tags** 标签页。

5. 选择要删除的标签旁边对应的复选框。

6. 选择 **Delete**。

   将出现确认对话框。

7. 选择 **Delete**。
