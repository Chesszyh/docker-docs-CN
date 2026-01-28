---
title: 构建缓存失效
description: 深入了解 Docker 构建缓存失效的工作原理
keywords: build, buildx, buildkit, cache, invalidation, cache miss
---

在构建镜像时，Docker 按照 Dockerfile 中指定的顺序逐步执行指令。对于每条指令，[构建器](/manuals/build/builders/_index.md)会检查是否可以从构建缓存中重用该指令。

## 一般规则

构建缓存失效的基本规则如下：

- 构建器首先检查基础镜像是否已经被缓存。每条后续指令都与缓存的层进行比较。如果没有缓存的层与该指令完全匹配，则缓存失效。

- 在大多数情况下，将 Dockerfile 指令与相应的缓存层进行比较就足够了。但是，某些指令需要额外的检查和说明。

- 对于 `ADD` 和 `COPY` 指令，以及带有绑定挂载的 `RUN` 指令（`RUN --mount=type=bind`），构建器根据文件元数据计算缓存校验和，以确定缓存是否有效。在缓存查找期间，如果涉及的任何文件的文件元数据发生变化，则缓存失效。

  在计算缓存校验和时，不会考虑文件的修改时间（`mtime`）。如果只有复制文件的 `mtime` 发生变化，缓存不会失效。

- 除了 `ADD` 和 `COPY` 命令外，缓存检查不会查看容器中的文件来确定缓存匹配。例如，在处理 `RUN apt-get -y update` 命令时，不会检查容器中更新的文件来确定是否存在缓存命中。在这种情况下，仅使用命令字符串本身来查找匹配项。

一旦缓存失效，所有后续的 Dockerfile 命令都会生成新镜像，并且不再使用缓存。

如果你的构建包含多个层，并且你希望确保构建缓存可重用，请尽可能将指令按照从较少更改到较频繁更改的顺序排列。

## RUN 指令

`RUN` 指令的缓存不会在构建之间自动失效。假设你的 Dockerfile 中有一个安装 `curl` 的步骤：

```dockerfile
FROM alpine:{{% param "example_alpine_version" %}} AS install
RUN apk add curl
```

这并不意味着你镜像中的 `curl` 版本始终是最新的。一周后重新构建镜像仍然会得到与之前相同的包。要强制重新执行 `RUN` 指令，你可以：

- 确保它之前的某个层发生了变化
- 在构建之前使用 [`docker builder prune`](/reference/cli/docker/builder/prune.md) 清除构建缓存
- 使用 `--no-cache` 或 `--no-cache-filter` 选项

`--no-cache-filter` 选项允许你指定要使其缓存失效的特定构建阶段：

```console
$ docker build --no-cache-filter install .
```

## 构建密钥

构建密钥的内容不是构建缓存的一部分。更改密钥的值不会导致缓存失效。

如果你想在更改密钥值后强制缓存失效，可以传递一个具有任意值的构建参数，并在更改密钥时也更改该参数。构建参数确实会导致缓存失效。

```dockerfile
FROM alpine
ARG CACHEBUST
RUN --mount=type=secret,id=TOKEN,env=TOKEN \
    some-command ...
```

```console
$ TOKEN="tkn_pat123456" docker build --secret id=TOKEN --build-arg CACHEBUST=1 .
```

密钥的属性（如 ID 和挂载路径）确实参与缓存校验和计算，如果更改则会导致缓存失效。
