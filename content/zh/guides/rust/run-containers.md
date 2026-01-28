---
title: 将你的 Rust 镜像作为容器运行
linkTitle: 运行容器
weight: 10
keywords: rust, run, image, container,
description: 了解如何将你的 Rust 镜像作为容器运行。
aliases:
  - /language/rust/run-containers/
  - /guides/language/rust/run-containers/
---

## 先决条件

你已完成 [构建你的 Rust 镜像](build-images.md) 并且已经构建了一个镜像。

## 概述

容器是一个正常的操作系统进程，不同之处在于 Docker 隔离了这个进程，使其拥有自己的文件系统、自己的网络，以及与其主机分离的自己的隔离进程树。

要在容器内运行镜像，你使用 `docker run` 命令。`docker run` 命令需要一个参数，即镜像的名称。

## 运行镜像

使用 `docker run` 运行你在 [构建你的 Rust 镜像](build-images.md) 中构建的镜像。

```console
$ docker run docker-rust-image
```

运行此命令后，你会注意到你没有返回到命令提示符。这是因为你的应用程序是一个服务器，它在循环中运行，等待传入请求，直到你停止容器才会将控制权返回给操作系统。

打开一个新终端，然后使用 `curl` 命令向服务器发出请求。

```console
$ curl http://localhost:8000
```

你应该会看到类似以下的输出。

```console
curl: (7) Failed to connect to localhost port 8000 after 2236 ms: Couldn't connect to server
```

如你所见，你的 `curl` 命令失败了。这意味着你无法连接到端口 8000 上的 localhost。这是正常的，因为你的容器是在隔离环境中运行的，其中包括网络。停止容器并重新启动，同时将端口 8000 发布到你的本地网络。

要停止容器，请按 ctrl-c。这将使你返回到终端提示符。

要为你的容器发布端口，你将在 `docker run` 命令上使用 `--publish` 标志（简写为 `-p`）。`--publish` 命令的格式是 `[主机端口]:[容器端口]`。因此，如果你想将容器内的端口 8000 暴露给容器外的端口 3001，你会将 `3001:8000` 传递给 `--publish` 标志。

你在容器中运行应用程序时没有指定端口，默认为 8000。如果你希望之前对端口 8000 的请求能够工作，你可以将主机的端口 3001 映射到容器的端口 8000：

```console
$ docker run --publish 3001:8000 docker-rust-image
```

现在，重新运行 curl 命令。记得打开一个新终端。

```console
$ curl http://localhost:3001
```

你应该会看到类似以下的输出。

```console
Hello, Docker!
```

成功！你能够连接到在容器内端口 8000 上运行的应用程序。切换回你的容器正在运行的终端并停止它。

按 ctrl-c 停止容器。

## 在分离模式下运行

到目前为止一切都很好，但你的示例应用程序是一个 Web 服务器，你不需要一直连接到容器。Docker 可以在分离模式或后台运行你的容器。为此，你可以使用 `--detach` 或简写 `-d`。Docker 会像以前一样启动你的容器，但这次会从容器“分离”并让你返回到终端提示符。

```console
$ docker run -d -p 3001:8000 docker-rust-image
ce02b3179f0f10085db9edfccd731101868f58631bdf918ca490ff6fd223a93b
```

Docker 在后台启动了你的容器，并在终端上打印了容器 ID。

再次确保你的容器正在正常运行。再次运行 curl 命令。

```console
$ curl http://localhost:3001
```

你应该会看到类似以下的输出。

```console
Hello, Docker!
```

## 列出容器

既然你在后台运行了容器，你怎么知道你的容器是否正在运行，或者你的机器上还运行着哪些其他容器？要查看机器上运行的容器列表，请运行 `docker ps`。这类似于你在 Linux 中使用 ps 命令查看进程列表。

你应该会看到类似以下的输出。

```console
CONTAINER ID   IMAGE                   COMMAND         CREATED         STATUS         PORTS                    NAMES
3074745e412c   docker-rust-image       "/bin/server"   8 seconds ago   Up 7 seconds   0.0.0.0:3001->8000/tcp   wonderful_kalam
```

`docker ps` 命令提供了关于你正在运行的容器的大量信息。你可以看到容器 ID、容器内运行的镜像、用于启动容器的命令、创建时间、状态、暴露的端口以及容器的名称。

