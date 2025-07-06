---
title: 构建并推送您的第一个镜像
keywords: 概念, 容器, docker desktop
description: 此概念页面将教您如何构建和推送您的第一个镜像
summary: |
  了解如何构建您的第一个 Docker 镜像，这是容器化您的
  应用程序的关键一步。我们将指导您完成创建镜像
  存储库以及构建和推送您的镜像到 Docker Hub 的过程。这使
  您能够轻松地在团队中共享您的镜像。
weight: 3
aliases: 
 - /guides/getting-started/build-and-push-first-image/
---

{{< youtube-embed 7ge1s5nAa34 >}}

## 说明

现在您已经更新了[待办事项列表应用程序](develop-with-containers.md)，您已准备好为该应用程序创建一个容器镜像并将其共享到 Docker Hub 上。为此，您需要执行以下操作：

1. 使用您的 Docker 帐户登录
2. 在 Docker Hub 上创建一个镜像存储库
3. 构建容器镜像
4. 将镜像推送到 Docker Hub

在您深入了解本动手指南之前，您应该了解以下几个核心概念。

### 容器镜像

如果您是容器镜像的新手��可以将它们视为一个标准化的包，其中包含运行应用程序所需的一切，包括其文件、配置和依赖项。然后可以将这些包分发并与他人共享。

### Docker Hub

要共享您的 Docker 镜像，您需要一个地方来存储它们。这就是仓库的用武之地。虽然有许多仓库，但 Docker Hub 是默认的、首选的镜像仓库。Docker Hub 不仅为您提供了一个存储您自己镜像的地方，还为您提供了一个查找他人镜像的地方，您可以直接运行这些镜像，也可以将它们用作您自己镜像的基础。

