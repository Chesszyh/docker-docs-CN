---
title: 多阶段构建 (Multi-stage builds)
linkTitle: 多阶段
weight: 10
description: |
  了解什么是多阶段构建，以及如何利用它优化构建任务并获得体积更小的镜像
keywords: build, best practices, 最佳实践, 构建
aliases:
- /engine/userguide/eng-image/multistage-build/
- /develop/develop-images/multistage-build/
---

多阶段构建对于任何苦于在保持 Dockerfile 易读、易维护的同时对其进行优化的人来说都非常有用。

## 使用多阶段构建

通过多阶段构建，您可以在 Dockerfile 中使用多个 `FROM` 语句。每个 `FROM` 指令可以使用不同的基础镜像，并且每个指令都开始一个新的构建阶段。您可以选择性地将产物从一个阶段复制到另一个阶段，从而在最终镜像中舍弃所有不需要的内容。

下面的 Dockerfile 有两个独立的阶段：一个用于构建二进制文件，另一个则将该二进制文件从第一阶段复制到下一阶段。

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

您只需要这一个 Dockerfile，无需额外的构建脚本。只需运行 `docker build` 即可。

```console
$ docker build -t hello .
```

最终结果是一个微小的生产镜像，内部除了二进制文件外一无所有。构建应用程序所需的任何构建工具都不会包含在最终镜像中。

它是如何工作的？第二个 `FROM` 指令以 `scratch` 镜像作为基础镜像开始一个新的构建阶段。`COPY --from=0` 这一行仅将前一阶段构建出的产物复制到这个新阶段。Go SDK 和任何中间产物都会被留在后面，不会保存到最终镜像中。

## 为您的构建阶段命名

默认情况下，这些阶段没有名称，您可以通过它们的整数编号来引用它们，第一个 `FROM` 指令对应的编号为 0。但是，您可以通过在 `FROM` 指令中添加 `AS <名称>` 来为阶段命名。下面的示例通过为阶段命名并在 `COPY` 指令中使用该名称来改进前一个示例。这意味着即使您稍后重新调整 Dockerfile 中指令的顺序，`COPY` 也不会失效。

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

构建镜像时，不一定需要构建包含每个阶段的整个 Dockerfile。您可以指定一个目标构建阶段。以下命令假设您使用的是前面的 `Dockerfile`，但构建停止在名为 `build` 的阶段：

```console
$ docker build --target build -t hello .
```

这种做法在以下几种场景中可能非常有用：

- 调试特定的构建阶段
- 使用开启了所有调试符号或工具的 `debug` 阶段，以及精简的 `production` 阶段
- 使用一个填充了测试数据的 `testing` 阶段，但生产环境构建则使用另一个采用真实数据的阶段

## 使用外部镜像作为阶段

使用多阶段构建时，您并不局限于仅从 Dockerfile 中早先创建的阶段进行复制。您可以使用 `COPY --from` 指令从一个单独的镜像进行复制，可以使用本地镜像名称、本地或 Docker 注册表上可用的标签，或者是标签 ID。Docker 客户端会在必要时拉取该镜像并从中复制产物。语法如下：

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

## 使用前一阶段作为新阶段

您可以通过在 `FROM` 指令中引用前一阶段，从而在它的基础上继续工作。例如：

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

## 旧版构建器与 BuildKit 之间的差异

旧版的 Docker Engine 构建器会处理 Dockerfile 中直至所选 `--target` 的所有阶段。即使所选目标不依赖于该阶段，它也会构建该阶段。

[BuildKit](../buildkit/_index.md) 则仅构建目标阶段所依赖的那些阶段。

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

在 [开启 BuildKit](../buildkit/_index.md#快速入门) 的情况下，构建此 Dockerfile 中的 `stage2` 目标意味着仅处理 `base` 和 `stage2`。由于不依赖 `stage1`，因此它会被跳过。

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

另一方面，在不使用 BuildKit 的情况下构建同一个目标会导致处理所有阶段：

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

旧版构建器即使在 `stage2` 不依赖 `stage1` 的情况下也会处理 `stage1`。