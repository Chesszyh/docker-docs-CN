---
title: 构建 Go 镜像
linkTitle: 构建镜像
weight: 5
keywords: containers, images, go, golang, dockerfiles, coding, build, push, run
description: 了解如何通过编写 Dockerfile 来构建你的第一个 Docker 镜像
aliases:
  - /get-started/golang/build-images/
  - /language/golang/build-images/
  - /guides/language/golang/build-images/
---

## 概览

在本节中，你将构建一个容器镜像。该镜像包含运行应用程序所需的一切——编译后的应用程序二进制文件、运行时、库以及应用程序所需的所有其他资源。

## 所需软件

要完成本教程，你需要以下内容：

- 本地运行的 Docker。按照 [下载并安装 Docker 的说明](/manuals/desktop/_index.md) 进行操作。
- 用于编辑文件的 IDE 或文本编辑器。[Visual Studio Code](https://code.visualstudio.com/) 是一个免费且流行的选择，但你可以使用任何你觉得舒服的工具。
- 一个 Git 客户端。本指南使用基于命令行的 `git` 客户端，但你可以自由使用任何适合你的客户端。
- 命令行终端应用程序。本模块中显示的示例来自 Linux shell，但只需极少修改（如果有的话），它们应该可以在 PowerShell、Windows 命令提示符或 OS X 终端中工作。

## 认识示例应用程序

示例应用程序是一个微服务的漫画。它故意设计得很简单，以便专注于学习 Go 应用程序容器化的基础知识。

该应用程序提供两个 HTTP 端点：

- 它对 `/` 的请求响应一个包含心形符号 (`<3`) 的字符串。
- 它对 `/health` 的请求响应 `{"Status" : "OK"}` JSON。

它对任何其他请求响应 HTTP 错误 404。

应用程序侦听由环境变量 `PORT` 的值定义的 TCP 端口。默认值为 `8080`。

该应用程序是无状态的。

应用程序的完整源代码在 GitHub 上：[github.com/docker/docker-gs-ping](https://github.com/docker/docker-gs-ping)。鼓励你 fork 它并随心所欲地进行实验。

要继续，请将应用程序存储库克隆到你的本地计算机：

```console
$ git clone https://github.com/docker/docker-gs-ping
```

如果你熟悉 Go，应用程序的 `main.go` 文件很简单：

```go
package main

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {

	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/", func(c echo.Context) error {
		return c.HTML(http.StatusOK, "Hello, Docker! <3")
	})

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "OK"})
	})

	httpPort := os.Getenv("PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}

// Simple implementation of an integer minimum
// Adapted from: https://gobyexample.com/testing-and-benchmarking
func IntMin(a, b int) int {
	if a < b {
		return a
	}
	return b
}
```

## 为应用程序创建 Dockerfile

要使用 Docker 构建容器镜像，需要一个包含构建指令的 `Dockerfile`。

以（可选的）解析器指令行开始你的 `Dockerfile`，该指令指示 BuildKit 根据指定版本的语法规则解释你的文件。

然后你告诉 Docker 你想为你的应用程序使用什么基础镜像：

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19
```

Docker 镜像可以从其他镜像继承。因此，你可以使用已经包含编译和运行 Go 应用程序所需的所有工具和库的官方 Go 镜像，而不是从头开始创建自己的基础镜像。

> [!NOTE]
>
> 如果你对创建自己的基础镜像感到好奇，可以查看本指南的以下部分：[创建基础镜像](/manuals/build/building/base-images.md#create-a-base-image)。
> 但是请注意，这对于继续你手头的任务不是必需的。

现在你已经定义了即将到来的容器镜像的基础镜像，你可以开始在它之上构建。

为了在运行其余命令时更轻松，请在你正在构建的镜像内创建一个目录。这也指示 Docker 将此目录用作所有后续命令的默认目标。这样你就不必在 `Dockerfile` 中输入完整的文件路径，相对路径将基于此目录。

```dockerfile
WORKDIR /app
```

通常，下载用 Go 编写的项目后你要做的第一件事就是安装编译它所需的模块。请注意，基础镜像已经有了工具链，但你的源代码还不在其中。

因此，在你可以在镜像内运行 `go mod download` 之前，你需要将 `go.mod` 和 `go.sum` 文件复制到其中。使用 `COPY` 命令来执行此操作。

在其最简单的形式中，`COPY` 命令采用两个参数。第一个参数告诉 Docker 你想将哪些文件复制到镜像中。最后一个参数告诉 Docker 你想将该文件复制到哪里。

将 `go.mod` 和 `go.sum` 文件复制到你的项目目录 `/app` 中，由于你使用了 `WORKDIR`，它是镜像内的当前目录 (`./`)。与一些现代 shell 似乎对使用尾部斜杠 (`/`) 漠不关心并能弄清楚用户的意图（大多数时候）不同，Docker 的 `COPY` 命令对其尾部斜杠的解释非常敏感。

```dockerfile
COPY go.mod go.sum ./
```

> [!NOTE]
>
> 如果你想熟悉 `COPY` 命令对尾部斜杠的处理，请参阅 [Dockerfile 参考](/reference/dockerfile.md#copy)。这个尾部斜杠可能会以超出你想象的方式导致问题。

现在你的正在构建的 Docker 镜像内有了模块文件，你可以使用 `RUN` 命令在那里运行命令 `go mod download`。这与你在本地机器上运行 `go` 完全相同，但这次这些 Go 模块将安装到镜像内的目录中。

```dockerfile
RUN go mod download
```

此时，你已经在镜像内安装了 Go 工具链版本 1.19.x 和所有 Go 依赖项。

你需要做的下一件事是将你的源代码复制到镜像中。你将使用 `COPY` 命令，就像你之前处理模块文件一样。

```dockerfile
COPY *.go ./
```

此 `COPY` 命令使用通配符将主机上当前目录（`Dockerfile` 所在的目录）中扩展名为 `.go` 的所有文件复制到镜像内的当前目录中。

现在，要编译你的应用程序，请使用熟悉的 `RUN` 命令：

```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping
```

这应该是熟悉的。该命令的结果将是一个名为 `docker-gs-ping` 的静态应用程序二进制文件，位于你正在构建的镜像的文件系统的根目录中。你可以将二进制文件放在该镜像内的任何其他你想要的地方，根目录在这方面没有特殊意义。使用它只是为了保持文件路径简短以提高可读性。

现在，剩下的就是告诉 Docker 当你的镜像用于启动容器时要运行什么命令。

你可以使用 `CMD` 命令来执行此操作：

```dockerfile
CMD ["/docker-gs-ping"]
```

这是完整的 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19

# Set destination for COPY
WORKDIR /app

# Download Go modules
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code. Note the slash at the end, as explained in
# https://docs.docker.com/reference/dockerfile/#copy
COPY *.go ./

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Optional:
# To bind to a TCP port, runtime parameters must be supplied to the docker command.
# But we can document in the Dockerfile what ports
# the application is going to listen on by default.
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 8080

# Run
CMD ["/docker-gs-ping"]
```

`Dockerfile` 也可以包含注释。它们总是以 `#` 符号开头，并且必须位于行首。注释是为了方便你记录你的 `Dockerfile`。

还有一个 Dockerfile 指令的概念，例如你添加的 `syntax` 指令。指令必须始终位于 `Dockerfile` 的最顶部，因此在添加注释时，请确保注释位于你可能使用的任何指令之后：

```dockerfile
# syntax=docker/dockerfile:1
# A sample microservice in Go packaged into a container image.

FROM golang:1.19

# ...
```

## 构建镜像

现在你已经创建了 `Dockerfile`，从中构建一个镜像。`docker build` 命令从 `Dockerfile` 和上下文创建 Docker 镜像。构建上下文是位于指定路径或 URL 中的一组文件。Docker 构建过程可以访问位于上下文中的任何文件。

构建命令可选地采用 `--tag` 标志。此标志用于用字符串值标记镜像，这对于人类来说很容易阅读和识别。如果你不传递 `--tag`，Docker 将使用 `latest` 作为默认值。

构建你的第一个 Docker 镜像。

```console
$ docker build --tag docker-gs-ping .
```

构建过程在执行构建步骤时将打印一些诊断消息。
以下只是这些消息可能是什么样子的一个示例。

```console
[+] Building 2.2s (15/15) FINISHED
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => => transferring dockerfile: 701B                                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => => transferring context: 2B                                                                                                            0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                                                 1.1s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:39b85bbfa7536a5feceb7372a0817649ecb2724562a38360f4d6a7782a409b14            0.0s
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/golang:1.19                                                                             0.7s
 => [1/6] FROM docker.io/library/golang:1.19@sha256:5d947843dde82ba1df5ac1b2ebb70b203d106f0423bf5183df3dc96f6bc5a705                       0.0s
 => [internal] load build context                                                                                                          0.0s
 => => transferring context: 6.08kB                                                                                                        0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                              0.0s
 => CACHED [3/6] COPY go.mod go.sum ./                                                                                                     0.0s
 => CACHED [4/6] RUN go mod download                                                                                                       0.0s
 => CACHED [5/6] COPY *.go ./                                                                                                              0.0s
 => CACHED [6/6] RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping                                                                  0.0s
 => exporting to image                                                                                                                     0.0s
 => => exporting layers                                                                                                                    0.0s
 => => writing image sha256:ede8ff889a0d9bc33f7a8da0673763c887a258eb53837dd52445cdca7b7df7e3                                               0.0s
 => => naming to docker.io/library/docker-gs-ping                                                                                          0.0s
```

你的确切输出会有所不同，但如果没有错误，你应该会在第一行输出中看到单词 `FINISHED`。这意味着 Docker 已成功构建名为 `docker-gs-ping` 的镜像。

## 查看本地镜像

要查看本地计算机上的镜像列表，你有两个选项。
一种是使用 CLI，另一种是使用 [Docker Desktop](/manuals/desktop/_index.md)。由于你目前在终端中工作，因此看看使用 CLI 列出镜像。

要列出镜像，请运行 `docker image ls` 命令（或 `docker images` 简写）：

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   2 minutes ago   1.11GB
...
```

你的确切输出可能会有所不同，但你应该看到带有 `latest` 标签的 `docker-gs-ping` 镜像。因为你在构建镜像时没有指定自定义标签，所以 Docker 假设标签是 `latest`，这是一个特殊值。

## 标记镜像

镜像名称由斜杠分隔的名称组件组成。名称组件可以包含小写字母、数字和分隔符。分隔符定义为句点、一个或两个下划线或一个或多个破折号。名称组件不能以分隔符开头或结尾。

镜像由清单和层列表组成。简而言之，标签指向这些工件的组合。你可以为镜像拥有多个标签，事实上，大多数镜像都有多个标签。为你构建的镜像创建第二个标签并查看其层。

使用 `docker image tag`（或 `docker tag` 简写）命令为你的镜像创建一个新标签。此命令采用两个参数；第一个参数是源镜像，第二个是要创建的新标签。以下命令为你构建的 `docker-gs-ping:latest` 创建一个新的 `docker-gs-ping:v1.0` 标签：

```console
$ docker image tag docker-gs-ping:latest docker-gs-ping:v1.0
```

Docker `tag` 命令为镜像创建一个新标签。它不会创建新镜像。标签指向同一个镜像，只是引用镜像的另一种方式。

现在再次运行 `docker image ls` 命令以查看更新后的本地镜像列表：

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   6 minutes ago   1.11GB
docker-gs-ping                   v1.0      7f153fbcc0a8   6 minutes ago   1.11GB
...
```

你可以看到有两个以 `docker-gs-ping` 开头的镜像。你知道它们是同一个镜像，因为如果你查看 `IMAGE ID` 列，你可以看到两个镜像的值是相同的。此值是 Docker 内部用于标识镜像的唯一标识符。

删除你刚刚创建的标签。为此，你将使用 `docker image rm` 命令，或简写 `docker rmi`（代表“删除镜像”）：

```console
$ docker image rm docker-gs-ping:v1.0
Untagged: docker-gs-ping:v1.0
```

请注意，来自 Docker 的响应告诉你镜像尚未被删除，而只是取消了标记。

通过运行以下命令来验证这一点：

```console
$ docker image ls
```

你将看到标签 `v1.0` 不再在 Docker 实例保留的镜像列表中。

```text
REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   7 minutes ago   1.11GB
...
```

标签 `v1.0` 已被删除，但你的机器上仍然有 `docker-gs-ping:latest` 标签，所以镜像还在那里。

## 多阶段构建

你可能已经注意到你的 `docker-gs-ping` 镜像重量超过 1 GB，这对于一个微小的编译 Go 应用程序来说是很大的。你可能还想知道构建镜像后全套 Go 工具（包括编译器）发生了什么。

答案是完整的工具链仍然在那里，在容器镜像中。这不仅因为文件大小大而不方便，而且在部署容器时也可能存在安全风险。

这两个问题可以通过使用 [多阶段构建](/manuals/build/building/multi-stage.md) 来解决。

简而言之，多阶段构建可以将工件从一个构建阶段延续到另一个构建阶段，并且每个构建阶段都可以从不同的基础镜像实例化。

因此，在以下示例中，你将使用全尺寸官方 Go 镜像来构建你的应用程序。然后你将把应用程序二进制文件复制到另一个镜像中，其基础非常精简，不包括 Go 工具链或其他可选组件。

示例应用程序存储库中的 `Dockerfile.multistage` 具有以下内容：

```dockerfile
# syntax=docker/dockerfile:1

# Build the application from source
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Run the tests in the container
FROM build-stage AS run-test-stage
RUN go test -v ./...

# Deploy the application binary into a lean image
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

由于你现在有两个 Dockerfile，你必须告诉 Docker 你想使用哪个 Dockerfile 来构建镜像。用 `multistage` 标记新镜像。这个标签（像任何其他标签一样，除了 `latest`）对 Docker 没有特殊意义，它只是你选择的东西。

```console
$ docker build -t docker-gs-ping:multistage -f Dockerfile.multistage .
```

比较 `docker-gs-ping:multistage` 和 `docker-gs-ping:latest` 的大小，你会看到几个数量级的差异。

```console
$ docker image ls
REPOSITORY       TAG          IMAGE ID       CREATED              SIZE
docker-gs-ping   multistage   e3fdde09f172   About a minute ago   28.1MB
docker-gs-ping   latest       336a3f164d0f   About an hour ago    1.11GB
```

这是因为你在构建的第二阶段使用的 ["distroless"](https://github.com/GoogleContainerTools/distroless) 基础镜像非常基础，专为静态二进制文件的精简部署而设计。

多阶段构建还有很多内容，包括多架构构建的可能性，所以请随时查看 [多阶段构建](/manuals/build/building/multi-stage.md)。但这对于你在此处的进展并不是必不可少的。

## 后续步骤

在本模块中，你遇到了你的示例应用程序，并为它构建了容器镜像。

在下一个模块中，你将了解如何将你的镜像作为容器运行。
