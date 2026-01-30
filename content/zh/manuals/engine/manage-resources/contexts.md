---
title: Docker 上下文 (Contexts)
description: 了解如何通过上下文从单个客户端管理多个守护进程
keywords: engine, context, cli, daemons, remote, 上下文, 远程
aliases:
  - /engine/context/working-with-contexts/
---

## 介绍

本指南介绍如何使用上下文 (contexts) 从单个客户端管理多个 Docker 守护进程。

每个上下文都包含管理该守护进程资源所需的所有信息。`docker context` 命令使得配置这些上下文并由于它们之间进行切换变得容易。

例如，一个 Docker 客户端可能配置了两个上下文：

- 一个在本地运行的默认 (default) 上下文
- 一个远程的、共享的上下文

配置好这些上下文后，您可以使用 `docker context use <context-name>` 命令在它们之间切换。

## 前提条件

要按照本指南中的示例进行操作，您需要：

- 一个支持顶级 `context` 命令的 Docker 客户端

运行 `docker context` 验证您的 Docker 客户端是否支持上下文。

## 上下文的构成

上下文是多个属性的组合。其中包括：

- 名称和描述
- 端点配置
- TLS 信息

要列出可用的上下文，请使用 `docker context ls` 命令。

```console
$ docker context ls
NAME        DESCRIPTION                               DOCKER ENDPOINT               ERROR
default *                                             unix:///var/run/docker.sock
```

这显示了一个名为 "default" 的上下文。它被配置为通过本地 `/var/run/docker.sock` Unix 套接字与守护进程通信。

`NAME` 列中的星号表示这是当前的活动上下文。这意味着除非通过 `DOCKER_HOST` 和 `DOCKER_CONTEXT` 等环境变量，或者在命令行中使用 `--context` 和 `--host` 标志进行覆盖，否则所有 `docker` 命令都针对该上下文运行。

使用 `docker context inspect` 进行更深入的探索。以下示例显示如何检查名为 `default` 的上下文。

```console
$ docker context inspect default
[
    {
        "Name": "default",
        "Metadata": {},
        "Endpoints": {
            "docker": {
                "Host": "unix:///var/run/docker.sock",
                "SkipTLSVerify": false
            }
        },
        "TLSMaterial": {},
        "Storage": {
            "MetadataPath": "\u003cIN MEMORY\u003e",
            "TLSPath": "\u003cIN MEMORY\u003e"
        }
    }
]
```

### 创建新上下文

您可以使用 `docker context create` 命令创建新上下文。

以下示例创建一个名为 `docker-test` 的新上下文，并将该上下文的主机端点指定为 TCP 套接字 `tcp://docker:2375`。

```console
$ docker context create docker-test --docker host=tcp://docker:2375
docker-test
Successfully created context "docker-test"
```

新上下文存储在 `~/.docker/contexts/` 下的 `meta.json` 文件中。您创建的每个新上下文都有其自己的 `meta.json`，存储在 `~/.docker/contexts/` 的专用子目录中。

您可以使用 `docker context ls` 和 `docker context inspect <context-name>` 查看新上下文。

```console
$ docker context ls
NAME          DESCRIPTION                             DOCKER ENDPOINT               ERROR
default *                                             unix:///var/run/docker.sock
docker-test                                           tcp://docker:2375
```

当前上下文用星号 ("\*") 指示。

## 使用不同的上下文

您可以使用 `docker context use` 在上下文之间切换。

以下命令将切换 `docker` CLI 以使用 `docker-test` 上下文。

```console
$ docker context use docker-test
docker-test
Current context is now "docker-test"
```

通过列出所有上下文并确保星号 ("\*") 位于 `docker-test` 上下文旁来验证操作。

```console
$ docker context ls
NAME            DESCRIPTION                           DOCKER ENDPOINT               ERROR
default                                               unix:///var/run/docker.sock
docker-test *                                         tcp://docker:2375
```

`docker` 命令现在将针对 `docker-test` 上下文中定义的端点。

您还可以使用 `DOCKER_CONTEXT` 环境变量设置当前上下文。该环境变量会覆盖使用 `docker context use` 设置的上下文。

使用以下适当的命令，通过环境变量将上下文设置为 `docker-test`。

{{< tabs >}}
{{< tab name="PowerShell" >}}

```ps
> $env:DOCKER_CONTEXT='docker-test'
```

{{< /tab >}}
{{< tab name="Bash" >}}

```console
$ export DOCKER_CONTEXT=docker-test
```

{{< /tab >}}
{{< /tabs >}}

运行 `docker context ls` 验证 `docker-test` 上下文现在是否为活动上下文。

您还可以使用全局 `--context` 标志来覆盖上下文。以下命令使用名为 `production` 的上下文。

```console
$ docker --context production container ls
```

## 导出和导入 Docker 上下文

您可以使用 `docker context export` 和 `docker context import` 命令在不同主机上导出和导入上下文。

`docker context export` 命令将现有上下文导出到文件中。该文件可以导入到任何安装了 `docker` 客户端的主机上。

### 导出和导入上下文

以下示例导出一个名为 `docker-test` 的现有上下文。它将被写入一个名为 `docker-test.dockercontext` 的文件中。

```console
$ docker context export docker-test
Written file "docker-test.dockercontext"
```

检查导出文件的内容。

```console
$ cat docker-test.dockercontext
```

使用 `docker context import` 在另一台主机上导入此文件，以创建具有相同配置的上下文。

```console
$ docker context import docker-test docker-test.dockercontext
docker-test
Successfully imported context "docker-test"
```

您可以使用 `docker context ls` 验证上下文是否已导入。

导入命令的格式为 `docker context import <context-name> <context-file>`。

## 更新上下文

您可以使用 `docker context update` 更新现有上下文中的字段。

以下示例更新现有 `docker-test` 上下文中的描述字段。

```console
$ docker context update docker-test --description "Test context"
docker-test
Successfully updated context "docker-test"
```
