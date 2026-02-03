---
title: 构建器 (Builders)
weight: 40
keywords: build, buildx, builders, buildkit, drivers, backend, 构建器, 驱动
description: 了解构建器及其管理方法
---

构建器 (builder) 是一个您可以用来运行构建任务的 BuildKit 守护进程。BuildKit 是一款构建引擎，它负责解析 Dockerfile 中的构建步骤，并生成容器镜像或其他产物。

您可以创建并管理构建器，检查其状态，甚至连接到远程运行的构建器。您可以通过 Docker CLI 与构建器进行交互。

## 默认构建器 (Default builder)

Docker Engine 会自动创建一个构建器，它将成为您构建任务的默认后端。该构建器使用守护进程捆绑的 BuildKit 库。此构建器无需任何配置。

默认构建器直接绑定到 Docker 守护进程及其 [上下文 (context)](/manuals/engine/manage-resources/contexts.md)。如果您更改了 Docker 上下文，您的 `default` 构建器将指向新的 Docker 上下文。

## 构建驱动 (Build drivers)

Buildx 实现了 [构建驱动 (build drivers)](drivers/_index.md) 的概念，用以指代不同的构建器配置。守护进程创建的默认构建器使用 [`docker` 驱动](drivers/docker.md)。

Buildx 支持以下构建驱动：

- `docker`：使用 Docker 守护进程捆绑的 BuildKit 库。
- `docker-container`：使用 Docker 创建一个专用的 BuildKit 容器。
- `kubernetes`：在 Kubernetes 集群中创建 BuildKit pod。
- `remote`：直接连接到手动管理的 BuildKit 守护进程。

## 已选构建器 (Selected builder)

已选构建器是指当您运行 build 命令时默认使用的构建器。

当您运行构建任务，或通过 CLI 与构建器交互时，可以使用可选的 `--builder` 标志，或 `BUILDX_BUILDER` [环境变量](../building/variables.md#buildx_builder) 来按名称指定构建器。如果您未指定构建器，则使用已选构建器。

使用 `docker buildx ls` 命令查看可用的构建器实例。构建器名称旁边的星号 (`*`) 表示当前已选中的构建器。

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT      STATUS   BUILDKIT PLATFORMS
default *       docker
  default       default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
my_builder      docker-container
  my_builder0   default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
```

### 选择不同的构建器

要切换构建器，请使用 `docker buildx use <名称>` 命令。

运行此命令后，在您调用构建任务时，指定的构建器将被自动选中。

### `docker build` 与 `docker buildx build` 的区别

虽然 `docker build` 是 `docker buildx build` 的别名，但这两个命令之间存在细微差异。通过 Buildx，构建客户端和守护进程 (BuildKit) 是解耦的。这意味着您可以从单个客户端使用多个构建器，甚至是远程构建器。

`docker build` 命令始终默认使用 Docker Engine 捆绑的默认构建器，以确保与旧版 Docker CLI 的向后兼容性。而 `docker buildx build` 命令在将构建请求发送给 BuildKit 之前，会先检查您是否设置了不同的构建器作为默认构建器。

要通过 `docker build` 命令使用非默认构建器，您必须：

- 显式指定构建器，使用 `--builder` 标志或 `BUILDX_BUILDER` 环境变量：

  ```console
  $ BUILDX_BUILDER=my_builder docker build .
  $ docker build --builder my_builder .
  ```

- 或者，通过运行以下命令将 Buildx 配置为默认客户端：

  ```console
  $ docker buildx install
  ```

  这将更新您的 [Docker CLI 配置文件](/reference/cli/docker/_index.md#配置文件) 以确保您所有的构建相关命令都通过 Buildx 路由。

  > [!TIP]
  > 要撤销此更改，请运行 `docker buildx uninstall`。

通常，当您想要使用自定义构建器时，我们建议使用 `docker buildx build` 命令。这可以确保您的 [已选构建器](#selected-builder) 配置得到正确解释。

## 额外信息

- 有关如何与构建器交互及管理的信息，请参阅 [管理构建器](./manage.md)
- 欲了解不同类型的构建器，请参阅 [构建驱动](drivers/_index.md)