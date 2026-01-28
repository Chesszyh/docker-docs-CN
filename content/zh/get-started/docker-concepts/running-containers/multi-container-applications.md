---
title: 多容器应用程序
weight: 5
keywords: concepts, build, images, container, docker desktop
description: 此概念页面将教您多容器应用程序的重要性以及它与单容器应用程序的区别
aliases: 
 - /guides/docker-concepts/running-containers/multi-container-applications/
---

{{< youtube-embed 1jUwR6F9hvM >}}

## 说明

启动单容器应用程序很容易。例如，执行特定数据处理任务的 Python 脚本在具有所有依赖项的容器中运行。同样，提供具有小型 API 端点的静态网站的 Node.js 应用程序可以有效地与其所有必要的库和依赖项一起容器化。但是，随着应用程序规模的扩大，将它们作为单独的容器进行管理变得更加困难。

想象一下，数据处理 Python 脚本需要连接到数据库。突然之间，您不仅要管理脚本，还要在同一个容器中管理数据库服务器。如果脚本需要用户登录，您将需要一种身份验证机制，从而进一步增加容器的大小。

容器的一个最佳实践是，每个容器应该做一件事并把它做好。虽然此规则也有例外，但应避免让一个容器做多件事的倾向。

现在您可能会问，“我需要分开运行这些容器吗？如果我分开运行它们，我该如何将它们全部连接在一起？”

虽然 `docker run` 是启动容器的便捷工具，但用它来管理不断增长的应用程序堆栈变得很困难。原因如下：

- 想象一下，为开发、测试和生产环境运行具有不同配置的多个 `docker run` 命令（前端、后端和数据库）。这容易出错且耗时。
- 应用程序通常相互依赖。随着堆栈的扩展，按特定顺序手动启动容器并管理网络连接变得困难。
- 每个应用程序都需要其 `docker run` 命令，这使得难以扩展单个服务。扩展整个应用程序意味着可能会在不需要增强的组件上浪费资源。
- 为每个应用程序持久化数据需要在每个 `docker run` 命令中进行单独的卷挂载或配置。这造成了分散的数据管理方法。
- 通过单独的 `docker run` 命令为每个应用程序设置环境变量既乏味又容易出错。

这就是 Docker Compose 派上用场的地方。

Docker Compose 在名为 `compose.yml` 的单个 YAML 文件中定义您的整个多容器应用程序。此文件指定了所有容器的配置、它们的依赖项、环境变量，甚至卷和网络。使用 Docker Compose：

- 您不需要运行多个 `docker run` 命令。您只需要在单个 YAML 文件中定义整个多容器应用程序。这集中了配置并简化了管理。
- 您可以按特定顺序运行容器并轻松管理网络连接。
- 您可以简单地在多容器设置中向上或向下扩展单个服务。这允许根据实时需求进行有效分配。
- 您可以轻松实现持久卷。
- 在 Docker Compose 文件中设置一次环境变量很容易。

通过利用 Docker Compose 运行多容器设置，您可以构建以模块化、可扩展性和一致性为核心的复杂应用程序。

## 试一试

在这个动手指南中，您首先将看到如何使用 `docker run` 命令构建和运行基于 Node.js 的计数器 Web 应用程序、Nginx 反向代理和 Redis 数据库。您还将看到如何使用 Docker Compose 简化整个部署过程。

### 设置

1. 获取示例应用程序。如果您有 Git，可以克隆示例应用程序的仓库。否则，您可以下载示例应用程序。选择以下选项之一。

   {{< tabs >}}
   {{< tab name="使用 git 克隆" >}}

   在终端中使用以下命令克隆示例应用程序仓库。

   ```console
   $ git clone https://github.com/dockersamples/nginx-node-redis
   ```
   
   导航到 `nginx-node-redis` 目录：

   ```console
   $ cd nginx-node-redis
   ```

   在此目录中，您将找到两个子目录 - `nginx` 和 `web`。
   

   {{< /tab >}}
   {{< tab name="下载" >}}

   下载源代码并解压缩。

   {{< button url="https://github.com/dockersamples/nginx-node-redis/archive/refs/heads/main.zip" text="下载源代码" >}}


   导航到 `nginx-node-redis-main` 目录：

   ```console
   $ cd nginx-node-redis-main
   ```

   在此目录中，您将找到两个子目录 - `nginx` 和 `web`。

   {{< /tab >}}
   {{< /tabs >}}


2. [下载并安装](/get-started/get-docker.md) Docker Desktop。

### 构建镜像


1. 导航到 `nginx` 目录，通过运行以下命令构建镜像：


    ```console
    $ docker build -t nginx .
    ```

