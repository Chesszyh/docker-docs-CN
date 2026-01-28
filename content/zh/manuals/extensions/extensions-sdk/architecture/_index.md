---
title: 扩展架构
linkTitle: 架构
description: Docker 扩展架构
keywords: Docker, extensions, sdk, metadata
aliases:
 - /desktop/extensions-sdk/architecture/
weight: 50
---

扩展是在 Docker Desktop 内运行的应用程序。它们被打包为 Docker 镜像，通过 Docker Hub 分发，用户可以通过 Docker Desktop 仪表板内的市场或 Docker 扩展 CLI 进行安装。

扩展可以由三个（可选的）组件组成：
- 前端（或用户界面）：在 Docker Desktop 仪表板的选项卡中显示的 Web 应用程序
- 后端：在 Docker Desktop 虚拟机中运行的一个或多个容器化服务
- 可执行文件：安装扩展时 Docker Desktop 复制到主机上的 Shell 脚本或二进制文件

![扩展三个组件的概述](images/extensions-architecture.png?w=600h=400)

扩展不一定需要包含所有这些组件，但根据扩展功能至少需要其中一个。要配置和运行这些组件，Docker Desktop 使用 `metadata.json` 文件。有关更多详细信息，请参阅[元数据](metadata)部分。

## 前端

前端基本上是由 HTML、Javascript 和 CSS 构成的 Web 应用程序。它可以用简单的 HTML 文件、一些原生 Javascript 或任何前端框架（如 React 或 Vue.js）构建。

当 Docker Desktop 安装扩展时，它会从扩展镜像中提取 UI 文件夹，如 `metadata.json` 中的 `ui` 部分所定义。有关更多详细信息，请参阅 [ui 元数据部分](metadata.md#ui-section)。

每次用户点击 **Extensions** 选项卡时，Docker Desktop 都会初始化扩展的 UI，就像第一次一样。当用户离开该选项卡时，UI 本身及其启动的所有子进程（如果有）都会被终止。

前端可以调用 `docker` 命令、与扩展后端通信，或通过 [Extensions SDK](https://www.npmjs.com/package/@docker/extension-api-client) 调用部署在主机上的扩展可执行文件。

> [!TIP]
>
> `docker extension init` 生成基于 React 的扩展。但您仍然可以将其作为自己扩展的起点，使用任何其他前端框架，如 Vue、Angular、Svelte 等，甚至使用原生 Javascript。

了解更多关于为扩展[构建前端](/manuals/extensions/extensions-sdk/build/frontend-extension-tutorial.md)的信息。

## 后端

除了前端应用程序外，扩展还可以包含一个或多个后端服务。在大多数情况下，扩展不需要后端，功能可以仅通过 SDK 调用 docker 命令来实现。但是，在某些情况下扩展需要后端服务，例如：
- 运行必须比前端存活更长时间的长时间运行进程
- 在本地数据库中存储数据并通过 REST API 返回
- 存储扩展状态，例如当按钮启动长时间运行的进程时，这样如果您离开扩展然后返回，前端可以从中断的地方继续
- 访问 Docker Desktop 虚拟机中的特定资源，例如通过在 compose 文件中挂载文件夹

> [!TIP]
>
> `docker extension init` 生成 Go 后端。但您仍然可以将其作为自己扩展的起点，使用任何其他语言，如 Node.js、Python、Java、.Net 或任何其他语言和框架。

通常，后端由一个在 Docker Desktop 虚拟机中运行的容器组成。在内部，Docker Desktop 创建一个 Docker Compose 项目，从 `metadata.json` 的 `vm` 部分的 `image` 选项创建容器，并将其附加到 Compose 项目。有关更多详细信息，请参阅 [ui 元数据部分](metadata.md#vm-section)。

在某些情况下，可以使用 `compose.yaml` 文件代替 `image`。当后端容器需要更具体的选项时，这很有用，例如挂载卷或请求无法仅用 Docker 镜像表达的[能力](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)。`compose.yaml` 文件还可用于添加扩展所需的多个容器，如数据库或消息代理。
请注意，如果 Compose 文件定义了多个服务，SDK 只能联系其中的第一个。

> [!NOTE]
>
> 在某些情况下，从后端与 Docker 引擎交互也很有用。
> 请参阅[如何从后端使用 Docker socket](../guides/use-docker-socket-from-backend.md)。

为了与后端通信，Extension SDK 提供了[函数](../dev/api/backend.md#get)来从前端发起 `GET`、`POST`、`PUT`、`HEAD` 和 `DELETE` 请求。在底层，通信是通过 socket 或命名管道完成的，具体取决于操作系统。如果后端监听端口，将很难防止与主机上运行的其他应用程序或容器中已有的应用程序发生冲突。此外，一些用户在受限环境中运行 Docker Desktop，无法在其机器上打开端口。

![后端和前端通信](images/extensions-arch-2.png?w=500h=300)

最后，后端可以用任何技术构建，只要它可以在容器中运行并监听 socket。

了解更多关于为扩展[添加后端](/manuals/extensions/extensions-sdk/build/backend-extension-tutorial.md)的信息。

## 可执行文件

除了前端和后端之外，扩展还可以包含可执行文件。可执行文件是在安装扩展时安装到主机上的二进制文件或 shell 脚本。前端可以使用[扩展 SDK](../dev/api/backend.md#invoke-an-extension-binary-on-the-host) 调用它们。

当扩展需要与第三方 CLI 工具交互时，这些可执行文件很有用，如 AWS、`kubectl` 等。将这些可执行文件与扩展一起提供可确保 CLI 工具始终可用，在用户机器上具有正确的版本。

当 Docker Desktop 安装扩展时，它会按照 `metadata.json` 中 `host` 部分的定义将可执行文件复制到主机上。有关更多详细信息，请参阅 [ui 元数据部分](metadata.md#host-section)。

![可执行文件和前端通信](images/extensions-arch-3.png?w=250h=300)

但是，由于它们在用户机器上执行，因此必须适用于它们运行的平台。例如，如果您想提供 `kubectl` 可执行文件，您需要为 Windows、Mac 和 Linux 提供不同的版本。多架构镜像还需要包含为正确架构（AMD / ARM）构建的二进制文件

请参阅 [host 元数据部分](metadata.md#host-section)了解更多详细信息。

了解如何[调用主机二进制文件](../guides/invoke-host-binaries.md)。
