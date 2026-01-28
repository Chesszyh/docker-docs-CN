---
title: 什么是 Docker Compose？
weight: 40
keywords: concepts, build, images, container, docker desktop, 概念, 构建, 镜像, 容器
description: 什么是 Docker Compose？
aliases:
 - /guides/walkthroughs/multi-container-apps/
 - /guides/docker-concepts/the-basics/what-is-docker-compose/
---

{{< youtube-embed xhcUIK4fGtY >}}

## 解释

如果您一直关注本指南，那么您一直在处理单容器应用程序。但是，现在您想要做一些更复杂的事情——运行数据库、消息队列、缓存或各种其他服务。您是将所有内容安装在单个容器中吗？运行多个容器？如果您运行多个，如何将它们全部连接在一起？

容器的一个最佳实践是每个容器应该只做一件事并做好它。虽然此规则有例外，但应避免让一个容器做多件事的倾向。

您可以使用多个 `docker run` 命令来启动多个容器。但是，您很快就会意识到您需要管理网络、连接容器到这些网络所需的所有标志等等。而当您完成时，清理工作会变得有点复杂。

使用 Docker Compose，您可以在单个 YAML 文件中定义所有容器及其配置。如果您在代码仓库中包含此文件，任何克隆您仓库的人都可以通过一个命令启动并运行。

重要的是要理解 Compose 是一个声明式工具——您只需定义它并开始即可。您并不总是需要从头开始重新创建所有内容。如果您进行了更改，再次运行 `docker compose up`，Compose 将协调您文件中的更改并智能地应用它们。

> **Dockerfile vs. Compose 文件**
>
> Dockerfile 提供构建容器镜像的指令，而 Compose 文件定义正在运行的容器。通常，Compose 文件引用 Dockerfile 来构建用于特定服务的镜像。


## 试一试

在此实践中，您将学习如何使用 Docker Compose 来运行多容器应用程序。您将使用一个使用 Node.js 构建的简单待办事项列表应用程序，并使用 MySQL 作为数据库服务器。

### 启动应用程序

按照说明在您的系统上运行待办事项列表应用程序。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。
2. 打开终端并[克隆此示例应用程序](https://github.com/dockersamples/todo-list-app)。

    ```console
    git clone https://github.com/dockersamples/todo-list-app 
    ```

3. 进入 `todo-list-app` 目录：

    ```console
    cd todo-list-app
    ```

    在此目录中，您会发现一个名为 `compose.yaml` 的文件。所有的奇迹都发生在这个 YAML 文件中！它定义了组成应用程序的所有服务及其配置。每个服务都指定了其镜像、端口、卷、网络以及其功能所需的任何其他设置。花点时间探索这个 YAML 文件并熟悉其结构。

4. 使用 [`docker compose up`](/reference/cli/docker/compose/up/) 命令启动应用程序：

    ```console
    docker compose up -d --build
    ```

    运行此命令时，您应该会看到如下所示的输出：

    ```console
    [+] Running 5/5
    ✔ app 3 layers [⣿⣿⣿]      0B/0B            Pulled          7.1s
      ✔ e6f4e57cc59e Download complete                          0.9s
      ✔ df998480d81d Download complete                          1.0s
      ✔ 31e174fedd23 Download complete                          2.5s
      ✔ 43c47a581c29 Download complete                          2.0s
    [+] Running 4/4
      ⠸ Network todo-list-app_default           Created         0.3s
      ⠸ Volume "todo-list-app_todo-mysql-data"  Created         0.3s
      ✔ Container todo-list-app-app-1           Started         0.3s
      ✔ Container todo-list-app-mysql-1         Started         0.3s
    ```

    这里发生了很多事情！有几点需要指出：

    - 从 Docker Hub 下载了两个容器镜像——Node 和 MySQL
    - 为您的应用程序创建了一个网络
    - 创建了一个卷，用于在容器重启之间持久化数据库文件
    - 启动了两个带有所有必要配置的容器

    如果这让您感到不知所措，不要担心！您会掌握它的！

5. 现在一切都已启动并运行，您可以在浏览器中打开 [http://localhost:3000](http://localhost:3000) 来查看站点。随意向列表中添加项目、勾选它们并删除它们。

    ![网页截图，显示在端口 3000 上运行的待办事项列表应用程序](images/todo-list-app.webp?border=true&w=950&h=400)

6. 如果查看 Docker Desktop 图形界面，您可以看到容器并深入了解它们的配置。

    ![Docker Desktop 仪表板截图，显示运行待办事项列表应用程序的容器列表](images/todo-list-containers.webp?border=true&w=950&h=400)


### 拆除

由于此应用程序是使用 Docker Compose 启动的，因此在完成后很容易将其全部拆除。

1. 在命令行中，使用 [`docker compose down`](/reference/cli/docker/compose/down/) 命令移除所有内容：

    ```console
    docker compose down
    ```

    您将看到类似以下的输出：

    ```console
    [+] Running 3/3
    ✔ Container todo-list-app-mysql-1  Removed        2.9s
    ✔ Container todo-list-app-app-1    Removed        0.1s
    ✔ Network todo-list-app_default    Removed        0.1s
    ```

    > **卷持久性**
    >
    > 默认情况下，在拆除 Compose 堆栈时*不会*自动移除卷。这是因为如果您再次启动堆栈，您可能希望保留数据。
    >
    > 如果您确实想要移除卷，请在运行 `docker compose down` 命令时添加 `--volumes` 标志：
    >
    > ```console
    > docker compose down --volumes
    > [+] Running 1/0
    > ✔ Volume todo-list-app_todo-mysql-data  Removed
    > ```

2. 或者，您可以使用 Docker Desktop 图形界面通过选择应用程序堆栈并选择 **Delete**（删除）按钮来移除容器。

    ![Docker Desktop 图形界面截图，显示容器视图，箭头指向“删除”按钮](images/todo-list-delete.webp?w=930&h=400)

    > **对 Compose 堆栈使用图形界面**
    >
    > 请注意，如果您在图形界面中移除 Compose 应用程序的容器，它仅移除容器。如果您想要移除网络和卷，则必须手动移除。

在此演练中，您学习了如何使用 Docker Compose 启动和停止多容器应用程序。


## 其他资源

本页是对 Compose 的简要介绍。在以下资源中，您可以更深入地了解 Compose 以及如何编写 Compose 文件。


* [Docker Compose 概览](/compose/)
* [Docker Compose 命令行概览](/compose/reference/)
* [Compose 工作原理](/compose/intro/compose-application-model/)