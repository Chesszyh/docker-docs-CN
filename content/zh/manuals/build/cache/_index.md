---
title: Docker 构建缓存
linkTitle: 缓存
weight: 60
description: 通过有效使用构建缓存来提高构建速度
keywords: build, buildx, buildkit, dockerfile, image layers, build instructions, build context
aliases:
  - /build/building/cache/
  - /build/guide/layers/
---

当你多次构建相同的 Docker 镜像时，了解如何优化构建缓存是确保构建快速运行的重要技巧。

## 构建缓存的工作原理

理解 Docker 的构建缓存有助于你编写更好的 Dockerfile，从而实现更快的构建。

以下示例展示了一个用于 C 语言程序的小型 Dockerfile。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essentials
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
```

这个 Dockerfile 中的每条指令都会转换为最终镜像中的一个层。你可以把镜像层想象成一个堆栈，每一层都在它之前的层上添加更多内容：

![镜像层示意图](../images/cache-stack.png)

每当一个层发生变化时，该层就需要重新构建。例如，假设你对 `main.c` 文件中的程序进行了修改。在这个修改之后，`COPY` 命令将需要重新运行，以便这些更改出现在镜像中。换句话说，Docker 将使该层的缓存失效。

如果一个层发生变化，它之后的所有其他层也会受到影响。当带有 `COPY` 命令的层被失效时，所有后续的层也需要重新运行：

![显示缓存失效的镜像层示意图](../images/cache-stack-invalidated.png)

这就是 Docker 构建缓存的要点。一旦一个层发生变化，那么所有下游的层都需要重新构建。即使它们不会以不同的方式构建任何内容，它们仍然需要重新运行。

## 其他资源

有关使用缓存进行高效构建的更多信息，请参阅：

- [缓存失效](invalidation.md)
- [优化构建缓存](optimization.md)
- [垃圾回收](garbage-collection.md)
- [缓存存储后端](./backends/_index.md)
