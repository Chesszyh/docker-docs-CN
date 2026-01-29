---
title: 构建器 (Builders)
weight: 40
keywords: build, buildx, builders, buildkit, drivers, backend
description: 了解构建器及其管理方式
---

构建器（Builder）是一个 BuildKit 守护进程，可用于运行您的构建。BuildKit 是构建引擎，用于解析 Dockerfile 中的构建步骤，以生成容器镜像或其他构件。

您可以创建和管理构建器、检查其状态，甚至连接到远程运行的构建器。您可以通过 Docker CLI 与构建器进行交互。

## 默认构建器

Docker Engine 会自动创建一个构建器，它将成为您构建的默认后端。该构建器使用守护进程中捆绑的 BuildKit 库。此构建器无需任何配置。

默认构建器直接绑定到 Docker 守护进程及其 [上下文 (context)](/manuals/engine/manage-resources/contexts.md)。如果您更改了 Docker 上下文，您的 `default` 构建器将指向新的 Docker 上下文。

## 构建驱动程序

Buildx 引入了 [构建驱动程序 (build drivers)](drivers/_index.md) 的概念，用以指代不同的构建器配置。守护进程创建的默认构建器使用 [`docker` 驱动程序](drivers/docker.md)。

Buildx 支持以下构建驱动程序：

- `docker`：使用 Docker 守护进程中捆绑的 BuildKit 库。
- `docker-container`：使用 Docker 创建一个专用的 BuildKit 容器。
- `kubernetes`：在 Kubernetes 集群中创建 BuildKit Pod。
- `remote`：直接连接到手动管理的 BuildKit 守护进程。

## 已选构建器

已选构建器是指在运行构建命令时默认使用的构建器。

当您运行构建或通过 CLI 与构建器交互时，可以使用可选的 `--builder` 标志或 `BUILDX_BUILDER` [环境变量](../building/variables.md#buildx_builder) 按名称指定构建器。如果您未指定构建器，则使用已选构建器。

使用 `docker buildx ls` 命令查看可用的构建器实例。构建器名称旁边的星号 (`*`) 表示它是当前已选构建器。

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT      STATUS   BUILDKIT PLATFORMS
default *       docker
  default       default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
my_builder      docker-container
  my_builder0   default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
```

### 选择不同的构建器

要在构建器之间切换，请使用 `docker buildx use <name>` 命令。

运行此命令后，您指定的构建器将在调用构建时自动被选中。

### `docker build` 与 `docker buildx build` 的区别

尽管 `docker build` 是 `docker buildx build` 的别名，但这两个命令之间存在细微差别。通过 Buildx，构建客户端与守护进程 (BuildKit) 是解耦的。这意味着您可以从单个客户端使用多个构建器，甚至是远程构建器。

`docker build` 命令始终默认使用 Docker Engine 捆绑的默认构建器，以确保与旧版 Docker CLI 的向后兼容性。另一方面，`docker buildx build` 命令在将构建发送到 BuildKit 之前，会检查您是否已将其他构建器设置为默认构建器。

要在非默认构建器上使用 `docker build` 命令，您必须执行以下操作之一：

- 使用 `--builder` 标志或 `BUILDX_BUILDER` 环境变量显式指定构建器：

  ```console
  $ BUILDX_BUILDER=my_builder docker build .
  $ docker build --builder my_builder .
  ```

- 通过运行以下命令将 Buildx 配置为默认客户端：

  ```console
  $ docker buildx install
  ```

  这会更新您的 [Docker CLI 配置文件](/reference/cli/docker/_index.md#configuration-files)，以确保所有与构建相关的命令都通过 Buildx 路由。

  > [!TIP]
  > 要撤销此更改，请运行 `docker buildx uninstall`。

通常，当您想使用自定义构建器时，我们建议您使用 `docker buildx build` 命令。这可以确保您的 [已选构建器](#已选构建器) 配置被正确解释。

## 更多信息

- 有关如何与构建器交互及管理构建器的信息，请参阅 [管理构建器](./manage.md)
- 要了解不同类型的构建器，请参阅 [构建驱动程序](drivers/_index.md)
