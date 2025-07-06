---
title: 什么是 Docker Compose？
weight: 40
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 什么是 Docker Compose？
aliases:
 - /guides/walkthroughs/multi-container-apps/
 - /guides/docker-concepts/the-basics/what-is-docker-compose/
---

{{< youtube-embed xhcUIK4fGtY >}}

## 说明

如果您到目前为止一直在关注这些指南，那么您一直在使用单容器应用程序。但是，现在您想做一些更复杂的事情 - 运行数据库、消息队列、缓存或各种其他服务。您是否将所有内容都安装在一个容器中？运行多个容器？如果运行多个，您如何将它们全部连接在一起？

容器的一个最佳实践是每个容器应该做一件事并把它做好。虽然这个规则有例外，但要避免让一个容器做多件事的倾向。

您可以使用多个 `docker run` 命令来启动多个容器。但是，您很快就会意识到您需要管理网络、将容器连接到这些网络所需的所有标志等等。当您完成后，清理工作会更复杂一些。

使用 Docker Compose，您可以在一个 YAML 文件中定义所有容器及其配置。如果您将此文件包含在您的代码存储库中，任何克隆您的存���库的人都可以通过一个命令启动并运行。

重要的是要了解 Compose 是一个声明性工具 - 您只需定义它然后运行即可。您不必总是从头开始重新创建所有内容。如果您进行了更改，请再次运行 `docker compose up`，Compose 将协调文件中的更改并智能地应用它们。

> **Dockerfile 与 Compose 文件**
>
> Dockerfile 提供构建容器镜像的说明，而 Compose 文件定义您正在运行的容器。通常，Compose 文件会引用 Dockerfile 来构建用于特定服务的镜像。


## 动手试试

在这个动手实践中，您将学习如何使用 Docker Compose 运行一个多容器应用程序。您将使用一个使用 Node.js 和 MySQL 作为数据库服务器构建的简单待办事项列表应用程序。

### 启动应用程序

按照说明在您的系统上运行待办事项列表应用程序。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。
2. 打开终端并[克隆此示例应用程序](https://github.com/dockersamples/todo-list-app)。

    ```console
    git clone https://github.com/dockersamples/todo-list-app 
    ```

3. 导航到 `todo-list-app` 目录：

    ```console
    cd todo-list-app
    ```

    在此目录中，您会找到一个名为 `compose.yaml` 的文件。这个 YAML 文件是所有魔法发生的地方！它定义了构成您应用程序的所有服务及其配置。每个服务都指定其镜像、端口、卷、网络以及其功能所需的任何其他设置。花点时间探索 YAML 文件并熟悉其结构。

4. 使用 [`docker compose up`](/reference/cli/docker/compose/up/) 命令启动应用程序：

    ```console
    docker compose up -d --build
    ```

    当您运行此命令时，您应该会看到如下输出：

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

    这里发生了很多事情！有几件事要提一下：

    - 从 Docker Hub 下载了两个容器镜像 - node 和 MySQL
    - 为您的应用程序创建���一个网络
    - 创建了一个卷以在容器重新启动之间持久化数据库文件
    - 启动了两个容器，并提供了所有必要的配置

    如果这让您感到不知所措，请不要担心！您会掌握的！

5. 现在一切都已启动并正在运行，您可以在浏览器中打开 [http://localhost:3000](http://localhost:3000) 查看网站。随时向列表中添加项目、勾选它们并删除它们。

    ![一个网页的屏幕截图，显示了在端口 3000 上运行的待办事项列表应用程序](images/todo-list-app.webp?border=true&w=950&h=400)

6. 如果您查看 Docker Desktop GUI，您可以看到容器并深入了解它们的配置。

    ![Docker Desktop 仪表板的屏幕截图，显示了运行待办事项列表应用程序的容器列表](images/todo-list-containers.webp?border=true&w=950&h=400)


### 拆除

由于此应用程序是使用 Docker Compose 启动的，因此在您完成后很容易将其全部拆除。

1. 在 CLI 中，使用 [`docker compose down`](/reference/cli/docker/compose/down/) 命令删除所有内容：

    ```console
    docker compose down
    ```

    您将看到类似于以下内容的输出：

    ```console
    [+] Running 3/3
    ✔ Container todo-list-app-mysql-1  Removed        2.9s
    ✔ Container todo-list-app-app-1    Removed        0.1s
    ✔ Network todo-list-app_default    Removed        0.1s
    ```

    > **卷持久性**
    >
    > 默认情况下，当您拆除 Compose 堆栈时，卷*不会*自动删除。这个想法是，如果您再次启动堆栈，您可能希望数据恢复。
    >
    > 如果您确实想删除卷，请在运行 `docker compose down` 命令时添加 `--volumes` 标志：
    >
    > ```console
    > docker compose down --volumes
    > [+] Running 1/0
    > ✔ Volume todo-list-app_todo-mysql-data  Removed
    > ```

2. 或者，您可以使用 Docker Desktop GUI 通过选择应用程序堆栈并选择 **Delete** 按钮来删除容器。

    ![Docker Desktop GUI 的屏幕截图，显示了容器视图，其中一个箭头指向“删除”按钮](images/todo-list-delete.webp?w=930&h=400)

    > **将 GUI 用于 Compose 堆栈**
    >
    > 请注意，如果您在 GUI 中删除 Compose 应用程序的容器，它只会删除容器。如果您想这样做，则必须手动删除网络和卷。

在此演练中，您学习了如何使用 Docker Compose 启动和停止多容器应用程序。


## 其他资源

此页面是对 Compose 的简要介绍。在以下资源中，您可以深入了解 Compose 以及如何编写 Compose 文件。


* [Docker Compose 概述](/compose/)
* [Docker Compose CLI 概述](/compose/reference/)
* [Compose 如何工作](/compose/intro/compose-application-model/)