在[使用容器进行开发](develop-with-containers.md)中，您使用了来自 Docker Hub 的以下镜像，每个镜像都是[Docker 官方镜像](/manuals/docker-hub/image-library/trusted-content.md#docker-official-images)：

- [node](https://hub.docker.com/_/node) - 提供一个 Node 环境，并用作您开发工作的基础。此镜像也用作最终应用程序镜像的基础。
- [mysql](https://hub.docker.com/_/mysql) - 提供一个 MySQL 数据库来存储待办事项列表项
- [phpmyadmin](https://hub.docker.com/_/phpmyadmin) - 提供 phpMyAdmin，一个基于 Web 的 MySQL 数据库界面
- [traefik](https://hub.docker.com/_/traefik) - 提供 Traefik，一个现代的 HTTP 反向代理和负载均衡器，可根据路由规则将请求路由��适当的容器

浏览[Docker 官方镜像](https://hub.docker.com/search?image_filter=official&q=)、[Docker 验证的发布者](https://hub.docker.com/search?q=&image_filter=store)和[Docker 赞助的开源软件](https://hub.docker.com/search?q=&image_filter=open_source)镜像的完整目录，以查看更多可运行和构建的内容。

## 动手试试

在这个动手指南中，您将学习如何登录 Docker Hub 并将镜像推送到 Docker Hub 存储库。

## 使用您的 Docker 帐户登录

要将镜像推送到 Docker Hub，您需要使用 Docker 帐户登录。

1. 打开 Docker 仪表板。

2. 选择右上角的 **Sign in**。

3. 如果需要，创建一个帐户，然后完成登录流程。

完成后，您应该会看到 **Sign in** 按钮变成一个个人资料图片。

## 创建一个镜像存储库

现在您有了一个帐户，您可以创建一个镜像存储库。就像 Git 存储库保存源代码一样，镜像存储库存储容器镜像。

1. 转到 [Docker Hub](https://hub.docker.com)。

2. 选择 **Create repository**。

3. 在 **Create repository** 页面上，输入以下信息：

    - **Repository name** - `getting-started-todo-app`
    - **Short description** - 如果您愿意，可以随时输入描述
    - **Visibility** - 选择 **Public** 以允许其他人拉取您自定义的待办事项应用程序

4. 选择 **Create** 以创建存储库。


## 构建并推送镜像

现在您有了一个存储库，您已准备好构建并推送您的镜像。一个重要的注意事项是，您正在构建的镜像扩展了 Node 镜像，这意味着您无需安装或配置 Node、yarn 等。您只需专注于使您的应用程序与众不同的地方。

> **什么是镜像/Dockerfile？**
>
> 不用太深入，可以将容器镜像视为一个包含
> 运行进程所需一切的单个包。在这种情况下，它将包含一个 Node 环境、
> 后端代码和已编译的 React 代码。
>
> 任何使用该镜像运行容器的机器，都将能够像
> 构建时一样运行该应用程序，而无需在机器上预先安装任何其他东西。
>
> `Dockerfile` 是一个基于文本的脚本，提供了有关如何构建
> 镜像的指令集。对于这个快速入门，存储库已经包含了 Dockerfile。


{{< tabs group="cli-or-vs-code" persist=true >}}
{{< tab name="CLI" >}}

1. 首先，将[项目克隆或下载为 ZIP 文件](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)到您的本地计算机。

   ```console
   $ git clone https://github.com/docker/getting-started-todo-app
   ```

   克隆项目后，导航到克隆创建的新目录：

   ```console
   $ cd getting-started-todo-app
   ```

2. 通过运行以下命令来构建项目，将 `DOCKER_USERNAME` 替换为您的用户名。

    ```console
    $ docker build -t <DOCKER_USERNAME>/getting-started-todo-app .
    ```

    例如，如果您的 Docker 用户名是 `mobydock`，您将运行以下命令：

    ```console
    $ docker build -t mobydock/getting-started-todo-app .
    ```

3. 要验证镜像是否在本地存在，您可以使用 `docker image ls` 命令：

    ```console
    $ docker image ls
    ```

    您将看到类似于以下内容的输出：

    ```console
    REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
    mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
    ...
    ```

4. 要推送镜像，请使用 `docker push` 命令。请务必将 `DOCKER_USERNAME` 替换为您的用户名：

    ```console
    $ docker push <DOCKER_USERNAME>/getting-started-todo-app
    ```

    根据您的上传速度，这可能需要一些时间才能推送。

{{< /tab >}}
{{< tab name="VS Code" >}}

1. 打开 Visual Studio Code。确保您已从[扩展市场](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)安装了 **Docker extension for VS Code**。

   ![VS code 扩展市场的屏幕截图](images/install-docker-extension.webp)

2. 在 **File** 菜单中，选择 **Open Folder**。选择 **Clone Git Repository** 并粘贴此 URL：[https://github.com/docker/getting-started-todo-app](https://github.com/docker/getting-started-todo-app)

    ![显示如何克隆存储库的 VS code 的屏幕截图](images/clone-the-repo.webp?border=true)



3. 右键单击 `Dockerfile` 并选择 **Build Image...** 菜单项。


    ![显示右键单击菜单和“Build Image”菜单项的 VS Code 的屏幕截图](images/build-vscode-menu-item.webp?border=true)

4. 在出现的对话框中，输入 `DOCKER_USERNAME/getting-started-todo-app` 的名称，将 `DOCKER_USERNAME` 替换为您的 Docker 用户名。

5. 按 **Enter** 后，您将看到一个终端出现，构建将在其中进行。完成后，随时关闭终端。

6. 通过选择左侧导航菜单中的 Docker 徽标打开 Docker Extension for VS Code。

7. 找到您创建的镜像。它的名称将是 `docker.io/DOCKER_USERNAME/getting-started-todo-app`。

8. 展开镜像以查看镜像的标签（或不同版本）。您应该会看到一个名为 `latest` 的标签，这是镜像的默认标签。

9. 右键单击 **latest** 项并选择 **Push...** 选���。

    ![Docker 扩展和用于推送镜像的右键单击菜单的屏幕截图](images/build-vscode-push-image.webp)

10. 按 **Enter** 确认，然后观看您的镜像被推送到 Docker Hub。根据您的上传速度，推送镜像可能需要一些时间。

    上传完成后，随时关闭终端。

{{< /tab >}}
{{< /tabs >}}


## 回顾

在继续之前，花点时间回顾一下这里发生的事情。在几分钟内，您就能够构建一个打包您的应用程序的容器镜像并将其推送到 Docker Hub。

展望未来，您需要记住：

- Docker Hub 是查找可信内容的首选仓库。Docker 提供了一系列可信内容，包括 Docker 官方镜像、Docker 验证的发布者和 Docker 赞助的开源软件，可直接使用或作为您自己镜像的基础。

- Docker Hub 提供了一个分发您自己应用程序的市场。任何人都可以创建一个帐户并分发镜像。虽然您正在公开发布您创建的镜像，但私有存储库可以确保您的镜像只能由授权用户访问。

> **其他仓库的使用**
>
> 虽然 Docker Hub 是默认仓库，但仓库是标准化的，并通过[开放容器倡议](https://opencontainers.org/)实现互操作。这允许公司和组织运行自己的私有仓库。通常，可信内容会从 Docker Hub 镜像（或复制）到这些私有仓库中。
>



## 后续步骤

现在您已经构建了一个镜像，是时候讨论一下为什么作为一名开发人员，您应该更多地了解 Docker 以及它将如何在您的日常任务中为您提供帮助。

{{< button text="下一步是什么" url="whats-next" >}}