2. 导航到 `web` 目录并运行以下命令以构建第一个 Web 镜像：
    
    ```console
    $ docker build -t web .
    ```

### 运行容器

1. 在运行多容器应用程序之前，您需要创建一个网络供它们全部通信。您可以使用 `docker network create` 命令执行此操作：

    ```console
    $ docker network create sample-app
    ```

2. 通过运行以下命令启动 Redis 容器，这将其附加到先前创建的网络并创建网络别名（对 DNS 查找很有用）：

    ```console
    $ docker run -d  --name redis --network sample-app --network-alias redis redis
    ```

3. 通过运行以下命令启动第一个 Web 容器：

    ```console
    $ docker run -d --name web1 -h web1 --network sample-app --network-alias web1 web
    ```

4. 通过运行以下命令启动第二个 Web 容器：

    ```console
    $ docker run -d --name web2 -h web2 --network sample-app --network-alias web2 web
    ```
    
5. 通过运行以下命令启动 Nginx 容器：

    ```console
    $ docker run -d --name nginx --network sample-app  -p 80:80 nginx
    ```

     > [!NOTE]
     >
     > Nginx 通常用作 Web 应用程序的反向代理，将流量路由到后端服务器。在这种情况下，它路由到 Node.js 后端容器（web1 或 web2）。


6.  通过运行以下命令验证容器是否已启动：

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

7. 如果您查看 Docker Desktop Dashboard，您可以看到容器并深入了解其配置。

   ![A screenshot of the Docker Desktop Dashboard showing multi-container applications](images/multi-container-apps.webp?w=5000&border=true)

8. 一切启动并运行后，您可以在浏览器中打开 [http://localhost](http://localhost) 来查看该站点。多次刷新页面以查看处理请求的主机和请求总数：

    ```console
    web2: Number of visits is: 9
    web1: Number of visits is: 10
    web2: Number of visits is: 11
    web1: Number of visits is: 12
    ```

    > [!NOTE]
    >
    > 您可能已经注意到，充当反向代理的 Nginx 可能会在两个后端容器之间以轮询方式分发传入请求。这意味着每个请求可能会轮流定向到不同的容器（web1 和 web2）。输出显示 web1 和 web2 容器的连续增量，并且存储在 Redis 中的实际计数器值仅在响应发送回客户端后才更新。

9. 您可以使用 Docker Desktop Dashboard 删除容器，方法是选择容器并选择 **Delete**（删除）按钮。

   ![A screenshot of Docker Desktop Dashboard showing how to delete the multi-container applications](images/delete-multi-container-apps.webp?border=true)
 
## 使用 Docker Compose 简化部署


Docker Compose 为管理多容器部署提供了一种结构化且简化的方法。如前所述，使用 Docker Compose，您不需要运行多个 `docker run` 命令。您只需要在名为 `compose.yml` 的单个 YAML 文件中定义整个多容器应用程序。让我们看看它是如何工作的。


导航到项目目录的根目录。在此目录中，您将找到一个名为 `compose.yml` 的文件。这个 YAML 文件就是奇迹发生的地方。它定义了构成您的应用程序的所有服务及其配置。每个服务都指定了其镜像、端口、卷、网络以及其功能所需的任何其他设置。

1. 使用 `docker compose up` 命令启动应用程序：

    ```console
    $ docker compose up -d --build
    ```

    当您运行此命令时，您应该会看到类似以下的输出：


    ```console
    Running 5/5
    ✔ Network nginx-nodejs-redis_default    Created                                                0.0s
    ✔ Container nginx-nodejs-redis-web1-1   Started                                                0.1s
    ✔ Container nginx-nodejs-redis-redis-1  Started                                                0.1s
    ✔ Container nginx-nodejs-redis-web2-1   Started                                                0.1s
    ✔ Container nginx-nodejs-redis-nginx-1  Started
    ```

2. 如果您查看 Docker Desktop Dashboard，您可以看到容器并深入了解其配置。


    ![A screenshot of the Docker Desktop Dashboard showing the containers of the application stack deployed using Docker Compose](images/list-containers.webp?border=true)

3. 或者，您可以使用 Docker Desktop Dashboard 删除容器，方法是选择应用程序堆栈并选择 **Delete**（删除）按钮。

   ![A screenshot of Docker Desktop Dashboard that shows how to remove the containers that you deployed using Docker Compose](images/delete-containers.webp?border=true)


在本指南中，您了解了与容易出错且难以管理的 `docker run` 相比，使用 Docker Compose 启动和停止多容器应用程序是多么容易。

## 其他资源

* [`docker container run` CLI 参考](reference/cli/docker/container/run/)
* [什么是 Docker Compose](/get-started/docker-concepts/the-basics/what-is-docker-compose/)