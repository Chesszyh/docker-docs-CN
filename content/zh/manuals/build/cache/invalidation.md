---
title: 构建缓存失效 (Cache invalidation)
description: 深入了解 Docker 构建缓存失效的工作机制
keywords: build, buildx, buildkit, cache, invalidation, cache miss, 缓存失效, 缓存未命中
---

构建镜像时，Docker 会逐步执行 Dockerfile 中的指令，并按指定的顺序执行每一条。对于每条指令，[构建器](/manuals/build/builders/_index.md) 都会检查是否可以从构建缓存中复用该指令的结果。

## 通用规则

构建缓存失效的基本规则如下：

- 构建器首先检查基础镜像是否已被缓存。之后的每一条指令都会与缓存层进行对比。如果没有缓存层与该指令完全匹配，则缓存失效。

- 在大多数情况下，仅需对比 Dockerfile 指令与对应的缓存层即可。然而，某些指令需要额外的检查和说明。

- 对于 `ADD` 和 `COPY` 指令，以及带有绑定挂载的 `RUN` 指令 (`RUN --mount=type=bind`)，构建器会根据文件元数据计算一个缓存校验和 (checksum)，以确定缓存是否有效。在缓存查找期间，如果涉及的任何文件的元数据发生了变化，缓存就会失效。

  计算缓存校验和时不会考虑文件的修改时间 (`mtime`)。如果仅复制文件的 `mtime` 发生了变化，缓存不会失效。

- 除了 `ADD` 和 `COPY` 命令外，缓存检查不会查看容器内的文件来确定缓存匹配。例如，在处理 `RUN apt-get -y update` 命令时，不会检查容器中更新的文件来确定是否存在缓存命中。在这种情况下，仅使用命令字符串本身来查找匹配项。

一旦缓存失效，所有后续的 Dockerfile 命令都将生成新镜像，不再使用缓存。

如果您的构建包含多个层，并且您希望确保构建缓存是可复用的，请尽可能将指令按更改频率从低到高排列。

## RUN 指令

`RUN` 指令的缓存不会在构建之间自动失效。假设您的 Dockerfile 中有一个安装 `curl` 的步骤：

```dockerfile
FROM alpine:{{% param "example_alpine_version" %}} AS install
RUN apk add curl
```

这并不意味着您镜像中的 `curl` 版本始终是最新的。一周后重新构建镜像仍会得到与之前相同的软件包。要强制重新执行 `RUN` 指令，您可以：

- 确保其之前的某一层发生了变化
- 在构建前使用 [`docker builder prune`](/reference/cli/docker/builder/prune.md) 清除构建缓存
- 使用 `--no-cache` 或 `--no-cache-filter` 选项

`--no-cache-filter` 选项允许您指定使特定构建阶段的缓存失效：

```console
$ docker build --no-cache-filter install .
```

## 构建机密 (Build secrets)

构建机密的内容不属于构建缓存的一部分。更改机密的值不会导致缓存失效。

如果您想在更改机密值后强制使缓存失效，可以传递一个带有任意值的构建参数，并在更改机密时同时更改该参数。构建参数会导致缓存失效。

```dockerfile
FROM alpine
ARG CACHEBUST
RUN --mount=type=secret,id=TOKEN,env=TOKEN \
    some-command ...
```

```console
$ TOKEN="tkn_pat123456" docker build --secret id=TOKEN --build-arg CACHEBUST=1 .
```

机密的属性（如 ID 和挂载路径）会参与缓存校验和计算，如果发生更改，会导致缓存失效。