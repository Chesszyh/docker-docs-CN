---
title: 针对云端构建进行优化
linkTitle: 优化 (Optimization)
weight: 40
description: 远程构建与本地构建不同。以下是针对远程构建器进行优化的方法。
keywords: build, cloud build, 优化, 远程, 本地, 云
---

Docker Build Cloud 在远程运行您的构建，而不是在您调用构建的机器上运行。这意味着客户端和构建器之间的文件传输是通过网络进行的。

与本地传输相比，通过网络传输文件具有更高的延迟和更低的带宽。Docker Build Cloud 提供了几项功能来缓解这一问题：

- 它使用挂载的存储卷作为构建缓存，这使得读取和写入缓存的速度非常快。
- 将构建结果加载回客户端时，仅拉取与之前构建相比发生更改的层。

尽管有这些优化，但对于大型项目或网络连接较慢的情况，远程构建仍然可能产生较慢的上下文传输和镜像加载。以下是一些优化构建的方法，可以使传输更高效：

- [Dockerignore 文件](#dockerignore-文件)
- [精简基础镜像](#精简基础镜像)
- [多阶段构建](#多阶段构建)
- [在构建中获取远程文件](#在构建中获取远程文件)
- [多线程工具](#多线程工具)

有关如何优化构建的更多信息，请参阅 [构建最佳实践](/manuals/build/building/best-practices.md)。

### Dockerignore 文件

通过使用 [`.dockerignore` 文件](/manuals/build/concepts/context.md#dockerignore-files)，您可以明确指出不想包含在构建上下文中的本地文件。ignore 文件中指定的通配符模式匹配的文件不会被传输到远程构建器。

您可能希望添加到 `.dockerignore` 文件中的一些示例包括：

- `.git` — 跳过在构建上下文中发送版本控制历史。请注意，这意味着您将无法在构建步骤中运行 Git 命令，例如 `git rev-parse`。
- 包含构建产物（如二进制文件）的目录。在开发期间本地创建的构建产物。
- 包管理器的供应商（vendor）目录，例如 `node_modules`。

总的来说，`.dockerignore` 文件的内容应该与您的 `.gitignore` 文件内容相似。

### 精简基础镜像

在 Dockerfile 的 `FROM` 指令中选择较小的镜像可以帮助减小最终镜像的体积。[Alpine 镜像](https://hub.docker.com/_/alpine) 是一个很好的最小化 Docker 镜像示例，它提供了您期望从 Linux 容器获得的所有操作系统实用程序。

还有一个 [特殊的 `scratch` 镜像](https://hub.docker.com/_/scratch)，它什么也不包含。例如，这对于创建静态链接二进制文件的镜像非常有用。

### 多阶段构建

[多阶段构建](/build/building/multi-stage/) 可以让您的构建运行得更快，因为各个阶段可以并行运行。它还可以使最终结果更小。编写 Dockerfile 时，应使最终的运行时阶段使用尽可能小的基础镜像，仅包含程序运行所需的资源。

还可以使用 Dockerfile 的 `COPY --from` 指令 [从其他镜像或阶段复制资源](/build/building/multi-stage/#name-your-build-stages)。此技术可以减少最终阶段的层数及这些层的大小。

### 在构建中获取远程文件

只要可能，您应该在构建过程中从远程位置获取文件，而不是将文件捆绑到构建上下文中。直接在 Docker Build Cloud 服务器上下载文件更好，因为这可能比随构建上下文传输文件更快。

您可以在构建期间使用 [Dockerfile `ADD` 指令](/reference/dockerfile/#add) 或在 `RUN` 指令中使用 `wget` 和 `rsync` 等工具获取远程文件。

### 多线程工具

您在构建指令中使用的一些工具默认可能不会利用多核。例如 `make` 默认使用单线程，除非您指定 `make --jobs=<n>` 选项。对于涉及此类工具的构建步骤，请尝试检查是否可以通过并行化来优化执行。
