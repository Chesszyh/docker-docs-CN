---
title: 容器化 Bun 应用程序
linkTitle: 容器化你的应用
weight: 10
keywords: bun, containerize, initialize
description: 了解如何容器化 Bun 应用程序。
aliases:
  - /language/bun/containerize/
---

## 先决条件

* 你有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 概览

很长一段时间以来，Node.js 一直是服务器端 JavaScript 应用程序的事实标准运行时。近年来，生态系统中出现了新的替代运行时，包括 [Bun 网站](https://bun.sh/)。像 Node.js 一样，Bun 是一个 JavaScript 运行时。Bun 是一个相对轻量级的运行时，旨在实现快速和高效。

为什么要使用 Docker 开发 Bun 应用程序？有多个运行时可供选择是很好的。但随着运行时数量的增加，在不同环境中一致地管理不同的运行时及其依赖项变得具有挑战性。这就是 Docker 发挥作用的地方。按需创建和销毁容器是管理不同运行时及其依赖项的好方法。此外，由于它是一个相当新的运行时，为 Bun 获取一致的开发环境可能具有挑战性。Docker 可以帮助你为 Bun 设置一致的开发环境。

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，将目录更改为你想要工作的目录，然后运行以下命令来克隆存储库：

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

现在你的 `bun-docker` 目录中应该有以下内容。

```text
├── bun-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.js
│ └── README.md
```

在 Dockerfile 中，你会注意到 `FROM` 指令使用 `oven/bun` 作为基础镜像。这是 Oven（Bun 背后的公司）创建的官方 Bun 镜像。此镜像 [可在 Docker Hub 上获取](https://hub.docker.com/r/oven/bun)。

```dockerfile
# Use the Bun image as the base image
FROM oven/bun:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port on which the API will listen
EXPOSE 3000

# Run the server when the container launches
CMD ["bun", "server.js"]
```

除了指定 `oven/bun` 作为基础镜像外，此 Dockerfile 还：

- 将容器中的工作目录设置为 `/app`
- 将当前目录的内容复制到容器中的 `/app` 目录
- 公开端口 3000，API 在该端口监听请求
- 最后，当容器启动时，使用命令 `bun server.js` 启动服务器。

## 运行应用程序

在 `bun-docker` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:3000](http://localhost:3000) 查看应用程序。你将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项，使应用程序脱离终端运行。在 `bun-docker` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:3000](http://localhost:3000) 查看应用程序。

在终端中，运行以下命令以停止应用程序。

```console
$ docker compose down
```

## 总结

在本节中，你学习了如何使用 Docker 容器化并运行你的 Bun 应用程序。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概览](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)

## 后续步骤

在下一节中，你将学习如何使用容器开发你的应用程序。
