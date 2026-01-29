---
title: 在 Bake 中使用附加上下文
linkTitle: 上下文 (Contexts)
weight: 80
description: |
  当您想要固定镜像版本或引用其他目标的输出时，附加上下文非常有用
keywords: build, buildx, bake, buildkit, hcl
alias:
  - /build/customize/bake/build-contexts/
  - /build/bake/build-contexts/
---

除了定义构建上下文的主 `context` 键之外，每个目标还可以通过 `contexts` 键定义的映射来定义额外的具名上下文。这些值对应于 [构建命令](/reference/cli/docker/buildx/build.md#build-context) 中的 `--build-context` 标志。

在 Dockerfile 内部，这些上下文可以与 `FROM` 指令或 `--from` 标志配合使用。

支持的上下文值包括：

- 本地文件系统目录
- 容器镜像
- Git URL
- HTTP URL
- Bake 文件中另一个目标的名称

## 固定 alpine 镜像

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello world"
```

```hcl {title=docker-bake.hcl}
target "app" {
  contexts = {
    alpine = "docker-image://alpine:313"
  }
}
```

## 使用辅助源目录

```dockerfile {title=Dockerfile}
FROM golang
COPY --from=src . .
```

```hcl {title=docker-bake.hcl}
# 运行 `docker buildx bake app` 将导致 `src` 不指向
# 之前的某个构建阶段，而是指向客户端文件系统，不属于上下文的一部分。
target "app" {
  contexts = {
    src = "../path/to/source"
  }
}
```

## 使用目标作为构建上下文

要将一个目标的结果用作另一个目标的构建上下文，请指定带有 `target:` 前缀的目标名称。

```dockerfile {title=baseapp.Dockerfile}
FROM scratch
```
```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
FROM baseapp
RUN echo "Hello world"
```

```hcl {title=docker-bake.hcl}
target "base" {
  dockerfile = "baseapp.Dockerfile"
}

target "app" {
  contexts = {
    baseapp = "target:base"
  }
}
```

在大多数情况下，您应该只使用带有多个目标的单个多阶段 Dockerfile 来实现类似的行为。仅当您有多个无法轻松合并为一个的 Dockerfile 时，才推荐使用此方案。

## 去重上下文传输

> [!NOTE] 
> 
> 自 Buildx 0.17.0 版本起，Bake 会自动为共享相同上下文的目标去重上下文传输。除了 Buildx 0.17.0 外，构建器必须运行 BuildKit 0.16.0 或更高版本，且 Dockerfile 语法必须为 `docker/dockerfile:1.10` 或更高版本。
> 
> 如果您满足这些要求，则不需要按照本节所述手动去重上下文传输。
> 
> - 要检查您的 Buildx 版本，请运行 `docker buildx version`。
> - 要检查您的 BuildKit 版本，请运行 `docker buildx inspect --bootstrap` 并查看 `BuildKit version` 字段。
> - 要检查您的 Dockerfile 语法版本，请查看 Dockerfile 中的 `syntax` [解析器指令](/reference/dockerfile.md#syntax)。如果不存在，则默认版本为当前 BuildKit 版本随附的版本。要显式设置版本，请在 Dockerfile 顶部添加 `#syntax=docker/dockerfile:1.10`。

当您使用组（group）并发构建目标时，每个目标的构建上下文都是独立加载的。如果组中的多个目标使用了相同的上下文，那么该上下文在每次使用时都会被传输一次。根据您的构建配置，这可能会对构建时间产生重大影响。例如，假设您有一个 Bake 文件定义了以下目标组：

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["target1", "target2"]
}

target "target1" {
  target = "target1"
  context = "."
}

target "target2" {
  target = "target2"
  context = "."
}
```

在这种情况下，当您构建默认组时，上下文 `.` 会被传输两次：一次用于 `target1`，一次用于 `target2`。

如果您的上下文很小，或者您使用的是本地构建器，重复的上下文传输可能不是什么大问题。但如果您的构建上下文很大，或者您有大量的目标，或者您是通过网络将上下文传输到远程构建器，那么上下文传输就会成为性能瓶颈。

为了避免多次传输相同的上下文，您可以定义一个仅加载上下文文件的具名上下文，并让每个需要这些文件的目标引用该具名上下文。例如，以下 Bake 文件定义了一个名为 `ctx` 的目标，`target1` 和 `target2` 都会用到它：

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["target1", "target2"]
}

target "ctx" {
  context = "."
  target = "ctx"
}

target "target1" {
  target = "target1"
  contexts = {
    ctx = "target:ctx"
  }
}

target "target2" {
  target = "target2"
  contexts = {
    ctx = "target:ctx"
  }
}
```

具名上下文 `ctx` 代表一个 Dockerfile 阶段，它从其上下文（`.`）中复制文件。Dockerfile 中的其他阶段现在可以引用 `ctx` 具名上下文，例如，使用 `--mount=from=ctx` 挂载其文件。

```dockerfile {title=Dockerfile}
FROM scratch AS ctx
COPY --link . .

FROM golang:alpine AS target1
WORKDIR /work
RUN --mount=from=ctx \
    go build -o /out/client ./cmd/client \

FROM golang:alpine AS target2
WORKDIR /work
RUN --mount=from=ctx \
    go build -o /out/server ./cmd/server
```
