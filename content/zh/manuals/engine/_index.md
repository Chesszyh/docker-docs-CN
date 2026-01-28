---
title: Docker Engine
weight: 10
description: Find a comprehensive overview of Docker Engine, including how to install, storage details, networking, and more
keywords: Engine
params:
  sidebar:
    group: Open source
grid:
- title: Install Docker Engine
  description: Learn how to install the open source Docker Engine for your distribution.
  icon: download
  link: /engine/install
- title: Storage
  description: Use persistent data with Docker containers.
  icon: database
  link: /storage
- title: Networking
  description: Manage network connections between containers.
  icon: network_node
  link: /network
- title: Container logs
  description: Learn how to view and read container logs.
  icon: text_snippet
  link: /config/containers/logging/
- title: Prune
  description: Tidy up unused resources.
  icon: content_cut
  link: /config/pruning
- title: Configure the daemon
  description: Delve into the configuration options of the Docker daemon.
  icon: tune
  link: /config/daemon
- title: Rootless mode
  description: Run Docker without root privileges.
  icon: security
  link: /engine/security/rootless
- title: Deprecated features
  description: Find out what features of Docker Engine you should stop using.
  icon: folder_delete
  link: /engine/deprecated/
- title: Release notes
  description: Read the release notes for the latest version.
  icon: note_add
  link: /engine/release-notes
aliases:
- /edge/
- /engine/ce-ee-node-activate/
- /engine/migration/
- /engine/misc/
- /linux/
---

Docker Engine 是一种开源容器化技术，用于构建和容器化您的应用程序。Docker Engine 作为客户端-服务器应用程序运行，包含：

- 一个带有长期运行的守护进程
  [`dockerd`](/reference/cli/dockerd) 的服务器。
- 一组 API，指定程序可以用来与 Docker 守护进程通信和指示的接口。
- 一个命令行界面 (CLI) 客户端
  [`docker`](/reference/cli/docker/)。

CLI 使用 [Docker API](/reference/api/engine/_index.md) 通过脚本或直接 CLI 命令来控制或与 Docker 守护进程交互。许多其他 Docker 应用程序使用底层 API 和 CLI。守护进程创建和管理 Docker 对象，例如镜像、容器、网络和卷。

有关更多详细信息，请参阅
[Docker 架构](/get-started/docker-overview.md#docker-architecture)。

{{< grid >}}

## 许可

Docker Engine 使用 Apache License, Version 2.0 许可。有关完整的许可文本，请参阅
[LICENSE](https://github.com/moby/moby/blob/master/LICENSE)。

但是，对于通过 Docker Desktop 获取的 Docker Engine 的商业使用，如果是在大型企业（员工超过 250 人或年收入超过 1000 万美元）中使用，则需要[付费订阅](https://www.docker.com/pricing/)。
