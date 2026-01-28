---
title: 多阶段构建
linkTitle: 多阶段
weight: 10
description: |
  了解多阶段构建以及如何使用它们来改进构建并获得更小的镜像
keywords: build, best practices
aliases:
- /engine/userguide/eng-image/multistage-build/
- /develop/develop-images/multistage-build/
---

多阶段构建（multi-stage builds）对于那些一直努力优化 Dockerfile 同时保持其易于阅读和维护的人来说非常有用。

## 使用多阶段构建

使用多阶段构建时，你在 Dockerfile 中使用多个 `FROM` 语句。每个 `FROM` 指令可以使用不同的基础，并且每个都开始构建的新阶段。你可以选择性地将工件从一个阶段复制到另一个阶段，在最终镜像中留下所有你不想要的东西。

以下 Dockerfile 有两个独立的阶段：一个用于构建二进制文件，另一个将二进制文件从第一阶段复制到下一阶段。

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:{{% param "example_go_version" %}}
WORKDIR /src
COPY <<EOF ./main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=0 /bin/hello /bin/hello
CMD ["/bin/hello"]
```

你只需要单个 Dockerfile。不需要单独的构建脚本。只需运行 `docker build`。

```console
$ docker build -t hello .
```

最终结果是一个只包含二进制文件的微小生产镜像。构建应用程序所需的所有构建工具都不包含在最终镜像中。

它是如何工作的？第二个 `FROM` 指令以 `scratch` 镜像作为基础开始新的构建阶段。`COPY --from=0` 行只将前一阶段构建的工件复制到这个新阶段。Go SDK 和任何中间工件都被留下，不会保存在最终镜像中。

## 命名你的构建阶段

默认情况下，阶段没有名称，你通过它们的整数编号引用它们，从第一个 `FROM` 指令的 0 开始。但是，你可以通过在 `FROM` 指令中添加 `AS <NAME>` 来命名你的阶段。此示例通过命名阶段并在 `COPY` 指令中使用名称来改进前一个示例。这意味着即使 Dockerfile 中的指令稍后被重新排序，`COPY` 也不会中断。

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:{{% param "example_go_version" %}} AS build
WORKDIR /src
COPY <<EOF /src/main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=build /bin/hello /bin/hello
CMD ["/bin/hello"]
```

## 在特定构建阶段停止

当你构建镜像时，你不一定需要构建整个 Dockerfile 包括每个阶段。你可以指定目标构建阶段。以下命令假设你使用的是前面的 `Dockerfile`，但在名为 `build` 的阶段停止：

```console
$ docker build --target build -t hello .
```

这可能有用的几个场景包括：

- 调试特定的构建阶段
- 使用启用了所有调试符号或工具的 `debug` 阶段，以及精简的 `production` 阶段
- 使用 `testing` 阶段，其中你的应用程序填充了测试数据，但使用不同的阶段构建生产环境，该阶段使用真实数据

## 使用外部镜像作为阶段

使用多阶段构建时，你不仅限于从之前在 Dockerfile 中创建的阶段复制。你可以使用 `COPY --from` 指令从单独的镜像复制，可以是本地镜像名称、本地或 Docker 注册表上可用的标签，或标签 ID。Docker 客户端会在必要时拉取镜像并从中复制工件。语法是：

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

## 将前一阶段用作新阶段

你可以通过在使用 `FROM` 指令时引用前一阶段来从其停止的地方继续。例如：

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine:latest AS builder
RUN apk --no-cache add build-base

FROM builder AS build1
COPY source1.cpp source.cpp
RUN g++ -o /binary source.cpp

FROM builder AS build2
COPY source2.cpp source.cpp
RUN g++ -o /binary source.cpp
```

## 传统构建器和 BuildKit 之间的差异

传统的 Docker 引擎构建器会处理 Dockerfile 中直到所选 `--target` 的所有阶段。即使所选目标不依赖该阶段，它也会构建该阶段。

[BuildKit](../buildkit/_index.md) 只构建目标阶段依赖的阶段。

例如，给定以下 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu AS base
RUN echo "base"

FROM base AS stage1
RUN echo "stage1"

FROM base AS stage2
RUN echo "stage2"
```

启用 [BuildKit](../buildkit/_index.md#getting-started) 后，在此 Dockerfile 中构建 `stage2` 目标意味着只处理 `base` 和 `stage2`。不存在对 `stage1` 的依赖，因此它被跳过。

```console
$ DOCKER_BUILDKIT=1 docker build --no-cache -f Dockerfile --target stage2 .
[+] Building 0.4s (7/7) FINISHED
 => [internal] load build definition from Dockerfile                                            0.0s
 => => transferring dockerfile: 36B                                                             0.0s
 => [internal] load .dockerignore                                                               0.0s
 => => transferring context: 2B                                                                 0.0s
 => [internal] load metadata for docker.io/library/ubuntu:latest                                0.0s
 => CACHED [base 1/2] FROM docker.io/library/ubuntu                                             0.0s
 => [base 2/2] RUN echo "base"                                                                  0.1s
 => [stage2 1/1] RUN echo "stage2"                                                              0.2s
 => exporting to image                                                                          0.0s
 => => exporting layers                                                                         0.0s
 => => writing image sha256:f55003b607cef37614f607f0728e6fd4d113a4bf7ef12210da338c716f2cfd15    0.0s
```

另一方面，在没有 BuildKit 的情况下构建相同的目标会导致所有阶段都被处理：

```console
$ DOCKER_BUILDKIT=0 docker build --no-cache -f Dockerfile --target stage2 .
Sending build context to Docker daemon  219.1kB
Step 1/6 : FROM ubuntu AS base
 ---> a7870fd478f4
Step 2/6 : RUN echo "base"
 ---> Running in e850d0e42eca
base
Removing intermediate container e850d0e42eca
 ---> d9f69f23cac8
Step 3/6 : FROM base AS stage1
 ---> d9f69f23cac8
Step 4/6 : RUN echo "stage1"
 ---> Running in 758ba6c1a9a3
stage1
Removing intermediate container 758ba6c1a9a3
 ---> 396baa55b8c3
Step 5/6 : FROM base AS stage2
 ---> d9f69f23cac8
Step 6/6 : RUN echo "stage2"
 ---> Running in bbc025b93175
stage2
Removing intermediate container bbc025b93175
 ---> 09fc3770a9c4
Successfully built 09fc3770a9c4
```

传统构建器处理 `stage1`，即使 `stage2` 不依赖它。
