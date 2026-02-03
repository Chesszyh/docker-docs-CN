---
description: 了解暂停 Docker Desktop 的含义
keywords: Docker Desktop Dashboard, 管理, 容器, gui, 控制面板, dashboard, 暂停, pause, 用户手册
title: 暂停 Docker Desktop
weight: 60
---

暂停 (Pause) Docker Desktop 会暂时挂起运行 Docker Engine 的 Linux 虚拟机。这将把所有容器的当前状态保存在内存中，并冻结所有正在运行的进程，从而显著降低 CPU 和内存的使用率，有助于节省笔记本电脑的电量。

要暂停 Docker Desktop，请点击 Docker 控制面板（Dashboard）底部左侧的 **Pause** 图标。要手动恢复 Docker Desktop，请在 Docker 菜单中选择 **Resume** 选项，或运行任何 Docker CLI 命令。

当您手动暂停 Docker Desktop 时，Docker 菜单和 Docker Desktop 控制面板上会显示已暂停状态。您仍然可以访问 **Settings（设置）** 和 **Troubleshoot（故障排除）** 菜单。

> [!TIP]
>
> 资源节约 (Resource Saver) 功能默认启用，与手动暂停功能相比，它能提供更好的 CPU 和内存节约效果。更多信息请参阅 [资源节约模式](resource-saver.md)。
