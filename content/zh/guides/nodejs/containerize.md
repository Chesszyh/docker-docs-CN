---
title: 容器化 Node.js 应用程序
linkTitle: 容器化你的应用
weight: 10
keywords: node.js, node, containerize, initialize
description: 学习如何容器化 Node.js 应用程序。
aliases:
  - /get-started/nodejs/build-images/
  - /language/nodejs/build-images/
  - /language/nodejs/run-containers/
  - /language/nodejs/containerize/
  - /guides/language/nodejs/containerize/
---

## 前提条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用命令行 git 客户端，但你可以使用任何客户端。

## 概述

本节将引导你完成容器化和运行 Node.js 应用程序的过程。

## 获取示例应用程序

克隆用于本指南的示例应用程序。打开终端，切换到你想要工作的目录，然后运行以下命令来克隆仓库：

```console
$ git clone https://github.com/docker/docker-nodejs-sample && cd docker-nodejs-sample
```

## 初始化 Docker 资源

现在你有了一个应用程序，可以创建必要的 Docker 资源来容器化你的应用程序。你可以使用 Docker Desktop 内置的 Docker Init 功能来帮助简化这个过程，或者手动创建这些资源。

{{< tabs >}}
{{< tab name="Use Docker Init" >}}

在 `docker-nodejs-sample` 目录中，在终端运行 `docker init` 命令。`docker init` 提供一些默认配置，但你需要回答几个关于应用程序的问题。请参考以下示例回答 `docker init` 的提示，并为你的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Node
? What version of Node do you want to use? 18.0.0
? Which package manager do you want to use? npm
? What command do you want to use to start the app: node src/index.js
? What port does your server listen on? 3000
```

{{< /tab >}}
{{< tab name="Manually create assets" >}}

如果你没有安装 Docker Desktop 或更喜欢手动创建资源，可以在项目目录中创建以下文件。

创建一个名为 `Dockerfile` 的文件，内容如下。

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG NODE_VERSION=18.0.0

FROM node:${NODE_VERSION}-alpine

# Use production node environment by default.
ENV NODE_ENV production


WORKDIR /usr/src/app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
# Leverage a bind mounts to package.json and package-lock.json to avoid having to copy them into
# into this layer.
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev

# Run the application as a non-root user.
USER node

# Copy the rest of the source files into the image.
COPY . .

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD node src/index.js
```

创建一个名为 `compose.yaml` 的文件，内容如下。

```yaml {collapse=true,title=compose.yaml}
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    environment:
      NODE_ENV: production
    ports:
      - 3000:3000
# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must create `db/password.txt` and add
# a password of your choosing to it before running `docker compose up`.
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql/data
#     environment:
#       - POSTGRES_DB=example
#       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
#     expose:
#       - 5432
#     healthcheck:
#       test: [ "CMD", "pg_isready" ]
#       interval: 10s
#       timeout: 5s
#       retries: 5
# volumes:
#   db-data:
# secrets:
#   db-password:
#     file: db/password.txt
```

创建一个名为 `.dockerignore` 的文件，内容如下。

```text {collapse=true,title=".dockerignore"}
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/.next
**/.cache
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/charts
**/docker-compose*
**/compose.y*ml
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
**/build
**/dist
LICENSE
README.md
```

{{< /tab >}}
{{< /tabs >}}

你的 `docker-nodejs-sample` 目录现在应该至少包含以下内容。

```text
├── docker-nodejs-sample/
│ ├── spec/
│ ├── src/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── package-lock.json
│ ├── package.json
│ └── README.md
```

要了解更多关于这些文件的信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `docker-nodejs-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 查看应用程序。你应该会看到一个简单的待办事项应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项使应用程序在后台运行，与终端分离。在 `docker-nodejs-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 查看应用程序。

你应该会看到一个简单的待办事项应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，你学习了如何使用 Docker 容器化和运行 Node.js 应用程序。

相关信息：

- [Dockerfile 参考](/reference/dockerfile.md)
- [.dockerignore 文件参考](/reference/dockerfile.md#dockerignore-file)
- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，你将学习如何使用容器开发你的应用程序。
