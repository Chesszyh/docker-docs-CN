---
title: 多容器应用程序
weight: 5
keywords: concepts, build, images, container, docker desktop, 概念, 构建, 镜像, 容器
description: 此概念页面将教您多容器应用程序的重要性以及它与单容器应用程序的区别
aliases: 
 - /guides/docker-concepts/running-containers/multi-container-applications/
---

{{< youtube-embed 1jUwR6F9hvM >}}

## 解释

启动一个单容器应用程序很容易。例如，一个执行特定数据处理任务的 Python 脚本在包含其所有依赖项的容器内运行。同样，一个提供静态网站并带有小型 API 端点的 Node.js 应用程序也可以使用其所有必要的库和依赖项进行有效的容器化。然而，随着应用程序规模的增长，将其作为单个容器进行管理变得越来越困难。

想象一下，数据处理 Python 脚本需要连接到数据库。突然之间，您现在不仅要管理脚本，还要在同一个容器中管理数据库服务器。如果脚本需要用户登录，您还需要一个身份验证机制，从而进一步膨胀了容器的大小。

容器的一个最佳实践是每个容器应该只做一件事并做好。虽然此规则有例外，但应避免让一个容器执行多项任务的倾向。

现在您可能会问：“我需要分别运行这些容器吗？如果我分别运行它们，该如何将它们连接在一起？”

虽然 `docker run` 是启动容器的便捷工具，但用它管理不断增长的应用程序堆栈会变得很困难。原因如下：

- 想象一下运行多个 `docker run` 命令（前端、后端和数据库），并为开发、测试和生产环境配置不同的设置。这既耗时又容易出错。
- 应用程序通常相互依赖。随着堆栈的扩展，手动按特定顺序启动容器并管理网络连接变得非常困难。
- 每个应用程序都需要自己的 `docker run` 命令，这使得扩展单个服务变得困难。扩展整个应用程序意味着可能会在不需要提升性能的组件上浪费资源。
- 为每个应用程序持久化数据需要在每个 `docker run` 命令中进行单独的卷挂载或配置。这导致了分散的数据管理方式。
- 通过单独的 `docker run` 命令为每个应用程序设置环境变量既繁琐又容易出错。

这就是 Docker Compose 大显身手的地方。

Docker Compose 在一个名为 `compose.yml` 的 YAML 文件中定义您的整个多容器应用程序。此文件指定了您所有容器的配置、它们的依赖项、环境变量，甚至卷和网络。使用 Docker Compose：

- 您不需要运行多个 `docker run` 命令。您所需要做的就是在单个 YAML 文件中定义您的整个多容器应用程序。这集中了配置并简化了管理。
- 您可以按特定顺序运行容器并轻松管理网络连接。
- 您可以简单地在多容器设置中向上或向下扩展单个服务。这允许根据实时需求进行高效分配。
- 您可以轻松实现持久卷。
- 在 Docker Compose 文件中设置一次环境变量非常容易。

通过利用 Docker Compose 运行多容器设置，您可以构建以模块化、可扩展性和一致性为核心的复杂应用程序。


## 试一试

在本实践指南中，您首先将看到如何使用 `docker run` 命令构建和运行一个基于 Node.js、Nginx 反向代理和 Redis 数据库的计数器 Web 应用程序。您还将看到如何使用 Docker Compose 简化整个部署过程。

### 设置

1. 获取示例应用程序。如果您有 Git，可以克隆示例应用程序的仓库。否则，您可以下载示例应用程序。选择以下选项之一。

   {{< tabs >}}
   {{< tab name="使用 git 克隆" >}}

   在终端中使用以下命令克隆示例应用程序仓库。

   ```console
   $ git clone https://github.com/dockersamples/nginx-node-redis
   ```
   
   进入 `nginx-node-redis` 目录：

   ```console
   $ cd nginx-node-redis
   ```

   在此目录中，您将找到两个子目录 - `nginx` 和 `web`。
   

   {{< /tab >}}
   {{< tab name="下载" >}}

   下载源码并解压。

   {{< button url="https://github.com/dockersamples/nginx-node-redis/archive/refs/heads/main.zip" text="下载源码" >}}


   进入 `nginx-node-redis-main` 目录：

   ```console
   $ cd nginx-node-redis-main
   ```

   在此目录中，您将找到两个子目录 - `nginx` 和 `web`。

   {{< /tab >}}
   {{< /tabs >}}


2. [下载并安装](/get-started/get-docker.md) Docker Desktop。

### 构建镜像


1. 进入 `nginx` 目录，运行以下命令构建镜像：


    ```console
    $ docker build -t nginx .
    ```

2. 进入 `web` 目录，运行以下命令构建第一个 Web 镜像：
    
    ```console
    $ docker build -t web .
    ```

### 运行容器

1. 在运行多容器应用程序之前，您需要为它们创建一个网络以便通信。您可以使用 `docker network create` 命令来执行此操作：

    ```console
    $ docker network create sample-app
    ```

