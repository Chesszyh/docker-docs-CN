---
title: 将你的 Go 镜像作为容器运行
linkTitle: 运行容器
weight: 10
keywords: get started, go, golang, run, container
description: 了解如何将镜像作为容器运行。
alias:
  - /get-started/golang/run-containers/
  - /language/golang/run-containers/
  - /guides/language/golang/run-containers/
---

## 先决条件

完成 [构建 Go 镜像](build-images.md) 中容器化 Go 应用程序的步骤。

## 概览

在上一模块中，你为示例应用程序创建了 `Dockerfile`，然后使用命令 `docker build` 创建了 Docker 镜像。现在你有了镜像，你可以运行该镜像并查看你的应用程序是否正在正确运行。

容器是一个正常的操作系统进程，只是该进程是隔离的，具有自己的文件系统、自己的网络以及与主机分离的自己的隔离进程树。

要在容器内运行镜像，请使用 `docker run` 命令。它需要一个参数，即镜像名称。启动你的镜像并确保它正在正确运行。在你的终端中运行以下命令。

```console
$ docker run docker-gs-ping
```

```text
   ____    __
  / __/___/ /  ___
 / _// __/ _ \/ _ \
/___/\__/_//_/\___/ v4.10.2
High performance, minimalist Go web framework
https://echo.labstack.com
____________________________________O/_______ 
                                    O\
⇨ http server started on [::]:8080
```

当你运行此命令时，你会注意到你没有返回到命令提示符。这是因为你的应用程序是一个 REST 服务器，将循环运行等待传入请求，直到你停止容器才将控制权返回给操作系统。

使用 curl 命令向服务器发出 GET 请求。

```console
$ curl http://localhost:8080/
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

你的 curl 命令失败了，因为与服务器的连接被拒绝。
这意味着你无法连接到端口 8080 上的 localhost。这是预期的，因为你的容器是隔离运行的，其中包括网络。停止容器并重新启动，并在本地网络上发布端口 8080。

要停止容器，请按 ctrl-c。这将使你返回到终端提示符。

要为容器发布端口，你将在 `docker run` 命令上使用 `--publish` 标志（简写为 `-p`）。`--publish` 命令的格式是 `[host_port]:[container_port]`。因此，如果你想将容器内的端口 `8080` 暴露给容器外的端口 `3000`，你将把 `3000:8080` 传递给 `--publish` 标志。

启动容器并将端口 `8080` 暴露给主机上的端口 `8080`。

```console
$ docker run --publish 8080:8080 docker-gs-ping
```

现在，重新运行 curl 命令。

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

成功！你能够连接到在端口 8080 上容器内运行的应用程序。切换回你的容器正在运行的终端，你应该看到 `GET` 请求已记录到控制台。

按 `ctrl-c` 停止容器。

## 以分离模式运行

到目前为止这很棒，但你的示例应用程序是一个 Web 服务器，你不应该必须让终端连接到容器。Docker 可以在后台以分离模式运行你的容器。为此，你可以使用 `--detach` 或简写 `-d`。Docker 将像以前一样启动你的容器，但这次将从容器分离并让你返回到终端提示符。

```console
$ docker run -d -p 8080:8080 docker-gs-ping
d75e61fcad1e0c0eca69a3f767be6ba28a66625ce4dc42201a8a323e8313c14e
```

Docker 在后台启动了你的容器并在终端上打印了容器 ID。

再次确保你的容器正在运行。运行相同的 `curl` 命令：

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

## 列出容器

由于你在后台运行了容器，你怎么知道你的容器是否正在运行，或者你的机器上正在运行什么其他容器？好吧，要查看机器上正在运行的容器列表，请运行 `docker ps`。这类似于使用 ps 命令查看 Linux 机器上的进程列表。

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"   41 seconds ago   Up 40 seconds   0.0.0.0:8080->8080/tcp   inspiring_ishizaka
```

