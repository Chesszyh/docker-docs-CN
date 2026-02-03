---
title: 在 GitHub Actions 中使用命名上下文
linkTitle: 命名上下文 (Named contexts)
description: 在 GitHub Actions 的多阶段构建中使用额外的上下文
keywords: ci, github actions, gha, buildkit, buildx, context, 命名上下文, 上下文
---

您可以定义 [额外的构建上下文 (additional build contexts)](/reference/cli/docker/buildx/build.md#build-context)，并在 Dockerfile 中通过 `FROM name` 或 `--from=name` 进行访问。当 Dockerfile 定义了同名的阶段时，该阶段会被覆盖。

这在 GitHub Actions 中非常有用，可以复用其他构建的结果，或者在工作流中将镜像固定到特定的标签。

## 将镜像固定到标签

将 `alpine:latest` 替换为一个固定的镜像：

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

默认情况下，[Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) Action 使用 `docker-container` 作为构建驱动，因此构建的 Docker 镜像不会自动加载。

使用命名上下文，您可以复用已构建的镜像：

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

如前一节所示，我们在使用命名上下文构建时没有使用默认的 [`docker-container` 驱动](../../builders/drivers/docker-container.md)。这是因为该驱动是隔离的，无法从 Docker 镜像库中加载镜像。为了解决这个问题，您可以使用 [本地注册表](local-registry.md) 在工作流中推送您的基础镜像：

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
          # 推送到本地注册表需要设置 network=host driver-opt
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