2. 运行以下命令启动 Redis 容器，它将连接到之前创建的网络并创建一个网络别名（对 DNS 查找很有用）：

    ```console
    $ docker run -d  --name redis --network sample-app --network-alias redis redis
    ```

3. 运行以下命令启动第一个 Web 容器：

    ```console
    $ docker run -d --name web1 -h web1 --network sample-app --network-alias web1 web
    ```

4. 运行以下命令启动第二个 Web 容器：

    ```console
    $ docker run -d --name web2 -h web2 --network sample-app --network-alias web2 web
    ```
    
5. 运行以下命令启动 Nginx 容器：

    ```console
    $ docker run -d --name nginx --network sample-app  -p 80:80 nginx
    ```

     > [!NOTE]
     >
     > Nginx 通常用作 Web 应用程序的反向代理，将流量路由到后端服务器。在这种情况下，它路由到 Node.js 后端容器（web1 或 web2）。


6. 运行以下命令验证容器是否已启动：

    ```console
    $ docker ps
    ```

    您将看到类似以下的输出：

    ```text
    CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                NAMES
    2cf7c484c144   nginx     "/docker-entrypoint.…"   9 seconds ago        Up 8 seconds        0.0.0.0:80->80/tcp   nginx
    7a070c9ffeaa   web       "docker-entrypoint.s…"   19 seconds ago       Up 18 seconds                            web2
    6dc6d4e60aaf   web       "docker-entrypoint.s…"   34 seconds ago       Up 33 seconds                            web1
    008e0ecf4f36   redis     "docker-entrypoint.s…"   About a minute ago   Up About a minute   6379/tcp             redis
    ```

7. 如果您查看 Docker Desktop Dashboard，可以看到容器并深入了解其配置。

   ![Docker Desktop Dashboard 截图，显示多容器应用程序](images/multi-container-apps.webp?w=5000&border=true)

8. 在一切运行起来后，您可以在浏览器中打开 [http://localhost](http://localhost) 查看该站点。多次刷新页面以查看处理请求的主机和请求总数：

    ```console
    web2: Number of visits is: 9
    web1: Number of visits is: 10
    web2: Number of visits is: 11
    web1: Number of visits is: 12
    ```

    > [!NOTE]
    >
    > 您可能已经注意到，作为反向代理的 Nginx 可能会以轮询 (round-robin) 的方式在两个后端容器之间分配传入请求。这意味着每个请求可能会轮流定向到不同的容器（web1 和 web2）。输出显示 web1 和 web2 容器的连续增加，而存储在 Redis 中的实际计数器值仅在响应发送回客户端后更新。

9. 您可以通过在 Docker Desktop Dashboard 中选择容器并点击 **Delete**（删除）按钮来移除容器。

   ![Docker Desktop Dashboard 截图，显示如何删除多容器应用程序](images/delete-multi-container-apps.webp?border=true)
 
## 使用 Docker Compose 简化部署


Docker Compose 为管理多容器部署提供了一种结构化且精简的方法。如前所述，使用 Docker Compose，您不需要运行多个 `docker run` 命令。您所需要做的就是在单个名为 `compose.yml` 的 YAML 文件中定义整个多容器应用程序。让我们看看它是如何工作的。


导航到项目根目录。在此目录中，您将找到一个名为 `compose.yml` 的文件。这个 YAML 文件是奇迹发生的地方。它定义了构成应用程序的所有服务及其配置。每个服务都指定了其镜像、端口、卷、网络以及其功能所需的任何其他设置。

1. 使用 `docker compose up` 命令启动应用程序：

    ```console
    $ docker compose up -d --build
    ```

    运行此命令时，您应该会看到类似以下的输出：


    ```console
    Running 5/5
    ✔ Network nginx-nodejs-redis_default    Created                                                0.0s
    ✔ Container nginx-nodejs-redis-web1-1   Started                                                0.1s
    ✔ Container nginx-nodejs-redis-redis-1  Started                                                0.1s
    ✔ Container nginx-nodejs-redis-web2-1   Started                                                0.1s
    ✔ Container nginx-nodejs-redis-nginx-1  Started
    ```

2. 如果您查看 Docker Desktop Dashboard，可以看到容器并深入了解其配置。


    ![Docker Desktop Dashboard 截图，显示使用 Docker Compose 部署的应用程序堆栈容器](images/list-containers.webp?border=true)

3. 或者，您可以使用 Docker Desktop Dashboard 通过选择应用程序堆栈并点击 **Delete**（删除）按钮来移除容器。

   ![Docker Desktop Dashboard 截图，显示如何移除使用 Docker Compose 部署的容器](images/delete-containers.webp?border=true)


在本指南中，您学习了与容易出错且难以管理的 `docker run` 相比，使用 Docker Compose 启动和停止多容器应用程序是多么容易。

## 其他资源

* [`docker container run` 命令行参考](reference/cli/docker/container/run/)
* [什么是 Docker Compose](/get-started/docker-concepts/the-basics/what-is-docker-compose/)
