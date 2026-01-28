---
title: 构建并推送您的第一个镜像
keywords: concepts, container, docker desktop
description: 本概念页面将教您如何构建并推送您的第一个镜像
summary: |
  学习如何构建您的第一个 Docker 镜像，这是容器化应用程序的关键步骤。我们将指导您完成创建镜像仓库以及构建和推送镜像到 Docker Hub 的过程。这使您能够轻松地在团队内共享镜像。
weight: 3
aliases:
 - /guides/getting-started/build-and-push-first-image/
---

{{< youtube-embed 7ge1s5nAa34 >}}

## 概念解释

现在您已经更新了[待办事项列表应用](develop-with-containers.md)，您可以准备为应用程序创建容器镜像并在 Docker Hub 上共享它。为此，您需要执行以下操作：

1. 使用您的 Docker 账户登录
2. 在 Docker Hub 上创建镜像仓库
3. 构建容器镜像
4. 将镜像推送到 Docker Hub

在深入动手指南之前，以下是您应该了解的一些核心概念。

### 容器镜像

如果您是容器镜像的新手，可以将它们视为包含运行应用程序所需的一切的标准化包，包括其文件、配置和依赖项。然后可以分发这些包并与他人共享。

### Docker Hub

要共享您的 Docker 镜像，您需要一个存储它们的地方。这就是镜像仓库发挥作用的地方。虽然有很多镜像仓库，但 Docker Hub 是默认的、首选的镜像仓库。Docker Hub 既提供了一个存储您自己镜像的地方，也可以从他人那里找到镜像，以便直接运行或作为您自己镜像的基础。

