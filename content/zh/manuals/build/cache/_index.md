---
title: Docker 构建缓存
linkTitle: 缓存 (Cache)
weight: 60
description: 有效利用构建缓存以提高构建速度
keywords: build, buildx, buildkit, dockerfile, 镜像层, 构建指令, 构建上下文
aliases:
  - /build/building/cache/
  - /build/guide/layers/
---

当您多次构建同一个 Docker 镜像时，了解如何优化构建缓存是确保构建快速运行的强大工具。

## 构建缓存的工作原理

了解 Docker 的构建缓存有助于您编写更好的 Dockerfile，从而实现更快的构建。

以下示例显示了一个用 C 语言编写的程序的简单 Dockerfile。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essentials
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
```

此 Dockerfile 中的每条指令都对应最终镜像中的一个层。您可以将镜像层想象成一个堆栈，每一层都在其之前的层之上添加更多内容：

![镜像层图表](../images/cache-stack.png)

每当某一层发生变化时，该层都需要重新构建。例如，假设您修改了 `main.c` 文件中的程序代码。更改后，为了让这些更改出现在镜像中，`COPY` 命令必须再次运行。换句话说，Docker 将使该层的缓存失效。

如果某一层发生了变化，其后的所有其他层也会受到影响。当带有 `COPY` 命令的层失效时，随后的所有层也都需要重新运行：

![显示缓存失效的镜像层图表](../images/cache-stack-invalidated.png)

简而言之，这就是 Docker 的构建缓存。一旦某一层发生变化，那么其所有下游层也都必须重新构建。即使它们的构建结果没有任何变化，也仍然需要重新运行。

## 其他资源

有关利用缓存进行高效构建的更多信息，请参阅：

- [缓存失效](invalidation.md)
- [优化构建缓存](optimize.md)
- [垃圾回收](garbage-collection.md)
- [缓存存储后端](./backends/_index.md)
