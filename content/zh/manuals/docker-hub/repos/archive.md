---
description: 了解如何在 Docker Hub 上归档或取消归档仓库
keywords: Docker Hub, Hub, repositories, archive, unarchive
title: 归档或取消归档仓库
linkTitle: 归档
toc_max: 3
weight: 35
---

您可以在 Docker Hub 上归档仓库，将其标记为只读并表明它不再被积极维护。这有助于防止在工作流程中使用过时或不受支持的镜像。如果需要，已归档的仓库也可以取消归档。

Docker Hub 会在[**仓库**页面](https://hub.docker.com/repositories/)上通过显示图标（{{< inline-image src="./images/outdated-icon.webp"
alt="outdated icon" >}}）来突出显示超过一年未更新的仓库。请考虑检查这些突出显示的仓库，并在必要时将它们归档。

当仓库被归档时，会发生以下情况：

- 无法修改仓库信息。
- 无法向仓库推送新镜像。
- 公共仓库页面上会显示 **Archived**（已归档）标签。
- 用户仍然可以拉取镜像。

您可以取消归档已归档的仓库以移除归档状态。取消归档后，会发生以下情况：

- 可以修改仓库信息。
- 可以向仓库推送新镜像。
- 公共仓库页面上的 **Archived** 标签被移除。

## 归档仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   您的仓库列表会出现。

3. 选择一个仓库。

   仓库的 **General** 页面会出现。

4. 选择 **Settings** 标签。
5. 选择 **Archive repository**。
6. 输入您的仓库名称以确认。
7. 选择 **Archive**。

## 取消归档仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   您的仓库列表会出现。

3. 选择一个仓库。

   仓库的 **General** 页面会出现。

4. 选择 **Settings** 标签。
5. 选择 **Unarchive repository**。
