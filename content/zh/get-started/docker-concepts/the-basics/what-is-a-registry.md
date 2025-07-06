---
title: 什么是仓库？
weight: 30
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 什么是仓库？这个 Docker 概念将解释什么是仓库，探讨它们的互操作性，并让您与仓库进行交互。
aliases:
- /guides/walkthroughs/run-hub-images/
- /guides/walkthroughs/publish-your-image/
- /guides/docker-concepts/the-basics/what-is-a-registry/
---

{{< youtube-embed 2WDl10Wv5rs >}}

## 说明

现在您已经知道什么是容器镜像以及它是如何工作的，您可能会想 - 您将这些镜像存储在哪里？

嗯，您可以将容器镜像存储在您的计算机系统上，但是如果您想与朋友分享它们或在另一台机器上使用它们怎么办？这就是镜像仓库的用武之地。

镜像仓库是用于存储和共享容器镜像的集中位置。它可以是公共的也可以是私有的。[Docker Hub](https://hub.docker.com) 是一个任何人都可以使用的公共仓库，也是默认仓库。

虽然 Docker Hub 是一个流行的选择，但如今还有许多其他可用的容器仓库，包括 [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/)、[Azure Container Registry (ACR)](https://azure.microsoft.com/en-in/products/container-registry) 和 [Google Container Registry (GCR)](https://cloud.google.com/artifact-registry)。您甚至可以在本地系统或组织内部运行您的私有仓库。例如，Harbor、JFrog Artifactory、GitLab Container registry 等。

### 仓库与存储库

在使用仓库时，您可能会听到术语 _registry_ 和 _repository_，就好像它们可以互换一样。尽管它们相关，但它们并不完全相同。

_registry_ 是一个存储和管理容器镜像的集中位置，而 _repository_ 是注册表中相关容器镜像的集合。可以把它想象成一个文件夹，您可以在其中根据项目组织镜像。每个存储库包含一个或多个容器镜像。

下图显示了注册表、存储库和镜像之间的关系。

```goat {class="text-sm"}
+---------------------------------------+
|               仓库                |
|---------------------------------------|
|                                       |
|    +-----------------------------+    |
|    |        存储库 A         |    |
|    |-----------------------------|    |
|    |   镜像: project-a:v1.0     |    |
|    |   镜像: project-a:v2.0     |    |
|    +-----------------------------+    |
|                                       |
|    +-----------------------------+    |
|    |        存储库 B         |    |
|    |-----------------------------|    |
|    |   镜像: project-b:v1.0     |    |
|    |   镜像: project-b:v1.1     |    |
|    |   镜像: project-b:v2.0     |    |
|    +-----------------------------+    |
|                                       |
+---------------------------------------+
```

> [!NOTE]
>
> 您可以使用免费版的 Docker Hub 创建一个私有存储库和无限个公共存储库。有关更多信息，请访问 [Docker Hub 订阅页面](https://www.docker.com/pricing/)。

## 动手试试

在这个动手实践中，您将学习如何构建 Docker 镜像并将其推送到 Docker Hub 存储库。

### 注册一个免费的 Docker 帐户

1. 如果您还没有创建，请前往 [Docker Hub](https://hub.docker.com) 页面注册一个新的 Docker 帐户。

    ![显示注册页面的官方 Docker Hub 页面的屏幕截图](images/dockerhub-signup.webp?border)

    您可以使用您的 Google 或 GitHub 帐户进行身份验证。

### 创建您的第一个存储库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择右上角的 **Create repository** 按钮。
3. 选择您的命名空间（很可能是您的用户名）并输入 `docker-quickstart` 作为存储库名称。

    ![显示如何创建公共存储库的 Docker Hub 页面的屏幕截图](images/create-hub-repository.webp?border)

4. 将可见性设置为 **Public**。
5. 选择 **Create** 按钮以创建存储库。

就是这样。您已成功创建了您的第一个存储库。🎉

此存储库现在是空的。您现在将通过向其推送镜像来解决此问题。

### 使用 Docker Desktop 登录

1. 如果尚未安装，请[下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。
2. 在 Docker Desktop GUI 中，选择右上角的 **Sign in** 按钮

### 克隆示例 Node.js 代码

为了创建镜像，您首先需要一个项目。为了让您快速入门，您将使用一个位于 [github.com/dockersamples/helloworld-demo-node](https://github.com/dockersamples/helloworld-demo-node) 的示例 Node.js 项目。此存储库包含构建 Docker 镜像所需的预构建 Dockerfile。

不要担心 Dockerfile 的具体细节，因为您将在后面的部分中学习。

1. 使用以下命令克隆 GitHub 存储库：

    ```console
    git clone https://github.com/dockersamples/helloworld-demo-node
    ```

2. 导航到新创建的目录。

    ```console
    cd helloworld-demo-node
    ```

3. 运行以下命令以构建 Docker 镜像，将 `YOUR_DOCKER_USERNAME` 替换为您的用户名。

    ```console
    docker build -t <YOUR_DOCKER_USERNAME>/docker-quickstart .
    ```

    > [!NOTE]
    >
    > 确保在 `docker build` 命令的末尾包含点 (.)。这会告诉 Docker 在哪里可以找到 Dockerfile。

4. 运行以下命令以列出新创建的 Docker 镜像：

    ```console
    docker images
    ```

    您将看到如下输出：

    ```console
    REPOSITORY                                 TAG       IMAGE ID       CREATED         SIZE
    <YOUR_DOCKER_USERNAME>/docker-quickstart   latest    476de364f70e   2 minutes ago   170MB
    ```

5. 通过运行以下命令启动一个容器来测试镜像（将用户名替换为您自己的用户名）：

    ```console
    docker run -d -p 8080:8080 <YOUR_DOCKER_USERNAME>/docker-quickstart 
    ```

    您可以通过使用浏览器访问 [http://localhost:8080](http://localhost:8080) 来验证容器是否正常工作。

6. 使用 [`docker tag`](/reference/cli/docker/image/tag/) 命令标记 Docker 镜像。Docker 标签允许您标记和版本化您的镜像。

    ```console 
    docker tag <YOUR_DOCKER_USERNAME>/docker-quickstart <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0 
    ```

7. 最后，是时候使用 [`docker push`](/reference/cli/docker/image/push/) 命令将新构建的镜像推送到您的 Docker Hub 存储库了：

    ```console 
    docker push <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
    ```

8. 打开 [Docker Hub](https://hub.docker.com) 并导航到您的存储库。导航到 **Tags** 部分，查看您新推送的镜像。

    ![显示新添加的镜像标签的 Docker Hub 页面的屏幕截图](images/dockerhub-tags.webp?border=true) 

在此演练中，您注册了一个 Docker 帐户，创建了您的第一个 Docker Hub 存储库，并构建、标记和推送了一个容器镜像到您的 Docker Hub 存储库。

## 其他资源

- [Docker Hub 快速入门](/docker-hub/quickstart/)
- [管理 Docker Hub 存储库](/docker-hub/repos/)

## 后续步骤

现在您已经了解了容器和镜像的基础知识，您已准备好学习 Docker Compose。

{{< button text="什么是 Docker Compose？" url="what-is-Docker-Compose" >}}
