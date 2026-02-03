---
title: 优化构建中的缓存利用
description: 优化 Docker 构建中缓存利用率的概览。
keywords: build, buildkit, buildx, guide, tutorial, mounts, cache mounts, bind mounts, 优化, 缓存, 挂载, 缓存挂载
aliases:
  - /build/guide/mounts/
---


使用 Docker 进行构建时，如果某条指令及其依赖的文件自上次构建以来未发生变化，则会从构建缓存中复用该层。复用缓存层可以显著加快构建过程，因为 Docker 无需重新执行该层。

以下是几种优化构建缓存并提升构建速度的技术：

- [对层进行排序](#对层进行排序)：按逻辑顺序排列 Dockerfile 中的命令，有助于避免不必要的缓存失效。
- [保持较小的上下文](#保持较小的上下文)：上下文是指发送给构建器以处理构建指令的一组文件和目录。尽可能保持较小的上下文，可以减少发送给构建器的数据量，并降低缓存失效的可能性。
- [使用绑定挂载 (Bind mounts)](#使用绑定挂载)：绑定挂载允许您将宿主机上的文件或目录挂载到构建容器中。使用绑定挂载可以帮助您避免在镜像中产生不必要的层，从而加快构建过程。
- [使用缓存挂载 (Cache mounts)](#使用缓存挂载)：缓存挂载允许您指定构建期间使用的持久化软件包缓存。持久化缓存有助于加快构建步骤，特别是涉及使用包管理器安装软件包的步骤。有了持久化的软件包缓存，即使重新构建某一层，也只需下载新增加或发生变化的包。
- [使用外部缓存](#使用外部缓存)：外部缓存允许您将构建缓存存储在远程位置。外部缓存镜像可以在多个构建任务以及不同的环境之间共享。

## 对层进行排序

将 Dockerfile 中的命令按逻辑顺序排列是一个很好的起点。由于任何更改都会导致其后的所有步骤重新构建，因此请尽量将昂贵的步骤放在 Dockerfile 的开头。变动频繁的步骤应放在 Dockerfile 的末尾，以避免触发未发生变化的层的重新构建。

考虑以下示例。这是一个从当前目录源代码运行 JavaScript 构建的 Dockerfile 代码片段：

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY . .          # 复制当前目录下的所有文件
RUN npm install   # 安装依赖
RUN npm build     # 运行构建
```

这个 Dockerfile 的效率相当低。每次构建 Docker 镜像时，即使依赖项自上次以来未发生变化，更新任何文件都会导致所有依赖项重新安装。

相反，我们可以将 `COPY` 命令拆分为两步。首先，复制包管理文件（在此例中为 `package.json` 和 `yarn.lock`）。然后，安装依赖项。最后，复制经常发生变动的项目源代码。

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY package.json yarn.lock .    # 复制包管理文件
RUN npm install                  # 安装依赖
COPY . .                         # 复制项目文件
RUN npm build                    # 运行构建
```

通过在 Dockerfile 较早的层中安装依赖项，当项目文件发生更改时，就没有必要重新构建这些层了。

## 保持较小的上下文

确保您的上下文不包含不必要文件的最简单方法是在构建上下文的根目录下创建一个 `.dockerignore` 文件。`.dockerignore` 文件的作用类似于 `.gitignore` 文件，允许您从构建上下文中排除文件和目录。

以下是一个 `.dockerignore` 文件示例，排除了 `node_modules` 目录以及所有以 `tmp` 开头的文件和目录：

```plaintext {title=".dockerignore"}
node_modules
tmp*
```

在 `.dockerignore` 文件中指定的忽略规则适用于整个构建上下文（包括子目录）。这意味着它是一个较为粗粒度的机制，但它是排除您确定不需要在构建上下文中的文件和目录的好方法，例如临时文件、日志文件和构建产物。

## 使用绑定挂载 (Bind mounts)

您可能已经熟悉使用 `docker run` 或 Docker Compose 运行容器时的绑定挂载。绑定挂载允许您将宿主机上的文件或目录挂载到容器中。

```bash
# 使用 -v 标志进行绑定挂载
docker run -v $(pwd):/path/in/container image-name
# 使用 --mount 标志进行绑定挂载
docker run --mount=type=bind,src=.,dst=/path/in/container image-name
```

要在构建中使用绑定挂载，您可以在 Dockerfile 的 `RUN` 指令中使用 `--mount` 标志：

```dockerfile
FROM golang:latest
WORKDIR /app
RUN --mount=type=bind,target=. go build -o /app/hello
```

在此示例中，在执行 `go build` 命令之前，当前目录被挂载到了构建容器中。源代码在该 `RUN` 指令执行期间在构建容器内可用。指令执行完成后，挂载的文件不会持久化在最终镜像或构建缓存中。仅保留 `go build` 命令的输出。

Dockerfile 中的 `COPY` 和 `ADD` 指令允许您将文件从构建上下文复制到构建容器中。使用绑定挂载对优化构建缓存很有利，因为您不会在缓存中增加不必要的层。如果您的构建上下文较大且仅用于生成产物，最好使用绑定挂载暂时将生成该产物所需的源码挂载到构建中。如果您使用 `COPY` 将文件添加到构建容器，BuildKit 会将所有这些文件包含在缓存中，即使这些文件在最终镜像中并未被使用。

在构建中使用绑定挂载时，有几点需要注意：

- 默认情况下，绑定挂载是只读的。如果您需要向挂载的目录写入数据，需要指定 `rw` 选项。然而，即使使用了 `rw` 选项，更改也不会持久化在最终镜像或构建缓存中。文件写入仅在 `RUN` 指令执行期间有效，并在指令完成后被丢弃。
- 挂载的文件不会持久化在最终镜像中。只有 `RUN` 指令的输出会持久化。如果您需要在最终镜像中包含构建上下文中的文件，则必须使用 `COPY` 或 `ADD` 指令。
- 如果目标目录不为空，目标目录的原有内容将被挂载的文件遮蔽。原有内容将在 `RUN` 指令完成后恢复。

  {{< accordion title="示例" >}}

  例如，假设构建上下文中仅有一个 `Dockerfile`：

  ```plaintext
  .
  └── Dockerfile
  ```

  以及一个将当前目录挂载到构建容器中的 Dockerfile：

  ```dockerfile
  FROM alpine:latest
  WORKDIR /work
  RUN touch foo.txt
  RUN --mount=type=bind,target=. ls
  RUN ls
  ```

  第一条带绑定挂载的 `ls` 命令显示挂载目录的内容。第二条 `ls` 则列出原始构建上下文的内容。

  ```plaintext {title="构建日志"}
  #8 [stage-0 3/5] RUN touch foo.txt
  #8 DONE 0.1s
  
  #9 [stage-0 4/5] RUN --mount=target=. ls -1
  #9 0.040 Dockerfile
  #9 DONE 0.0s
  
  #10 [stage-0 5/5] RUN ls -1
  #10 0.046 foo.txt
  #10 DONE 0.1s
  ```

  {{< /accordion >}}

## 使用缓存挂载 (Cache mounts)

Docker 中的常规缓存层对应于指令及其依赖文件的精确匹配。如果指令或其依赖的文件自该层构建以来发生了变化，该层就会失效，构建过程必须重新构建该层。

缓存挂载是指定构建期间使用的持久化缓存位置的一种方式。缓存是跨构建累积的，因此您可以多次读写该缓存。这种持久化缓存意味着即使您需要重新构建某一层，也只需下载新增或发生变化的包。任何未发生变化的包都会从缓存挂载中复用。

要在构建中使用缓存挂载，您可以在 Dockerfile 的 `RUN` 指令中使用 `--mount` 标志：

```dockerfile
FROM node:latest
WORKDIR /app
RUN --mount=type=cache,target=/root/.npm npm install
```

在此示例中，`npm install` 命令为 `/root/.npm` 目录（npm 缓存的默认位置）使用了缓存挂载。该缓存挂载会跨构建持久化，因此即使您最终重新构建了该层，也只需下载新包或已变动的包。对缓存的任何更改都会在不同构建之间保留，且缓存可在多个构建任务间共享。

具体如何指定缓存挂载取决于您使用的构建工具。如果您不确定如何指定，请参考所用构建工具的文档。以下是一些示例：

{{< tabs >}}
{{< tab name="Go" >}}

```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    go build -o /app/hello
```

{{< /tab >}}
{{< tab name="Apt" >}}

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt-get --no-install-recommends install -y gcc
```

{{< /tab >}}
{{< tab name="Python" >}}

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

{{< /tab >}}
{{< tab name="Ruby" >}}

```dockerfile
RUN --mount=type=cache,target=/root/.gem \
    bundle install
```

{{< /tab >}}
{{< tab name="Rust" >}}

```dockerfile
RUN --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/git/db \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    cargo build
```

{{< /tab >}}
{{< tab name=".NET" >}}

```dockerfile
RUN --mount=type=cache,target=/root/.nuget/packages \
    dotnet restore
```

{{< /tab >}}
{{< tab name="PHP" >}}  

```dockerfile
RUN --mount=type=cache,target=/tmp/cache \
    composer install
```

{{< /tab >}}
{{< /tabs >}}

请务必阅读所用构建工具的文档，以确保使用了正确的缓存挂载选项。不同的包管理器对如何使用缓存有不同的要求，使用错误的选项可能会导致非预期的行为。例如，Apt 需要独占访问其数据，因此这些缓存使用 `sharing=locked` 选项，以确保使用相同缓存挂载的并行构建相互等待，而不会同时访问相同的缓存文件。

## 使用外部缓存

构建任务的默认缓存存储位于您正在使用的构建器（BuildKit 实例）内部。每个构建器都有自己的缓存存储。当您在不同构建器之间切换时，缓存是不共享的。使用外部缓存可以让您定义一个远程位置来推送和拉取缓存数据。

外部缓存对于 CI/CD 流水线特别有用，因为那里的构建器通常是临时的，且构建时长非常宝贵。在不同构建任务间复用缓存可以大幅加快构建过程并降低成本。您甚至可以在本地开发环境中使用同样的缓存。

要使用外部缓存，请在 `docker buildx build` 命令中指定 `--cache-to` 和 `--cache-from` 选项。

- `--cache-to`：将构建缓存导出到指定位置。
- `--cache-from`：指定构建要使用的远程缓存。

以下示例展示了如何使用 `docker/build-push-action` 设置 GitHub Actions 工作流，并将构建缓存层推送到 OCI 注册表镜像：

```yaml {title=".github/workflows/ci.yml"}
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: 登录到 Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: 设置 Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: 构建并推送
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

此设置告知 BuildKit 在 `user/app:buildcache` 镜像中寻找缓存。构建完成后，新的构建缓存会被推送到同一个镜像中，覆盖旧的缓存。

此缓存也可以在本地使用。要在本地构建中拉取缓存，可以在 `docker buildx build` 命令中使用 `--cache-from` 选项：

```console
$ docker buildx build --cache-from type=registry,ref=user/app:buildcache .
```

## 总结

优化构建中的缓存利用可以显著加快构建过程。保持较小的构建上下文、使用绑定挂载、缓存挂载以及外部缓存，都是您可以用来充分利用构建缓存并提升构建效率的技术。

欲了解更多关于本指南中讨论的概念，请参阅：

- [.dockerignore 文件](/manuals/build/concepts/context.md#dockerignore-文件)
- [缓存失效 (Cache invalidation)](/manuals/build/cache/invalidation.md)
- [缓存挂载 (Cache mounts)](/reference/dockerfile.md#run---mounttypecache)
- [缓存后端类型](/manuals/build/cache/backends/_index.md)
- [构建最佳实践](/manuals/build/building/best-practices.md)