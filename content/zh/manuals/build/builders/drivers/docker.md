---
title: Docker 驱动程序
description: |
  Docker 驱动程序是默认驱动程序。
  它使用 Docker Engine 捆绑的 BuildKit。
keywords: build, buildx, driver, builder, docker
aliases:
  - /build/buildx/drivers/docker/
  - /build/building/drivers/docker/
  - /build/drivers/docker/
---

Buildx Docker 驱动程序是默认驱动程序。它使用直接内置于 Docker Engine 中的 BuildKit 服务器组件。Docker 驱动程序无需配置。

与其他驱动程序不同，使用 Docker 驱动程序的构建器无法手动创建。它们只能从 Docker 上下文自动创建。

使用 Docker 驱动程序构建的镜像会自动加载到本地镜像库。

## 概要

```console
# Buildx 默认使用 Docker 驱动程序
docker buildx build .
```

无法配置要使用的 BuildKit 版本，也无法向使用 Docker 驱动程序的构建器传递任何额外的 BuildKit 参数。BuildKit 版本和参数由 Docker Engine 在内部预设。

如果您需要额外的配置和灵活性，请考虑使用 [Docker 容器驱动程序](./docker-container.md)。

## 延伸阅读

有关 Docker 驱动程序的更多信息，请参阅 [buildx 参考](/reference/cli/docker/buildx/create.md#driver)。
