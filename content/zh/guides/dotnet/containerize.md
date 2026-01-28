---
title: 容器化 .NET 应用程序
linkTitle: 容器化你的应用
weight: 10
keywords: .net, 容器化, 初始化
description: 学习如何容器化 ASP.NET 应用程序。
aliases:
- /language/dotnet/build-images/
- /language/dotnet/run-containers/
- /language/dotnet/containerize/
- /guides/language/dotnet/containerize/
---

## 前提条件

* 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
* 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用命令行 git 客户端，但你可以使用任何客户端。

## 概述

本节将引导你完成 .NET 应用程序的容器化和运行。

## 获取示例应用程序

在本指南中，你将使用一个预构建的 .NET 应用程序。该应用程序类似于 Docker 博客文章[使用 Docker Desktop 构建多容器 .NET 应用程序](https://www.docker.com/blog/building-multi-container-net-app-using-docker-desktop/)中构建的应用程序。

打开终端，切换到你想要工作的目录，然后运行以下命令克隆仓库。

```console
$ git clone https://github.com/docker/docker-dotnet-sample
```

## 初始化 Docker 资源

现在你有了一个应用程序，可以使用 `docker init` 创建容器化应用程序所需的 Docker 资源。在 `docker-dotnet-sample` 目录中，在终端中运行 `docker init` 命令。`docker init` 提供了一些默认配置，但你需要回答一些关于应用程序的问题。参考以下示例来回答 `docker init` 的提示，并对你的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? ASP.NET Core
? What's the name of your solution's main project? myWebApp
? What version of .NET do you want to use? 8.0
? What local port do you want to use to access your server? 8080
```

现在你的 `docker-dotnet-sample` 目录中应该有以下内容。

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── src/
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

要了解更多关于 `docker init` 添加的文件，请参阅以下内容：
 - [Dockerfile](/reference/dockerfile.md)
 - [.dockerignore](/reference/dockerfile.md#dockerignore-file)
 - [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `docker-dotnet-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。你应该能看到一个简单的 Web 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项使应用程序与终端分离运行。在 `docker-dotnet-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。你应该能看到一个简单的 Web 应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，你学习了如何使用 Docker 容器化和运行 .NET 应用程序。

相关信息：
 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件参考](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，你将学习如何使用 Docker 容器开发应用程序。
