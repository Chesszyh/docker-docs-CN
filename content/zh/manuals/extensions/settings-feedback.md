---
description: 扩展
keywords: Docker Extensions, Docker Desktop, Linux, Mac, Windows, feedback
title: Docker 扩展的设置和反馈
linkTitle: 设置和反馈
weight: 40
aliases:
 - /desktop/extensions/settings-feedback/
---

## 设置

### 开启或关闭扩展

Docker 扩展默认是开启的。要更改设置：

1. 导航到 **Settings**。
2. 选择 **Extensions** 选项卡。
3. 在 **Enable Docker Extensions** 旁边，选中或清除复选框以设置所需状态。
4. 在右下角，选择 **Apply**。

> [!NOTE]
>
> 如果您是[组织所有者](/manuals/admin/organization/manage-a-team.md#organization-owner)，您可以为用户关闭扩展。打开 `settings-store.json` 文件，将 `"extensionsEnabled"` 设置为 `false`。
> `settings-store.json` 文件（或 Docker Desktop 4.34 及更早版本的 `settings.json`）位于：
>   - Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
>   - Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
>
> 这也可以通过[加固的 Docker Desktop](/manuals/security/for-admins/hardened-desktop/_index.md) 来完成

### 开启或关闭市场中没有的扩展

您可以通过市场或扩展 SDK 工具安装扩展。您可以选择只允许已发布的扩展。这些是已经过审核并发布在扩展市场中的扩展。

1. 导航到 **Settings**。
2. 选择 **Extensions** 选项卡。
3. 在 **Allow only extensions distributed through the Docker Marketplace** 旁边，选中或清除复选框以设置所需状态。
4. 在右下角，选择 **Apply**。

### 查看扩展创建的容器

默认情况下，扩展创建的容器在 Docker Desktop 仪表板和 Docker CLI 的容器列表中是隐藏的。要使它们可见，请更新您的设置：

1. 导航到 **Settings**。
2. 选择 **Extensions** 选项卡。
3. 在 **Show Docker Extensions system containers** 旁边，选中或清除复选框以设置所需状态。
4. 在右下角，选择 **Apply**。

> [!NOTE]
>
> 启用扩展本身不会使用计算机资源（CPU / 内存）。
>
> 特定扩展可能会使用计算机资源，这取决于每个扩展的功能和实现，但启用扩展本身没有预留资源或使用成本。

## 提交反馈

可以通过专用的 Slack 频道或 GitHub 向扩展作者提供反馈。要提交关于特定扩展的反馈：

1. 导航到 Docker Desktop 仪表板并选择 **Manage** 选项卡。
   这会显示您已安装的扩展列表。
2. 选择您想要提供反馈的扩展。
3. 滚动到扩展描述的底部，根据扩展的不同，选择：
    - Support
    - Slack
    - Issues。您将被转到 Docker Desktop 外部的页面提交反馈。

如果扩展没有提供反馈方式，请联系我们，我们会为您转达反馈。要提供反馈，请选择 **Extensions Marketplace** 右侧的 **Give feedback**。
