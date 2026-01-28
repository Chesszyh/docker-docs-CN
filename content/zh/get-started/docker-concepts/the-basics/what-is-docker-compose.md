---
title: 什么是 Docker Compose？
weight: 40
keywords: concepts, build, images, container, docker desktop
description: 什么是 Docker Compose？
aliases:
 - /guides/walkthroughs/multi-container-apps/
 - /guides/docker-concepts/the-basics/what-is-docker-compose/
---

{{< youtube-embed xhcUIK4fGtY >}}

## 概念解释

如果您一直在跟随之前的指南，那么您一直在使用单容器应用程序。但是，现在您想做一些更复杂的事情——运行数据库、消息队列、缓存或各种其他服务。您是将所有内容安装在一个容器中？还是运行多个容器？如果运行多个容器，您如何将它们全部连接在一起？

容器的一个最佳实践是每个容器应该做一件事并把它做好。虽然这个规则有例外，但要避免让一个容器做多件事的倾向。

您可以使用多个 `docker run` 命令来启动多个容器。但是，您很快就会意识到您需要管理网络、将容器连接到这些网络所需的所有标志等等。当您完成后，清理工作也会更加复杂。

使用 Docker Compose，您可以在一个 YAML 文件中定义所有容器及其配置。如果您将此文件包含在代码仓库中，任何克隆您仓库的人都可以通过一个命令启动并运行。

重要的是要理解 Compose 是一个声明式工具——您只需定义它然后运行即可。您不需要总是从头开始重新创建所有内容。如果您进行更改，再次运行 `docker compose up`，Compose 将协调文件中的更改并智能地应用它们。

> **Dockerfile 与 Compose 文件**
>
> Dockerfile 提供构建容器镜像的指令，而 Compose 文件定义您正在运行的容器。通常，Compose 文件会引用 Dockerfile 来构建用于特定服务的镜像。


## 动手实践

在本动手实践中，您将学习如何使用 Docker Compose 运行多容器应用程序。您将使用一个用 Node.js 构建的简单待办事项列表应用程序和一个 MySQL 数据库服务器。

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

    在这个目录中，您会找到一个名为 `compose.yaml` 的文件。这个 YAML 文件是魔法发生的地方！它定义了组成您应用程序的所有服务及其配置。每个服务指定其镜像、端口、卷、网络以及其功能所需的任何其他设置。花一些时间探索 YAML 文件并熟悉其结构。

4. 使用 [`docker compose up`](/reference/cli/docker/compose/up/) 命令启动应用程序：

    ```console
    docker compose up -d --build
    ```

    运行此命令时，您应该会看到类似以下的输出：

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

    这里发生了很多事情！有几点需要说明：

    - 从 Docker Hub 下载了两个容器镜像——node 和 MySQL
    - 为您的应用程序创建了一个网络
    - 创建了一个卷来在容器重启之间持久化数据库文件
    - 启动了两个具有所有必要配置的容器

    如果这让您感到不知所措，别担心！您会逐渐掌握的！

5. 现在一切都已启动并运行，您可以在浏览器中打开 [http://localhost:3000](http://localhost:3000) 查看网站。随意向列表添加项目、勾选它们并删除它们。

    ![显示在端口 3000 上运行的待办事项列表应用程序的网页截图](images/todo-list-app.webp?border=true&w=950&h=400)

6. 如果您查看 Docker Desktop GUI，您可以看到容器并深入了解它们的配置。

    ![Docker Desktop 仪表板的截图，显示运行待办事项列表应用的容器列表](images/todo-list-containers.webp?border=true&w=950&h=400)


### 清理

由于此应用程序是使用 Docker Compose 启动的，当您完成后很容易将其全部清理掉。

1. 在 CLI 中，使用 [`docker compose down`](/reference/cli/docker/compose/down/) 命令删除所有内容：

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

    > **卷持久化**
    >
    > 默认情况下，当您拆除 Compose 栈时，卷 _不会_ 自动删除。这样做的目的是，如果您再次启动栈，您可能希望恢复数据。
    >
    > 如果您确实想删除卷，请在运行 `docker compose down` 命令时添加 `--volumes` 标志：
    >
    > ```console
    > docker compose down --volumes
    > [+] Running 1/0
    > ✔ Volume todo-list-app_todo-mysql-data  Removed
    > ```

2. 或者，您可以使用 Docker Desktop GUI 通过选择应用程序栈并选择 **Delete** 按钮来删除容器。

    ![Docker Desktop GUI 的截图，显示容器视图，箭头指向"Delete"按钮](images/todo-list-delete.webp?w=930&h=400)

    > **在 GUI 中使用 Compose 栈**
    >
    > 请注意，如果您在 GUI 中删除 Compose 应用的容器，它只会删除容器。如果您想删除网络和卷，需要手动操作。

在本实践中，您学习了如何使用 Docker Compose 启动和停止多容器应用程序。


## 其他资源

本页面是对 Compose 的简要介绍。在以下资源中，您可以更深入地了解 Compose 以及如何编写 Compose 文件。


* [Docker Compose 概述](/compose/)
* [Docker Compose CLI 概述](/compose/reference/)
* [Compose 工作原理](/compose/intro/compose-application-model/)
