---
title: 在 Bake 中使用附加上下文
linkTitle: 上下文
weight: 80
description: |
  当您想要固定镜像版本或引用其他目标的输出时，附加上下文非常有用
keywords: build, buildx, bake, buildkit, hcl
alias:
  - /build/customize/bake/build-contexts/
  - /build/bake/build-contexts/
---

除了定义构建上下文的主要 `context` 键之外，每个目标还可以使用定义为 `contexts` 键的映射来定义附加的命名上下文。这些值映射到 [build 命令](/reference/cli/docker/buildx/build.md#build-context) 中的 `--build-context` 标志。

在 Dockerfile 内部，这些上下文可以与 `FROM` 指令或 `--from` 标志一起使用。

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
    alpine = "docker-image://alpine:3.13"
  }
}
```

## 使用辅助源目录

```dockerfile {title=Dockerfile}
FROM golang
COPY --from=src . .
```

```hcl {title=docker-bake.hcl}
# 运行 `docker buildx bake app` 将导致 `src` 指向客户端文件系统，
# 而不是某个先前的构建阶段，这不属于上下文的一部分。
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

在大多数情况下，您应该只使用具有多个目标的单个多阶段 Dockerfile 来实现类似的行为。只有当您有多个无法轻松合并为一个的 Dockerfile 时，才建议使用这种情况。

## 去重上下文传输

> [!NOTE]
> 
> 从 Buildx 版本 0.17.0 及更高版本开始，Bake 会自动为共享相同上下文的目标去重上下文传输。除了 Buildx 版本 0.17.0 之外，构建器必须运行 BuildKit 版本 0.16.0 或更高版本，并且 Dockerfile 语法必须是 `docker/dockerfile:1.10` 或更高版本。
> 
> 如果您满足这些要求，则不需要按照本节所述手动去重上下文传输。
> 
> - 要检查您的 Buildx 版本，请运行 `docker buildx version`。
> - 要检查您的 BuildKit 版本，请运行 `docker buildx inspect --bootstrap` 并查找 `BuildKit version` 字段。
> - 要检查您的 Dockerfile 语法版本，请检查 Dockerfile 中的 `syntax` [解析器指令](/reference/dockerfile.md#syntax)。如果不存在，则默认版本为当前 BuildKit 版本捆绑的任何版本。要显式设置版本，请在 Dockerfile 顶部添加 `#syntax=docker/dockerfile:1.10`。

当您使用组并发构建目标时，构建上下文将为每个目标独立加载。如果组中的多个目标使用相同的上下文，则每次使用该上下文时都会传输一次。这可能会对构建时间产生重大影响，具体取决于您的构建配置。例如，假设您有一个定义了以下目标组的 Bake 文件：

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

在这种情况下，当您构建默认组时，上下文 `.` 会传输两次：一次用于 `target1`，一次用于 `target2`。

如果您的上下文很小，并且您使用的是本地构建器，重复的上下文传输可能没什么大不了的。但是，如果您的构建上下文很大，或者您有大量目标，或者您正在通过网络将上下文传输到远程构建器，上下文传输将成为性能瓶颈。

为了避免多次传输相同的上下文，您可以定义一个仅加载上下文文件的命名上下文，并让每个需要这些文件的目标引用该命名上下文。例如，以下 Bake 文件定义了一个命名目标 `ctx`，`target1` 和 `target2` 都使用了它：

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
