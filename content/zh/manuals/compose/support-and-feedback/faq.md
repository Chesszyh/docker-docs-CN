---
description: 解答关于 Docker Compose 的常见问题，包括 v1 与 v2、命令、关闭行为和开发设置。
keywords: docker compose faq, docker compose questions, docker-compose vs docker compose, docker compose json, docker compose stop delay, run multiple docker compose
title: Docker Compose 常见问题
linkTitle: 常见问题
weight: 10
tags: [FAQ]
aliases:
- /compose/faq/
---

### `docker compose` 和 `docker-compose` 有什么区别

Docker Compose 命令行工具的第一个版本于 2014 年首次发布。它使用 Python 编写，通过 `docker-compose` 调用。通常，Compose v1 项目在 `compose.yaml` 文件中包含一个顶级 version 元素，其值范围从 2.0 到 3.8，这些值指的是特定的文件格式。

Docker Compose 命令行工具的第二个版本于 2020 年发布，使用 Go 编写，通过 `docker compose` 调用。Compose v2 忽略 compose.yaml 文件中的 version 顶级元素。

有关更多信息，请参阅 [Compose 的历史和发展](/manuals/compose/intro/history.md)。

### `up`、`run` 和 `start` 有什么区别？

通常，您需要使用 `docker compose up`。使用 `up` 来启动或重启 `compose.yaml` 中定义的所有服务。在默认的"附加"模式下，您可以看到所有容器的所有日志。在"分离"模式（`-d`）下，Compose 在启动容器后退出，但容器继续在后台运行。

`docker compose run` 命令用于运行"一次性"或"临时"任务。它需要您想要运行的服务名称，并且仅启动运行服务所依赖的服务的容器。使用 `run` 来运行测试或执行管理任务，例如向数据卷容器添加或删除数据。`run` 命令的行为类似于 `docker run -ti`，它会打开一个到容器的交互式终端，并返回与容器中进程的退出状态匹配的退出状态。

`docker compose start` 命令仅用于重启之前创建但已停止的容器。它永远不会创建新容器。

### 为什么我的服务需要 10 秒才能重新创建或停止？

`docker compose stop` 命令尝试通过发送 `SIGTERM` 来停止容器。然后它会等待[默认超时 10 秒](/reference/cli/docker/compose/stop.md)。超时后，会向容器发送 `SIGKILL` 以强制终止它。如果您在等待此超时，这意味着您的容器在收到 `SIGTERM` 信号时没有关闭。

关于[容器中进程处理信号](https://medium.com/@gchudnov/trapping-signals-in-docker-containers-7a57fdda7d86)的问题已经有很多文章。

要解决此问题，请尝试以下方法：

- 确保在 Dockerfile 中使用 `CMD` 和 `ENTRYPOINT` 的 exec 形式。

  例如使用 `["program", "arg1", "arg2"]` 而不是 `"program arg1 arg2"`。
  使用字符串形式会导致 Docker 使用 `bash` 运行您的进程，而 bash 无法正确处理信号。Compose 始终使用 JSON 形式，所以如果您在 Compose 文件中覆盖命令或入口点，则无需担心。

- 如果可以，修改您运行的应用程序，为 `SIGTERM` 添加显式的信号处理程序。

- 将 `stop_signal` 设置为应用程序知道如何处理的信号：

  ```yaml
  services:
    web:
      build: .
      stop_signal: SIGINT
  ```

- 如果无法修改应用程序，请将应用程序包装在轻量级 init 系统（如 [s6](https://skarnet.org/software/s6/)）或信号代理（如 [dumb-init](https://github.com/Yelp/dumb-init) 或 [tini](https://github.com/krallin/tini)）中。这些包装器中的任何一个都会正确处理 `SIGTERM`。

### 如何在同一主机上运行多个 Compose 文件副本？

Compose 使用项目名称为项目的所有容器和其他资源创建唯一标识符。要运行项目的多个副本，请使用 `-p` 命令行选项或 [`COMPOSE_PROJECT_NAME` 环境变量](/manuals/compose/how-tos/environment-variables/envvars.md#compose_project_name)设置自定义项目名称。

### 我可以使用 JSON 代替 YAML 作为 Compose 文件吗？

可以。[YAML 是 JSON 的超集](https://stackoverflow.com/a/1729545/444646)，所以任何 JSON 文件都应该是有效的 YAML。要在 Compose 中使用 JSON 文件，请指定要使用的文件名，例如：

```console
$ docker compose -f compose.json up
```

### 我应该使用 `COPY`/`ADD` 还是卷来包含我的代码？

您可以使用 `Dockerfile` 中的 `COPY` 或 `ADD` 指令将代码添加到镜像中。如果您需要将代码与 Docker 镜像一起移动，例如当您将代码发送到另一个环境（生产环境、CI 等）时，这很有用。

如果您想对代码进行更改并立即看到更改生效，例如当您正在开发代码且服务器支持热代码重载或实时重载时，请使用 `volume`。

可能存在您想同时使用两者的情况。您可以让镜像使用 `COPY` 包含代码，并在 Compose 文件中使用 `volume` 在开发期间包含来自主机的代码。卷会覆盖镜像的目录内容。
