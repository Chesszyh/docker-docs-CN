---
title: 覆盖容器默认值
weight: 2
keywords: concepts, build, images, container, docker desktop
description: 本概念页面将教您如何使用 `docker run` 命令覆盖容器默认值。
aliases:
 - /guides/docker-concepts/running-containers/overriding-container-defaults/
---

{{< youtube-embed PFszWK3BB8I >}}

## 概念解释

当 Docker 容器启动时，它会执行应用程序或命令。容器从其镜像的配置中获取此可执行文件（脚本或文件）。容器带有通常运行良好的默认设置，但如果需要，您可以更改它们。这些调整有助于容器的程序按您希望的方式运行。

例如，如果您有一个现有的数据库容器监听标准端口，并且您想运行同一数据库容器的新实例，那么您可能需要更改新容器监听的端口设置，以免与现有容器冲突。有时您可能想增加容器可用的内存，如果程序需要更多资源来处理繁重的工作负载，或者设置环境变量以提供程序正常运行所需的特定配置详情。

`docker run` 命令提供了一种强大的方式来覆盖这些默认值，并根据您的喜好定制容器的行为。该命令提供多个标志，让您可以即时自定义容器行为。

以下是一些实现方法。

### 覆盖网络端口

有时您可能希望为开发和测试目的使用单独的数据库实例。在同一端口上运行这些数据库实例可能会产生冲突。您可以使用 `docker run` 中的 `-p` 选项将容器端口映射到主机端口，允许您运行多个容器实例而不会发生冲突。

```console
$ docker run -d -p HOST_PORT:CONTAINER_PORT postgres
```

### 设置环境变量

此选项在容器内设置一个值为 `bar` 的环境变量 `foo`。

```console
$ docker run -e foo=bar postgres env
```

您将看到如下输出：

```console
HOSTNAME=2042f2e6ebe4
foo=bar
```

> [!TIP]
>
> `.env` 文件是为 Docker 容器设置环境变量的便捷方式，无需在命令行中使用大量 `-e` 标志。要使用 `.env` 文件，您可以在 `docker run` 命令中传递 `--env-file` 选项。
> ```console
> $ docker run --env-file .env postgres env
> ```

### 限制容器消耗的资源

您可以使用 `docker run` 命令的 `--memory` 和 `--cpus` 标志来限制容器可以使用的 CPU 和内存量。例如，您可以为 Python API 容器设置内存限制，防止它在主机上消耗过多资源。以下是命令：

```console
$ docker run -e POSTGRES_PASSWORD=secret --memory="512m" --cpus="0.5" postgres
 ```

此命令将容器内存使用限制为 512 MB，并定义 0.5 的 CPU 配额（半个核心）。

> **监控实时资源使用情况**
>
> 您可以使用 `docker stats` 命令监控正在运行的容器的实时资源使用情况。这有助于您了解分配的资源是否足够或需要调整。

通过有效使用这些 `docker run` 标志，您可以定制容器化应用程序的行为以满足您的特定要求。

## 动手实践

在本动手指南中，您将了解如何使用 `docker run` 命令覆盖容器默认值。

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

### 运行多个 Postgres 数据库实例

