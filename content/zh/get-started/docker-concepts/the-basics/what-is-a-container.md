---
title: 什么是容器？
weight: 10
keywords: concepts, build, images, container, docker desktop
description: 什么是容器？本概念页面将教您了解容器，并提供一个快速动手实践，让您运行第一个容器。
aliases:
- /guides/walkthroughs/what-is-a-container/
- /guides/walkthroughs/run-a-container/
- /guides/walkthroughs/
- /get-started/run-your-own-container/
- /guides/docker-concepts/the-basics/what-is-a-container/
---

{{< youtube-embed W1kWqFkiu7k >}}

## 概念解释

假设您正在开发一个出色的 Web 应用程序，它有三个主要组件——React 前端、Python API 和 PostgreSQL 数据库。如果您想在这个项目上工作，您需要安装 Node、Python 和 PostgreSQL。

您如何确保您拥有与团队中其他开发人员相同的版本？或者与您的 CI/CD 系统相同？或者与生产环境中使用的版本相同？

您如何确保应用程序所需的 Python（或 Node 或数据库）版本不受机器上已安装版本的影响？您如何管理潜在的冲突？

这就是容器的用武之地！

什么是容器？简单来说，容器是应用程序每个组件的隔离进程。每个组件——React 前端应用、Python API 引擎和数据库——都在自己的隔离环境中运行，与机器上的其他一切完全隔离。

以下是容器的优势所在。容器具有以下特点：

- 自包含。每个容器都拥有运行所需的一切，无需依赖主机上任何预先安装的依赖项。
- 隔离性。由于容器是隔离运行的，它们对主机和其他容器的影响最小，从而提高了应用程序的安全性。
- 独立性。每个容器都是独立管理的。删除一个容器不会影响其他容器。
- 可移植性。容器可以在任何地方运行！在您的开发机器上运行的容器将以相同的方式在数据中心或云端的任何地方工作！

### 容器与虚拟机（VM）的对比

简而言之，虚拟机是一个完整的操作系统，拥有自己的内核、硬件驱动程序、程序和应用程序。仅为隔离单个应用程序而启动虚拟机会带来很大的开销。

容器只是一个隔离的进程，包含运行所需的所有文件。如果您运行多个容器，它们都共享相同的内核，这使您能够在更少的基础设施上运行更多的应用程序。

> **同时使用虚拟机和容器**
>
> 您经常会看到容器和虚拟机一起使用。例如，在云环境中，配置的机器通常是虚拟机。但是，与其配置一台机器来运行一个应用程序，不如使用带有容器运行时的虚拟机来运行多个容器化应用程序，从而提高资源利用率并降低成本。


## 动手实践

在本动手实践中，您将了解如何使用 Docker Desktop GUI 运行 Docker 容器。

{{< tabs group=concept-usage persist=true >}}
{{< tab name="Using the GUI" >}}

按照以下说明运行容器。

1. 打开 Docker Desktop 并选择顶部导航栏上的 **Search** 字段。

2. 在搜索输入框中输入 `welcome-to-docker`，然后选择 **Pull** 按钮。

    ![Docker Desktop 仪表板的截图，显示 welcome-to-docker Docker 镜像的搜索结果](images/search-the-docker-image.webp?border=true&w=1000&h=700)

3. 镜像成功拉取后，选择 **Run** 按钮。

4. 展开 **Optional settings**。

5. 在 **Container name** 中，输入 `welcome-to-docker`。

6. 在 **Host port** 中，输入 `8080`。

    ![Docker Desktop 仪表板的截图，显示容器运行对话框，容器名称为 welcome-to-docker，端口号为 8080](images/run-a-new-container.webp?border=true&w=550&h=400)

7. 选择 **Run** 启动您的容器。

恭喜！您刚刚运行了您的第一个容器！🎉

### 查看您的容器

您可以通过进入 Docker Desktop 仪表板的 **Containers** 视图来查看所有容器。

