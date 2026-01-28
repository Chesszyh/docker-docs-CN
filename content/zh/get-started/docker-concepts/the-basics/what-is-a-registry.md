---
title: 什么是注册表？
weight: 30
keywords: concepts, build, images, container, docker desktop
description: 什么是注册表？此 Docker 概念将解释什么是注册表，探索它们的互操作性，并让您与注册表进行交互。
aliases:
- /guides/walkthroughs/run-hub-images/
- /guides/walkthroughs/publish-your-image/
- /guides/docker-concepts/the-basics/what-is-a-registry/
---

{{< youtube-embed 2WDl10Wv5rs >}}

## 说明

既然您知道什么是容器镜像及其工作原理，您可能想知道 - 您在哪里存储这些镜像？

嗯，您可以将容器镜像存储在您的计算机系统上，但是如果您想与朋友分享它们或在另一台机器上使用它们怎么办？这就是镜像注册表 (Registry) 发挥作用的地方。

镜像注册表是存储和共享容器镜像的中心位置。它可以是公共的或私有的。[Docker Hub](https://hub.docker.com) 是一个任何人都可以使用的公共注册表，也是默认注册表。

虽然 Docker Hub 是一个流行的选择，但今天还有许多其他可用的容器注册表，包括 [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/)、[Azure Container Registry (ACR)](https://azure.microsoft.com/en-in/products/container-registry) 和 [Google Container Registry (GCR)](https://cloud.google.com/artifact-registry)。您甚至可以在本地系统上或组织内部运行您的私有注册表。例如，Harbor、JFrog Artifactory、GitLab Container registry 等。

### 注册表与仓库

当您使用注册表时，您可能会听到术语 _注册表 (registry)_ 和 _仓库 (repository)_，好像它们是可以互换的。尽管它们相关，但它们并不完全是一回事。

_注册表_ 是存储和管理容器镜像的中心位置，而 _仓库_ 是注册表中相关容器镜像的集合。将其视为一个文件夹，您可以在其中根据项目组织镜像。每个仓库包含一个或多个容器镜像。

下图显示了注册表、仓库和镜像之间的关系。

```goat {class="text-sm"}
+---------------------------------------+
|               Registry                |
|---------------------------------------|
|                                       |
|    +-----------------------------+    |
|    |        Repository A         |    |
|    |-----------------------------|    |
|    |   Image: project-a:v1.0     |    |
|    |   Image: project-a:v2.0     |    |
|    +-----------------------------+    |
|                                       |
|    +-----------------------------+    |
|    |        Repository B         |    |
|    |-----------------------------|    |
|    |   Image: project-b:v1.0     |    |
|    |   Image: project-b:v1.1     |    |
|    |   Image: project-b:v2.0     |    |
|    +-----------------------------+    |
|                                       |
+---------------------------------------+
```

> [!NOTE]
>
> 使用 Docker Hub 的免费版本，您可以创建一个私有仓库和无限的公共仓库。有关更多信息，请访问 [Docker Hub 订阅页面](https://www.docker.com/pricing/)。

## 试一试

在这个动手操作中，您将学习如何构建 Docker 镜像并将其推送到 Docker Hub 仓库。

### 注册免费的 Docker 帐户

1. 如果您还没有帐户，请前往 [Docker Hub](https://hub.docker.com) 页面注册一个新的 Docker 帐户。

    ![显示注册页面的官方 Docker Hub 页面屏幕截图](images/dockerhub-signup.webp?border)

    您可以使用您的 Google 或 GitHub 帐户进行身份验证。

### 创建您的第一个仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择右上角的 **Create repository**（创建仓库）按钮。
3. 选择您的命名空间（很可能是您的用户名）并输入 `docker-quickstart` 作为仓库名称。

    ![显示如何创建公共仓库的 Docker Hub 页面屏幕截图](images/create-hub-repository.webp?border)

4. 将可见性设置为 **Public**（公开）。
5. 选择 **Create**（创建）按钮以创建仓库。

就是这样。您已成功创建了您的第一个仓库。🎉

目前此仓库为空。您现在将通过推送镜像来修复此问题。

### 使用 Docker Desktop 登录

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop（如果尚未安装）。
2. 在 Docker Desktop GUI 中，选择右上角的 **Sign in**（登录）按钮。

### 克隆示例 Node.js 代码

为了创建镜像，您首先需要一个项目。为了让您快速入门，您将使用位于 [github.com/dockersamples/helloworld-demo-node](https://github.com/dockersamples/helloworld-demo-node) 的示例 Node.js 项目。此仓库包含构建 Docker 镜像所需的预构建 Dockerfile。

不用担心 Dockerfile 的细节，因为您将在后面的章节中了解相关内容。

1. 使用以下命令克隆 GitHub 仓库：

    ```console
    git clone https://github.com/dockersamples/helloworld-demo-node
    ```

2. 导航到新创建的目录。

    ```console
    cd helloworld-demo-node
    ```

3. 运行以下命令构建 Docker 镜像，将 `YOUR_DOCKER_USERNAME` 替换为您的用户名。

    ```console
    docker build -t <YOUR_DOCKER_USERNAME>/docker-quickstart .
    ```

    > [!NOTE]
    >
    > 确保在 `docker build` 命令的末尾包含点 (.)。这告诉 Docker 在哪里可以找到 Dockerfile。

4. 运行以下命令列出新创建的 Docker 镜像：

    ```console
    docker images
    ```

    您将看到类似以下的输出：

    ```console
    REPOSITORY                                 TAG       IMAGE ID       CREATED         SIZE
    <YOUR_DOCKER_USERNAME>/docker-quickstart   latest    476de364f70e   2 minutes ago   170MB
    ```

5. 通过运行以下命令启动容器以测试镜像（将用户名替换为您自己的用户名）：

    ```console
    docker run -d -p 8080:8080 <YOUR_DOCKER_USERNAME>/docker-quickstart 
    ```

    您可以通过浏览器访问 [http://localhost:8080](http://localhost:8080) 来验证容器是否正在运行。

6. 使用 [`docker tag`](/reference/cli/docker/image/tag/) 命令标记 Docker 镜像。Docker 标签允许您对镜像进行标记和版本控制。

    ```console 
    docker tag <YOUR_DOCKER_USERNAME>/docker-quickstart <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0 
    ```

7. 最后，是时候使用 [`docker push`](/reference/cli/docker/image/push/) 命令将新构建的镜像推送到您的 Docker Hub 仓库了：

    ```console 
    docker push <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
    ```

8. 打开 [Docker Hub](https://hub.docker.com) 并导航到您的仓库。导航到 **Tags**（标签）部分并查看您新推送的镜像。

    ![显示新添加的镜像标签的 Docker Hub 页面屏幕截图](images/dockerhub-tags.webp?border=true) 

在本演练中，您注册了 Docker 帐户，创建了您的第一个 Docker Hub 仓库，并构建、标记和推送了容器镜像到您的 Docker Hub 仓库。

## 其他资源

- [Docker Hub 快速入门](/docker-hub/quickstart/)
- [管理 Docker Hub 仓库](/docker-hub/repos/)

## 下一步

现在您了解了容器和镜像的基础知识，您已准备好学习 Docker Compose。

{{< button text="什么是 Docker Compose？" url="what-is-Docker-Compose" >}}
