---
title: 什么是容器？
weight: 10
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 什么是容器？此概念页面将向您介绍容器，并提供一个快速的动手实践，您将在其中运行您的第一个容器。
aliases:
- /guides/walkthroughs/what-is-a-container/
- /guides/walkthroughs/run-a-container/
- /guides/walkthroughs/
- /get-started/run-your-own-container/
- /guides/docker-concepts/the-basics/what-is-a-container/
---

{{< youtube-embed W1kWqFkiu7k >}}

## 说明

想象一下，您正在开发一个杀手级的 Web 应用程序，它有三个主要组件 - 一个 React 前端、一个 Python API 和一个 PostgreSQL 数据库。如果您想参与这个项目，您必须安装 Node、Python 和 PostgreSQL。

您如何确保您拥有与团队中其他开发人员相同的版本？或者您的 CI/CD 系统？或者生产环境中使用的版本？

您如何确保您的应用程序需要的 Python（或 Node 或数据库）版本不受您机器上已安装内容的影响？您如何管理潜在的冲突？

进入容器！

什么是容器？简而言之，容器是应用程序每个组件的隔离进程。每个组件 - 前端 React 应用程序、Python API 引擎和数据库 - 都在其自己的隔离环境中运行，与您机器上的其他所有内容完全隔离。

这就是它们如此出色的原因。容器是：

- 自包含的。每个容器都拥有其运行所需的一切，不依赖于主机上任何预先安装的依赖项。
- 隔离的。由于容器在隔离环境中运行，因此它们对主机和其他容器的影响最小，从而提高了应用程序的安全性。
- 独立的。每个容器都是独立管理的。删除一个容器不会影响任何其他容器。
- 可移植的。容器可以在任何地方运行！在您的开发机器上运行的容器在数据中心或云中的任何地方都将以相同的方式工作！

### 容器与虚拟机 (VM)

不深入探讨，VM 是一个完整的操作系统，拥有自己的内核、硬件驱动程序、程序和应用程序。仅为了隔离单个应用程序而启动 VM 会产生大量开销。

容器只是一个隔离的进程，其中包含其运行所需的所有文件。如果您运行多个容器，它们都共享相同的内核，从而使您可以在更少的基础设施上运行更多的应用程序。

> **同时使用 VM 和容器**
>
> 您经常���看到容器和 VM 一起使用。例如，在云环境中，预配的机器通常是 VM。但是，与其预配一台机器来运行一个应用程序，不如使用带有容器运行时的 VM 来运行多个容器化应用程序，从而提高资源利用率并降低成本。


## 动手试试

在这个动手实践中，您将看到如何使用 Docker Desktop GUI 运行 Docker 容器。

{{< tabs group=concept-usage persist=true >}}
{{< tab name="使用 GUI" >}}

使用以下说明运行容器。

1. 打开 Docker Desktop 并选择顶部导航栏上的 **Search** 字段。

2. 在搜索输入中指定 `welcome-to-docker`，然后选择 **Pull** 按钮。

    ![Docker Desktop 仪表板的屏幕截图，显示了 welcome-to-docker Docker 镜像的搜索结果](images/search-the-docker-image.webp?border=true&w=1000&h=700)

3. 镜像成功拉取后，选择 **Run** 按钮。

4. 展开 **Optional settings**。

5. 在 **Container name** 中，指定 `welcome-to-docker`。

6. 在 **Host port** 中，指定 `8080`。

    ![Docker Desktop 仪表板的屏幕截图，显示了容器运行对话框，其中 welcome-to-docker 作为容器名称输入，8080 作为端口号指定](images/run-a-new-container.webp?border=true&w=550&h=400)

7. 选择 **Run** 以启动您的容器。

恭喜！您刚刚运行了���的第一个容器！🎉
 
### 查看您的容器

您可以通过转到 Docker Desktop 仪表板的 **Containers** 视图来查看所有容器。

![Docker Desktop GUI 的容器视图的屏幕截图，显示了在主机端口 8080 上运行的 welcome-to-docker 容器](images/view-your-containers.webp?border=true&w=750&h=600)

