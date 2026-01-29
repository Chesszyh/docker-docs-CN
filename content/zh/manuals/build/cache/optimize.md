--- 
title: 优化构建中的缓存使用
description: 关于如何优化 Docker 构建中缓存利用率的概览。
keywords: build, buildkit, buildx, 指南, 教程, 挂载, 缓存挂载, 绑定挂载
alias:
  - /build/guide/mounts/
---


使用 Docker 构建时，如果指令及其依赖的文件自上次构建以来没有发生变化，就会从构建缓存中重用该层。重用缓存层可以加快构建过程，因为 Docker 不必再次重新构建该层。

以下是几种可用于优化构建缓存并加快构建过程的技术：

- [调整层顺序](#调整层顺序)：将 Dockerfile 中的命令按逻辑顺序排列，可以帮助您避免不必要的缓存失效。
- [保持上下文精简](#保持上下文精简)：上下文是发送到构建器以处理构建指令的文件和目录集。保持上下文尽可能小可以减少需要发送到构建器的数据量，并降低缓存失效的可能性。
- [使用绑定挂载 (Bind mounts)](#使用绑定挂载)：绑定挂载允许您将宿主机上的文件或目录挂载到构建容器中。使用绑定挂载可以帮助您避免在镜像中产生不必要的层，从而减慢构建过程。
- [使用缓存挂载 (Cache mounts)](#使用缓存挂载)：缓存挂载允许您指定构建期间使用的持久化软件包缓存。持久化缓存有助于加快构建步骤，特别是涉及使用包管理器安装软件包的步骤。拥有持久化的软件包缓存意味着即使您重新构建某一层，也只需下载新包或已更改的包。
- [使用外部缓存](#使用外部缓存)：外部缓存允许您将构建缓存存储在远程位置。外部缓存镜像可以在多个构建之间以及不同环境之间共享。

## 调整层顺序

将 Dockerfile 中的命令按逻辑顺序排列是一个很好的起点。因为一项更改会导致后续步骤重新构建，所以请尝试将代价高昂的步骤放在 Dockerfile 的开头附近。经常变动的步骤应该放在 Dockerfile 的末尾附近，以避免触发未变动层的重新构建。

考虑以下示例。一个从当前目录中的源文件运行 JavaScript 构建的 Dockerfile 代码片段：

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY . .          # 复制当前目录下的所有文件
RUN npm install   # 安装依赖项
RUN npm build     # 运行构建
```

这个 Dockerfile 相当低效。每次构建 Docker 镜像时，更新任何文件都会导致重新安装所有依赖项，即使依赖项自上次以来并未发生变化。

相反，`COPY` 命令可以一分为二。首先，复制包管理文件（在本例中为 `package.json` 和 `yarn.lock`）。然后，安装依赖项。最后，复制项目源代码，因为源代码经常变动。

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY package.json yarn.lock .
RUN npm install                  # 安装依赖项
COPY . .
RUN npm build                    # 运行构建
```

通过在 Dockerfile 的较早层安装依赖项，当项目文件发生更改时，就无需重新构建这些层。

## 保持上下文精简

确保上下文不包含不必要文件的最简单方法是在构建上下文的根目录中创建一个 `.dockerignore` 文件。`.dockerignore` 文件的工作方式与 `.gitignore` 文件类似，允许您从构建上下文中排除文件和目录。

以下是一个 `.dockerignore` 文件示例，它排除了 `node_modules` 目录以及所有以 `tmp` 开头的文件和目录：

```plaintext {title=".dockerignore"}
node_modules
tmp*
```

`.dockerignore` 文件中指定的忽略规则适用于整个构建上下文，包括子目录。这意味着它是一个相当粗粒度的机制，但它是排除您知道在构建上下文中不需要的文件和目录的好方法，例如临时文件、日志文件和构建产物。

## 使用绑定挂载

您可能对使用 `docker run` 或 Docker Compose 运行容器时的绑定挂载很熟悉。绑定挂载允许您将宿主机上的文件或目录挂载到容器中。

```bash
# 使用 -v 标志进行绑定挂载
docker run -v $(pwd):/path/in/container image-name
# 使用 --mount 标志进行绑定挂载
docker run --mount=type=bind,src=.,dst=/path/in/container image-name
```

要在构建中使用绑定挂载，可以在 Dockerfile 的 `RUN` 指令中使用 `--mount` 标志：

```dockerfile
FROM golang:latest
WORKDIR /app
RUN --mount=type=bind,target=. go build -o /app/hello
```

在此示例中，在执行 `go build` 命令之前，当前目录被挂载到构建容器中。源代码在 `RUN` 指令执行期间在构建容器中可用。当指令执行完毕时，挂载的文件不会持久化在最终镜像或构建缓存中。仅保留 `go build` 命令的输出。

Dockerfile 中的 `COPY` 和 `ADD` 指令允许您将文件从构建上下文复制到构建容器中。使用绑定挂载有利于优化构建缓存，因为您不会向缓存中添加不必要的层。如果您的构建上下文较大，且仅用于生成构件，那么最好使用绑定挂载将生成构件所需的源代码临时挂载到构建中。如果您使用 `COPY` 将文件添加到构建容器，BuildKit 会将所有这些文件包含在缓存中，即使这些文件在最终镜像中并未被使用。

在构建中使用绑定挂载时，有几点需要注意：

- 默认情况下，绑定挂载是只读的。如果您需要写入挂载目录，需要指定 `rw` 选项。但是，即使使用了 `rw` 选项，更改也不会持久化在最终镜像或构建缓存中。文件写入仅在 `RUN` 指令执行期间维持，并在指令完成后被丢弃。
- 挂载的文件不会持久化在最终镜像中。只有 `RUN` 指令的输出才会持久化在最终镜像中。如果您需要在最终镜像中包含来自构建上下文的文件，则需要使用 `COPY` 或 `ADD` 指令。
- 如果目标目录不为空，目标目录的内容会被挂载的文件隐藏。原内容将在 `RUN` 指令完成后恢复。

  {{< accordion title="示例" >}}

  例如，假设构建上下文中只有一个 `Dockerfile`：

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

  第一个带有绑定挂载的 `ls` 命令显示挂载目录的内容。第二个 `ls` 列出原始构建上下文的内容。

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

## 使用缓存挂载

Docker 中的常规缓存层对应于指令及其依赖文件的精确匹配。如果指令及依赖的文件自该层构建以来已发生更改，则该层将失效，构建过程必须重新构建该层。

缓存挂载是一种指定构建期间使用的持久化缓存位置的方法。缓存可以跨构建累积，因此您可以多次读取和写入缓存。这种持久化缓存意味着即使您需要重新构建某一层，也只需下载新包或已更改的包。任何未更改的包都会从缓存挂载中重用。

要在构建中使用缓存挂载，可以在 Dockerfile 的 `RUN` 指令中使用 `--mount` 标志：

```dockerfile
FROM node:latest
WORKDIR /app
RUN --mount=type=cache,target=/root/.npm npm install
```

在此示例中，`npm install` 命令为 `/root/.npm` 目录（npm 缓存的默认位置）使用缓存挂载。缓存挂载在构建之间持久存在，因此即使您最终重新构建了该层，也只需下载新包或已更改的包。对缓存的任何更改都会在构建之间持久存在，并且缓存在多个构建之间共享。

如何指定缓存挂载取决于您使用的构建工具。如果您不确定如何指定缓存挂载，请参阅所用构建工具的文档。以下是一些示例：

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

务必阅读所用构建工具的文档，以确保使用了正确的缓存挂载选项。包管理器对其使用缓存的方式有不同的要求，使用错误的选项可能会导致意外行为。例如，Apt 需要对其数据进行排他性访问，因此缓存使用 `sharing=locked` 选项，以确保使用相同缓存挂载的并行构建相互等待，而不是同时访问相同的缓存文件。

## 使用外部缓存

构建的默认缓存存储位于您使用的构建器（BuildKit 实例）内部。每个构建器使用自己的缓存存储。当您在不同的构建器之间切换时，缓存不会在它们之间共享。使用外部缓存允许您定义一个远程位置来推送和拉取缓存数据。

外部缓存对于 CI/CD 流水线特别有用，因为那里的构建器通常是临时的，且构建时长非常宝贵。在构建之间重用缓存可以极大地加快构建过程并降低成本。您甚至可以在本地开发环境中使用相同的缓存。

要使用外部缓存，请在 `docker buildx build` 命令中指定 `--cache-to` 和 `--cache-from` 选项。

- `--cache-to` 将构建缓存导出到指定位置。
- `--cache-from` 指定构建要使用的远程缓存。

以下示例显示了如何使用 `docker/build-push-action` 设置 GitHub Actions 工作流，并将构建缓存层推送到 OCI 镜像库镜像：

```yaml {title=".github/workflows/ci.yml"}
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

此设置告诉 BuildKit 在 `user/app:buildcache` 镜像中查找缓存。构建完成后，新的构建缓存会被推送到同一个镜像中，从而覆盖旧缓存。

此缓存也可以在本地使用。要在本地构建中拉取缓存，可以在 `docker buildx build` 命令中使用 `--cache-from` 选项：

```console
$ docker buildx build --cache-from type=registry,ref=user/app:buildcache .
```

## 总结

优化构建中的缓存使用可以显著加快构建过程。保持构建上下文精简、使用绑定挂载、缓存挂载和外部缓存都是您可以用来充分利用构建缓存并加快构建过程的技术。

有关本指南中讨论的概念的更多信息，请参阅：

- [.dockerignore 文件](/manuals/build/concepts/context.md#dockerignore-files)
- [缓存失效](/manuals/build/cache/invalidation.md)
- [缓存挂载](/reference/dockerfile.md#run---mounttypecache)
- [缓存后端类型](/manuals/build/cache/backends/_index.md)
- [构建最佳实践](/manuals/build/building/best-practices.md)

