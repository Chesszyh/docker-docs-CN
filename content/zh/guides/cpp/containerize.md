---
title: 容器化 C++ 应用程序
linkTitle: 使用 Docker Compose 构建和运行 C++ 应用程序
weight: 10
keywords: C++, containerize, initialize
description: 学习如何使用 Docker Compose 构建和运行 C++ 应用程序。
aliases:
  - /language/cpp/containerize/
  - /guides/language/cpp/containerize/
---

## 前提条件

- 您需要有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 概述

本节将引导您完成使用 Docker Compose 容器化和运行 C++ 应用程序的过程。

## 获取示例应用程序

我们使用的是与本指南前几节相同的示例仓库。如果您还没有克隆该仓库，请现在克隆：

```console
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

现在您的 `c-plus-plus-docker`（根）目录中应该有以下内容。

```text
├── c-plus-plus-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── ok_api.cpp
│ └── README.md

```

要了解仓库中文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yml](/reference/compose-file/_index.md)

## 运行应用程序

在 `c-plus-plus-docker` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项使应用程序在后台运行，与终端分离。在 `c-plus-plus-docker` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI
参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化和运行 C++ 应用程序。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，您将学习如何使用容器开发应用程序。