你可能想知道容器的名称是从哪里来的。由于你在启动容器时没有为容器提供名称，Docker 生成了一个随机名称。你稍后会修复这个问题，但首先你需要停止容器。要停止容器，运行 `docker stop` 命令，它的作用正如其名，停止容器。你需要传递容器的名称，或者你可以使用容器 ID。

```console
$ docker stop wonderful_kalam
wonderful_kalam
```

现在，重新运行 `docker ps` 命令查看正在运行的容器列表。

```console
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

## 停止、启动和命名容器

你可以启动、停止和重启 Docker 容器。当你停止一个容器时，它不会被移除，而是状态变为已停止，容器内的进程也会停止。当你在上一个模块中运行 `docker ps` 命令时，默认输出仅显示正在运行的容器。当你传递 `--all` 或简写 `-a` 时，你会看到机器上的所有容器，无论其启动或停止状态如何。

```console
$ docker ps -a
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS                      PORTS
     NAMES
3074745e412c   docker-rust-image       "/bin/server"            3 minutes ago    Exited (0) 6 seconds ago
     wonderful_kalam
6cfa26e2e3c9   docker-rust-image       "/bin/server"            14 minutes ago   Exited (0) 5 minutes ago
     friendly_montalcini
4cbe94b2ea0e   docker-rust-image       "/bin/server"            15 minutes ago   Exited (0) 14 minutes ago
     tender_bose
```

你现在应该看到列出了几个容器。这些是你启动和停止过但尚未移除的容器。

重启你刚刚停止的容器。找到你刚刚停止的容器的名称，并在以下重启命令中替换容器的名称。

```console
$ docker restart wonderful_kalam
```

现在使用 `docker ps` 命令再次列出所有容器。

```console
$ docker ps --all
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS                      PORTS
     NAMES
3074745e412c   docker-rust-image       "/bin/server"            6 minutes ago    Up 4 seconds                0.0.0.0:3001->8000/tcp           wonderful_kalam
6cfa26e2e3c9   docker-rust-image       "/bin/server"            16 minutes ago   Exited (0) 7 minutes ago
     friendly_montalcini
4cbe94b2ea0e   docker-rust-image       "/bin/server"            18 minutes ago   Exited (0) 17 minutes ago
     tender_bose
```

注意，你刚刚重启的容器已在分离模式下启动。此外，观察容器的状态是 "Up X seconds"。当你重启容器时，它会使用最初启动时使用的相同标志或命令启动。

现在，停止并移除所有容器，并看看如何修复随机命名问题。停止你刚刚启动的容器。找到正在运行的容器的名称，并在以下命令中将名称替换为你系统上的容器名称。

```console
$ docker stop wonderful_kalam
wonderful_kalam
```

既然你已经停止了所有容器，那就移除它们。当你移除一个容器时，它不再运行，也不处于停止状态，而是容器内的进程已被停止，容器的元数据已被移除。

要移除容器，运行带有容器名称的 `docker rm` 命令。你可以在单个命令中传递多个容器名称。再次将以下命令中的容器名称替换为你系统中的容器名称。

```console
$ docker rm wonderful_kalam friendly_montalcini tender_bose
wonderful_kalam
friendly_montalcini
tender_bose
```

再次运行 `docker ps --all` 命令以查看 Docker 是否移除了所有容器。

现在，是时候解决随机命名问题了。标准做法是为你的容器命名，原因很简单，这样更容易识别容器中运行的内容以及它与哪个应用程序或服务相关联。

要命名容器，你只需要将 `--name` 标志传递给 `docker run` 命令。

```console
$ docker run -d -p 3001:8000 --name docker-rust-container docker-rust-image
1aa5d46418a68705c81782a58456a4ccdb56a309cb5e6bd399478d01eaa5cdda
$ docker ps
CONTAINER ID   IMAGE                   COMMAND         CREATED         STATUS         PORTS                    NAMES
c68fa18de1f6   docker-rust-image       "/bin/server"   7 seconds ago   Up 6 seconds   0.0.0.0:3001->8000/tcp   docker-rust-container
```

好多了！你现在可以根据名称轻松识别你的容器。

## 总结

在本节中，你了解了如何运行容器。你还了解了如何通过启动、停止和重启来管理容器。最后，你了解了如何命名你的容器，以便更容易识别它们。

相关信息：

- [docker run CLI 参考](/reference/cli/docker/container/run.md)

## 下一步

在下一节中，你将学习如何在容器中运行数据库并将其连接到 Rust 应用程序。
