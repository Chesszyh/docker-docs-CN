---
title: 管理自动构建
description: 如何在 Docker Hub 中管理自动构建
keywords: autobuilds, automated, docker hub, registry
aliases:
- /docker-hub/builds/manage-builds/
---

> [!NOTE]
>
> 自动构建需要 Docker Pro、Team 或 Business 订阅。


## 取消或重试构建

当构建在队列中或正在运行时，**General** 选项卡和 **Builds** 选项卡上的构建报告链接旁边会出现一个 **Cancel** 图标。您也可以在 **Build report** 页面上选择 **Cancel**，或者从 **Timeline** 选项卡的日志显示中取消构建。

![显示取消图标的构建列表](images/build-cancelicon.png)

## 检查活跃构建

仓库的构建摘要会同时显示在仓库的 **General** 选项卡和 **Builds** 选项卡中。**Builds** 选项卡还会显示一个颜色编码的构建队列时间和持续时间条形图。两个视图都显示仓库任何标签的待处理、进行中、成功和失败的构建。

![活跃构建](images/index-active.png)

从任一位置，您可以选择一个构建任务来查看其构建报告。构建报告显示有关构建任务的信息。这包括源仓库和分支或标签、构建日志、构建持续时间、创建时间和位置，以及构建发生的用户账户。

> [!NOTE]
>
> 现在，当您刷新 **Builds** 页面时，每 30 秒可以查看构建进度。通过进行中的构建日志，您可以在构建完成之前调试构建问题。

![构建报告](./images/index-report.png)

## 禁用自动构建

自动构建是按分支或标签启用的，可以禁用和重新启用。例如，当您正在对代码进行重大重构时，您可能想暂时只进行手动构建。禁用自动构建不会禁用[自动测试](automated-testing.md)。

要禁用自动构建：

1. 在 [Docker Hub](https://hub.docker.com) 中，转到 **My Hub** > **Repositories**，选择一个仓库，然后选择 **Builds** 选项卡。

2. 选择 **Configure automated builds** 来编辑仓库的构建设置。

3. 在 **Build Rules** 部分，找到您不再想要自动构建的分支或标签。

4. 选择配置行旁边的 **Autobuild** 开关。禁用时，开关显示为灰色。

5. 选择 **Save**。
