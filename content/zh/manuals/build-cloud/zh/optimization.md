---
title: 优化云端构建
linkTitle: 优化
weight: 40
description: 远程构建与本地构建不同。以下是针对远程构建器的优化方法。
keywords: build, cloud build, optimize, remote, local, cloud
aliases:
  - /build/cloud/optimization/
---

Docker Build Cloud 在远程运行您的构建，而不是在您调用构建的机器上。这意味着客户端和构建器之间的文件传输通过网络进行。

通过网络传输文件比本地传输具有更高的延迟和更低的带宽。Docker Build Cloud 具有多项功能来缓解这一问题：

- 它使用附加的存储卷作为构建缓存，这使得读取和写入缓存非常快。
- 将构建结果加载回客户端时，只拉取与之前构建相比发生变化的层。

尽管有这些优化，对于大型项目或网络连接较慢的情况，远程构建仍可能导致上下文传输和镜像加载缓慢。以下是一些可以优化构建以使传输更高效的方法：

- [Dockerignore 文件](#dockerignore-files)
- [精简基础镜像](#slim-base-images)
- [多阶段构建](#multi-stage-builds)
- [在构建中获取远程文件](#fetch-remote-files-in-build)
- [多线程工具](#multi-threaded-tools)

有关如何优化构建的更多信息，请参阅[构建最佳实践](/manuals/build/building/best-practices.md)。

### Dockerignore 文件

使用 [`.dockerignore` 文件](/manuals/build/concepts/context.md#dockerignore-files)，您可以明确指定哪些本地文件不想包含在构建上下文中。被您在 ignore 文件中指定的 glob 模式匹配的文件不会传输到远程构建器。

您可能想添加到 `.dockerignore` 文件的一些示例包括：

- `.git` — 跳过在构建上下文中发送版本控制历史。请注意，这意味着您将无法在构建步骤中运行 Git 命令，例如 `git rev-parse`。
- 包含构建产物的目录，例如二进制文件。在本地开发期间创建的构建产物。
- 包管理器的 vendor 目录，例如 `node_modules`。

通常，`.dockerignore` 文件的内容应该与 `.gitignore` 中的内容类似。

### 精简基础镜像

为 Dockerfile 中的 `FROM` 指令选择较小的镜像可以帮助减小最终镜像的大小。[Alpine 镜像](https://hub.docker.com/_/alpine)是一个很好的最小 Docker 镜像示例，它提供了您期望从 Linux 容器获得的所有操作系统实用程序。

还有[特殊的 `scratch` 镜像](https://hub.docker.com/_/scratch)，它完全不包含任何内容。例如，它对于创建静态链接二进制文件的镜像很有用。

### 多阶段构建

[多阶段构建](/build/building/multi-stage/)可以使您的构建运行更快，因为阶段可以并行运行。它还可以使您的最终结果更小。编写 Dockerfile 时，使最终运行时阶段使用尽可能小的基础镜像，只包含程序运行所需的资源。

还可以使用 Dockerfile 的 `COPY --from` 指令[从其他镜像或阶段复制资源](/build/building/multi-stage/#name-your-build-stages)。此技术可以减少最终阶段中的层数和这些层的大小。

### 在构建中获取远程文件

如果可能，您应该在构建中从远程位置获取文件，而不是将文件捆绑到构建上下文中。直接在 Docker Build Cloud 服务器上下载文件更好，因为这可能比通过构建上下文传输文件更快。

您可以在构建期间使用 [Dockerfile `ADD` 指令](/reference/dockerfile/#add)获取远程文件，或者在 `RUN` 指令中使用 `wget` 和 `rsync` 等工具。

### 多线程工具

您在构建指令中使用的某些工具默认可能不会利用多核。一个这样的例子是 `make`，除非您指定 `make --jobs=<n>` 选项，否则它默认使用单线程。对于涉及此类工具的构建步骤，请尝试检查是否可以通过并行化来优化执行。
