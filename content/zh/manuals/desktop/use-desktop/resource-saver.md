---
description: 了解什么是 Docker Desktop 资源节约模式以及如何配置它
keywords: Docker Dashboard, resource saver, 资源节约, 管理, 容器, gui, 控制面板, dashboard, 用户手册
title: Docker Desktop 资源节约模式 (Resource Saver mode)
linkTitle: 资源节约模式
weight: 50
---

资源节约模式 (Resource Saver mode) 通过在一段时间内没有容器运行时自动停止 Docker Desktop Linux 虚拟机，可显著降低 Docker Desktop 在宿主机上的 CPU 和内存占用（通常可减少 2 GB 或更多）。默认空闲时间设置为 5 分钟，但您可以根据需要进行调整。

在资源节约模式下，Docker Desktop 在空闲时仅占用极少的系统资源，从而延长笔记本电脑的电池续航并提升多任务处理体验。

## 配置资源节约模式

资源节约模式默认启用，但可以在 **Settings（设置）** 的 **Resources** 选项卡中禁用。您也可以配置空闲计时器，如下图所示。

![资源节约模式设置](../images/resource-saver-settings.png)

如果预设的值无法满足您的需求，您可以通过修改 Docker Desktop 的 `settings-store.json` 文件（或 Docker Desktop 4.34 及更早版本中的 `settings.json`）中的 `autoPauseTimeoutSeconds`，将其重新配置为任何大于 30 秒的值：

  - Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
  - Windows: `C:\Users\[用户名]\AppData\Roaming\Docker\settings-store.json`
  - Linux: `~/.docker/desktop/settings-store.json`

修改后无需重启 Docker Desktop。

当 Docker Desktop 进入资源节约模式时：
- Docker Desktop 状态栏以及系统托盘中的 Docker 图标上会显示一个绿叶图标。下图显示了开启资源节约模式后，Linux 虚拟机的 CPU 和内存占用降至零的情况。

   ![资源节约模式状态栏](../images/resource-saver-status-bar.png)

- 不涉及运行容器的 Docker 命令（例如列出镜像或卷）不一定会触发退出资源节约模式，因为 Docker Desktop 可以在不唤醒 Linux 虚拟机的情况下处理此类命令。

> [!NOTE]
>
> Docker Desktop 会在需要时自动退出资源节约模式。导致退出该模式的命令执行时间会稍长一些（约 3 到 10 秒），因为 Docker Desktop 需要重新启动 Linux 虚拟机。在 Mac 和 Linux 上通常较快，而在 Windows 的 Hyper-V 模式下较慢。一旦 Linux 虚拟机重启，随后的容器运行将像往常一样立即执行。

## 资源节约模式与暂停 (Pause) 的对比

资源节约模式的优先级高于旧版的 [暂停 (Pause)](pause.md) 功能。这意味着当 Docker Desktop 处于资源节约模式时，无法手动暂停 Docker Desktop（也没有必要，因为资源节约模式实际上已经停止了虚拟机）。通常，我们建议保持资源节约模式开启，而不是禁用它并使用手动暂停功能，因为它在节约 CPU 和内存方面的效果要好得多。

## Windows 上的资源节约模式

在 Windows 的 WSL 模式下，资源节约模式的工作方式略有不同。它并不会停止 WSL 虚拟机，而只是暂停 `docker-desktop` 发行版内部的 Docker 引擎。这是因为在 WSL 中，所有发行版共享同一个 Linux 虚拟机，Docker Desktop 无法停止该虚拟机（即 WSL Linux 虚拟机不归 Docker Desktop 所有）。因此，资源节约模式在 WSL 上可以降低 CPU 占用，但不会降低内存占用。

为了降低 WSL 上的内存占用，我们建议用户按照 [Docker Desktop WSL 文档](/manuals/desktop/features/wsl/_index.md) 中的说明，启用 WSL 的 `autoMemoryReclaim` 功能。最后，由于 Docker Desktop 在 WSL 上不会停止虚拟机，因此退出资源节约模式是即时的（没有延迟）。
