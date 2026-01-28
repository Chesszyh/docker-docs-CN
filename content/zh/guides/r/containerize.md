---
title: 容器化 R 应用程序
linkTitle: 容器化您的应用
weight: 10
keywords: R, containerize, initialize
description: 学习如何容器化 R 应用程序。
aliases:
  - /language/R/build-images/
  - /language/R/run-containers/
  - /language/r/containerize/
  - /guides/language/r/containerize/
---

## 前提条件

- 您有一个 [git 客户端](https://git-scm.com/downloads)。本节示例使用命令行 git 客户端，但您可以使用任何客户端。

## 概述

本节将引导您完成 R 应用程序的容器化和运行。

## 获取示例应用程序

示例应用程序使用流行的 [Shiny](https://shiny.posit.co/) 框架。

克隆示例应用程序以配合本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git && cd r-docker-dev
```

现在您的 `r-docker-dev` 目录中应该包含以下内容。

```text
├── r-docker-dev/
│ ├── src/
│ │ └── app.R
│ ├── src_db/
│ │ └── app_db.R
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

要了解更多关于仓库中文件的信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `r-docker-dev` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，访问 [http://localhost:3838](http://localhost:3838) 查看应用程序。您应该能看到一个简单的 Shiny 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项使应用程序在后台运行，脱离终端。在 `r-docker-dev` 目录中，在终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，访问 [http://localhost:3838](http://localhost:3838)。

您应该能看到一个简单的 Shiny 应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI
参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化并运行 R 应用程序。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，您将学习如何使用容器开发应用程序。
