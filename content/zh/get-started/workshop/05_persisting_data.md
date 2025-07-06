---
title: 持久化数据库
weight: 50
linkTitle: "第四部分：持久化数据库"
keywords: 入门, 设置, 定位, 快速入门, 介绍, 概念, 容器,
  docker desktop
description: 在您的应用程序中使您的数据库持久化
aliases:
 - /get-started/05_persisting_data/
 - /guides/workshop/05_persisting_data/
---

如果您没有注意到，您的待办事项列表在每次
启动容器时都是空的。这是为什么呢？在这一部分中，您将深入了解容器的工作原理。

## 容器的文件系统

当容器运行时，它会使用镜像中的各个层作为其文件系统。
每个容器还会获得自己的“暂存空间”来创建/更新/删除文件。任何
更改都不会在另一个容器中看到，即使它们使用的是相同的镜像。

### 实践一下

为了看到这一点，您将启动两个容器。在一个容器中，
您将创建一个文件。在另一个容器中，您将检查该文件是否存在。

1. 启动一个 Alpine 容器并在其中创建一个新文件。

    ```console
    $ docker run --rm alpine touch greeting.txt
    ```

    > [!TIP]
    > 您在镜像名称（在本例中为 `alpine`）之后指定的任何命令
    > 都会在容器内执行。在这种情况下，命令 `touch
    > greeting.txt` 会在容器的文件系统上放置一个名为 `greeting.txt` 的文件。

2. 运行一个新的 Alpine 容器并使用 `stat` 命令检查文件是否存在。
   
   ```console
   $ docker run --rm alpine stat greeting.txt
   ```

   您应该会看到类似于以下内容的输出，表明该文件在新容器中不存在。

   ```console
   stat: can't stat 'greeting.txt': No such file or directory
   ```

第一个容器创建的 `greeting.txt` 文件在
第二个容器中不存在。这是因为每个容器的可写“顶层”
是隔离的。尽管两个容器共享构成
基础镜像的相同底层，但可写层对于每个容器都是唯一的。

## 容器卷

通过前面的实验，您看到每个容器每次启动时都从镜像定义开始。
虽然容器可以创建、更新和删除文件，但当您删除容器时，这些更改会丢失，
并且 Docker 会将所有更改隔离到该容器中。使用卷，您可以改变这一切。

[卷](/manuals/engine/storage/volumes.md) 提供了将容器的特定文件系统路径连接回
主机的功能。如果您在容器中挂载一个目录，该
目录中的更改也会在主机上看到。如果您在容器重新启动时挂载相同的目录，您会看到
相同的文件��

主要有两种类型的卷。您最终会同时使用这两种类型，但您将从卷挂载开始。

## 持久化待办事项数据

默认情况下，待办事项应用程序将其数据存储在容器文件系统中
`/etc/todos/todo.db` 的 SQLite 数据库中。如果您不熟悉 SQLite，请不要担心！它只是一个将所有数据存储在单个文件中的关系数据库。虽然这不适用于大型应用程序，
但它适用于小型演示。您稍后将学习如何将其切换到不同的数据库引擎。

由于数据库是单个文件，如果您可以将该文件持久化在主机上并使其可用于
下一个容器，那么它应该能够从上一个容器停止的地方继续。通过创建一个卷并将其附加
（通常称为“挂载”）到您存储数据的目录，您可以持久化数据。当您的容器
写入 `todo.db` 文件时，它会将数据持久化到卷中的主机上。

如前所述，您将使用卷挂载。可以将卷挂载视为一个不透明的数据桶。
Docker 完全管理该卷，包括磁盘上的存储位置。您只需要记住
卷的名称。

### 创建一个卷并启动容器

您可以使用 CLI 或 Docker Desktop 的图形界面创建卷并启动容器。

{{< tabs >}}
{{< tab name="CLI" >}}

1. 使用 `docker volume create` 命令创建一��卷。

   ```console
   $ docker volume create todo-db
   ```

2. 再次使用 `docker rm -f <id>` 停止并删除待办事项应用程序容器，
   因为它仍在不使用持久卷的情况下运行。

3. 启动待办事项应用程序容器，但添加 `--mount` 选项以指定
   卷挂载。为卷指定一个名称，并将其挂载到
   容器中的 `/etc/todos`，这将捕获在该路径下创建的所有文件。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 --mount type=volume,src=todo-db,target=/etc/todos getting-started
   ```

   > [!NOTE]
   >
   > 如果您使用的是 Git Bash，则必须为此命令使用不同的语法。
   >
   > ```console
   > $ docker run -dp 127.0.0.1:3000:3000 --mount type=volume,src=todo-db,target=//etc/todos getting-started
   > ```
   >
   > 有关 Git Bash 语法差异的更多详细信息，请参阅
   > [使用 Git Bash](/desktop/troubleshoot-and-support/troubleshoot/topics/#docker-commands-failing-in-git-bash)。


{{< /tab >}}
{{< tab name="Docker Desktop" >}}

要创建一个卷：

1. 在 Docker Desktop 中选择 **Volumes**。
2. 在 **Volumes** 中，选择 **Create**。
3. 指定 `todo-db` 作为卷名称，然后选择 **Create**。

要停止并删除应用程序容��：

1. 在 Docker Desktop 中选择 **Containers**。
2. 在容器的 **Actions** 列中选择 **Delete**。

要使用挂载的卷启动待办事项应用程序容器：

1. 在 Docker Desktop 顶部选择搜索框。
2. 在搜索窗口中，选择 **Images** 选项卡。
3. 在搜索框中，指定镜像名称 `getting-started`。

   > [!TIP]
   >
   >  使用搜索过滤器来过滤镜像并仅显示 **Local images**。

4. 选择您的镜像，然后选择 **Run**。
5. 选择 **Optional settings**。
6. 在 **Host port** 中，指定端口，例如 `3000`。
7. 在 **Host path** 中，指定卷的名称 `todo-db`。
8. 在 **Container path** 中，指定 `/etc/todos`。
9. 选择 **Run**。

{{< /tab >}}
{{< /tabs >}}

### 验证数据是否持久化

1. 容器启动后，打开应用程序并向您的待办事项列表中添加一些项目。

    ![添加到待办事项列表中的项目](images/items-added.webp)
    

2. 停止并删除待办事项应用程序的容器。使用 Docker Desktop 或 `docker ps` 获取 ID，然后使用 `docker rm -f <id>` 将其删除。

3. 使用前面的步骤启动一个新容器。

4. 打开应用程序。您应该会看到您的项目仍在列表中。

5. 检查完列表后，继续删除容器。

您现在已经学习了���何持久化数据。

## 深入了解卷

很多人经常问“当我使用卷时，Docker 将我的数据存储在哪里？”如果您想知道，
您可以使用 `docker volume inspect` 命令。

```console
$ docker volume inspect todo-db
```
您应该会看到类似于以下内容的输出：
```console
[
    {
        "CreatedAt": "2019-09-26T02:18:36Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/todo-db/_data",
        "Name": "todo-db",
        "Options": {},
        "Scope": "local"
    }
]
```

`Mountpoint` 是数据在磁盘上的实际位置。请注意，在大多数机器上，您将
需要具有 root 访问权限才能从主机访问此目录。

## 总结

在本节中，您学习了如何持久化容器数据。

相关信息：

 - [docker CLI 参考](/reference/cli/docker/)
 - [卷](/manuals/engine/storage/volumes.md)

## 后续步骤

接下来，您将学习如何使用绑定挂载更有效地开发您的应用程序。

{{< button text="使用绑定挂载" url="06_bind_mounts.md" >}}
