---
title: 什么是镜像仓库？
weight: 30
keywords: concepts, build, images, container, docker desktop
description: 什么是镜像仓库？本 Docker 概念页面将解释什么是镜像仓库，探索其互操作性，并让您与镜像仓库进行交互。
aliases:
- /guides/walkthroughs/run-hub-images/
- /guides/walkthroughs/publish-your-image/
- /guides/docker-concepts/the-basics/what-is-a-registry/
---

{{< youtube-embed 2WDl10Wv5rs >}}

## 概念解释

现在您知道了什么是容器镜像以及它是如何工作的，您可能想知道——这些镜像存储在哪里？

您可以将容器镜像存储在您的计算机系统上，但如果您想与朋友共享或在另一台机器上使用它们怎么办？这就是镜像仓库（registry）发挥作用的地方。

镜像仓库是用于存储和共享容器镜像的集中位置。它可以是公共的或私有的。[Docker Hub](https://hub.docker.com) 是任何人都可以使用的公共镜像仓库，也是默认的镜像仓库。

虽然 Docker Hub 是一个流行的选择，但今天还有许多其他可用的容器镜像仓库，包括 [Amazon Elastic Container Registry（ECR）](https://aws.amazon.com/ecr/)、[Azure Container Registry（ACR）](https://azure.microsoft.com/en-in/products/container-registry) 和 [Google Container Registry（GCR）](https://cloud.google.com/artifact-registry)。您甚至可以在本地系统或组织内部运行自己的私有镜像仓库。例如，Harbor、JFrog Artifactory、GitLab Container Registry 等。

### 镜像仓库与仓库

在使用镜像仓库时，您可能会听到 _registry_（镜像仓库）和 _repository_（仓库）这两个术语，好像它们可以互换使用。尽管它们相关，但实际上并不完全相同。

_registry_（镜像仓库）是存储和管理容器镜像的集中位置，而 _repository_（仓库）是镜像仓库中相关容器镜像的集合。可以将其视为一个文件夹，您可以根据项目组织镜像。每个仓库包含一个或多个容器镜像。

下图展示了镜像仓库、仓库和镜像之间的关系。

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
> 使用 Docker Hub 的免费版本，您可以创建一个私有仓库和无限数量的公共仓库。更多信息，请访问 [Docker Hub 订阅页面](https://www.docker.com/pricing/)。

## 动手实践

在本动手实践中，您将学习如何构建 Docker 镜像并将其推送到 Docker Hub 仓库。

### 注册免费 Docker 账户

1. 如果您还没有创建账户，请前往 [Docker Hub](https://hub.docker.com) 页面注册一个新的 Docker 账户。

    ![Docker Hub 官方页面的截图，显示注册页面](images/dockerhub-signup.webp?border)

    您可以使用 Google 或 GitHub 账户进行身份验证。

### 创建您的第一个仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择右上角的 **Create repository** 按钮。
3. 选择您的命名空间（通常是您的用户名）并输入 `docker-quickstart` 作为仓库名称。

    ![Docker Hub 页面的截图，显示如何创建公共仓库](images/create-hub-repository.webp?border)

4. 将可见性设置为 **Public**。
5. 选择 **Create** 按钮创建仓库。

就这样。您已成功创建了您的第一个仓库。🎉

这个仓库目前是空的。您现在将通过推送镜像来填充它。

### 使用 Docker Desktop 登录

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop（如果尚未安装）。
2. 在 Docker Desktop GUI 中，选择右上角的 **Sign in** 按钮

### 克隆示例 Node.js 代码

为了创建镜像，您首先需要一个项目。为了让您快速入门，您将使用在 [github.com/dockersamples/helloworld-demo-node](https://github.com/dockersamples/helloworld-demo-node) 找到的示例 Node.js 项目。这个仓库包含构建 Docker 镜像所需的预构建 Dockerfile。

不用担心 Dockerfile 的具体内容，您将在后面的章节中学习相关知识。

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
    > 确保在 `docker build` 命令末尾包含点（.）。这告诉 Docker 在哪里找到 Dockerfile。

4. 运行以下命令列出新创建的 Docker 镜像：

    ```console
    docker images
    ```

    您将看到类似以下的输出：

    ```console
    REPOSITORY                                 TAG       IMAGE ID       CREATED         SIZE
    <YOUR_DOCKER_USERNAME>/docker-quickstart   latest    476de364f70e   2 minutes ago   170MB
    ```

5. 通过运行以下命令启动容器来测试镜像（将用户名替换为您自己的用户名）：

    ```console
    docker run -d -p 8080:8080 <YOUR_DOCKER_USERNAME>/docker-quickstart
    ```

    您可以通过在浏览器中访问 [http://localhost:8080](http://localhost:8080) 来验证容器是否正常工作。

6. 使用 [`docker tag`](/reference/cli/docker/image/tag/) 命令为 Docker 镜像添加标签。Docker 标签允许您对镜像进行标记和版本控制。

    ```console
    docker tag <YOUR_DOCKER_USERNAME>/docker-quickstart <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
    ```

7. 最后，是时候使用 [`docker push`](/reference/cli/docker/image/push/) 命令将新构建的镜像推送到您的 Docker Hub 仓库了：

    ```console
    docker push <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
    ```

8. 打开 [Docker Hub](https://hub.docker.com) 并导航到您的仓库。导航到 **Tags** 部分，查看您新推送的镜像。

    ![Docker Hub 页面的截图，显示新添加的镜像标签](images/dockerhub-tags.webp?border=true)

在本实践中，您注册了 Docker 账户，创建了您的第一个 Docker Hub 仓库，并构建、标记和推送了容器镜像到您的 Docker Hub 仓库。

## 其他资源

- [Docker Hub 快速入门](/docker-hub/quickstart/)
- [管理 Docker Hub 仓库](/docker-hub/repos/)

## 后续步骤

现在您了解了容器和镜像的基础知识，您可以开始学习 Docker Compose 了。

{{< button text="什么是 Docker Compose？" url="what-is-Docker-Compose" >}}
