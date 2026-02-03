---
title: Docker 驱动 (Docker driver)
description: |
  Docker 驱动是默认驱动。
  它使用 Docker Engine 捆绑的 BuildKit。
keywords: build, buildx, driver, builder, docker, 驱动, 构建器
aliases:
  - /build/buildx/drivers/docker/
  - /build/building/drivers/docker/
  - /build/drivers/docker/
---

Buildx Docker 驱动是默认驱动。它使用直接内置在 Docker Engine 中的 BuildKit 服务器组件。Docker 驱动无需任何配置。

与其他驱动不同，使用 Docker 驱动的构建器无法手动创建。它们只能根据 Docker 上下文自动创建。

使用 Docker 驱动构建的镜像会自动加载到本地镜像库中。

## 语法

```console
# buildx 默认使用 Docker 驱动
docker buildx build .
```

无法配置要使用的 BuildKit 版本，也无法向使用 Docker 驱动的构建器传递任何额外的 BuildKit 参数。BuildKit 版本和参数由 Docker Engine 在内部预设。

如果您需要额外的配置和灵活性，请考虑使用 [Docker 容器驱动](./docker-container.md)。

## 深入阅读

欲了解更多关于 Docker 驱动的信息，请参阅 [Buildx 参考](/reference/cli/docker/buildx/create.md#driver)。