`ps` 命令告诉你关于正在运行的容器的一堆信息。你可以看到容器 ID、容器内运行的镜像、用于启动容器的命令、创建时间、状态、暴露的端口以及容器的名称。

你可能想知道容器的名称是从哪里来的。由于你在启动容器时没有为容器提供名称，Docker 生成了一个随机名称。你马上就会解决这个问题，但首先你需要停止容器。要停止容器，请运行 `docker stop` 命令，传递容器的名称或 ID。

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

现在重新运行 `docker ps` 命令以查看正在运行的容器列表。

```console
$ docker ps

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## 停止、启动和命名容器

Docker 容器可以启动、停止和重启。当你停止容器时，它不会被删除，但状态会更改为已停止，并且容器内的进程也会停止。当你运行 `docker ps` 命令时，默认输出仅显示正在运行的容器。如果你传递 `--all` 或简写 `-a`，你将看到系统上的所有容器，包括已停止的容器和正在运行的容器。

```console
$ docker ps --all

CONTAINER ID   IMAGE            COMMAND                  CREATED              STATUS                      PORTS     NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        About a minute ago   Exited (2) 23 seconds ago             inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 2 minutes ago              wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 3 minutes ago              magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        9 minutes ago        Exited (2) 3 minutes ago              gifted_mestorf
```

如果你一直按照操作，你应该会看到列出了几个容器。这些是你启动和停止但尚未删除的容器。

重启你刚刚停止的容器。找到容器的名称，并在以下 `restart` 命令中替换容器的名称：

```console
$ docker restart inspiring_ishizaka
```

现在，再次使用 `ps` 命令列出所有容器：

```console
$ docker ps -a

CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                     PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        2 minutes ago    Up 5 seconds               0.0.0.0:8080->8080/tcp   inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 2 minutes ago                            wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 4 minutes ago                            magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        10 minutes ago   Exited (2) 4 minutes ago                            gifted_mestorf
```

请注意，你刚刚重启的容器已在分离模式下启动，并且暴露了端口 `8080`。此外，请注意容器的状态是 `Up X seconds`。当你重启容器时，它将使用最初启动它时使用的相同标志或命令启动。

停止并删除所有容器，并看看如何解决随机命名问题。

停止你刚刚启动的容器。找到正在运行的容器的名称，并在以下命令中将名称替换为你系统上的容器名称：

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

现在所有的容器都已停止，删除它们。当容器被删除时，它不再运行，也不处于停止状态。相反，容器内的进程被终止，容器的元数据被删除。

要删除容器，请运行 `docker rm` 命令并传递容器名称。你可以在一个命令中向该命令传递多个容器名称。

再次确保在以下命令中用你系统中的容器名称替换容器名称：

```console
$ docker rm inspiring_ishizaka wizardly_joliot magical_carson gifted_mestorf

inspiring_ishizaka
wizardly_joliot
magical_carson
gifted_mestorf
```

再次运行 `docker ps --all` 命令以验证所有容器都已消失。

现在，解决讨厌的随机名称问题。标准做法是命名你的容器，原因很简单：更容易识别容器中运行的内容以及它与哪个应用程序或服务相关联。就像代码中变量的良好命名约定使其更易于阅读一样。命名容器也是如此。

要命名容器，你必须将 `--name` 标志传递给 `run` 命令：

```console
$ docker run -d -p 8080:8080 --name rest-server docker-gs-ping
3bbc6a3102ea368c8b966e1878a5ea9b1fc61187afaac1276c41db22e4b7f48f
```

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
3bbc6a3102ea   docker-gs-ping   "/docker-gs-ping"   25 seconds ago   Up 24 seconds   0.0.0.0:8080->8080/tcp   rest-server
```

现在，你可以根据名称轻松识别你的容器。

## 后续步骤

在本模块中，你学习了如何运行容器和发布端口。你还学习了管理容器的生命周期。然后，你了解了命名容器的重要性，以便更容易识别它们。在下一个模块中，你将学习如何在容器中运行数据库并将其连接到你的应用程序。

