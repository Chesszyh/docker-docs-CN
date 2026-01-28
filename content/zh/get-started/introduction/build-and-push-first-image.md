---
title: 构建并推送您的第一个镜像
keywords: concepts, container, docker desktop, 概念, 容器
description: 此概念页面将教您如何构建并推送您的第一个镜像
summary: |
  学习如何构建您的第一个 Docker 镜像，这是容器化应用程序的关键一步。我们将指导您完成创建镜像仓库以及构建并将镜像推送到 Docker Hub 的过程。这使您能够轻松地在团队内共享您的镜像。
weight: 3
aliases: 
 - /guides/getting-started/build-and-push-first-image/
---

{{< youtube-embed 7ge1s5nAa34 >}}

## 解释

现在您已经更新了[待办事项列表应用程序](develop-with-containers.md)，您准备好为该应用程序创建容器镜像并在 Docker Hub 上共享它了。为此，您需要执行以下操作：

1. 登录您的 Docker 帐户
2. 在 Docker Hub 上创建一个镜像仓库
3. 构建容器镜像
4. 将镜像推送到 Docker Hub

在深入实践指南之前，您应该了解以下几个核心概念。

### 容器镜像

如果您是容器镜像的新手，可以将其视为包含运行应用程序所需一切（包括其文件、配置和依赖项）的标准化包。这些包随后可以分发并与他人共享。

### Docker Hub

要共享您的 Docker 镜像，您需要一个地方来存储它们。这就是注册表（Registry）的用武之地。虽然有许多注册表，但 Docker Hub 是默认且首选的镜像注册表。Docker Hub 提供了一个存储您自己的镜像的地方，也提供了一个查找他人镜像的地方，以便直接运行或作为您自己镜像的基础。

