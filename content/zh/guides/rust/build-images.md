---
title: 构建你的 Rust 镜像
linkTitle: 构建镜像
weight: 5
keywords: rust, build, images, dockerfile
description: 了解如何构建你的第一个 Rust Docker 镜像
aliases:
  - /language/rust/build-images/
  - /guides/language/rust/build-images/
---

## 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

## 概述

本指南将带你构建你的第一个 Rust 镜像。镜像包含运行应用程序所需的一切——代码或二进制文件、运行时、依赖项以及所需的任何其他文件系统对象。

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，将目录切换到你想工作的目录，然后运行以下命令来克隆存储库：

```console
$ git clone https://github.com/docker/docker-rust-hello && cd docker-rust-hello
```

## 为 Rust 创建 Dockerfile

既然你有了一个应用程序，你可以使用 `docker init` 为其创建一个 Dockerfile。在 `docker-rust-hello` 目录内，运行 `docker init` 命令。`docker init` 提供了一些默认配置，但你需要回答几个关于你的应用程序的问题。参考以下示例来回答 `docker init` 的提示，并对你的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Rust
? What version of Rust do you want to use? 1.70.0
? What port does your server listen on? 8000
```

你现在应该在 `docker-rust-hello` 目录中拥有以下新文件：

- Dockerfile
- .dockerignore
- compose.yaml
- README.Docker.md

要构建镜像，只需要 Dockerfile。在你喜欢的 IDE 或文本编辑器中打开 Dockerfile，查看其包含的内容。要了解有关 Dockerfile 的更多信息，请参阅 [Dockerfile 参考](/reference/dockerfile.md)。

## .dockerignore 文件

当你运行 `docker init` 时，它还会创建一个 [`.dockerignore`](/reference/dockerfile.md#dockerignore-file) 文件。使用 `.dockerignore` 文件来指定你不希望复制到镜像中的模式和路径，以保持镜像尽可能小。在你喜欢的 IDE 或文本编辑器中打开 `.dockerignore` 文件，查看里面已经有什么内容。

## 构建镜像

既然你已经创建了 Dockerfile，你就可以构建镜像了。为此，请使用 `docker build` 命令。`docker build` 命令从 Dockerfile 和上下文构建 Docker 镜像。构建的上下文是位于指定 PATH 或 URL 中的一组文件。Docker 构建过程可以访问位于此上下文中的任何文件。

构建命令可选地接受 `--tag` 标志。该标签设置镜像的名称和格式为 `name:tag` 的可选标签。如果你不传递标签，Docker 使用 "latest" 作为其默认标签。

构建 Docker 镜像。

```console
$ docker build --tag docker-rust-image .
```

你应该会看到类似以下的输出。

```console
[+] Building 62.6s (14/14) FINISHED
 => [internal] load .dockerignore                                                                                                    0.1s
 => => transferring context: 2B                                                                                                      0.0s
 => [internal] load build definition from Dockerfile                                                                                 0.1s
 => => transferring dockerfile: 2.70kB                                                                                               0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                                           2.3s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:39b85bbfa7536a5feceb7372a0817649ecb2724562a38360f4d6a7782a409b14      0.0s
 => [internal] load metadata for docker.io/library/debian:bullseye-slim                                                              1.9s
 => [internal] load metadata for docker.io/library/rust:1.70.0-slim-bullseye                                                         1.7s
 => [build 1/3] FROM docker.io/library/rust:1.70.0-slim-bullseye@sha256:585eeddab1ec712dade54381e115f676bba239b1c79198832ddda397c1f  0.0s
 => [internal] load build context                                                                                                    0.0s
 => => transferring context: 35.29kB                                                                                                 0.0s
 => [final 1/3] FROM docker.io/library/debian:bullseye-slim@sha256:7606bef5684b393434f06a50a3d1a09808fee5a0240d37da5d181b1b121e7637  0.0s
 => CACHED [build 2/3] WORKDIR /app                                                                                                  0.0s
 => [build 3/3] RUN --mount=type=bind,source=src,target=src     --mount=type=bind,source=Cargo.toml,target=Cargo.toml     --mount=  57.7s
 => CACHED [final 2/3] RUN adduser     --disabled-password     --gecos ""     --home "/nonexistent"     --shell "/sbin/nologin"      0.0s
 => CACHED [final 3/3] COPY --from=build /bin/server /bin/                                                                           0.0s
 => exporting to image                                                                                                               0.0s
 => => exporting layers                                                                                                              0.0s
 => => writing image sha256:f1aa4a9f58d2ecf73b0c2b7f28a6646d9849b32c3921e42adc3ab75e12a3de14                                         0.0s
 => => naming to docker.io/library/docker-rust-image
