---
title: 什么是注册表？
weight: 30
keywords: concepts, build, images, container, docker desktop, 概念, 构建, 镜像, 容器
description: 什么是注册表？此 Docker 概念将解释什么是注册表，探索它们的互操作性，并让您与注册表进行交互。
aliases:
- /guides/walkthroughs/run-hub-images/
- /guides/walkthroughs/publish-your-image/
- /guides/docker-concepts/the-basics/what-is-a-registry/
---

{{< youtube-embed 2WDl10Wv5rs >}}

## 解释

现在您已经知道什么是容器镜像以及它是如何工作的，您可能会想——您将这些镜像存储在哪里呢？

嗯，您可以将容器镜像存储在您的计算机系统上，但如果您想与朋友分享或在另一台机器上使用它们怎么办？这就是镜像注册表（Image Registry）的用武之地。

镜像注册表是存储和共享容器镜像的集中位置。它可以是公共的，也可以是私有的。[Docker Hub](https://hub.docker.com) 是一个任何人都可以使用的公共注册表，也是默认的注册表。

虽然 Docker Hub 是一个受欢迎的选择，但当今还有许多其他可用的容器注册表，包括 [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/)、[Azure Container Registry (ACR)](https://azure.microsoft.com/en-in/products/container-registry) 和 [Google Container Registry (GCR)](https://cloud.google.com/artifact-registry)。您甚至可以在本地系统或组织内部运行私有注册表。例如 Harbor、JFrog Artifactory、GitLab Container registry 等。

### 注册表 vs. 仓库

在使用注册表时，您可能会听到“注册表”（Registry）和“仓库”（Repository）这两个术语，好像它们是可以互换的。尽管它们相关，但它们并不完全是同一回事。

“注册表”是存储和管理容器镜像的集中位置，而“仓库”是注册表中相关容器镜像的集合。可以将其视为一个文件夹，您可以在其中根据项目组织镜像。每个仓库包含一个或多个容器镜像。

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
> 使用 Docker Hub 免费版，您可以创建一个私有仓库和无限数量的公共仓库。有关更多信息，请访问 [Docker Hub 订阅页面](https://www.docker.com/pricing/)。

## 试一试

在此实践中，您将学习如何构建 Docker 镜像并将其推送到 Docker Hub 仓库。

### 注册免费 Docker 帐户

1. 如果您尚未创建帐户，请前往 [Docker Hub](https://hub.docker.com) 页面注册一个新的 Docker 帐户。

    ![官方 Docker Hub 页面截图，显示注册页面](images/dockerhub-signup.webp?border)

    您可以使用您的 Google 或 GitHub 帐户进行身份验证。

### 创建您的第一个仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择右上角的 **Create repository**（创建仓库）按钮。
3. 选择您的命名空间（通常是您的用户名）并输入 `docker-quickstart` 作为仓库名称。

    ![Docker Hub 页面截图，显示如何创建公共仓库](images/create-hub-repository.webp?border)

4. 将可见性设置为 **Public**（公开）。
5. 选择 **Create**（创建）按钮以创建仓库。

就是这样。您已经成功创建了您的第一个仓库。🎉

这个仓库现在是空的。您现在将通过向其推送一个镜像来解决这个问题。

### 使用 Docker Desktop 登录

1. 如果尚未安装，请[下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。
2. 在 Docker Desktop 图形界面中，选择右上角的 **Sign in**（登录）按钮。

### 克隆 Node.js 示例代码

为了创建镜像，您首先需要一个项目。为了让您快速开始，您将使用位于 [github.com/dockersamples/helloworld-demo-node](https://github.com/dockersamples/helloworld-demo-node) 的示例 Node.js 项目。此仓库包含构建 Docker 镜像所需的预构建 Dockerfile。

不用担心 Dockerfile 的细节，您将在后面的章节中学习。

1. 使用以下命令克隆 GitHub 仓库：

    ```console
    git clone https://github.com/dockersamples/helloworld-demo-node
    ```

2. 进入新创建的目录。

    ```console
    cd helloworld-demo-node
    ```

3. 运行以下命令构建 Docker 镜像，将 `YOUR_DOCKER_USERNAME` 替换为您的用户名。

    ```console
    docker build -t <YOUR_DOCKER_USERNAME>/docker-quickstart .
    ```

    > [!NOTE]
    >
    > 请确保在 `docker build` 命令末尾包含点号 (.)。这告诉 Docker 在哪里查找 Dockerfile。

4. 运行以下命令列出新创建的 Docker 镜像：

    ```console
    docker images
    ```

    您将看到如下所示的输出：

    ```console
    REPOSITORY                                 TAG       IMAGE ID       CREATED         SIZE
    <YOUR_DOCKER_USERNAME>/docker-quickstart   latest    476de364f70e   2 minutes ago   170MB
    ```

5. 通过运行以下命令启动一个容器来测试镜像（将用户名替换为您自己的用户名）：

    ```console
    docker run -d -p 8080:8080 <YOUR_DOCKER_USERNAME>/docker-quickstart 
    ```

    您可以通过浏览器访问 [http://localhost:8080](http://localhost:8080) 来验证容器是否正常工作。

6. 使用 [`docker tag`](/reference/cli/docker/image/tag/) 命令为 Docker 镜像打标签。Docker 标签允许您为镜像标记标签和版本。

    ```console 
    docker tag <YOUR_DOCKER_USERNAME>/docker-quickstart <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0 
    ```

7. 最后，是时候使用 [`docker push`](/reference/cli/docker/image/push/) 命令将新构建的镜像推送到您的 Docker Hub 仓库了：

    ```console 
    docker push <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
    ```

8. 打开 [Docker Hub](https://hub.docker.com) 并导航到您的仓库。转到 **Tags**（标签）部分，查看您新推送的镜像。

    ![Docker Hub 页面截图，显示新添加的镜像标签](images/dockerhub-tags.webp?border=true) 

在此演练中，您注册了一个 Docker 帐户，创建了您的第一个 Docker Hub 仓库，并构建、标记和推送了一个容器镜像到您的 Docker Hub 仓库。

## 其他资源

- [Docker Hub 快速入门](/docker-hub/quickstart/)
- [管理 Docker Hub 仓库](/docker-hub/repos/)

## 下一步

既然您已经了解了容器和镜像的基础知识，您就可以开始学习 Docker Compose 了。

{{< button text="什么是 Docker Compose？" url="what-is-Docker-Compose" >}}