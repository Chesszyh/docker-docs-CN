---
description: 了解您可以通过 Docker 控制面板的“镜像 (Images)”视图进行哪些操作
keywords: Docker Dashboard, 管理, 容器, gui, 控制面板, dashboard, images, 镜像, 用户手册
title: 探索 Docker Desktop 中的镜像 (Images) 视图
linkTitle: 镜像 (Images)
weight: 20
---


**镜像 (Images)** 视图显示了您的 Docker 镜像列表，并允许您将镜像作为容器运行、从 Docker Hub 拉取镜像的最新版本以及检查镜像详情。它还会显示镜像漏洞的摘要。此外，**Images** 视图还包含清理选项，用于从磁盘中删除不需要的镜像以回收空间。如果您已登录，还可以看到您及您的组织在 Docker Hub 上分享的镜像。有关更多信息，请参阅 [探索您的镜像](images.md)。

**Images** 视图让您无需使用 CLI 即可管理 Docker 镜像。默认情况下，它会显示本地磁盘上所有 Docker 镜像的列表。

登录 Docker Hub 后，您还可以查看 Hub 镜像。这使您能够直接通过 Docker Desktop 与团队协作并管理您的镜像。

**Images** 视图允许您执行核心操作，如将镜像作为容器运行、从 Docker Hub 拉取最新版本的镜像、将镜像推送到 Docker Hub 以及检查镜像。

它还会显示镜像的元数据，例如：
- 标签 (Tag)
- 镜像 ID (Image ID)
- 创建日期
- 镜像大小

在运行中或已停止的容器所使用的镜像旁边会显示 **In Use** 标签。您可以通过选择搜索栏右侧的 **More options** 菜单，然后根据您的偏好使用切换开关来选择要显示的信息。

**Images on disk** 状态栏显示了镜像的数量、镜像占用的总磁盘空间以及该信息的最后刷新时间。

## 管理您的镜像

使用 **Search** 字段搜索特定的镜像。

您可以按以下类别对镜像进行排序：

- 在用 (In use)
- 未用 (Unused)
- 悬空 (Dangling)

## 将镜像作为容器运行

在 **Images** 视图中，将鼠标悬停在镜像上并选择 **Run**。

系统提示时，您可以：

- 选择 **Optional settings** 下拉菜单来指定名称、端口、卷、环境变量，然后选择 **Run**。
- 或者直接选择 **Run** 而不指定任何可选设置。

## 检查镜像 (Inspect)

要检查镜像，请选择镜像行。检查镜像会显示有关镜像的详细信息，例如：

- 镜像历史记录
- 镜像 ID
- 镜像创建日期
- 镜像大小
- 构成镜像的层 (Layers)
- 使用的基础镜像
- 发现的漏洞
- 镜像内部的软件包

[Docker Scout](/manuals/scout/_index.md) 为这些漏洞信息提供支持。有关此视图的更多信息，请参阅 [镜像详情视图](/manuals/scout/explore/image-details-view.md)。

## 从 Docker Hub 拉取最新镜像

从列表中选择镜像，点击 **More options** 按钮并选择 **Pull**。

> [!NOTE]
>
> 只有当存储库存在于 Docker Hub 上时，才能拉取镜像的最新版本。拉取私有镜像必须处于登录状态。

## 将镜像推送到 Docker Hub

从列表中选择镜像，点击 **More options** 按钮并选择 **Push to Hub**。

> [!NOTE]
>
> 只有当镜像属于您的 Docker ID 或您的组织时，您才能将其推送到 Docker Hub。也就是说，镜像的标签中必须包含正确的用户名/组织名才能推送到 Docker Hub。

## 移除镜像

> [!NOTE]
>
> 要移除运行中或已停止的容器正在使用的镜像，必须先移除关联的容器。

“未用镜像 (Unused image)”是指未被任何运行中或已停止的容器使用的镜像。当您构建了带有相同标签的新版本镜像时，旧版本镜像会变为“悬空镜像 (Dangling image)”。

要移除单个镜像，请点击垃圾桶图标。

## Docker Hub 存储库

**Images** 视图还允许您管理 Docker Hub 存储库中的镜像并与之交互。
默认情况下，当您进入 Docker Desktop 的 **Images** 界面时，看到的是本地镜像库中的镜像列表。
顶部的 **Local** 和 **Docker Hub repositories** 选项卡可在查看本地镜像库和查看您有权访问的远程 Docker Hub 存储库镜像之间切换。

切换到 **Docker Hub repositories** 选项卡时，如果您尚未登录，系统会提示您登录 Docker Hub 帐户。登录后，它会显示您有权访问的 Docker Hub 组织和存储库中的镜像列表。

从下拉菜单中选择一个组织以查看该组织的存储库列表。

如果您在存储库上启用了 [Docker Scout](../../scout/_index.md)，镜像标签旁边会显示镜像分析结果（如果您的 Docker 组织符合条件，还会显示 [健康评分](/manuals/scout/policy/scores.md)）。

将鼠标悬停在镜像标签上会显示两个选项：

- **Pull**：从 Docker Hub 拉取该镜像的最新版本。
- **View in Hub**：打开 Docker Hub 页面并显示有关该镜像的详细信息。

## 额外资源

- [什么是镜像？](/get-started/docker-concepts/the-basics/what-is-an-image.md)