在[使用容器进行开发](develop-with-containers.md)中，您使用了来自 Docker Hub 的以下镜像，每个镜像都是 [Docker 官方镜像](/manuals/docker-hub/image-library/trusted-content.md#docker-official-images)：

- [node](https://hub.docker.com/_/node) - 提供 Node 环境，并用作开发工作的基础。此镜像也用作最终应用程序镜像的基础。
- [mysql](https://hub.docker.com/_/mysql) - 提供 MySQL 数据库来存储待办事项列表项
- [phpmyadmin](https://hub.docker.com/_/phpmyadmin) - 提供 phpMyAdmin，一个与 MySQL 数据库交互的基于 Web 的界面
- [traefik](https://hub.docker.com/_/traefik) - 提供 Traefik，一个现代 HTTP 反向代理和负载均衡器，根据路由规则将请求路由到适当的容器

浏览完整的 [Docker 官方镜像](https://hub.docker.com/search?image_filter=official&q=)、[Docker 认证发布者](https://hub.docker.com/search?q=&image_filter=store)和 [Docker 赞助的开源软件](https://hub.docker.com/search?q=&image_filter=open_source)镜像目录，查看更多可运行和构建的内容。

## 动手实践

在本动手指南中，您将学习如何登录 Docker Hub 并将镜像推送到 Docker Hub 仓库。

## 使用您的 Docker 账户登录

要将镜像推送到 Docker Hub，您需要使用 Docker 账户登录。

1. 打开 Docker Dashboard。

2. 选择右上角的 **Sign in**。

3. 如果需要，创建一个账户，然后完成登录流程。

完成后，您应该会看到 **Sign in** 按钮变成个人资料图片。

## 创建镜像仓库

现在您有了账户，可以创建镜像仓库了。就像 Git 仓库存放源代码一样，镜像仓库存储容器镜像。

1. 进入 [Docker Hub](https://hub.docker.com)。

2. 选择 **Create repository**。

3. 在 **Create repository** 页面上，输入以下信息：

    - **Repository name** - `getting-started-todo-app`
    - **Short description** - 如果您愿意，可以输入描述
    - **Visibility** - 选择 **Public** 以允许其他人拉取您自定义的待办事项应用

4. 选择 **Create** 创建仓库。


## 构建并推送镜像

现在您有了仓库，可以准备构建和推送镜像了。需要注意的一点是，您构建的镜像扩展了 Node 镜像，这意味着您不需要安装或配置 Node、yarn 等。您可以简单地专注于使您的应用程序独特的地方。

> **什么是镜像/Dockerfile？**
>
> 简单地说，可以将容器镜像视为包含运行进程所需的一切的单个包。在本例中，它将包含 Node 环境、后端代码和编译后的 React 代码。
>
> 使用该镜像运行容器的任何机器都将能够按构建时的方式运行应用程序，而无需在机器上预先安装任何其他内容。
>
> `Dockerfile` 是一个基于文本的脚本，提供如何构建镜像的指令集。对于此快速入门，仓库已经包含 Dockerfile。


{{< tabs group="cli-or-vs-code" persist=true >}}
{{< tab name="CLI" >}}

1. 首先，将项目克隆或[下载为 ZIP 文件](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)到您的本地机器。

   ```console
   $ git clone https://github.com/docker/getting-started-todo-app
   ```

   项目克隆后，进入克隆创建的新目录：

   ```console
   $ cd getting-started-todo-app
   ```

2. 通过运行以下命令构建项目，将 `DOCKER_USERNAME` 替换为您的用户名。

    ```console
    $ docker build -t <DOCKER_USERNAME>/getting-started-todo-app .
    ```

    例如，如果您的 Docker 用户名是 `mobydock`，您将运行以下命令：

    ```console
    $ docker build -t mobydock/getting-started-todo-app .
    ```

3. 要验证镜像是否存在于本地，您可以使用 `docker image ls` 命令：

    ```console
    $ docker image ls
    ```

    您将看到类似以下的输出：

    ```console
    REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
    mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
    ...
    ```

4. 要推送镜像，请使用 `docker push` 命令。务必将 `DOCKER_USERNAME` 替换为您的用户名：

    ```console
    $ docker push <DOCKER_USERNAME>/getting-started-todo-app
    ```

    根据您的上传速度，这可能需要一段时间才能推送。

{{< /tab >}}
{{< tab name="VS Code" >}}

1. 打开 Visual Studio Code。确保您已从 [Extension Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) 安装了 **Docker extension for VS Code**。

   ![VS Code 扩展市场截图](images/install-docker-extension.webp)

2. 在 **File** 菜单中，选择 **Open Folder**。选择 **Clone Git Repository** 并粘贴此 URL：[https://github.com/docker/getting-started-todo-app](https://github.com/docker/getting-started-todo-app)

    ![VS Code 显示如何克隆仓库的截图](images/clone-the-repo.webp?border=true)



3. 右键单击 `Dockerfile` 并选择 **Build Image...** 菜单项。


    ![VS Code 显示右键菜单和"Build Image"菜单项的截图](images/build-vscode-menu-item.webp?border=true)

4. 在出现的对话框中，输入名称 `DOCKER_USERNAME/getting-started-todo-app`，将 `DOCKER_USERNAME` 替换为您的 Docker 用户名。

5. 按 **Enter** 后，您将看到一个终端出现，构建将在其中进行。完成后，随时关闭终端。

6. 通过选择左侧导航菜单中的 Docker 徽标打开 VS Code 的 Docker 扩展。

7. 找到您创建的镜像。它的名称将是 `docker.io/DOCKER_USERNAME/getting-started-todo-app`。

8. 展开镜像以查看镜像的标签（或不同版本）。您应该会看到一个名为 `latest` 的标签，这是给镜像的默认标签。

9. 右键单击 **latest** 项并选择 **Push...** 选项。

    ![Docker 扩展和推送镜像的右键菜单截图](images/build-vscode-push-image.webp)

10. 按 **Enter** 确认，然后观看您的镜像推送到 Docker Hub。根据您的上传速度，可能需要一段时间才能推送镜像。

    上传完成后，随时关闭终端。

{{< /tab >}}
{{< /tabs >}}


## 回顾

在继续之前，花点时间反思一下这里发生了什么。在几分钟内，您能够构建一个打包您应用程序的容器镜像并将其推送到 Docker Hub。

展望未来，您需要记住：

- Docker Hub 是查找可信内容的首选镜像仓库。Docker 提供一系列可信内容，包括 Docker 官方镜像、Docker 认证发布者和 Docker 赞助的开源软件，可直接使用或作为您自己镜像的基础。

- Docker Hub 提供了一个分发您自己应用程序的市场。任何人都可以创建账户并分发镜像。虽然您正在公开分发您创建的镜像，但私有仓库可以确保您的镜像仅对授权用户可访问。

> **使用其他镜像仓库**
>
> 虽然 Docker Hub 是默认镜像仓库，但镜像仓库通过 [Open Container Initiative](https://opencontainers.org/) 被标准化和互操作。这允许公司和组织运行自己的私有镜像仓库。通常，可信内容会从 Docker Hub 镜像（或复制）到这些私有镜像仓库。
>



## 后续步骤

现在您已经构建了镜像，是时候讨论为什么作为开发人员您应该更多地了解 Docker，以及它将如何帮助您完成日常任务。

{{< button text="下一步" url="whats-next" >}}
