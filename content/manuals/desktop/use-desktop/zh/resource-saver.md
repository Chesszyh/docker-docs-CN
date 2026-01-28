---
description: 了解 Docker Desktop Resource Saver 模式是什么以及如何配置它
keywords: Docker Dashboard, resource saver, manage, containers, gui, dashboard, user manual
title: Docker Desktop 的 Resource Saver 模式
linkTitle: Resource Saver 模式
weight: 50
---

Resource Saver（资源节省）模式通过在一段时间内没有容器运行时自动停止 Docker Desktop Linux 虚拟机，可显著减少 Docker Desktop 在主机上的 CPU 和内存利用率 2 GB 或更多。默认时间设置为 5 分钟，但可以根据您的需要进行调整。

使用 Resource Saver 模式，Docker Desktop 在空闲时使用最少的系统资源，从而允许您节省笔记本电脑的电池寿命并改善多任务处理体验。

## 配置 Resource Saver

Resource Saver 默认启用，但可以通过导航到 **Settings** 中的 **Resources**（资源）选项卡来禁用。您还可以如下所示配置空闲计时器。

![Resource Saver 设置](../images/resource-saver-settings.png)

如果可用的值不能满足您的需求，您可以将其重新配置为任何值，只要该值大于 30 秒，方法是更改 Docker Desktop `settings-store.json` 文件（或 Docker Desktop 4.34 及更早版本的 `settings.json`）中的 `autoPauseTimeoutSeconds`：

  - Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
  - Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
  - Linux: `~/.docker/desktop/settings-store.json`

重新配置后无需重启 Docker Desktop。

当 Docker Desktop 进入 Resource Saver 模式时：
- Docker Desktop 状态栏以及系统托盘中的 Docker 图标上会显示一个叶子图标。下图显示了当 Resource Saver 模式开启时，Linux 虚拟机的 CPU 和内存利用率降至零。

   ![Resource Saver 状态栏](../images/resource-saver-status-bar.png)

- 不运行容器的 Docker 命令，例如列出容器镜像或卷，不一定会触发退出 Resource Saver 模式，因为 Docker Desktop 可以在不必要唤醒 Linux 虚拟机的情况下处理此类命令。

> [!NOTE]
>
> Docker Desktop 会在需要时自动退出 Resource Saver 模式。导致退出 Resource Saver 的命令执行时间会稍长（大约 3 到 10 秒），因为 Docker Desktop 需要重启 Linux 虚拟机。在 Mac 和 Linux 上通常更快，在使用 Hyper-V 的 Windows 上较慢。一旦 Linux 虚拟机重启，后续的容器运行会像往常一样立即执行。

## Resource Saver 模式与 Pause 的对比

Resource Saver 的优先级高于较旧的 [Pause（暂停）](pause.md)功能，这意味着当 Docker Desktop 处于 Resource Saver 模式时，无法手动暂停 Docker Desktop（这样做也没有意义，因为 Resource Saver 实际上会停止 Docker Desktop Linux 虚拟机）。通常，我们建议保持 Resource Saver 启用，而不是禁用它并使用手动 Pause 功能，因为这样可以获得更好的 CPU 和内存节省效果。

## Windows 上的 Resource Saver 模式

Resource Saver 在使用 WSL 的 Windows 上工作方式略有不同。它不会停止 WSL 虚拟机，而只会暂停 `docker-desktop` WSL 发行版内的 Docker Engine。这是因为在 WSL 中，所有 WSL 发行版共享一个 Linux 虚拟机，所以 Docker Desktop 无法停止 Linux 虚拟机（即 WSL Linux 虚拟机不属于 Docker Desktop）。因此，Resource Saver 可以减少 WSL 上的 CPU 利用率，但不会减少 Docker 的内存利用率。

要减少 WSL 上的内存利用率，我们建议用户按照 [Docker Desktop WSL 文档](/manuals/desktop/features/wsl/_index.md)中描述的方式启用 WSL 的 `autoMemoryReclaim` 功能。最后，由于 Docker Desktop 不会在 WSL 上停止 Linux 虚拟机，从 Resource Saver 模式退出是即时的（没有退出延迟）。
