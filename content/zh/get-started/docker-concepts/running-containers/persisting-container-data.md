---
title: 持久化容器数据
weight: 3
keywords: concepts, build, images, container, docker desktop
description: 此概念页面将教您 Docker 中数据持久性的重要性
aliases:
 - /guides/walkthroughs/persist-data/
 - /guides/docker-concepts/running-containers/persisting-container-data/
---

{{< youtube-embed 10_2BjqB_Ls >}}

## 说明

当容器启动时，它使用镜像提供的文件和配置。每个容器都能够创建、修改和删除文件，这样做不会影响任何其他容器。当容器被删除时，这些文件更改也会被删除。

虽然容器的这种短暂性很棒，但当您想要持久化数据时，这就构成了挑战。例如，如果您重启数据库容器，您可能不希望以空数据库开始。那么，您如何持久化文件？

### 容器卷 (Volumes)

卷（Volumes）是一种存储机制，提供在单个容器生命周期之外持久化数据的能力。可以将其视为提供从容器内部到容器外部的快捷方式或符号链接。

举个例子，假设您创建了一个名为 `log-data` 的卷。

```console
$ docker volume create log-data
```

当使用以下命令启动容器时，该卷将被挂载（或附加）到容器内的 `/logs` 处：

```console
$ docker run -d -p 80:80 -v log-data:/logs docker/welcome-to-docker
```

如果卷 `log-data` 不存在，Docker 会自动为您创建它。

当容器运行时，它写入 `/logs` 文件夹的所有文件都将保存在此卷中，即容器外部。如果您删除容器并使用相同的卷启动一个新容器，文件仍然会在那里。

> **使用卷共享文件**
>
> 您可以将同一个卷附加到多个容器，以便在容器之间共享文件。这在诸如日志聚合、数据管道或其他事件驱动的应用程序等场景中可能会有所帮助。

### 管理卷

卷拥有超出容器生命周期的自身生命周期，并且根据您使用的数据和应用程序类型，卷可能会变得非常大。以下命令将有助于管理卷：

- `docker volume ls` - 列出所有卷
- `docker volume rm <volume-name-or-id>` - 删除卷（仅当卷未附加到任何容器时有效）
- `docker volume prune` - 删除所有未使用的（未附加的）卷

## 试一试

在本指南中，您将练习创建和使用卷来持久化由 Postgres 容器创建的数据。当数据库运行时，它将文件存储到 `/var/lib/postgresql/data` 目录中。通过在此处附加卷，您将能够多次重启容器，同时保留数据。

### 使用卷

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 使用 [Postgres 镜像](https://hub.docker.com/_/postgres) 启动容器，命令如下：

    ```console
    $ docker run --name=db -e POSTGRES_PASSWORD=secret -d -v postgres_data:/var/lib/postgresql/data postgres
    ```

    这将在后台启动数据库，使用密码对其进行配置，并将卷附加到 PostgreSQL 将持久化数据库文件的目录。

3. 使用以下命令连接到数据库：

    ```console
    $ docker exec -ti db psql -U postgres
    ```

4. 在 PostgreSQL 命令行中，运行以下命令创建一个数据库表并插入两条记录：

    ```text
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        description VARCHAR(100)
    );
    INSERT INTO tasks (description) VALUES ('Finish work'), ('Have fun');
    ```

5. 在 PostgreSQL 命令行中运行以下命令，验证数据是否在数据库中：

    ```text
    SELECT * FROM tasks;
    ```

    您应该得到类似以下的输出：

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

7. 停止并移除数据库容器。请记住，即使容器已被删除，数据仍持久保存在 `postgres_data` 卷中。

    ```console
    $ docker stop db
    $ docker rm db
    ```

8. 通过运行以下命令启动一个新容器，并附加具有持久数据的相同卷：

    ```console
    $ docker run --name=new-db -d -v postgres_data:/var/lib/postgresql/data postgres 
    ```

    您可能已经注意到 `POSTGRES_PASSWORD` 环境变量已被省略。这是因为该变量仅在引导新数据库时使用。

9. 通过运行以下命令验证数据库是否仍有记录：

    ```console
    $ docker exec -ti new-db psql -U postgres -c "SELECT * FROM tasks"
    ```

### 查看卷内容

Docker Desktop Dashboard 提供了查看任何卷内容的能力，以及导出、导入和克隆卷的能力。

1. 打开 Docker Desktop Dashboard 并导航到 **Volumes**（卷）视图。在此视图中，您应该看到 **postgres_data** 卷。

2. 选择 **postgres_data** 卷的名称。

3. **Data**（数据）选项卡显示卷的内容并提供浏览文件的能力。双击文件将允许您查看内容并进行更改。

4. 右键单击任何文件以保存或删除它。

### 删除卷

在删除卷之前，它必须未附加到任何容器。如果您尚未删除以前的容器，请使用以下命令执行此操作（`-f` 将先停止容器，然后将其删除）：

```console
$ docker rm -f new-db
```

有几种删除卷的方法，包括以下方法：

- 在 Docker Desktop Dashboard 中的卷上选择 **Delete Volume**（删除卷）选项。
- 使用 `docker volume rm` 命令：

    ```console
    $ docker volume rm postgres_data
    ```
- 使用 `docker volume prune` 命令删除所有未使用的卷：

    ```console
    $ docker volume prune
    ```

## 其他资源

以下资源将帮助您了解有关卷的更多信息：

- [在 Docker 中管理数据](/engine/storage)
- [卷](/engine/storage/volumes)
- [卷挂载](/engine/containers/run/#volume-mounts)

## 下一步

既然您已了解持久化容器数据，是时候学习与容器共享本地文件了。

{{< button text="与容器共享本地文件" url="sharing-local-files" >}}