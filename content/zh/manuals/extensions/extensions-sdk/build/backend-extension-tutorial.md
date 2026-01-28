---
title: 为扩展添加后端
description: 了解如何为扩展添加后端。
keywords: Docker, extensions, sdk, build
aliases:
 - /desktop/extensions-sdk/tutorials/minimal-backend-extension/
 - /desktop/extensions-sdk/build/minimal-backend-extension/
 - /desktop/extensions-sdk/build/set-up/backend-extension-tutorial/
 - /desktop/extensions-sdk/build/backend-extension-tutorial/
---

您的扩展可以附带一个后端部分，前端可以与其进行交互。本页面提供了关于为何以及如何添加后端的信息。

在开始之前，请确保您已安装最新版本的 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。

> Tip
>
> 请查看[快速入门指南](../quickstart.md)和 `docker extension init <my-extension>`。它们为您的扩展提供了更好的基础，因为它们更新，并且与您安装的 Docker Desktop 相关。

## 为什么要添加后端？

借助 Docker Extensions SDK，大多数情况下您应该能够直接从[前端](frontend-extension-tutorial.md#use-the-extension-apis-client)通过 Docker CLI 完成您需要的操作。

尽管如此，在某些情况下您可能需要为扩展添加后端。到目前为止，扩展开发者使用后端来：
- 在本地数据库中存储数据，并通过 REST API 返回这些数据。
- 存储扩展状态，例如当按钮启动一个长时间运行的进程时，这样如果您导航离开扩展用户界面然后返回，前端可以从中断的地方继续。

有关扩展后端的更多信息，请参阅[架构](../architecture/_index.md#the-backend)。

## 为扩展添加后端

如果您使用 `docker extension init` 命令创建扩展，您已经有了后端设置。否则，您必须首先创建一个包含代码的 `vm` 目录，并更新 Dockerfile 以将其容器化。

以下是包含后端的扩展文件夹结构：

```bash
.
├── Dockerfile # (1)
├── Makefile
├── metadata.json
├── ui
    └── index.html
└── vm # (2)
    ├── go.mod
    └── main.go
```

1. 包含构建后端并将其复制到扩展容器文件系统中所需的所有内容。
2. 包含扩展后端代码的源文件夹。

虽然您可以从空目录或 `vm-ui extension` [示例](https://github.com/docker/extensions-sdk/tree/main/samples)开始，但强烈建议您从 `docker extension init` 命令开始，然后根据需要进行修改。

> [!TIP]
>
> `docker extension init` 生成 Go 后端。但您仍然可以将其作为您自己扩展的起点，并使用任何其他语言，如 Node.js、Python、Java、.Net 或任何其他语言和框架。

在本教程中，后端服务只是暴露一个返回 JSON 负载的路由，内容是 "Hello"。

```json
{ "Message": "Hello" }
```

> [!IMPORTANT]
>
> 我们建议前端和后端通过套接字（sockets）进行通信，在 Windows 上使用命名管道（named pipes），而不是 HTTP。这可以防止与主机上运行的任何其他应用程序或容器发生端口冲突。此外，一些 Docker Desktop 用户在受限环境中运行，他们无法在其机器上打开端口。在选择后端的语言和框架时，请确保它支持套接字连接。

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

```go
package main

import (
	"flag"
	"log"
	"net"
	"net/http"
	"os"

	"github.com/labstack/echo"
	"github.com/sirupsen/logrus"
)

func main() {
	var socketPath string
	flag.StringVar(&socketPath, "socket", "/run/guest/volumes-service.sock", "Unix domain socket to listen on")
	flag.Parse()

	os.RemoveAll(socketPath)

	logrus.New().Infof("Starting listening on %s\n", socketPath)
	router := echo.New()
	router.HideBanner = true

	startURL := ""

	ln, err := listen(socketPath)
	if err != nil {
		log.Fatal(err)
	}
	router.Listener = ln

	router.GET("/hello", hello)

	log.Fatal(router.Start(startURL))
}

func listen(path string) (net.Listener, error) {
	return net.Listen("unix", path)
}

func hello(ctx echo.Context) error {
	return ctx.JSON(http.StatusOK, HTTPMessageBody{Message: "hello world"})
}

type HTTPMessageBody struct {
	Message string
}
```

{{< /tab >}}
{{< tab name="Node" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Node 的可用示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Node)
> 告诉我们您是否需要 Node 的示例。

{{< /tab >}}
{{< tab name="Python" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Python 的可用示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Python)
> 告诉我们您是否需要 Python 的示例。

{{< /tab >}}
{{< tab name="Java" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Java 的可用示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Java)
> 告诉我们您是否需要 Java 的示例。

{{< /tab >}}
{{< tab name=".NET" >}}

> [!IMPORTANT]
>
> 我们目前还没有 .NET 的可用示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=.Net)
> 告诉我们您是否需要 .NET 的示例。

{{< /tab >}}
{{< /tabs >}}

## 调整 Dockerfile

> [!NOTE]
>
> 使用 `docker extension init` 时，它会创建一个已经包含 Go 后端所需内容的 `Dockerfile`。

{{< tabs group="lang" >}}
{{< tab name="Go" >}}

要在安装扩展时部署您的 Go 后端，您首先需要配置 `Dockerfile`，使其：
- 构建后端应用程序
- 将二进制文件复制到扩展的容器文件系统中
- 在容器启动时启动二进制文件，监听扩展套接字

> [!TIP]
>
> 为了简化版本管理，您可以重用同一个镜像来构建前端、构建后端服务以及打包扩展。

```dockerfile
# syntax=docker/dockerfile:1
FROM node:17.7-alpine3.14 AS client-builder
# ... build frontend application

# Build the Go backend
FROM golang:1.17-alpine AS builder
ENV CGO_ENABLED=0
WORKDIR /backend
COPY vm/go.* .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go mod download
COPY vm/. .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -trimpath -ldflags="-s -w" -o bin/service

FROM alpine:3.15
# ... add labels and copy the frontend application

COPY --from=builder /backend/bin/service /
CMD /service -socket /run/guest-services/extension-allthethings-extension.sock
```

{{< /tab >}}
{{< tab name="Node" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Node 的可用 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Node)
> 告诉我们您是否需要 Node 的 Dockerfile。

{{< /tab >}}
{{< tab name="Python" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Python 的可用 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Python)
> 告诉我们您是否需要 Python 的 Dockerfile。

{{< /tab >}}
{{< tab name="Java" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Java 的可用 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=Java)
> 告诉我们您是否需要 Java 的 Dockerfile。

{{< /tab >}}
{{< tab name=".NET" >}}

> [!IMPORTANT]
>
> 我们目前还没有 .Net 的可用 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.25798127=.Net)
> 告诉我们您是否需要 .Net 的 Dockerfile。

{{< /tab >}}
{{< /tabs >}}

## 配置元数据文件

要在 Docker Desktop 的虚拟机中启动扩展的后端服务，您必须在 `metadata.json` 文件的 `vm` 部分配置镜像名称。

```json
{
  "vm": {
    "image": "${DESKTOP_PLUGIN_IMAGE}"
  },
  "icon": "docker.svg",
  "ui": {
    ...
  }
}
```

有关 `metadata.json` 中 `vm` 部分的更多信息，请参阅[元数据](../architecture/metadata.md)。

> [!WARNING]
>
> 不要替换 `metadata.json` 文件中的 `${DESKTOP_PLUGIN_IMAGE}` 占位符。当扩展安装时，占位符会自动替换为正确的镜像名称。

## 从前端调用扩展后端

使用[高级前端扩展示例](frontend-extension-tutorial.md)，我们可以调用扩展后端。

使用 Docker Desktop Client 对象，然后通过 `ddClient.extension.vm.service.get` 从后端服务调用 `/hello` 路由，该方法返回响应体。

{{< tabs group="framework" >}}
{{< tab name="React" >}}

将 `ui/src/App.tsx` 文件替换为以下代码：

```tsx

// ui/src/App.tsx
import React, { useEffect } from 'react';
import { createDockerDesktopClient } from "@docker/extension-api-client";

//obtain docker desktop extension client
const ddClient = createDockerDesktopClient();

export function App() {
  const ddClient = createDockerDesktopClient();
  const [hello, setHello] = useState<string>();

  useEffect(() => {
    const getHello = async () => {
      const result = await ddClient.extension.vm?.service?.get('/hello');
      setHello(JSON.stringify(result));
    }
    getHello()
  }, []);

  return (
    <Typography>{hello}</Typography>
  );
}

```

{{< /tab >}}
{{< tab name="Vue" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Vue 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> 告诉我们您是否需要 Vue 的示例。

{{< /tab >}}
{{< tab name="Angular" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Angular 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> 告诉我们您是否需要 Angular 的示例。

{{< /tab >}}
{{< tab name="Svelte" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Svelte 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> 告诉我们您是否需要 Svelte 的示例。

{{< /tab >}}
{{< /tabs >}}

## 重新构建扩展并更新

由于您修改了扩展的配置并在 Dockerfile 中添加了一个阶段，您必须重新构建扩展。

```bash
docker build --tag=awesome-inc/my-extension:latest .
```

构建完成后，您需要更新它，如果之前没有安装过，则需要安装。

```bash
docker extension update awesome-inc/my-extension:latest
```

现在您可以在 Docker Desktop 仪表板的**容器**视图中看到后端服务正在运行，并在需要调试时查看日志。

> [!TIP]
>
> 您可能需要在**设置**中开启**显示系统容器**选项才能看到后端容器运行。
> 有关更多信息，请参阅[显示扩展容器](../dev/test-debug.md#show-the-extension-containers)。

打开 Docker Desktop 仪表板并选择**容器**选项卡。您应该会看到后端服务调用返回的响应。

## 下一步

- 了解如何[分享和发布您的扩展](../extensions/_index.md)。
- 了解更多关于扩展[架构](../architecture/_index.md)的信息。
