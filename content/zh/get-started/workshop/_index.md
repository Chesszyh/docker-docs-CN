---
title: Docker 研讨会概述
linkTitle: Docker 研讨会
keywords: docker 基础, 如何启动 docker 容器, 容器设置, 设置
  docker, 如何设置 docker, 设置 docker, docker 容器指南, 如何开始
  使用 docker
description: 在本研讨会中开始学习 Docker 基础知识，您将
  了解容器、镜像以及如何容器化您的第一个应用程序。
aliases:
- /guides/get-started/
- /get-started/hands-on-overview/
- /guides/workshop/
---

这个 45 分钟的研讨会包含有关如何开始使用 Docker 的分步说明。本研讨会向您展示如何：

- 构建并运行一个镜像作为容器。
- 使用 Docker Hub 共享镜像。
- 使用带有数据库的多个容器部署 Docker 应用程序。
- 使用 Docker Compose 运行应用程序。

> [!NOTE]
>
> 有关 Docker 的快速介绍以及容器化应用程序的好处，请参阅[入门](/get-started/introduction/_index.md)。

## 什么是容器？

容器是在主机上运行的沙盒进程，与在该主机上运行的所有其他进程隔离。这种隔离利用了[内核命名空间和 cgroups](https://medium.com/@saschagrunert/demystifying-containers-part-i-kernel-space-2c53d6979504)，
这些功能在 Linux 中已经存在了很长时间。Docker 使这些功能易于使用。总而言之，一个容器：

- 是镜像的可运行实例。您可以使用 Docker API 或 CLI 创建、启动、停止、移动或删除容器。
- 可以在本地计算机、虚拟机上运行，也可以部署到云端。
- 是可移植的（并且可以在任何操作系统上运行）。
- 与其他容器隔离，并运行自己的软件、二进制文件、配置等。

如果您熟悉 `chroot`，那么可以将容器视为 `chroot` 的扩展版本。文件系统来自镜像。但是，容器增加了使用 chroot 时无法获得的额外隔离。

## 什么是镜像？

正在运行的容器使用隔离的文件系统。这个隔离的文件系统由一个镜像提供，该镜像必须包含运行应用程序所需的一切——所有依赖项、配置、脚本、二进制文件等。该镜像还包含容器的其他配置，例如环境变量、要运行的默认命令以及其他元数据。

## 后续步骤

在本节中，您了解了容器和镜像。

接下来，您将容器化一个简单的应用程序，并亲身体验这些概念。

{{< button text="容器化一个应用程序" url="02_our_app.md" >}}