在[使用容器进行开发](develop-with-containers.md)中，您使用了来自 Docker Hub 的以下镜像，每一个都是 [Docker 官方镜像](/manuals/docker-hub/image-library/trusted-content.md#docker-official-images)：

- [node](https://hub.docker.com/_/node) - 提供 Node 环境，用作您开发工作的基础。此镜像也用作最终应用程序镜像的基础。
- [mysql](https://hub.docker.com/_/mysql) - 提供 MySQL 数据库来存储待办事项列表项
- [phpmyadmin](https://hub.docker.com/_/phpmyadmin) - 提供 phpMyAdmin，一个用于 MySQL 数据库的基于 Web 的界面
- [traefik](https://hub.docker.com/_/traefik) - 提供 Traefik，一个现代 HTTP 反向代理和负载均衡器，可根据路由规则将请求路由到适当的容器

浏览 [Docker 官方镜像](https://hub.docker.com/search?image_filter=official&q=)、[Docker 验证发布者](https://hub.docker.com/search?q=&image_filter=store)和 [Docker 赞助开源软件](https://hub.docker.com/search?q=&image_filter=open_source)镜像的完整目录，查看更多可用于运行和构建的内容。

## 试一试

在本实践指南中，您将学习如何登录 Docker Hub 并将镜像推送到 Docker Hub 仓库。

## 登录您的 Docker 帐户

要将镜像推送到 Docker Hub，您需要登录 Docker 帐户。

1. 打开 Docker Dashboard。

2. 选择右上角的 **Sign in**（登录）。

3. 如果需要，创建一个帐户，然后完成登录流程。

完成后，您应该会看到 **Sign in** 按钮变为个人资料图片。

## 创建镜像仓库

现在您拥有了一个帐户，您可以创建一个镜像仓库。就像 Git 仓库保存源代码一样，镜像仓库存储容器镜像。

1.前往 [Docker Hub](https://hub.docker.com)。

2. 选择 **Create repository**（创建仓库）。

3. 在 **Create repository** 页面上，输入以下信息：

    - **Repository name**（仓库名称） - `getting-started-todo-app`
    - **Short description**（简短描述） - 如果您愿意，可以随意输入描述
    - **Visibility**（可见性） - 选择 **Public**（公开）以允许其他人拉取您定制的待办事项应用程序

4. 选择 **Create**（创建）以创建仓库。


## 构建并推送镜像

现在您有了一个仓库，可以准备构建并推送您的镜像了。重要的一点是，您正在构建的镜像扩展了 Node 镜像，这意味着您无需安装或配置 Node、yarn 等。您只需专注于使您的应用程序与众不同的部分。

> **什么是镜像/Dockerfile？**
>
> 暂时不深入探讨，您可以将容器镜像视为包含运行进程所需一切的单个包。在这种情况下，它将包含 Node 环境、后端代码和编译后的 React 代码。
>
> 任何使用该镜像运行容器的机器都可以按原样运行应用程序，而无需在机器上预先安装任何其他内容。
>
> `Dockerfile` 是一个基于文本的脚本，提供了有关如何构建镜像的指令集。对于此快速入门，仓库已经包含 Dockerfile。


{{< tabs group="cli-or-vs-code" persist=true >}}
{{< tab name="CLI" >}}

1. 首先，克隆或[以 ZIP 文件形式下载项目](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)到您的本地机器。

   ```console
   $ git clone https://github.com/docker/getting-started-todo-app
   ```

   项目克隆后，进入克隆创建的新目录：

   ```console
   $ cd getting-started-todo-app
   ```

2. 运行以下命令构建项目，将 `DOCKER_USERNAME` 替换为您的用户名。

    ```console
    $ docker build -t <DOCKER_USERNAME>/getting-started-todo-app .
    ```

    例如，如果您的 Docker 用户名是 `mobydock`，您将运行以下命令：

    ```console
    $ docker build -t mobydock/getting-started-todo-app .
    ```

3. 要验证镜像是否存在于本地，可以使用 `docker image ls` 命令：

    ```console
    $ docker image ls
    ```

    您将看到类似以下的输出：

    ```console
    REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
    mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
    ...
    ```

4. 要推送镜像，请使用 `docker push` 命令。请务必将 `DOCKER_USERNAME` 替换为您的用户名：

    ```console
    $ docker push <DOCKER_USERNAME>/getting-started-todo-app
    ```

    根据您的上传速度，这可能需要一些时间来推送。

{{< /tab >}}
{{< tab name="VS Code" >}}

1. 打开 Visual Studio Code。确保您已从[扩展市场](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)安装了 **Docker extension for VS Code**。

   ![VS code 扩展市场截图](images/install-docker-extension.webp)

2. 在 **File**（文件）菜单中，选择 **Open Folder**（打开文件夹）。选择 **Clone Git Repository**（克隆 Git 仓库）并粘贴此 URL：[https://github.com/docker/getting-started-todo-app](https://github.com/docker/getting-started-todo-app)

    ![显示如何克隆仓库的 VS code 截图](images/clone-the-repo.webp?border=true)



3. 右键单击 `Dockerfile` 并选择 **Build Image...**（构建镜像...）菜单项。


    ![显示右键菜单和“构建镜像”菜单项的 VS Code 截图](images/build-vscode-menu-item.webp?border=true)

4. 在出现的对话框中，输入名称 `DOCKER_USERNAME/getting-started-todo-app`，将 `DOCKER_USERNAME` 替换为您的 Docker 用户名。

5. 按 **Enter** 后，您将看到出现一个终端，构建将在其中进行。完成后，您可以关闭终端。

6. 通过选择左侧导航菜单中的 Docker 徽标打开 VS Code 的 Docker 扩展。

7. 找到您创建的镜像。它的名称将是 `docker.io/DOCKER_USERNAME/getting-started-todo-app`。

8. 展开镜像以查看镜像的标签（或不同版本）。您应该看到一个名为 `latest` 的标签，这是给镜像的默认标签。

9. 右键单击 **latest** 项目并选择 **Push...**（推送...）选项。

    ![Docker 扩展和推送镜像的右键菜单截图](images/build-vscode-push-image.webp)

10. 按 **Enter** 确认，然后观察您的镜像被推送到 Docker Hub。根据您的上传速度，推送镜像可能需要一些时间。

    上传完成后，您可以关闭终端。

{{< /tab >}}
{{< /tabs >}}


## 回顾

在继续之前，花点时间回顾一下这里发生的事情。在短短几分钟内，您就构建了一个打包了您的应用程序的容器镜像，并将其推送到了 Docker Hub。

展望未来，您需要记住：

- Docker Hub 是查找可信内容的首选注册表。Docker 提供了一系列可信内容，由 Docker 官方镜像、Docker 验证发布者和 Docker 赞助开源软件组成，可直接使用或作为您自己镜像的基础。

- Docker Hub 提供了一个分发您自己的应用程序的市场。任何人都可以创建一个帐户并分发镜像。虽然您正在公开发布您创建的镜像，但私有仓库可以确保您的镜像仅供授权用户访问。

> **使用其他注册表**
>
> 虽然 Docker Hub 是默认注册表，但注册表通过[开放容器计划 (Open Container Initiative)](https://opencontainers.org/) 实现了标准化和互操作性。这允许公司和组织运行自己的私有注册表。通常，可信内容会从 Docker Hub 镜像（或复制）到这些私有注册表中。
>



## 下一步

现在您已经构建了一个镜像，是时候讨论为什么作为开发人员的您应该了解更多关于 Docker 的信息，以及它将如何帮助您的日常任务。

{{< button text="下一步" url="whats-next" >}}