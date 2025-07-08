---
description: 有关 Docker Compose 的常见问题解答，包括 v1 与 v2 的区别、命令、关闭行为和开发设置。
keywords: docker compose faq, docker compose questions, docker-compose vs docker compose, docker compose json, docker compose stop delay, run multiple docker compose, 常见问题, 命令对比, 关闭延迟
title: Docker Compose 常见问题
linkTitle: 常见问题
weight: 10
tags: [FAQ]
aliases:
- /compose/faq/
---

### `docker compose` 和 `docker-compose` 有什么区别？

Docker Compose 命令行二进制文件的一代于 2014 年首次发布。它用 Python 编写，并通过 `docker-compose` 调用。通常，Compose v1 项目在 `compose.yaml` 文件中包含一���顶层 `version` 元素，其值范围从 2.0 到 3.8，这些值指的是特定的文件格式。

Docker Compose 命令行二进制文件的二代于 2020 年宣布，用 Go 编写，并通过 `docker compose` 调用。Compose v2 会忽略 `compose.yaml` 文件中的顶层 `version` 元素。

更多信息，请参阅 [Compose 的历史和发展](/manuals/compose/intro/history.md)。

### `up`、`run` 和 `start` 有什么区别？

通常，你会使用 `docker compose up`。使用 `up` 来启动或重启在 `compose.yaml` 中定义的所有服务。在默认的“附加”模式下，你可以看到所有容器的日志。在“分离”模式（`-d`）下，Compose 在启动容器后退出，但容器会继续在后台运行。

`docker compose run` 命令用于运行“一次性”或“临时”任务。它需要你想要运行的服务名称，并且只启动运行中服务所依赖的服务的容器。使用 `run` 来运行测试或执行管理任务，例如从数据卷容器中删除或添加数据。`run` 命令的行为类似于 `docker run -ti`，它会打开一个到容器的交互式终端，并返回与容器中进程退出状态相匹配的退出状态。

`docker compose start` 命令仅用于重启先前已创建但已停止的容器。它从不创建新容器。

### 为什么我的服务需要 10 秒才能重新创建���停止？

`docker compose stop` 命令尝试通过发送 `SIGTERM` 来停止容器。然后它会等待一个[默认超时时间 10 秒](/reference/cli/docker/compose/stop.md)。超时后，会向容器发送一个 `SIGKILL` 以强制杀死它。如果你在等待这个超时，这意味着你的容器在收到 `SIGTERM` 信号时没有关闭。

关于容器中[进程处理信号](https://medium.com/@gchudnov/trapping-signals-in-docker-containers-7a57fdda7d86)的问题已经有很多文章讨论过了。

要解决这个问题，请尝试以下方法：

- 确保你在 Dockerfile 中使用了 `CMD` 和 `ENTRYPOINT` 的 exec 形式。

  例如，使用 `["program", "arg1", "arg2"]` 而不是 `"program arg1 arg2"`。使用字符串形式会导致 Docker 使用 `bash` 来运行你的进程，而 `bash` 不能正确处理信号。Compose 总是使用 JSON 形式，所以如果你在 Compose 文件中覆盖了命令或入口点，也不用担心。

- 如果可以，修改你正在运行的应用程序，为 `SIGTERM` 添加一个显式的信号处理器。

- 将 `stop_signal` 设置为应用程序知道如何处理的信号：

  ```yaml
  services:
    web:
      build: .
      stop_signal: SIGINT
  ```

- 如果你无法修改应用程序，请将应用程序包装在一个轻量级的 init 系统（如 [s6](https://skarnet.org/software/s6/)）或信号代理（如 [dumb-init](https://github.com/Yelp/dumb-init) 或 [tini](https://github.com/krallin/tini)）中。这两种包装器都能正确处理 `SIGTERM`。

### 如何在同一主机上运行一个 Compose 文件的多个副本？

Compose 使用项目名称为项目的所有容器和其他资源创建唯一的标识符。要运行一个项目的多个副本，请使用 `-p` 命令行选项或 [`COMPOSE_PROJECT_NAME` 环境变量](/manuals/compose/how-tos/environment-variables/envvars.md#compose_project_name)设置一个自定义项目名称。

### 我可以用 JSON 代替 YAML 作为我的 Compose 文件吗？

可以。[YAML 是 JSON 的超集](https://stackoverflow.com/a/1729545/444646)，所以任何 JSON 文件都应该是有效的 YAML。要将 JSON 文件与 Compose 一起使用，请指定要使用的文件名，例如：

```console
$ docker compose -f compose.json up
```

### 我应该用 `COPY`/`ADD` 还是用卷来包含我的代码？

你可以使用 `Dockerfile` 中的 `COPY` 或 `ADD` 指令将你的代码添加到镜像中。如果你需要将代码与 Docker 镜像一起迁移，例如将代码发送到另一个环境（生产、CI 等），这会很有用。

如果你想对代码进行更改并立即看到它们反映出来，例如在开发代码并且你的服务器支持热代���重载或实时重载时，请使用 `volume`。

在某些情况下，你可能希望两者都使用。你可以让镜像使用 `COPY` 包含代码，并在你的 Compose 文件中使用 `volume` 在开发期间包含来自主机的代码。卷会覆盖镜像的目录内容。
