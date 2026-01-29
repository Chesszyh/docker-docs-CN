---
title: 多阶段构建
linkTitle: 多阶段 (Multi-stage)
weight: 10
description: |
  了解多阶段构建，以及如何使用它们来改进构建并获得更小的镜像
keywords: build, 最佳实践
---

多阶段构建对于任何在努力优化 Dockerfile 且同时想保持其易读和易维护的人来说都非常有用。

## 使用多阶段构建

在多阶段构建中，您可以在 Dockerfile 中使用多个 `FROM` 语句。每个 `FROM` 指令可以使用不同的基础镜像，并且每个指令都开启了一个新的构建阶段。您可以选择性地将构件（artifacts）从一个阶段复制到另一个阶段，从而在最终镜像中舍弃所有不需要的内容。

以下 Dockerfile 包含两个独立的阶段：一个用于构建二进制文件，另一个将该二进制文件从第一阶段复制到下一阶段。

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

您只需要这一个 Dockerfile。不需要单独的构建脚本。只需运行 `docker build` 即可。

```console
$ docker build -t hello .
```

最终结果是一个微小的生产镜像，里面除了二进制文件什么都没有。构建应用程序所需的任何构建工具都不会包含在生成的镜像中。

它是如何工作的？第二个 `FROM` 指令以 `scratch` 镜像为基础开启了一个新的构建阶段。`COPY --from=0` 这一行仅将上一个阶段构建的产物复制到这个新阶段。Go SDK 和任何中间产物都会被留下，不会保存在最终镜像中。

## 命名构建阶段

默认情况下，构建阶段没有名称，您可以通过整数编号来引用它们，第一个 `FROM` 指令从 0 开始。但是，您可以通过在 `FROM` 指令中添加 `AS <NAME>` 来为阶段命名。下面的示例改进了前一个示例，为阶段命名并在 `COPY` 指令中使用该名称。这意味着即使以后重新排列 Dockerfile 中的指令，`COPY` 也不会失效。

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

## 停止在特定的构建阶段

构建镜像时，您不一定需要构建整个 Dockerfile 包含的每一个阶段。您可以指定一个目标构建阶段。以下命令假设您正在使用之前的 `Dockerfile`，但停止在名为 `build` 的阶段：

```console
$ docker build --target build -t hello .
```

以下是这种做法可能有用的一些场景：

- 调试特定的构建阶段
- 使用一个开启了所有调试符号或工具的 `debug` 阶段，以及一个精简的 `production` 阶段
- 使用一个填充了测试数据的 `testing` 阶段，而为生产环境构建时使用另一个使用真实数据的阶段

## 使用外部镜像作为阶段

在使用多阶段构建时，您并不局限于从之前在 Dockerfile 中创建的阶段进行复制。您可以使用 `COPY --from` 指令从一个单独的镜像中进行复制，可以使用本地镜像名称、本地或 Docker 镜像库中可用的标签，或者是标签 ID。如果有必要，Docker 客户端会拉取该镜像并从中复制构件。语法如下：

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

## 使用前一个阶段作为新阶段

您可以在使用 `FROM` 指令时引用前一个阶段，从而从该阶段结束的地方继续。例如：

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

## 传统构建器与 BuildKit 的区别

传统的 Docker Engine 构建器会处理 Dockerfile 中直到选定 `--target` 之前的所有阶段。即使选定的目标不依赖于某个阶段，它也会构建该阶段。

[BuildKit](../buildkit/_index.md) 仅构建目标阶段所依赖的阶段。

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

在 [启用 BuildKit](../buildkit/_index.md#快速入门) 的情况下，在此 Dockerfile 中构建 `stage2` 目标意味着仅处理 `base` 和 `stage2`。由于不依赖于 `stage1`，因此它会被跳过。

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

另一方面，在不使用 BuildKit 的情况下构建相同的目标会导致处理所有阶段：

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

即使 `stage2` 不依赖于 `stage1`，传统构建器也会处理它。
