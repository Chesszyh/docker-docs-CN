---
title: 容器化 PHP 应用程序
linkTitle: 容器化你的应用
weight: 10
keywords: php, containerize, initialize, apache, composer
description: 了解如何容器化 PHP 应用程序。
aliases:
  - /language/php/containerize/
  - /guides/language/php/containerize/
---

## 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

## 概览

本节将带你完成容器化和运行 PHP 应用程序的过程。

## 获取示例应用程序

在本指南中，你将使用一个预构建的 PHP 应用程序。该应用程序使用 Composer 进行库依赖项管理。你将通过 Apache Web 服务器提供该应用程序。

打开终端，将目录更改为你想要工作的目录，然后运行以下命令来克隆存储库。

```console
$ git clone https://github.com/docker/docker-php-sample
```

示例应用程序是一个基本的 hello world 应用程序和一个在数据库中递增计数器的应用程序。此外，该应用程序使用 PHPUnit 进行测试。

## 初始化 Docker 资产

现在你拥有了一个应用程序，你可以使用 `docker init` 来创建必要的 Docker 资产来容器化你的应用程序。在 `docker-php-sample` 目录内，在终端中运行 `docker init` 命令。`docker init` 提供了一些默认配置，但你需要回答几个关于你的应用程序的问题。例如，此应用程序使用 PHP 版本 8.2。参考以下 `docker init` 示例并为你的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? PHP with Apache
? What version of PHP do you want to use? 8.2
? What's the relative directory (with a leading .) for your app? ./src
? What local port do you want to use to access your server? 9000
```

现在你的 `docker-php-sample` 目录中应该有以下内容。

```text
├── docker-php-sample/
│ ├── .git/
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── composer.json
│ ├── composer.lock
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

要了解有关 `docker init` 添加的文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `docker-php-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 查看应用程序。你应该看到一个简单的 hello world 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项，使应用程序脱离终端运行。在 `docker-php-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 查看应用程序。你应该看到一个简单的 hello world 应用程序。

在终端中，运行以下命令以停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，你学习了如何使用 Docker 容器化并运行一个简单的 PHP 应用程序。

相关信息：

- [docker init 参考](/reference/cli/docker/init.md)

## 后续步骤

在下一节中，你将学习如何使用 Docker 容器开发你的应用程序。
