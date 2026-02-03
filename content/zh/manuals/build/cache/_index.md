---
title: Docker 构建缓存 (Docker build cache)
linkTitle: 缓存
weight: 60
description: 通过有效利用构建缓存来提升您的构建速度
keywords: build, buildx, buildkit, dockerfile, image layers, build instructions, build context, 缓存, 镜像层
aliases:
  - /build/building/cache/
  - /build/guide/layers/
---

当您多次构建同一个 Docker 镜像时，了解如何优化构建缓存是确保构建快速运行的一项利器。

## 构建缓存的工作原理

理解 Docker 的构建缓存有助于您编写更好的 Dockerfile，从而实现更快的构建。

以下示例展示了一个用 C 语言编写的程序的小型 Dockerfile。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essentials
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
```

此 Dockerfile 中的每条指令都对应最终镜像中的一个层 (layer)。您可以将镜像层看作一个栈，每一层都在其之前的层之上添加更多内容：

![镜像层图表](../images/cache-stack.png)

每当一层发生变化时，该层就需要重新构建。例如，假设您修改了 `main.c` 文件中的程序。在此更改之后，`COPY` 命令必须再次运行，以便这些更改出现在镜像中。换句话说，Docker 将使该层的缓存失效 (invalidate)。

如果某一层发生了变化，其后的所有层也会受到影响。当带有 `COPY` 命令的层失效时，其后的所有层也都必须重新运行：

![镜像层图表，显示缓存失效](../images/cache-stack-invalidated.png)

简而言之，这就是 Docker 构建缓存。一旦某一层发生变化，其所有的下游层也都需要重新构建。即使它们构建出的内容没有任何不同，它们仍需重新运行。

## 其他资源

欲了解更多关于利用缓存进行高效构建的信息，请参阅：

- [缓存失效 (Cache invalidation)](invalidation.md)
- [优化构建缓存 (Optimize build cache)](optimize.md)
- [垃圾回收 (Garbage collection)](garbage-collection.md)
- [缓存存储后端 (Cache storage backends)](./backends/_index.md)