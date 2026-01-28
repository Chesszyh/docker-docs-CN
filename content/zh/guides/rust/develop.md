--- 
title: 开发你的 Rust 应用程序
linkTitle: 开发你的应用
weight: 20
keywords: rust, local, development, run,
description: 了解如何在本地开发你的 Rust 应用程序。
alias: 
  - /language/rust/develop/
  - /guides/language/rust/develop/
---

## 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你已完成 Docker Desktop [学习中心](/manuals/desktop/use-desktop/_index.md) 中的演练，了解了 Docker 概念。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

## 概述

在本节中，你将学习如何在 Docker 中使用卷和网络。你还将使用 Docker 构建镜像，并使用 Docker Compose 使一切变得更加简单。

首先，你将了解如何在容器中运行数据库，以及如何使用卷和网络来持久化数据并让应用程序与数据库通信。然后，你将把所有内容整合到一个 Compose 文件中，这让你只需一个命令即可设置并运行本地开发环境。

## 在容器中运行数据库

你可以使用 PostgreSQL 的 Docker 官方镜像并在容器中运行它，而不是下载 PostgreSQL、安装、配置，然后作为服务运行 PostgreSQL 数据库。

在容器中运行 PostgreSQL 之前，创建一个 Docker 可以管理的卷来存储你的持久化数据和配置。使用 Docker 提供的命名卷功能，而不是使用绑定挂载。

运行以下命令来创建你的卷。

```console
$ docker volume create db-data
```

现在创建一个你的应用程序和数据库将用来相互通信的网络。该网络称为用户定义的桥接网络，并为你提供一个很好的 DNS 查找服务，你在创建连接字符串时可以使用它。

```console
$ docker network create postgresnet
```

现在你可以在容器中运行 PostgreSQL 并附加到你之前创建的卷和网络。Docker 会从 Hub 拉取镜像并在本地为你运行。
在以下命令中，选项 `--mount` 用于启动带有卷的容器。有关更多信息，请参阅 [Docker 卷](/manuals/engine/storage/volumes.md)。

```console
$ docker run --rm -d --mount \
  "type=volume,src=db-data,target=/var/lib/postgresql/data" \
  -p 5432:5432 \
  --network postgresnet \
  --name db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=example \
  postgres
```

现在，确保你的 PostgreSQL 数据库正在运行，并且你可以连接到它。连接到容器内正在运行的 PostgreSQL 数据库。

```console
$ docker exec -it db psql -U postgres
```

你应该会看到类似以下的输出。

```console
psql (15.3 (Debian 15.3-1.pgdg110+1))
Type "help" for help.

postgres=#
```

在前面的命令中，你通过将 `psql` 命令传递给 `db` 容器登录到了 PostgreSQL 数据库。按 ctrl-d 退出 PostgreSQL 交互式终端。

## 获取并运行示例应用程序