此容器运行一个 Web 服务器，该服务器显示一个简单的网站。在处理更复杂的项目时，您将在不同的容器中运行不同的部分。例如，您可能会为前端、后端和数据库运行不同的容器。

### 访问前端

当您启动容器时，您将容器的一个端口暴露到您的机器上。可以将其视为创建配置以允许您通过容器的隔离环境进行连接。

对于此容器，前端可在端口 `8080` 上访问。要打开网站，请选择容器的 **Port(s)** 列中的链接或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![来自正在运行的容器的登录页面的屏幕截图](images/access-the-frontend.webp?border)

### 探索您的容器

Docker Desktop 允许您探索和与容器的不同方面进行交互。自己试试吧。

1. 转到 Docker Desktop 仪表板中的 **Containers** 视图。

2. 选择您的容器。

3. 选择 **Files** 选项卡以探索容器的隔离文件系统。

    ![Docker Desktop 仪表板的屏幕截图，显示了正在运行的容器内的文件和目录](images/explore-your-container.webp?border)

### 停止您的容器

`docker/welcome-to-docker` 容器将继续运行，直到您停止它。

1. 转到 Docker Desktop 仪表板中的 **Containers** 视图。

2. 找到您要停止的容器。

3. 在 **Actions** 列中选择 **Stop** 操作。

    ![Docker Desktop 仪表板的屏幕截图，其中选择了 welcome 容器并准备停止](images/stop-your-container.webp?border)

{{< /tab >}}
{{< tab name="使用 CLI" >}}

按照说明使用 CLI 运行容器：

1. 打开您的 CLI 终端并使用 [`docker run`](/reference/cli/docker/container/run/) 命令启动一个容器：

    ```console
    $ docker run -d -p 8080:80 docker/welcome-to-docker
    ```

    此命令的输出是完整的容器 ID。

恭喜！您刚刚启动了您的第一个容器！🎉

### 查看您正在运行的容器

您可以使用 [`docker ps`](/reference/cli/docker/container/ls/) 命令验证容器是否已启动并正在运行：

```console
docker ps
```

您将看到如下输出：

```console
 CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                      NAMES
 a1f7a4bb3a27   docker/welcome-to-docker   "/docker-entrypoint.…"   11 seconds ago   Up 11 seconds   0.0.0.0:8080->80/tcp       gracious_keldysh
```

此容器运行一个 Web 服务器，该服务器显示一个简单的网站。在处理更复杂的项目时，您将在不同的容器中运行不同的部分。例如，为 `frontend`、`backend` 和 `database` 分别运行一个不同的容器。

> [!TIP]
>
> `docker ps` 命令将*仅*显示正在运行的容器。要查看已停止的容器，请添加 `-a` 标志以列出所有容器：`docker ps -a`


### 访问前端

当您启动容器时，您将容器的一个端口暴露到您的机器上。可以将其视为创建配置以允许您通过容器的隔离环境进行连接。

对于此容器，前端可在端口 `8080` 上访问。要打开网站，请选择容器的 **Port(s)** 列中的链接或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![来自正在运行的容器的 Nginx Web 服务器登录页面的屏幕截图](images/access-the-frontend.webp?border)

### 停止您的容器

`docker/welcome-to-docker` 容器将继续运行，直到您停止它。您可以使用 `docker stop` 命令停止容器。

1. 运行 `docker ps` 以获取容器的 ID

2. 将容器 ID 或名称提供给 [`docker stop`](/reference/cli/docker/container/stop/) 命令：

    ```console
    docker stop <the-container-id>
    ```

> [!TIP]
>
> 按 ID 引用容器时，您无需提供完整的 ID。您只需提供足够的 ID 使其唯一即可。例如，可以通过运行以下命令来停止上一个容器：
>
> ```console
> docker stop a1f
> ```

{{< /tab >}}
{{< /tabs >}}

## 其他资源

以下链接提供了有关容器的其他指导：

- [运行容器](/engine/containers/run/)
- [容器概述](https://www.docker.com/resources/what-container/)
- [为什么选择 Docker？](https://www.docker.com/why-docker/)

## 后续步骤

现在您已经了解了 Docker 容器的基础知识，是时候了解 Docker 镜像了。

{{< button text="什么是镜像？" url="what-is-an-image" >}}
