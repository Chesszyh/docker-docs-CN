---
title: 持久化容器数据
weight: 3
keywords: concepts, build, images, container, docker desktop
description: 本概念页面将教您了解 Docker 中数据持久化的重要性
aliases:
 - /guides/walkthroughs/persist-data/
 - /guides/docker-concepts/running-containers/persisting-container-data/
---

{{< youtube-embed 10_2BjqB_Ls >}}

## 概念解释

当容器启动时，它使用镜像提供的文件和配置。每个容器都能够创建、修改和删除文件，并且不会影响任何其他容器。当容器被删除时，这些文件更改也会被删除。

虽然容器的这种临时性很好，但当您想持久化数据时会带来挑战。例如，如果您重启数据库容器，您可能不希望从空数据库开始。那么，如何持久化文件呢？

### 容器卷

卷（Volume）是一种存储机制，提供了超越单个容器生命周期的数据持久化能力。可以将其视为从容器内部到容器外部的快捷方式或符号链接。

例如，假设您创建一个名为 `log-data` 的卷。

```console
$ docker volume create log-data
```

使用以下命令启动容器时，该卷将被挂载（或附加）到容器的 `/logs` 目录：

```console
$ docker run -d -p 80:80 -v log-data:/logs docker/welcome-to-docker
```

如果 `log-data` 卷不存在，Docker 会自动为您创建它。

当容器运行时，它写入 `/logs` 文件夹的所有文件都将保存在这个卷中，位于容器外部。如果您删除容器并使用相同的卷启动新容器，这些文件仍然存在。

> **使用卷共享文件**
>
> 您可以将同一个卷附加到多个容器以在容器之间共享文件。这在日志聚合、数据管道或其他事件驱动应用程序等场景中可能很有帮助。


### 管理卷

卷有超越容器的自己的生命周期，根据您使用的数据类型和应用程序，卷可能会变得相当大。以下命令有助于管理卷：

- `docker volume ls` - 列出所有卷
- `docker volume rm <volume-name-or-id>` - 删除卷（仅在卷未附加到任何容器时有效）
- `docker volume prune` - 删除所有未使用（未附加）的卷



## 动手实践

在本指南中，您将练习创建和使用卷来持久化 Postgres 容器创建的数据。当数据库运行时，它将文件存储到 `/var/lib/postgresql/data` 目录中。通过在此处附加卷，您将能够多次重启容器同时保留数据。

### 使用卷

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 使用以下命令通过 [Postgres 镜像](https://hub.docker.com/_/postgres)启动容器：

    ```console
    $ docker run --name=db -e POSTGRES_PASSWORD=secret -d -v postgres_data:/var/lib/postgresql/data postgres
    ```

    这将在后台启动数据库，使用密码配置它，并将卷附加到 PostgreSQL 持久化数据库文件的目录。

3. 使用以下命令连接到数据库：

    ```console
    $ docker exec -ti db psql -U postgres
    ```

4. 在 PostgreSQL 命令行中，运行以下命令创建数据库表并插入两条记录：

    ```text
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        description VARCHAR(100)
    );
    INSERT INTO tasks (description) VALUES ('Finish work'), ('Have fun');
    ```

5. 通过在 PostgreSQL 命令行中运行以下命令验证数据是否在数据库中：

    ```text
    SELECT * FROM tasks;
    ```

    您应该得到如下所示的输出：

    ```text
     id | description
    ----+-------------
      1 | Finish work
      2 | Have fun
    (2 rows)
    ```

6. 通过运行以下命令退出 PostgreSQL shell：

    ```console
    \q
    ```

7. 停止并删除数据库容器。请记住，即使容器已被删除，数据仍保存在 `postgres_data` 卷中。

    ```console
    $ docker stop db
    $ docker rm db
    ```

8. 通过运行以下命令启动新容器，附加具有持久化数据的相同卷：

    ```console
    $ docker run --name=new-db -d -v postgres_data:/var/lib/postgresql/data postgres
    ```

    您可能注意到省略了 `POSTGRES_PASSWORD` 环境变量。那是因为该变量仅在引导新数据库时使用。

9. 通过运行以下命令验证数据库仍然有这些记录：

    ```console
    $ docker exec -ti new-db psql -U postgres -c "SELECT * FROM tasks"
    ```

### 查看卷内容

Docker Desktop 仪表板提供了查看任何卷内容的功能，以及导出、导入和克隆卷的能力。

1. 打开 Docker Desktop 仪表板并导航到 **Volumes** 视图。在此视图中，您应该会看到 **postgres_data** 卷。

2. 选择 **postgres_data** 卷的名称。

3. **Data** 选项卡显示卷的内容，并提供浏览文件的功能。双击文件将让您查看内容并进行更改。

4. 右键单击任何文件以保存或删除它。


### 删除卷

在删除卷之前，它必须未附加到任何容器。如果您尚未删除之前的容器，请使用以下命令删除（`-f` 将首先停止容器然后删除它）：

```console
$ docker rm -f new-db
```

有几种删除卷的方法，包括以下内容：

- 在 Docker Desktop 仪表板中选择卷上的 **Delete Volume** 选项。
- 使用 `docker volume rm` 命令：

    ```console
    $ docker volume rm postgres_data
    ```
- 使用 `docker volume prune` 命令删除所有未使用的卷：

    ```console
    $ docker volume prune
    ```


## 其他资源

以下资源将帮助您了解更多关于卷的信息：

- [在 Docker 中管理数据](/engine/storage)
- [卷](/engine/storage/volumes)
- [卷挂载](/engine/containers/run/#volume-mounts)


## 后续步骤

现在您已经学习了持久化容器数据，是时候学习与容器共享本地文件了。

{{< button text="与容器共享本地文件" url="sharing-local-files" >}}
