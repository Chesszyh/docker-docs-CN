---
description: 了解暂停 Docker Desktop Dashboard 的含义
keywords: Docker Desktop Dashboard, manage, containers, gui, dashboard, pause, user manual
title: 暂停 Docker Desktop
weight: 60
---

暂停 Docker Desktop 会临时挂起运行 Docker Engine 的 Linux 虚拟机。这会将所有容器的当前状态保存在内存中并冻结所有正在运行的进程，从而显著减少 CPU 和内存使用，这对于节省笔记本电脑的电池电量非常有帮助。

要暂停 Docker Desktop，请选择 Docker Dashboard 底部左侧的 **Pause**（暂停）图标。要手动恢复 Docker Desktop，请在 Docker 菜单中选择 **Resume**（恢复）选项，或运行任何 Docker CLI 命令。

当您手动暂停 Docker Desktop 时，Docker 菜单和 Docker Desktop Dashboard 上会显示暂停状态。您仍然可以访问 **Settings** 和 **Troubleshoot** 菜单。

> [!TIP]
>
> Resource Saver（资源节省）功能默认启用，与手动 Pause（暂停）功能相比，它提供更好的 CPU 和内存节省效果。有关更多信息，请参阅 [Resource Saver 模式](resource-saver.md)。
