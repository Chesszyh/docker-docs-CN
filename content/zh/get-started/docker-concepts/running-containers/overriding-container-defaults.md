---
title: 覆盖容器默认值
weight: 2
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 此概念页面将教您如何使用 `docker run` 命令覆盖容器默认值。
aliases: 
 - /guides/docker-concepts/running-containers/overriding-container-defaults/
---

{{< youtube-embed PFszWK3BB8I >}}

## 说明

当 Docker 容器启动时，它会执行一个应用程序或命令。容器从其镜像的配置中获取此可执行文件（脚本或文件）。容器带有通常运行良好的默认设置，但如果需要，您可以更改它们。这些调整有助于容器的程序完全按照您想要的方式运行。

例如，如果您有一个现有的数据库容器在标准端口上侦听，并且您想运行同一个数据库容器的新实例，那么您可能需要更改新容器侦听的端口设置，以免它与现有容器冲突。有时，如果程序需要更多资源来处理繁重的工作负载，您可能需要增加容器可用的内存，或者设置环境变量以提供程序正常运行所需的特定配置详细信息。

`docker run` 命令提供了一种强大的方法来覆盖这些默认值并根据您的喜好定制容器的行为。该命令提供了几个标志，可让���动态自定义容器行为。

以下是实现此目的的几种方法。

### 覆盖网络端口

有时您可能希望为开发和测试目的使用单独的数据库实例。在同一端口上运行这些数据库实例可能会发生冲突。您可以在 `docker run` 中使用 `-p` 选项将容器端口映射到主机端口，从而允许您在没有任何冲突的情况下运行容器的多个实例。

```console
$ docker run -d -p HOST_PORT:CONTAINER_PORT postgres
```

### 设置环境变量

此选项在容器内设置一个名为 `foo` 的环境变量，其值为 `bar`。

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
> `.env` 文件是一种为 Docker 容器设置环境变量的便捷方法，无需在命令行中使用大量 `-e` 标志。要使用 `.env` 文件，您可以在 `docker run` 命令中传递 `--env-file` 选项。
> ```console
> $ docker run --env-file .env postgres env
> ```

### 限制容器消耗资源

您可以在 `docker run` 命令中使用 `--memory` 和 `--cpus` 标志来限制容器可以使用的 CPU 和内存量。例如，您可以为 Python API 容器设置内存限制，以防止其在主机上消耗过多资源。命令如下：

```console
$ docker run -e POSTGRES_PASSWORD=secret --memory="512m" --cpus="0.5" postgres
 ```

此命令将容器内存使用量限制为 512 MB，并将 CPU 配额定义为半个核心的 0.5。

> **监控实时资源使用情况**
>
> 您可以使用 `docker stats` 命令来监控正在运行的容器的实时资源使用情况。这有助于您了解分配的资源是否足够或需要调整。

通过有效地使用这些 `docker run` 标志，您可以根据您的特定要求定制容器化应用程序的行为。

## 动手试试

在这个动手指南中，您将看到如何使用 `docker run` 命令来覆盖容器默认值。

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

### 运行 Postgres 数据库的多个实例

