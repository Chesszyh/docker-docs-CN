---
title: Docker 上下文
description: 学习如何使用上下文从单个客户端管理多个守护进程
keywords: engine, context, cli, daemons, remote
aliases:
  - /engine/context/working-with-contexts/
---

## 简介

本指南展示如何使用上下文（Context）从单个客户端管理 Docker 守护进程。

每个上下文包含管理守护进程上资源所需的所有信息。
`docker context` 命令使配置这些上下文和在它们之间切换变得简单。

例如，单个 Docker 客户端可能配置了两个上下文：

- 一个本地运行的默认上下文
- 一个远程共享上下文

配置好这些上下文后，
你可以使用 `docker context use <context-name>` 命令
在它们之间切换。

## 前提条件

要按照本指南中的示例操作，你需要：

- 一个支持顶层 `context` 命令的 Docker 客户端

运行 `docker context` 来验证你的 Docker 客户端是否支持上下文。

## 上下文的组成部分

上下文是多个属性的组合。这些属性包括：

- 名称和描述
- 端点配置
- TLS 信息

要列出可用的上下文，使用 `docker context ls` 命令。

```console
$ docker context ls
NAME        DESCRIPTION                               DOCKER ENDPOINT               ERROR
default *                                             unix:///var/run/docker.sock
```

这显示了一个名为 "default" 的单一上下文。
它被配置为通过本地 `/var/run/docker.sock` Unix 套接字与守护进程通信。

`NAME` 列中的星号表示这是活动上下文。
这意味着所有 `docker` 命令都针对此上下文运行，
除非被环境变量（如 `DOCKER_HOST` 和 `DOCKER_CONTEXT`）覆盖，
或在命令行中使用 `--context` 和 `--host` 标志覆盖。

使用 `docker context inspect` 深入了解更多细节。
以下示例展示如何检查名为 `default` 的上下文。

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

你可以使用 `docker context create` 命令创建新上下文。

以下示例创建一个名为 `docker-test` 的新上下文，并指定
上下文的主机端点为 TCP 套接字 `tcp://docker:2375`。

```console
$ docker context create docker-test --docker host=tcp://docker:2375
docker-test
Successfully created context "docker-test"
```

新上下文存储在 `~/.docker/contexts/` 下的 `meta.json` 文件中。
你创建的每个新上下文都会在 `~/.docker/contexts/` 的专用子目录中获得自己的 `meta.json` 文件。

你可以使用 `docker context ls` 和 `docker context inspect <context-name>` 查看新上下文。

```console
$ docker context ls
NAME          DESCRIPTION                             DOCKER ENDPOINT               ERROR
default *                                             unix:///var/run/docker.sock
docker-test                                           tcp://docker:2375
```

当前上下文用星号（"\*"）表示。

## 使用不同的上下文

你可以使用 `docker context use` 在上下文之间切换。

以下命令将 `docker` CLI 切换为使用 `docker-test` 上下文。

```console
$ docker context use docker-test
docker-test
Current context is now "docker-test"
```

通过列出所有上下文并确保星号（"\*"）在 `docker-test` 上下文旁边来验证操作。

```console
$ docker context ls
NAME            DESCRIPTION                           DOCKER ENDPOINT               ERROR
default                                               unix:///var/run/docker.sock
docker-test *                                         tcp://docker:2375
```

`docker` 命令现在将针对 `docker-test` 上下文中定义的端点。

你也可以使用 `DOCKER_CONTEXT` 环境变量设置当前上下文。
环境变量会覆盖使用 `docker context use` 设置的上下文。

使用下面相应的命令通过环境变量将上下文设置为 `docker-test`。

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

运行 `docker context ls` 验证 `docker-test` 上下文现在是
活动上下文。

你也可以使用全局 `--context` 标志来覆盖上下文。
以下命令使用名为 `production` 的上下文。

```console
$ docker --context production container ls
```

## 导出和导入 Docker 上下文

你可以使用 `docker context export` 和 `docker context import` 命令
在不同主机上导出和导入上下文。

`docker context export` 命令将现有上下文导出到文件。
该文件可以在任何安装了 `docker` 客户端的主机上导入。

### 导出和导入上下文

以下示例导出名为 `docker-test` 的现有上下文。
它将被写入名为 `docker-test.dockercontext` 的文件。

```console
$ docker context export docker-test
Written file "docker-test.dockercontext"
```

检查导出文件的内容。

```console
$ cat docker-test.dockercontext
```

使用 `docker context import` 在另一台主机上导入此文件
以创建具有相同配置的上下文。

```console
$ docker context import docker-test docker-test.dockercontext
docker-test
Successfully imported context "docker-test"
```

你可以使用 `docker context ls` 验证上下文已导入。

导入命令的格式是 `docker context import <context-name> <context-file>`。

## 更新上下文

你可以使用 `docker context update` 更新现有上下文中的字段。

以下示例更新现有 `docker-test` 上下文中的描述字段。

```console
$ docker context update docker-test --description "Test context"
docker-test
Successfully updated context "docker-test"
```
