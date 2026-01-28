---
title: Docker 驱动
description: |
  Docker 驱动是默认驱动。
  它使用与 Docker Engine 捆绑的 BuildKit。
keywords: build, buildx, driver, builder, docker
aliases:
  - /build/buildx/drivers/docker/
  - /build/building/drivers/docker/
  - /build/drivers/docker/
---

Buildx Docker 驱动是默认驱动。它使用直接内置于 Docker Engine 中的 BuildKit 服务器组件。Docker 驱动无需任何配置。

与其他驱动不同，使用 Docker 驱动的构建器无法手动创建。它们只能从 Docker context 自动创建。

使用 Docker 驱动构建的镜像会自动加载到本地镜像存储中。

## 概要

```console
# The Docker driver is used by buildx by default
docker buildx build .
```

无法配置使用哪个 BuildKit 版本，也无法向使用 Docker 驱动的构建器传递任何额外的 BuildKit 参数。BuildKit 版本和参数由 Docker Engine 内部预设。

如果您需要额外的配置和灵活性，请考虑使用 [Docker container 驱动](./docker-container.md)。

## 延伸阅读

有关 Docker 驱动的更多信息，请参阅 [buildx 参考文档](/reference/cli/docker/buildx/create.md#driver)。
