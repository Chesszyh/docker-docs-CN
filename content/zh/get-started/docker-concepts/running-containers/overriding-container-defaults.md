---
title: 覆盖容器默认值
weight: 2
keywords: concepts, build, images, container, docker desktop
description: 此概念页面将教您如何使用 `docker run` 命令覆盖容器默认值。
aliases: 
 - /guides/docker-concepts/running-containers/overriding-container-defaults/
---

{{< youtube-embed PFszWK3BB8I >}}

## 说明

当 Docker 容器启动时，它会执行一个应用程序或命令。容器从其镜像的配置中获取此可执行文件（脚本或文件）。容器带有通常运行良好的默认设置，但如果需要，您可以更改它们。这些调整有助于容器的程序完全按照您的意愿运行。

例如，如果您有一个在标准端口上侦听的现有数据库容器，并且您想运行同一数据库容器的新实例，那么您可能希望更改新容器侦听的端口设置，以免与现有容器冲突。有时您可能希望增加容器可用的内存，如果程序需要更多资源来处理繁重的工作负载，或者设置环境变量以提供程序正常运行所需的特定配置详细信息。

`docker run` 命令提供了一种强大的方式来覆盖这些默认值并根据您的喜好定制容器的行为。该命令提供了几个标志，允许您随时自定义容器行为。

以下是您可以实现此目标的几种方法。

### 覆盖网络端口

有时您可能希望将单独的数据库实例用于开发和测试目的。在同一端口上运行这些数据库实例可能会发生冲突。您可以在 `docker run` 中使用 `-p` 选项将容器端口映射到主机端口，从而允许您运行容器的多个实例而不会发生任何冲突。

```console
$ docker run -d -p HOST_PORT:CONTAINER_PORT postgres
```

### 设置环境变量

此选项在容器内设置一个环境变量 `foo`，其值为 `bar`。

```console
$ docker run -e foo=bar postgres env
```

您将看到类似以下的输出：

```console
HOSTNAME=2042f2e6ebe4
foo=bar
```

> [!TIP]
>
> `.env` 文件是为 Docker 容器设置环境变量的便捷方式，而无需使用大量 `-e` 标志使命令行变得混乱。要使用 `.env` 文件，您可以在 `docker run` 命令中传递 `--env-file` 选项。
> ```console
> $ docker run --env-file .env postgres env
> ```

### 限制容器消耗资源

您可以将 `--memory` 和 `--cpus` 标志与 `docker run` 命令一起使用，以限制容器可以使用的 CPU 和内存量。例如，您可以为 Python API 容器设置内存限制，防止其消耗主机上过多的资源。这是命令：

```console
$ docker run -e POSTGRES_PASSWORD=secret --memory="512m" --cpus="0.5" postgres
 ```

此命令将容器内存使用限制为 512 MB，并将 CPU 配额定义为 0.5，即半个核心。

> **监控实时资源使用情况**
>
> 您可以使用 `docker stats` 命令监控正在运行的容器的实时资源使用情况。这有助于您了解分配的资源是否充足或需要调整。

通过有效地使用这些 `docker run` 标志，您可以定制容器化应用程序的行为以满足您的特定要求。

## 试一试

在这个动手指南中，您将看到如何使用 `docker run` 命令覆盖容器默认值。

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

### 运行 Postgres 数据库的多个实例

