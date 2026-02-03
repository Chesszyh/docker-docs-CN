---
description: 了解您可以通过 Docker 控制面板的“卷 (Volumes)”视图进行哪些操作
keywords: Docker Dashboard, 管理, 容器, gui, 控制面板, dashboard, volumes, 卷, 用户手册
title: 探索 Docker Desktop 中的卷 (Volumes) 视图
linkTitle: 卷 (Volumes)
weight: 30
---

Docker Desktop 中的 **卷 (Volumes)** 视图让您可以创建、检查、删除、克隆、清空、导出和导入 [Docker 卷](/manuals/engine/storage/volumes.md)。您还可以浏览卷中的文件和文件夹，并查看哪些容器正在使用它们。

## 查看您的卷

您可以查看有关卷的以下信息：

- **Name**：卷的名称。
- **Status**：卷是否正在被容器使用。
- **Created**：卷创建的时间。
- **Size**：卷的大小。
- **Scheduled exports**：计划导出任务是否处于活动状态。

默认情况下，**Volumes** 视图显示所有卷的列表。

您可以过滤和排序卷，也可以通过以下操作修改显示的列：

- 按名称过滤卷：使用 **Search** 字段。
- 按状态过滤卷：在搜索栏右侧，按 **In use**（在用）或 **Unused**（未用）过滤。
- 排序卷：点击列名对卷进行排序。
- 自定义列：在搜索栏右侧，选择要显示的卷信息。

## 创建一个卷

