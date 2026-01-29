---
description: 关于 Docker Compose 常见问题的解答，包括 v1 与 v2 的区别、命令、关闭行为以及开发设置。
keywords: docker compose faq, docker compose 问题, docker-compose vs docker compose, docker compose json, docker compose 停止延迟, 运行多个 docker compose
title: Docker Compose 常见问题 (FAQ)
linkTitle: FAQ
weight: 10
tags: [FAQ]
aliases:
- /compose/faq/
---

### `docker compose` 和 `docker-compose` 之间有什么区别？

Docker Compose 命令行二进制文件的第一个版本发布于 2014 年。它是用 Python 编写的，通过 `docker-compose` 调用。通常，Compose v1 项目在 `compose.yaml` 文件中包含一个顶级的 version 元素，其值在 2.0 到 3.8 之间，代表特定的文件格式。

Docker Compose 命令行二进制文件的第二个版本于 2020 年发布，它是用 Go 语言编写的，通过 `docker compose` 调用。Compose v2 会忽略 `compose.yaml` 文件中的 version 顶级元素。

有关更多信息，请参阅 [Compose 的历史与发展](/manuals/compose/intro/history.md)。

### `up`、`run` 和 `start` 之间有什么区别？

通常，您会使用 `docker compose up`。使用 `up` 来启动或重启 `compose.yaml` 中定义的所有服务。在默认的“前台 (attached)”模式下，您可以看到所有容器的所有日志。在“分离 (detached)”模式（`-d`）下，Compose 在启动容器后会退出，但容器会继续在后台运行。

`docker compose run` 命令用于运行“一次性”或“临时”任务。它需要您指定想要运行的服务名称，并且只会启动该运行服务所依赖的其他服务的容器。使用 `run` 来运行测试或执行管理任务，例如删除或向数据卷容器添加数据。`run` 命令的行为类似于 `docker run -ti` ，它会为容器开启一个交互式终端，并返回与容器内进程退出状态相匹配的退出状态。

`docker compose start` 命令仅用于重启之前已创建但已停止的容器。它绝不会创建新容器。

### 为什么我的服务需要 10 秒钟才能重新创建或停止？

`docker compose stop` 命令尝试通过发送 `SIGTERM` 信号来停止容器。然后它会等待一个 [默认 10 秒的超时时间](/reference/cli/docker/compose/stop.md)。超时后，会向容器发送 `SIGKILL` 信号以强制杀掉它。如果您在等待此超时，这意味着您的容器在收到 `SIGTERM` 信号时没有正常关闭。

关于容器中 [进程处理信号](https://medium.com/@gchudnov/trapping-signals-in-docker-containers-7a57fdda7d86) 的这一问题，已经有很多相关的讨论和文章。

要解决此问题，请尝试以下操作：

- 确保在 Dockerfile 中使用 `CMD` 和 `ENTRYPOINT` 的 exec 形式。

  例如使用 `["program", "arg1", "arg2"]` 而不是 `"program arg1 arg2"`。使用字符串形式会导致 Docker 使用 `bash` 运行您的进程，而 `bash` 无法正确处理信号。Compose 始终使用 JSON 形式，因此即使您在 Compose 文件中覆盖了命令（command）或入口点（entrypoint）也不必担心。

- 如果可以，修改您正在运行的应用程序，为 `SIGTERM` 添加显式的信号处理程序。

- 将 `stop_signal` 设置为应用程序知道如何处理的信号：

  ```yaml
  services:
    web:
      build: .
      stop_signal: SIGINT
  ```

- 如果您无法修改应用程序，请将其包装在一个轻量级的 init 系统（如 [s6](https://skarnet.org/software/s6/)）或信号代理（如 [dumb-init](https://github.com/Yelp/dumb-init) 或 [tini](https://github.com/krallin/tini)）中。这些包装器都能正确处理 `SIGTERM`。

### 如何在同一台宿主机上运行同一个 Compose 文件的多个副本？

Compose 使用项目名称为项目的所有容器及其他资源创建唯一标识符。要运行一个项目的多个副本，请使用 `-p` 命令行选项或 [`COMPOSE_PROJECT_NAME` 环境变量](/manuals/compose/how-tos/environment-variables/envvars.md#compose_project_name) 来设置自定义项目名称。

### 我可以在 Compose 文件中使用 JSON 代替 YAML 吗？

可以。[YAML 是 JSON 的超集](https://stackoverflow.com/a/1729545/444646) ，因此任何 JSON 文件都应该是有效的 YAML。要将 JSON 文件用于 Compose，请指定要使用的文件名，例如：

```console
$ docker compose -f compose.json up
```

### 我应该使用 `COPY`/`ADD` 指令还是卷（volume）来包含我的代码？

您可以在 `Dockerfile` 中使用 `COPY` 或 `ADD` 指令将代码添加到镜像中。如果您需要将代码随 Docker 镜像一起迁移，这非常有用，例如当您将代码发送到另一个环境（生产、CI 等）时。

如果您希望对代码进行更改并立即看到效果，请使用 `volume`。例如，当您正在开发代码且您的服务器支持热代码重载（hot code reloading）或实时重载（live-reload）时。

有时您可能希望两者都用。您可以让镜像通过 `COPY` 包含代码，并在 Compose 文件中使用 `volume` 在开发期间包含来自宿主机的代码。卷会覆盖镜像中的目录内容。