1.  使用以下命令通过 [Postgres 镜像](https://hub.docker.com/_/postgres)启动容器：

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres
    ```

    这将在后台启动 Postgres 数据库，监听标准容器端口 `5432` 并映射到主机的端口 `5432`。

2. 启动另一个映射到不同端口的 Postgres 容器。

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5433:5432 postgres
    ```

    这将在后台启动另一个 Postgres 容器，监听容器内的标准 postgres 端口 `5432`，但映射到主机的端口 `5433`。您覆盖主机端口只是为了确保这个新容器不会与现有运行的容器冲突。

3. 通过进入 Docker Desktop 仪表板的 **Containers** 视图验证两个容器都在运行。

    ![Docker Desktop 仪表板的截图，显示正在运行的 Postgres 容器实例](images/running-postgres-containers.webp?border=true)

### 在受控网络中运行 Postgres 容器

默认情况下，当您运行容器时，它们会自动连接到一个称为桥接网络（bridge network）的特殊网络。此桥接网络充当虚拟桥梁，允许同一主机上的容器相互通信，同时将它们与外部世界和其他主机隔离。这是大多数容器交互的便捷起点。但是，对于特定场景，您可能需要对网络配置有更多控制。

这就是自定义网络发挥作用的地方。您可以通过在 `docker run` 命令中传递 `--network` 标志来创建自定义网络。所有没有 `--network` 标志的容器都连接到默认桥接网络。

按照以下步骤了解如何将 Postgres 容器连接到自定义网络。

1. 使用以下命令创建新的自定义网络：

    ```console
    $ docker network create mynetwork
    ```

2. 通过运行以下命令验证网络：

    ```console
    $ docker network ls
    ```

    此命令列出所有网络，包括新创建的"mynetwork"。

3. 使用以下命令将 Postgres 连接到自定义网络：

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5434:5432 --network mynetwork postgres
    ```

    这将在后台启动 Postgres 容器，映射到主机端口 5434 并连接到 `mynetwork` 网络。您传递了 `--network` 参数来覆盖容器默认值，将容器连接到自定义 Docker 网络以实现更好的隔离和与其他容器的通信。您可以使用 `docker network inspect` 命令查看容器是否连接到这个新的桥接网络。


    > **默认桥接网络和自定义网络之间的主要区别**
    >
    > 1. DNS 解析：默认情况下，连接到默认桥接网络的容器可以相互通信，但只能通过 IP 地址（除非您使用 `--link` 选项，该选项被认为是遗留的）。由于各种[技术缺陷](/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge)，不建议在生产中使用。在自定义网络上，容器可以通过名称或别名相互解析。
    > 2. 隔离性：所有没有指定 `--network` 的容器都连接到默认桥接网络，因此可能存在风险，因为不相关的容器能够通信。使用自定义网络提供范围网络，只有连接到该网络的容器才能通信，从而提供更好的隔离。

### 管理资源

默认情况下，容器的资源使用不受限制。但是，在共享系统上，有效管理资源至关重要。重要的是不要让运行中的容器消耗太多主机的内存。

这就是 `docker run` 命令再次发挥作用的地方。它提供了 `--memory` 和 `--cpus` 等标志来限制容器可以使用的 CPU 和内存量。

```console
$ docker run -d -e POSTGRES_PASSWORD=secret --memory="512m" --cpus=".5" postgres
```

`--cpus` 标志指定容器的 CPU 配额。这里设置为半个 CPU 核心（0.5），而 `--memory` 标志指定容器的内存限制。在本例中，设置为 512 MB。

### 在 Docker Compose 中覆盖默认的 CMD 和 ENTRYPOINT



有时，您可能需要覆盖 Docker 镜像中定义的默认命令（`CMD`）或入口点（`ENTRYPOINT`），特别是在使用 Docker Compose 时。

1. 创建一个 `compose.yml` 文件，内容如下：

    ```yaml
    services:
      postgres:
        image: postgres
        entrypoint: ["docker-entrypoint.sh", "postgres"]
        command: ["-h", "localhost", "-p", "5432"]
        environment:
          POSTGRES_PASSWORD: secret
    ```


    Compose 文件定义了一个名为 `postgres` 的服务，使用官方 Postgres 镜像，设置入口点脚本，并使用密码认证启动容器。

2. 通过运行以下命令启动服务：

    ```console
    $ docker compose up -d
    ```

    此命令启动 Docker Compose 文件中定义的 Postgres 服务。

3. 使用 Docker Desktop 仪表板验证认证。

    打开 Docker Desktop 仪表板，选择 **Postgres** 容器并选择 **Exec** 进入容器 shell。您可以输入以下命令连接到 Postgres 数据库：

    ```console
    # psql -U postgres
    ```

    ![Docker Desktop 仪表板的截图，选择 Postgres 容器并使用 EXEC 按钮进入其 shell](images/exec-into-postgres-container.webp?border=true)


    > [!NOTE]
    >
    > PostgreSQL 镜像在本地设置了信任认证，因此您可能会注意到从 localhost（同一容器内）连接时不需要密码。但是，如果从不同的主机/容器连接，则需要密码。

### 使用 `docker run` 覆盖默认的 CMD 和 ENTRYPOINT

您也可以使用以下命令直接通过 `docker run` 命令覆盖默认值：

```console
$ docker run -e POSTGRES_PASSWORD=secret postgres docker-entrypoint.sh -h localhost -p 5432
```

此命令运行 Postgres 容器，设置密码认证的环境变量，覆盖默认启动命令并配置主机名和端口映射。


## 其他资源

* [使用 Compose 设置环境变量的方法](/compose/how-tos/environment-variables/set-environment-variables/)
* [什么是容器](/get-started/docker-concepts/the-basics/what-is-a-container/)

## 后续步骤

现在您已经学习了覆盖容器默认值，是时候学习如何持久化容器数据了。

{{< button text="持久化容器数据" url="persisting-container-data" >}}