1.  使用 [Postgres 镜像](https://hub.docker.com/_/postgres) 启动容器，命令如下：
    
    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres
    ```

    这将在后台启动 Postgres 数据库，侦听标准容器端口 `5432` 并映射到主机上的端口 `5432`。

2. 启动第二个映射到不同端口的 Postgres 容器。

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5433:5432 postgres
    ```

    这将在后台启动另一个 Postgres 容器，在容器中侦听标准 postgres 端口 `5432`，但映射到主机上的端口 `5433`。您覆盖主机端口只是为了确保此新容器不会与现有正在运行的容器发生冲突。

3. 通过转到 Docker Desktop Dashboard 中的 **Containers** 视图验证两个容器是否都在运行。

    ![A screenshot of the Docker Desktop Dashboard showing the running instances of Postgres containers](images/running-postgres-containers.webp?border=true)

### 在受控网络中运行 Postgres 容器

默认情况下，当您运行容器时，它们会自动连接到一个名为桥接网络（bridge network）的特殊网络。此桥接网络就像一个虚拟桥梁，允许同一主机上的容器相互通信，同时使它们与外界和其他主机隔离。这是大多数容器交互的便捷起点。但是，对于特定场景，您可能希望更好地控制网络配置。

这就是自定义网络发挥作用的地方。您可以通过在 `docker run` 命令中传递 `--network` 标志来创建自定义网络。所有没有 `--network` 标志的容器都连接到默认桥接网络。

按照步骤查看如何将 Postgres 容器连接到自定义网络。

1. 使用以下命令创建一个新的自定义网络：

    ```console
    $ docker network create mynetwork
    ```

2. 通过运行以下命令验证网络：

    ```console
    $ docker network ls
    ```

    此命令列出所有网络，包括新创建的 "mynetwork"。

3. 使用以下命令将 Postgres 连接到自定义网络：

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5434:5432 --network mynetwork postgres
    ```

    这将在后台启动 Postgres 容器，映射到主机端口 5434 并连接到 `mynetwork` 网络。您传递了 `--network` 参数以通过将容器连接到自定义 Docker 网络来覆盖容器默认值，以便更好地隔离并与其他容器通信。您可以使用 `docker network inspect` 命令查看容器是否绑定到此新桥接网络。


    > **默认桥接网络与自定义网络的关键区别**
    >
    > 1. DNS 解析：默认情况下，连接到默认桥接网络的容器可以相互通信，但只能通过 IP 地址。（除非您使用被视为遗留的 `--link` 选项）。由于各种[技术缺陷](/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge)，不建议在生产中使用。在自定义网络上，容器可以通过名称或别名相互解析。
    > 2. 隔离：所有未指定 `--network` 的容器都连接到默认桥接网络，因此可能存在风险，因为不相关的容器也能够通信。使用自定义网络提供了一个范围网络，其中只有连接到该网络的容器才能通信，从而提供更好的隔离。

### 管理资源

默认情况下，容器的资源使用不受限制。但是，在共享系统上，有效管理资源至关重要。重要的是不要让正在运行的容器消耗过多的主机内存。

这又是 `docker run` 命令大显身手的地方。它提供了像 `--memory` 和 `--cpus` 这样的标志来限制容器可以使用的 CPU 和内存量。

```console
$ docker run -d -e POSTGRES_PASSWORD=secret --memory="512m" --cpus=".5" postgres
```

`--cpus` 标志指定容器的 CPU 配额。在这里，它设置为半个 CPU 核心 (0.5)，而 `--memory` 标志指定容器的内存限制。在这种情况下，它设置为 512 MB。

### 在 Docker Compose 中覆盖默认 CMD 和 ENTRYPOINT

有时，您可能需要覆盖 Docker 镜像中定义的默认命令 (`CMD`) 或入口点 (`ENTRYPOINT`)，尤其是在使用 Docker Compose 时。

1. 创建一个包含以下内容的 `compose.yml` 文件：

    ```yaml
    services:
      postgres:
        image: postgres
        entrypoint: ["docker-entrypoint.sh", "postgres"]
        command: ["-h", "localhost", "-p", "5432"]
        environment:
          POSTGRES_PASSWORD: secret 
    ```

    Compose 文件定义了一个名为 `postgres` 的服务，该服务使用官方 Postgres 镜像，设置入口点脚本，并使用密码身份验证启动容器。

2. 通过运行以下命令启动服务：

    ```console
    $ docker compose up -d
    ```

    此命令启动 Docker Compose 文件中定义的 Postgres 服务。

3. 使用 Docker Desktop Dashboard 验证身份验证。

    打开 Docker Desktop Dashboard，选择 **Postgres** 容器并选择 **Exec** 进入容器 shell。您可以键入以下命令以连接到 Postgres 数据库：

    ```console
    # psql -U postgres
    ```

    ![A screenshot of the Docker Desktop Dashboard selecting the Postgres container and entering into its shell using EXEC button](images/exec-into-postgres-container.webp?border=true)


    > [!NOTE]
    > 
    > PostgreSQL 镜像在本地设置信任身份验证，因此您可能会注意到从 localhost（同一容器内）连接时不需要密码。但是，如果从不同的主机/容器连接，则需要密码。

### 使用 `docker run` 覆盖默认 CMD 和 ENTRYPOINT

您还可以使用以下命令直接使用 `docker run` 命令覆盖默认值：

```console 
$ docker run -e POSTGRES_PASSWORD=secret postgres docker-entrypoint.sh -h localhost -p 5432
```

此命令运行一个 Postgres 容器，设置用于密码身份验证的环境变量，覆盖默认启动命令并配置主机名和端口映射。


## 其他资源

* [使用 Compose 设置环境变量的方法](/compose/how-tos/environment-variables/set-environment-variables/)
* [什么是容器](/get-started/docker-concepts/the-basics/what-is-a-container/)

## 下一步

既然您已了解如何覆盖容器默认值，是时候学习如何持久化容器数据了。

{{< button text="持久化容器数据" url="persisting-container-data" >}}