对于示例应用程序，你将使用来自 [Awesome Compose](https://github.com/docker/awesome-compose/tree/master/react-rust-postgres) 的 react-rust-postgres 应用程序后端的变体。

1. 使用以下命令克隆示例应用程序存储库。

   ```console
   $ git clone https://github.com/docker/docker-rust-postgres
   ```

2. 在克隆的存储库目录中，运行 `docker init` 来创建必要的 Docker 文件。参考以下示例来回答 `docker init` 的提示。

   ```console
   $ docker init
   Welcome to the Docker Init CLI!

   This utility will walk you through creating the following files with sensible defaults for your project:
     - .dockerignore
     - Dockerfile
     - compose.yaml
     - README.Docker.md

   Let's get started!

   ? What application platform does your project use? Rust
   ? What version of Rust do you want to use? 1.70.0
   ? What port does your server listen on? 8000
   ```

3. 在克隆的存储库目录中，在 IDE 或文本编辑器中打开 `Dockerfile` 以更新它。

   `docker init` 处理了 Dockerfile 中大部分指令的创建，但你需要针对你的特定应用程序更新它。除了 `src` 目录外，此应用程序还包含一个 `migrations` 目录来初始化数据库。在 Dockerfile 的构建阶段添加 `migrations` 目录的绑定挂载。以下是更新后的 Dockerfile。

   ```dockerfile {hl_lines="28"}
   # syntax=docker/dockerfile:1

   # Comments are provided throughout this file to help you get started.
   # If you need more help, visit the Dockerfile reference guide at
   # https://docs.docker.com/reference/dockerfile/

   ################################################################################
   # Create a stage for building the application.

   ARG RUST_VERSION=1.70.0
   ARG APP_NAME=react-rust-postgres
   FROM rust:${RUST_VERSION}-slim-bullseye AS build
   ARG APP_NAME
   WORKDIR /app

   # Build the application.
   # Leverage a cache mount to /usr/local/cargo/registry/
   # for downloaded dependencies and a cache mount to /app/target/ for
   # compiled dependencies which will speed up subsequent builds.
   # Leverage a bind mount to the src directory to avoid having to copy the
   # source code into the container. Once built, copy the executable to an
   # output directory before the cache mounted /app/target is unmounted.
   RUN --mount=type=bind,source=src,target=src \
       --mount=type=bind,source=Cargo.toml,target=Cargo.toml \
       --mount=type=bind,source=Cargo.lock,target=Cargo.lock \
       --mount=type=cache,target=/app/target/ \
       --mount=type=cache,target=/usr/local/cargo/registry/ \
       --mount=type=bind,source=migrations,target=migrations \
       <<EOF
   set -e
   cargo build --locked --release
   cp ./target/release/$APP_NAME /bin/server
   EOF

   ################################################################################
   # Create a new stage for running the application that contains the minimal
   # runtime dependencies for the application. This often uses a different base
   # image from the build stage where the necessary files are copied from the build
   # stage.
   #
   # The example below uses the debian bullseye image as the foundation for    running the app.
   # By specifying the "bullseye-slim" tag, it will also use whatever happens to    be the
   # most recent version of that tag when you build your Dockerfile. If
   # reproducibility is important, consider using a digest
   # (e.g.,    debian@sha256:ac707220fbd7b67fc19b112cee8170b41a9e97f703f588b2cdbbcdcecdd8af57).
   FROM debian:bullseye-slim AS final

   # Create a non-privileged user that the app will run under.
   # See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/   #user
   ARG UID=10001
   RUN adduser \
       --disabled-password \
       --gecos "" \
       --home "/nonexistent" \
       --shell "/sbin/nologin" \
       --no-create-home \
       --uid "${UID}" \
       appuser
   USER appuser

   # Copy the executable from the "build" stage.
   COPY --from=build /bin/server /bin/

   # Expose the port that the application listens on.
   EXPOSE 8000

   # What the container should run when it is started.
   CMD ["/bin/server"]
   ```

4. 在克隆的存储库目录中，运行 `docker build` 来构建镜像。

   ```console
   $ docker build -t rust-backend-image .
   ```

5. 运行带有以下选项的 `docker run`，以在与数据库相同的网络上将镜像作为容器运行。

   ```console
   $ docker run \
     --rm -d \
     --network postgresnet \
     --name docker-develop-rust-container \
     -p 3001:8000 \
     -e PG_DBNAME=example \
     -e PG_HOST=db \
     -e PG_USER=postgres \
     -e PG_PASSWORD=mysecretpassword \
     -e ADDRESS=0.0.0.0:8000 \
     -e RUST_LOG=debug \
     rust-backend-image
   ```

6. 使用 Curl 访问应用程序以验证它是否连接到数据库。

   ```console
   $ curl http://localhost:3001/users
   ```

   你应该会得到类似以下的响应。

   ```json
   [{ "id": 1, "login": "root" }]
   ```

## 使用 Compose 进行本地开发

当你运行 `docker init` 时，除了 `Dockerfile` 之外，它还会创建一个 `compose.yaml` 文件。

这个 Compose 文件非常方便，因为你不必键入所有参数来传递给 `docker run` 命令。你可以使用 Compose 文件声明性地做到这一点。

在克隆的存储库目录中，在 IDE 或文本编辑器中打开 `compose.yaml` 文件。`docker init` 处理了大部分指令的创建，但你需要针对你的特定应用程序更新它。

你需要更新 `compose.yaml` 文件中的以下项目：

- 取消注释所有数据库指令。
- 在服务器服务下添加环境变量。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines=["17-23","30-55"]} 
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker compose reference guide at
# https://docs.docker.com/reference/compose-file/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8000:8000
    environment:
      - PG_DBNAME=example
      - PG_HOST=db
      - PG_USER=postgres
      - PG_PASSWORD=mysecretpassword
      - ADDRESS=0.0.0.0:8000
      - RUST_LOG=debug
    # The commented out section below is an example of how to define a PostgreSQL
    # database that your application can use. `depends_on` tells Docker Compose to
    # start the database before your application. The `db-data` volume persists the
    # database data between container restarts. The `db-password` secret is used
    # to set the database password. You must create `db/password.txt` and add
    # a password of your choosing to it before running `docker compose up`.
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

请注意，该文件没有为这两个服务指定网络。当你使用 Compose 时，它​​会自动创建一个网络并将服务连接到它。有关更多信息，请参阅 [Compose 中的网络](/manuals/compose/how-tos/networking.md)。

在使用 Compose 运行应用程序之前，请注意此 Compose 文件指定了一个 `password.txt` 文件来保存数据库的密码。你必须创建此文件，因为它不包含在源存储库中。

在克隆的存储库目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件，其中包含数据库的密码。使用你喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件中。

```text
mysecretpassword
```

如果你有任何从前几节运行的其他容器，请现在 [停止](./run-containers.md#stop-start-and-name-containers) 它们。

现在，运行以下 `docker compose up` 命令来启动你的应用程序。

```console
$ docker compose up --build
```

该命令传递了 `--build` 标志，以便 Docker 编译你的镜像然后启动容器。

现在测试你的 API 端点。打开一个新终端，然后使用 curl 命令向服务器发出请求：

```console
$ curl http://localhost:8000/users
```

你应该收到以下响应：

```json
[{ "id": 1, "login": "root" }]
```

## 总结

在本节中，你了解了如何设置 Compose 文件以使用单个命令运行 Rust 应用程序和数据库。

相关信息：

- [Docker 卷](/manuals/engine/storage/volumes.md)
- [Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，你将了解如何使用 GitHub Actions 设置 CI/CD 管道。