![Docker Desktop GUI 容器视图的截图，显示 welcome-to-docker 容器在主机端口 8080 上运行](images/view-your-containers.webp?border=true&w=750&h=600)

这个容器运行一个 Web 服务器，显示一个简单的网站。在处理更复杂的项目时，您将在不同的容器中运行不同的部分。例如，您可能会为前端、后端和数据库分别运行不同的容器。

### 访问前端

当您启动容器时，您将容器的一个端口暴露到了您的机器上。可以将此视为创建配置，让您能够连接到容器的隔离环境。

对于这个容器，前端可以在端口 `8080` 上访问。要打开网站，请选择容器 **Port(s)** 列中的链接，或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![正在运行的容器的登录页面截图](images/access-the-frontend.webp?border)

### 探索您的容器

Docker Desktop 允许您探索容器的不同方面并与之交互。请自己尝试一下。

1. 在 Docker Desktop 仪表板中进入 **Containers** 视图。

2. 选择您的容器。

3. 选择 **Files** 选项卡以探索容器的隔离文件系统。

    ![Docker Desktop 仪表板的截图，显示正在运行的容器内的文件和目录](images/explore-your-container.webp?border)

### 停止您的容器

`docker/welcome-to-docker` 容器会持续运行，直到您停止它。

1. 在 Docker Desktop 仪表板中进入 **Containers** 视图。

2. 找到您要停止的容器。

3. 选择 **Actions** 列中的 **Stop** 操作。

    ![Docker Desktop 仪表板的截图，选中了 welcome 容器并准备停止](images/stop-your-container.webp?border)

{{< /tab >}}
{{< tab name="Using the CLI" >}}

按照以下说明使用 CLI 运行容器：

1. 打开您的 CLI 终端，使用 [`docker run`](/reference/cli/docker/container/run/) 命令启动容器：

    ```console
    $ docker run -d -p 8080:80 docker/welcome-to-docker
    ```

    此命令的输出是完整的容器 ID。

恭喜！您刚刚启动了您的第一个容器！🎉

### 查看正在运行的容器

您可以使用 [`docker ps`](/reference/cli/docker/container/ls/) 命令验证容器是否正在运行：

```console
docker ps
```

您将看到类似以下的输出：

```console
 CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                      NAMES
 a1f7a4bb3a27   docker/welcome-to-docker   "/docker-entrypoint.…"   11 seconds ago   Up 11 seconds   0.0.0.0:8080->80/tcp       gracious_keldysh
```

这个容器运行一个 Web 服务器，显示一个简单的网站。在处理更复杂的项目时，您将在不同的容器中运行不同的部分。例如，为 `frontend`、`backend` 和 `database` 分别运行不同的容器。

> [!TIP]
>
> `docker ps` 命令将 _只_ 显示正在运行的容器。要查看已停止的容器，请添加 `-a` 标志以列出所有容器：`docker ps -a`


### 访问前端

当您启动容器时，您将容器的一个端口暴露到了您的机器上。可以将此视为创建配置，让您能够连接到容器的隔离环境。

对于这个容器，前端可以在端口 `8080` 上访问。要打开网站，请选择容器 **Port(s)** 列中的链接，或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![Nginx Web 服务器登录页面的截图，来自正在运行的容器](images/access-the-frontend.webp?border)

### 停止您的容器

`docker/welcome-to-docker` 容器会持续运行，直到您停止它。您可以使用 `docker stop` 命令停止容器。

1. 运行 `docker ps` 获取容器的 ID

2. 将容器 ID 或名称提供给 [`docker stop`](/reference/cli/docker/container/stop/) 命令：

    ```console
    docker stop <the-container-id>
    ```

> [!TIP]
>
> 通过 ID 引用容器时，您不需要提供完整的 ID。您只需要提供足够使其唯一的 ID 部分即可。例如，可以通过运行以下命令停止前面的容器：
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

现在您已经了解了 Docker 容器的基础知识，是时候学习 Docker 镜像了。

{{< button text="什么是镜像？" url="what-is-an-image" >}}
