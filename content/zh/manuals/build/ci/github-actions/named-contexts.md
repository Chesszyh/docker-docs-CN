---
title: 在 GitHub Actions 中使用命名上下文
linkTitle: Named contexts
description: 在 GitHub Actions 中使用多阶段构建的额外上下文
keywords: ci, github actions, gha, buildkit, buildx, context
---

您可以定义[额外的构建上下文](/reference/cli/docker/buildx/build.md#build-context)，并在 Dockerfile 中使用 `FROM name` 或 `--from=name` 来访问它们。当 Dockerfile 定义了同名的阶段时，它会被覆盖。

这在 GitHub Actions 中非常有用，可以重用其他构建的结果或在工作流中将镜像固定到特定标签。

## 将镜像固定到标签

将 `alpine:latest` 替换为固定版本：

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

默认情况下，[Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) action 使用 `docker-container` 作为构建驱动程序，因此构建的 Docker 镜像不会自动加载。

使用命名上下文，您可以重用构建的镜像：

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

## 与容器构建器一起使用

如上一节所示，我们没有使用默认的 [`docker-container` 驱动程序](../../builders/drivers/docker-container.md)来使用命名上下文进行构建。这是因为此驱动程序无法从 Docker 存储加载镜像，因为它是隔离的。要解决这个问题，您可以在工作流中使用[本地镜像仓库](local-registry.md)来推送基础镜像：

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
          # network=host driver-opt needed to push to local registry
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
