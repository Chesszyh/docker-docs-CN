---
title: 在 GitHub Actions 中使用命名上下文
linkTitle: 命名上下文 (Named contexts)
description: 在 GitHub Actions 的多阶段构建中使用附加上下文
keywords: ci, github actions, gha, buildkit, buildx, 上下文
---

您可以定义 [附加上下文 (additional build contexts)](/reference/cli/docker/buildx/build.md#build-context)，并在 Dockerfile 中通过 `FROM name` 或 `--from=name` 访问它们。如果 Dockerfile 定义了同名的阶段，它将被覆盖。

这在 GitHub Actions 中非常有用，可以复用其他构建的结果，或者在工作流中将镜像固定到特定的标签。

## 将镜像固定到标签

将 `alpine:latest` 替换为固定的版本：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        uses: docker/build-push-action@v6
        with:
          build-contexts: |
            alpine=docker-image://alpine:{{% param "example_alpine_version" %}}
          tags: myimage:latest
```

## 在后续步骤中使用镜像

默认情况下，[Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) action 使用 `docker-container` 作为构建驱动程序，因此构建好的 Docker 镜像不会被自动加载。

使用命名上下文，您可以复用构建好的镜像：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: docker

      - name: Build base image
        uses: docker/build-push-action@v6
        with:
          context: "{{defaultContext}}:base"
          load: true
          tags: my-base-image:latest

      - name: Build
        uses: docker/build-push-action@v6
        with:
          build-contexts: |
            alpine=docker-image://my-base-image:latest
          tags: myimage:latest
```

## 配合容器构建器使用

如上一节所示，我们在使用命名上下文构建时没有使用默认的 [`docker-container` 驱动程序](../../builders/drivers/docker-container.md)。这是因为该驱动程序是隔离的，无法从 Docker 存储中加载镜像。为了解决这个问题，您可以使用 [本地镜像库 (local registry)](local-registry.md) 在工作流中推送您的基础镜像：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    services:
      registry:
        image: registry:2
        ports:
          - 5000:5000
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          # 需要 network=host driver-opt 才能推送到本地镜像库
          driver-opts: network=host

      - name: Build base image
        uses: docker/build-push-action@v6
        with:
          context: "{{defaultContext}}:base"
          tags: localhost:5000/my-base-image:latest
          push: true

      - name: Build
        uses: docker/build-push-action@v6
        with:
          build-contexts: |
            alpine=docker-image://localhost:5000/my-base-image:latest
          tags: myimage:latest
```
