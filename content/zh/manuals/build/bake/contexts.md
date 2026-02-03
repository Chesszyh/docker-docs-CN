---
title: 配合额外上下文使用 Bake
linkTitle: 上下文 (Contexts)
weight: 80
description: |
  当您想要固定镜像版本或引用其他目标的输出时，额外的上下文非常有用
keywords: build, buildx, bake, buildkit, hcl, 上下文
---

除了定义主构建上下文的 `context` 键外，每个目标还可以通过 `contexts` 键定义的映射来定义额外的命名上下文。这些值对应于 [build 命令](/reference/cli/docker/buildx/build.md#build-context) 中的 `--build-context` 标志。

在 Dockerfile 内部，这些上下文可以配合 `FROM` 指令或 `--from` 标志使用。

支持的上下文值包括：

- 本地文件系统目录
- 容器镜像
- Git URL
- HTTP URL
- Bake 文件中另一个目标的名称

## 固定 alpine 镜像版本

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello world"
```

```hcl {title=docker-bake.hcl}
target "app" {
  contexts = {
    alpine = "docker-image://alpine:3.13"
  }
}
```

## 使用备用源码目录

```dockerfile {title=Dockerfile}
FROM golang
COPY --from=src . .
```

```hcl {title=docker-bake.hcl}
# 运行 `docker buildx bake app` 会导致 `src` 不再指向
# 之前的某个构建阶段，而是指向客户端文件系统，不属于主上下文。
target "app" {
  contexts = {
    src = "../path/to/source"
  }
}
```

## 使用目标作为构建上下文

要将一个目标的结果用作另一个目标的构建上下文，请使用 `target:` 前缀指定目标名称。

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

在大多数情况下，对于相似的行为，您应该仅使用包含多个目标的单个多阶段 Dockerfile。此案例仅在您有多个无法轻松合并为一个的 Dockerfile 时才推荐使用。

## 上下文传输去重

> [!NOTE]
> 
> 自 Buildx 0.17.0 及更高版本起，Bake 会自动为共享相同上下文的目标执行上下文传输去重。除了要求 Buildx 版本 0.17.0 外，构建器必须运行 BuildKit 0.16.0 或更高版本，且 Dockerfile 语法必须为 `docker/dockerfile:1.10` 或更高。
> 
> 如果您满足这些要求，则无需按照本节所述手动进行上下文传输去重。
> 
> - 要检查 Buildx 版本，运行 `docker buildx version`。
> - 要检查 BuildKit 版本，运行 `docker buildx inspect --bootstrap` 并查看 `BuildKit version` 字段。
> - 要检查 Dockerfile 语法版本，查看 Dockerfile 中的 `syntax` [解析器指令](/reference/dockerfile.md#syntax)。如果不存在，则默认为当前 BuildKit 版本捆绑的版本。要显式设置版本，请在 Dockerfile 顶部添加 `#syntax=docker/dockerfile:1.10`。

当您使用组 (groups) 并发构建目标时，构建上下文会为每个目标独立加载。如果组中的多个目标使用了相同的上下文，那么该上下文在每次使用时都会被传输一次。根据您的构建配置，这可能会对构建时间产生重大影响。例如，假设您有一个定义了以下目标组的 Bake 文件：

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

在这种情况下，当您构建 `default` 组时，上下文 `.` 会被传输两次：一次针对 `target1`，另一次针对 `target2`。

如果您的上下文很小，并且您使用的是本地构建器，重复的上下文传输可能不是什么大问题。但如果您的构建上下文很大，或者您有大量的目标，或者您是通过网络向远程构建器传输上下文，那么上下文传输就会成为性能瓶颈。

为了避免多次传输相同的上下文，您可以定义一个仅加载上下文文件的命名上下文，并让每个需要这些文件的目标引用该命名上下文。例如，以下 Bake 文件定义了一个命名目标 `ctx`，它被 `target1` 和 `target2` 共同使用：

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

命名上下文 `ctx` 代表一个 Dockerfile 阶段，它从其上下文 (`.`) 复制文件。Dockerfile 中的其他阶段现在可以引用 `ctx` 命名上下文，例如，使用 `--mount=from=ctx` 挂载其文件。

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