您可以按照以下步骤创建一个空卷。或者，如果您 [启动一个带有尚未存在的卷的容器](/manuals/engine/storage/volumes.md#使用卷启动容器)，Docker 会自动为您创建该卷。

要创建卷：

1. 在 **Volumes** 视图中，点击 **Create** 按钮。
2. 在 **New Volume** 弹窗中，指定卷名称，然后选择 **Create**。

有关在容器中使用卷的信息，请参阅 [使用卷](/manuals/engine/storage/volumes.md#使用卷启动容器)。

## 检查卷 (Inspect)

要探索特定卷的详情，请从列表中选择一个卷。这将打开详情视图。

**Container in-use** 选项卡显示使用该卷的容器名称、镜像名称、容器使用的端口号以及目标路径。目标路径（Target）是容器内部用于访问卷中文件的路径。

**Stored data** 选项卡显示卷中的文件和文件夹及其大小。要保存文件或文件夹，右键点击该文件或文件夹以显示选项菜单，选择 **Save as...**，然后指定下载位置。

要从卷中删除文件或文件夹，右键点击该文件或文件夹以显示选项菜单，选择 **Delete**，然后再次选择 **Delete** 进行确认。

**Exports** 选项卡让您可以 [导出卷](#导出卷)。

## 克隆卷 (Clone)

克隆卷会创建一个新卷，其中包含被克隆卷所有数据的副本。当克隆正在被一个或多个运行中容器使用的卷时，容器会在 Docker 克隆数据期间暂时停止，并在克隆过程完成后重新启动。

要克隆卷：

1. 登录 Docker Desktop。克隆卷需要处于登录状态。
2. 在 **Volumes** 视图中，点击您想要克隆的卷对应的 **Actions** 列中的 **Clone** 图标。
3. 在 **Clone a volume** 弹窗中，指定 **Volume name**，然后选择 **Clone**。

## 删除一个或多个卷

删除卷会同时删除该卷及其所有数据。当容器正在使用某个卷时，即使容器已停止，您也无法删除该卷。在删除卷之前，必须先停止并移除任何使用该卷的容器。

要删除卷：

1. 在 **Volumes** 视图中，点击您想要删除的卷对应的 **Actions** 列中的 **Delete** 图标。
2. 在 **Delete volume?** 弹窗中，选择 **Delete forever**。

要删除多个卷：

1. 在 **Volumes** 视图中，勾选您想要删除的所有卷旁边的复选框。
2. 选择 **Delete**。
3. 在 **Delete volumes?** 弹窗中，选择 **Delete forever**。

## 清空卷 (Empty)

清空卷会删除卷中的所有数据，但不会删除卷本身。当清空正在被一个或多个运行中容器使用的卷时，容器会在 Docker 清空数据期间暂时停止，并在清空过程完成后重新启动。

要清空卷：

1. 登录 Docker Desktop。清空卷需要处于登录状态。
2. 在 **Volumes** 视图中，选择您想要清空的卷。
3. 在 **Import** 旁边，点击 **More volume actions** 图标，然后选择 **Empty volume**。
4. 在 **Empty a volume?** 弹窗中，选择 **Empty**。

## 导出卷

您可以将卷的内容导出到本地文件、本地镜像、Docker Hub 上的镜像或受支持的云提供商处。当从正在被一个或多个运行中容器使用的卷导出内容时，容器会在 Docker 导出内容期间暂时停止，并在导出完成后重新启动。

您可以选择 [立即导出卷](#立即导出卷) 或 [计划定期导出](#计划导出卷)。

### 立即导出卷

1. 登录 Docker Desktop。导出卷需要处于登录状态。
2. 在 **Volumes** 视图中，选择您想要导出的卷。
3. 选择 **Exports** 选项卡。
4. 选择 **Quick export**。
5. 选择将卷导出到 **Local or Hub storage**（本地或 Hub 存储）还是 **External cloud storage**（外部云存储），然后根据您的选择指定以下附加详细信息。

   {{< tabs >}}
   {{< tab name="本地或 Hub 存储" >}}
   
   - **Local file**：指定文件名并选择文件夹。
   - **Local image**：选择一个本地镜像来导出内容。镜像中的任何现有数据都将被导出的内容替换。
   - **New image**：为新镜像指定一个名称。
   - **Registry**：指定一个 Docker Hub 存储库。

   {{< /tab >}}
   {{< tab name="外部云存储" >}}

   您必须拥有 [Docker Business 订阅](../../subscription/details.md) 才能导出到外部云提供商。

   选择您的云提供商，然后指定上传到存储的 URL。请参考您云提供商的以下文档了解如何获取 URL。

   - Amazon Web Services：[使用 AWS SDK 为 Amazon S3 创建预签名 URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
   - Microsoft Azure：[生成 SAS 令牌和 URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
   - Google Cloud：[创建用于上传对象的签名 URL](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)

   {{< /tab >}}
   {{< /tabs >}}

6. 选择 **Save**。

### 计划导出卷

1. 登录 Docker Desktop。计划导出卷需要处于登录状态并拥有付费的 [Docker 订阅](../../subscription/details.md)。
2. 在 **Volumes** 视图中，选择您想要导出的卷。
3. 选择 **Exports** 选项卡。
4. 选择 **Schedule export**。
5. 在 **Recurrence**（频率）中，选择导出的频率，然后根据您的选择指定以下详细信息。

   - **Daily**（每日）：指定每天进行备份的时间。
   - **Weekly**（每周）：指定每周进行备份的一个或多个日期及时间。
   - **Monthly**（每月）：指定每月进行备份的日期及时间。

6. 选择将卷导出到 **Local or Hub storage** 还是 **External cloud storage**，然后根据您的选择指定相关详细信息。
   
   {{< tabs >}}
   {{< tab name="本地或 Hub 存储" >}}
   
   - **Local file**：指定文件名并选择文件夹。
   - **Local image**：选择一个本地镜像来导出内容。
   - **New image**：指定新镜像名称。
   - **Registry**：指定 Docker Hub 存储库。

   {{< /tab >}}
   {{< tab name="外部云存储" >}}

   （需 Docker Business 订阅）选择云提供商并提供上传 URL（详见上文）。

   {{< /tab >}}
   {{< /tabs >}}

7. 选择 **Save**。

## 导入卷

您可以导入本地文件、本地镜像或来自 Docker Hub 的镜像。卷中的任何现有数据都将被导入的内容替换。当向正在被一个或多个运行中容器使用的卷导入内容时，容器会在 Docker 导入内容期间暂时停止，并在导入完成后重新启动。

要导入卷：

1. 登录 Docker Desktop。导入卷需要处于登录状态。
2. （可选）[创建一个新卷](#创建一个卷) 用于导入内容。
3. 选择您想要导入内容的卷。
4. 选择 **Import**。
5. 选择内容来源，然后根据您的选择指定以下详细信息：

   - **Local file**：选择包含内容的本地文件。
   - **Local image**：选择包含内容的本地镜像。
   - **Registry**：指定 Docker Hub 上包含内容的镜像。

6. 选择 **Import**。

## 额外资源

- [持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data.md)
- [使用卷](/manuals/engine/storage/volumes.md)