1.  使用以下命令启动一个使用 [Postgres 镜像](https://hub.docker.com/_/postgres) 的容器：
    
    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres
    ```

    这将在后台启动 Postgres 数据库，侦听标准容器端口 `5432` 并映射到主机上的端口 `5432`。

2. 启动第二个映射到不同端口的 Postgres 容器。

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5433:5432 postgres
    ```

    这将在后台启动另一个 Postgres 容器，侦听容器中的标准 postgres 端口 `5432`，但映射到主机上的端口 `5433`。您覆盖主机端口只是为了确保这个新容器不会与现有的正在运行的容器冲突。

3. 通过转到 Docker Desktop 仪表板中的 **Containers** 视图来验证两个容器都在运行。

    ![显示正在运行的 Postgres 容器实例的 Docker Desktop 仪表板的屏幕截图](images/running-postgres-containers.webp?border=true)

### 在受控网络中运行 Postgres 容器

默认情况下，当您运行容器时，它们会自动连接到一个名为桥接网络的特殊网络。这个桥接网络就像一个虚拟网桥，允许同一主机上的容器相互通信，同时将它们与外部世界和其他主机隔离开来。对于大多数容器交互来说，这是一个方便的起点。但是，对于特定场景，您可能需要对网络配置进行更多控制。

这就是自定义网络的用武之地。您可以通过在 `docker run` 命令中传递 `--network` 标志来创建自定义网络。所有没有 `--network` 标志的容器都附加到默认的桥接网络。

按照以下步骤了解如何将 Postgres 容器连接到自定义网络。

1. 使用以下命令创建一个新的自定义网络：

    ```console
    $ docker network create mynetwork
    ```

2. 通过运行以下命令来验证网络：

    ```console
    $ docker network ls
    ```

    此命令列出所有网络，包括新创建的“mynetwork”。

3. 使用以下命令将 Postgres 连接到自定义网络：

    ```console
    $ docker run -d -e POSTGRES_PASSWORD=secret -p 5434:5432 --network mynetwork postgres
    ```

    这将在后台启动 Postgres 容器，映射到主机端口 5434 并附加到 `mynetwork` 网络。您传递了 `--network` 参数以通过将容器连接到自定义 Docker 网络来覆盖容器默认值，以实现更好的隔离和与其他容器的通信。您可以使用 `docker network inspect` 命令来查看容器是否已绑定到此新的桥接网络。


    > **默认桥接网络和自定义网络之间的主要区别**
    >
    > 1. DNS 解析：默认情况下，连接到默认桥接网络的容器可以相互通信，但只能通过 IP 地址。（除非您使用被认为是旧版的 `--link` 选项）。由于各种[技术缺陷](/engine/network/drivers/bridge/#differences-between-user-defined-bridges-and-the-default-bridge)，不建议在生产中使用它。在自定义网络上，容器可以通过名称或别名相互解析。
    > 2. 隔离：所有未指定 `--network` 的容器都附加到默认的桥接网络，因此可能存在风险，因为不相关的容器可以通信。使用自定义网络提供了一个作用域网络，其中只有附加到该网络的容器才能通信，从而提供更好的隔离。

### 管理资源

默认情况下，容器的资源使用不受限制。但是，在共享系统上，有效管理资源至关重要。重要的是不要让正在运行的容器消耗过多的主机内存。

这就是 `docker run` 命令再次发挥作用的地方。它提供了 `--memory` 和 `--cpus` 等标志来限制容器可以使用的 CPU 和内存量。

```console
$ docker run -d -e POSTGRES_PASSWORD=secret --memory="512m" --cpus=".5" postgres
```

`--cpus` 标志指定容器的 CPU 配额。在这里，它设置为半个 CPU 内核 (0.5)，而 `--memory` 标志指定容器的内存限制。在这种情况下，它设置为 512 MB。

### 在 Docker Compose 中覆盖默认的 CMD 和 ENTRYPOINT



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


    Compose 文件定义了一个名为 `postgres` 的服务，该服务使用官方的 Postgres 镜像，设置一个入口点脚本，并使用密码身份验证启动容器。

2. 通过运行以下命令来启动服务：

    ```console
    $ docker compose up -d
    ```

    此命令启动 Docker Compose 文件中定义的 Postgres 服务。

3. 使用 Docker Desktop 仪表板验证身份验证。

    打开 Docker Desktop 仪表板，选择 **Postgres** 容器并选择 **Exec** 进入容器 shell。您可以键入以下命令来连接到 Postgres 数据库：

    ```console
    # psql -U postgres
    ```

    ![选择 Postgres 容器并使用 EXEC 按钮进入其 shell 的 Docker Desktop 仪表板的屏幕截图](images/exec-into-postgres-container.webp?border=true)


    > [!NOTE]
    > 
    > PostgreSQL 镜像在本地设置信任身份验证，因此您可能会注意到从 localhost（在同一容器内）连接时不需要密码。但是，如果从不同的主机/容器连接，则需要密码。

### 使用 `docker run` 覆盖默认的 CMD 和 ENTRYPOINT

您还可以使用 `docker run` 命令直接覆盖默认值，命令如下：

```console 
$ docker run -e POSTGRES_PASSWORD=secret postgres docker-entrypoint.sh -h localhost -p 5432
```

此命令运行一个 Postgres 容器，设置一个用于密码身份验证的环境变量，覆盖默认的启动命令并配置主机名和��口映射。


## 其他资源

* [使用 Compose 设置环境变量的方法](/compose/how-tos/environment-variables/set-environment-variables/)
* [什么是容器](/get-started/docker-concepts/the-basics/what-is-a-container/)

## 后续步骤

现在您已经了解了如何覆盖容器默认值，是时候学习如何持久化容器数据了。

{{< button text="持久化容器数据" url="persisting-container-data" >}}

