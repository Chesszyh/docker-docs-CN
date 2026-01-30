---
description: 了解如何在守护进程不可用时保持容器运行
keywords: docker, upgrade, daemon, dockerd, live-restore, daemonless container, 升级, 实时恢复, 无守护进程容器
title: 实时恢复 (Live restore)
weight: 40
aliases:
  - /config/containers/live-restore/
  - /engine/admin/live-restore/
  - /engine/containers/live-restore/
---

默认情况下，当 Docker 守护进程终止时，它会关闭正在运行的容器。您可以配置守护进程，使其在守护进程不可用时容器仍保持运行。此功能称为 *实时恢复 (live restore)*。实时恢复选项有助于减少由于守护进程崩溃、计划内停机或升级而导致的容器停机时间。

> [!NOTE]
>
> 实时恢复不支持 Windows 容器，但它适用于在 Docker Desktop for Windows 上运行的 Linux 容器。

## 启用实时恢复

有两种方式可以启用实时恢复设置，以便在守护进程不可用时保持容器存活。**请仅执行以下操作之一**。

- 将配置添加到守护进程配置文件中。在 Linux 上，默认路径为 `/etc/docker/daemon.json`。在 Docker Desktop for Mac 或 Docker Desktop for Windows 上，从任务栏中选择 Docker 图标，然后点击 **Settings** -> **Docker Engine**。

  - 使用以下 JSON 启用 `live-restore`。

    ```json
    {
      "live-restore": true
    }
    ```

  - 重启 Docker 守护进程。在 Linux 上，您可以通过重新加载 Docker 守护进程来避免重启 (并避免容器停机)。如果您使用 `systemd`，请使用命令 `systemctl reload docker`。否则，向 `dockerd` 进程发送 `SIGHUP` 信号。

- 如果您愿意，也可以手动启动带有 `--live-restore` 标志的 `dockerd` 进程。不推荐这种方法，因为它没有设置 `systemd` 或其他进程管理器在启动 Docker 进程时会使用的环境。这可能会导致意外行为。

## 升级期间的实时恢复

实时恢复允许您在 Docker 守护进程更新期间保持容器运行，但仅在安装补丁版本 (`YY.MM.x`) 时受支持，不支持大版本 (`YY.MM`) 的守护进程升级。

如果您在升级期间跨越了版本，守护进程可能无法恢复其与容器的连接。如果守护进程无法恢复连接，它将无法管理正在运行的容器，您必须手动停止它们。

## 重启后的实时恢复

实时恢复选项仅在守护进程选项 (如网桥 IP 地址和图形驱动程序) 未更改的情况下才能恢复容器。如果这些守护进程级配置选项中的任何一个发生了变化，实时恢复可能无法工作，您可能需要手动停止容器。

## 实时恢复对运行中容器的影响

如果守护进程停机时间过长，正在运行的容器可能会填满守护进程通常读取的 FIFO 日志。日志填满后会阻止容器记录更多数据。默认缓冲区大小为 64K。如果缓冲区填满，您必须重启 Docker 守护进程以清空它们。

在 Linux 上，您可以通过更改 `/proc/sys/fs/pipe-max-size` 来修改内核的缓冲区大小。在 Docker Desktop for Mac 或 Docker Desktop for Windows 上无法修改缓冲区大小。

## 实时恢复与 Swarm 模式

实时恢复选项仅适用于独立容器，不适用于 Swarm 服务。Swarm 服务由 Swarm 管理节点 (managers) 管理。如果 Swarm 管理节点不可用，Swarm 服务会继续在工作节点上运行，但无法进行管理，直到有足够的 Swarm 管理节点可用以维持法定人数 (quorum)。
