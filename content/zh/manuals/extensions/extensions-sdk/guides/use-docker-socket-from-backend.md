---
title: 从扩展后端使用 Docker socket
linkTitle: 使用 Docker socket
description: Docker 扩展元数据
keywords: Docker, extensions, sdk, metadata
aliases:
 - /desktop/extensions-sdk/guides/use-docker-socket-from-backend/
---

扩展可以使用 SDK 直接从前端调用 Docker 命令。

在某些情况下，从后端与 Docker Engine 交互也很有用。

扩展后端容器可以挂载 Docker socket，并使用它从扩展后端逻辑与 Docker Engine 交互。了解更多关于 [Docker Engine socket](/reference/cli/dockerd/#examples) 的信息。

但是，当从位于 Desktop 虚拟机中的扩展容器挂载 Docker socket 时，您需要挂载虚拟机内部的 Docker socket，而不是从主机文件系统挂载 `/var/run/docker.sock`（从主机使用 Docker socket 可能导致容器中的权限问题）。

为此，您可以使用 `/var/run/docker.sock.raw`。Docker Desktop 会挂载位于 Desktop 虚拟机中的 socket，而不是来自主机的 socket。

```yaml
services:
  myExtension:
    image: ${DESKTOP_PLUGIN_IMAGE}
    volumes:
      - /var/run/docker.sock.raw:/var/run/docker.sock
```
