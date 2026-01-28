---
description: 了解在 Docker Dashboard 上使用 Images 视图可以执行的操作
keywords: Docker Dashboard, manage, containers, gui, dashboard, images, user manual
title: 探索 Docker Desktop 中的 Images 视图
linkTitle: Images
weight: 20
---


**Images**（镜像）视图显示您的 Docker 镜像列表，并允许您将镜像作为容器运行、从 Docker Hub 拉取镜像的最新版本以及检查镜像。它还显示镜像漏洞摘要。此外，**Images** 视图包含清理选项，可从磁盘中删除不需要的镜像以回收空间。如果您已登录，还可以查看您和您的组织在 Docker Hub 上共享的镜像。有关更多信息，请参阅[探索您的镜像](images.md)。

**Images** 视图允许您无需使用 CLI 即可管理 Docker 镜像。默认情况下，它显示本地磁盘上所有 Docker 镜像的列表。

登录 Docker Hub 后，您还可以查看 Hub 镜像。这允许您与团队协作，并直接通过 Docker Desktop 管理您的镜像。

**Images** 视图允许您执行核心操作，例如将镜像作为容器运行、从 Docker Hub 拉取镜像的最新版本、将镜像推送到 Docker Hub 以及检查镜像。

它还显示有关镜像的元数据，例如：
- 标签
- 镜像 ID
- 创建日期
- 镜像大小

正在运行和已停止容器使用的镜像旁边会显示 **In Use**（使用中）标签。您可以通过选择搜索栏右侧的 **More options**（更多选项）菜单，然后根据您的偏好使用切换开关来选择要显示的信息。

**Images on disk**（磁盘上的镜像）状态栏显示镜像数量、镜像使用的总磁盘空间以及此信息的最后刷新时间。

## 管理您的镜像

使用 **Search** 字段搜索任何特定镜像。

您可以按以下方式排序镜像：

- In use（使用中）
- Unused（未使用）
- Dangling（悬空）

## 将镜像作为容器运行

从 **Images** 视图，将鼠标悬停在镜像上并选择 **Run**（运行）。

出现提示时，您可以：

- 选择 **Optional settings**（可选设置）下拉菜单来指定名称、端口、卷、环境变量，然后选择 **Run**
- 选择 **Run** 而不指定任何可选设置。

## 检查镜像

要检查镜像，请选择镜像行。检查镜像会显示有关镜像的详细信息，例如：

- 镜像历史
- 镜像 ID
- 镜像创建日期
- 镜像大小
- 组成镜像的层
- 使用的基础镜像
- 发现的漏洞
- 镜像内的包

[Docker Scout](/manuals/scout/_index.md) 提供此漏洞信息。有关此视图的更多信息，请参阅[镜像详情视图](/manuals/scout/explore/image-details-view.md)

## 从 Docker Hub 拉取最新镜像

从列表中选择镜像，选择 **More options** 按钮，然后选择 **Pull**（拉取）。

> [!NOTE]
>
> 仓库必须存在于 Docker Hub 上才能拉取镜像的最新版本。您必须登录才能拉取私有镜像。

## 将镜像推送到 Docker Hub

从列表中选择镜像，选择 **More options** 按钮，然后选择 **Push to Hub**（推送到 Hub）。

> [!NOTE]
>
> 您只能将属于您的 Docker ID 或您的组织的镜像推送到 Docker Hub。也就是说，镜像的标签中必须包含正确的用户名/组织名才能将其推送到 Docker Hub。

## 删除镜像

> [!NOTE]
>
> 要删除正在运行或已停止容器使用的镜像，您必须先删除关联的容器。

未使用的镜像是指未被任何正在运行或已停止的容器使用的镜像。当您使用相同标签构建镜像的新版本时，镜像会变成悬空状态。

要删除单个镜像，请选择垃圾桶图标。

## Docker Hub 仓库

**Images** 视图还允许您管理和与 Docker Hub 仓库中的镜像进行交互。默认情况下，当您在 Docker Desktop 中进入 **Images** 时，您会看到本地镜像存储中存在的镜像列表。顶部附近的 **Local**（本地）和 **Docker Hub repositories**（Docker Hub 仓库）选项卡可在查看本地镜像存储中的镜像和您有权访问的远程 Docker Hub 仓库中的镜像之间切换。

切换到 **Docker Hub repositories** 选项卡会提示您登录 Docker Hub 账户（如果您尚未登录）。登录后，它会显示您有权访问的 Docker Hub 组织和仓库中的镜像列表。

从下拉菜单中选择一个组织以查看该组织的仓库列表。

如果您在仓库上启用了 [Docker Scout](../../scout/_index.md)，镜像分析结果（如果您的 Docker 组织符合条件，还有[健康评分](/manuals/scout/policy/scores.md)）会显示在镜像标签旁边。

将鼠标悬停在镜像标签上会显示两个选项：

- **Pull**（拉取）：从 Docker Hub 拉取镜像的最新版本。
- **View in Hub**（在 Hub 中查看）：打开 Docker Hub 页面并显示有关镜像的详细信息。

## 其他资源

- [什么是镜像？](/get-started/docker-concepts/the-basics/what-is-an-image.md)
