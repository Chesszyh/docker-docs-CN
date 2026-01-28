---
description: 了解如何删除镜像标签。
keywords: Docker Hub, Hub, tags, delete
title: 镜像管理
linktitle: 镜像管理
weight: 12
---

{{< summary-bar feature_name="Image management" >}}

镜像和镜像索引是仓库中容器镜像的基础。下图展示了镜像和镜像索引之间的关系。

  ![a pretty wide image](./images/image-index.svg)

这种结构通过单个引用实现多架构支持。需要注意的是，镜像并不总是由镜像索引引用。图中显示了以下对象。

- 镜像索引（Image index）：指向多个特定架构镜像（如 AMD 和 ARM）的镜像，使单个引用可以在不同平台上工作。
- 镜像（Image）：包含特定架构和操作系统的实际配置和层的单个容器镜像。

## 管理仓库镜像和镜像索引

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。
3. 在列表中，选择一个仓库。
4. 选择 **Image Management**。
5. 搜索、筛选或排序项目。
   - 搜索：在列表上方的搜索框中，指定您的搜索内容。
   - 筛选：在 **Filter by** 下拉菜单中，选择 **Tagged**、**Image index** 或 **Image**。
   - 排序：选择 **Size**、**Last pushed** 或 **Last pulled** 列标题。

   > [!NOTE]
   >
   > 超过 6 个月未被拉取的镜像在 **Status** 列中标记为 **Stale**（陈旧）。

6. 可选。删除一个或多个项目。
   1. 选择列表中项目旁边的复选框。选择任何顶级索引也会移除任何未在其他地方引用的底层镜像。
   2. 选择 **Preview and delete**。
   3. 在出现的窗口中，验证将被删除的项目以及您将回收的存储量。
   4. 选择 **Delete forever**。