```

## 查看本地镜像

要查看你本地机器上的镜像列表，你有两个选择。一是使用 Docker CLI，二是使用 [Docker Desktop](/manuals/desktop/use-desktop/images.md)。既然你已经在终端中工作，那就看看如何使用 CLI 列出镜像。

要列出镜像，运行 `docker images` 命令。

```console
$ docker images
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-rust-image         latest            8cae92a8fbd6   3 minutes ago   123MB
```

你应该看到至少列出了一个镜像，包括你刚刚构建的镜像 `docker-rust-image:latest`。

## 标记镜像

如前所述，镜像名称由斜杠分隔的名称组件组成。名称组件可以包含小写字母、数字和分隔符。分隔符可以包括一个句点、一个或两个下划线，或一个或多个破折号。名称组件不能以分隔符开头或结尾。

镜像由清单和层列表组成。此时不要太担心清单和层，只要知道“标签”指向这些工件的组合即可。你可以为一个镜像拥有多个标签。为你构建的镜像创建第二个标签并查看其层。

要为你构建的镜像创建新标签，请运行以下命令。

```console
$ docker tag docker-rust-image:latest docker-rust-image:v1.0.0
```

`docker tag` 命令为镜像创建一个新标签。它不会创建新镜像。标签指向同一个镜像，只是引用该镜像的另一种方式。

现在，运行 `docker images` 命令查看本地镜像列表。

```console
$ docker images
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-rust-image         latest            8cae92a8fbd6   4 minutes ago   123MB
docker-rust-image         v1.0.0            8cae92a8fbd6   4 minutes ago   123MB
rust                      latest            be5d294735c6   4 minutes ago   113MB
```

你可以看到两个以 `docker-rust-image` 开头的镜像。你知道它们是同一个镜像，因为如果你查看 `IMAGE ID` 列，你可以看到这两个镜像的值是相同的。

移除你刚刚创建的标签。为此，使用 `rmi` 命令。`rmi` 命令代表移除镜像（remove image）。

```console
$ docker rmi docker-rust-image:v1.0.0
Untagged: docker-rust-image:v1.0.0
```

请注意，Docker 的响应告诉你 Docker 并没有移除镜像，而只是“取消标记”了它。你可以通过运行 `docker images` 命令来检查这一点。

```console
$ docker images
REPOSITORY               TAG               IMAGE ID       CREATED         SIZE
docker-rust-image        latest            8cae92a8fbd6   6 minutes ago   123MB
rust                     latest            be5d294735c6   6 minutes ago   113MB
```

Docker 移除了标记为 `:v1.0.0` 的镜像，但 `docker-rust-image:latest` 标签在你的机器上仍然可用。

## 总结

本节展示了如何使用 `docker init` 为 Rust 应用程序创建 Dockerfile 和 .dockerignore 文件。然后它展示了如何构建镜像。最后，它展示了如何标记镜像并列出所有镜像。

相关信息：

- [Dockerfile 参考](/reference/dockerfile.md)
- [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
- [docker init CLI 参考](/reference/cli/docker/init.md)
- [docker build CLI 参考](/reference/cli/docker/buildx/build.md)

## 下一步

在下一节中，学习如何将你的镜像作为容器运行。
