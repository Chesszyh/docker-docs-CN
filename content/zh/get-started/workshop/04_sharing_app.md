---
title: 共享应用程序
weight: 40
linkTitle: "第 3 部分：共享应用程序"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers,
  docker desktop, docker hub, sharing
description: 共享您为示例应用程序构建的镜像，以便您可以在其他地方运行它，并且其他开发人员也可以使用它
aliases:
 - /get-started/part3/
 - /get-started/04_sharing_app/
 - /guides/workshop/04_sharing_app/
---

既然您已经构建了一个镜像，就可以分享它了。要共享 Docker 镜像，您必须使用 Docker 注册表（registry）。默认注册表是 Docker Hub，您使用的所有镜像都来自那里。

> **Docker ID**
>
> Docker ID 允许您访问 Docker Hub，这是世界上最大的容器镜像库和社区。如果您没有 [Docker ID](https://hub.docker.com/signup)，请免费创建一个。

## 创建仓库

要推送镜像，您首先需要在 Docker Hub 上创建一个仓库（repository）。

1. [注册](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade)或登录 [Docker Hub](https://hub.docker.com)。

2. 选择 **Create Repository**（创建仓库）按钮。

3. 对于仓库名称，使用 `getting-started`。确保 **Visibility**（可见性）为 **Public**（公开）。

4. 选择 **Create**（创建）。

在下图中，您可以看到来自 Docker Hub 的示例 Docker 命令。此命令将推送到此仓库。

![Docker command with push example](images/push-command.webp)


## 推送镜像

让我们尝试将镜像推送到 Docker Hub。

1. 在命令行中，运行以下命令：

   ```console
   docker push docker/getting-started
   ```

   您将看到类似如下的错误：

   ```console
   $ docker push docker/getting-started
   The push refers to repository [docker.io/docker/getting-started]
   An image does not exist locally with the tag: docker/getting-started
   ```

   失败是预期的，因为镜像尚未正确标记。
   Docker 正在寻找名为 `docker/getting started` 的镜像，但您的本地镜像仍名为 `getting-started`。

   您可以通过运行以下命令来确认这一点：

   ```console
   docker image ls
   ```

2. 要解决此问题，首先使用您的 Docker ID 登录到 Docker Hub：`docker login YOUR-USER-NAME`。
3. 使用 `docker tag` 命令为 `getting-started` 镜像赋予一个新名称。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker tag getting-started YOUR-USER-NAME/getting-started
   ```

4. 现在再次运行 `docker push` 命令。如果您是从 Docker Hub 复制的值，则可以删除 `tagname` 部分，因为您没有向镜像名称添加标签。如果您不指定标签，Docker 将使用名为 `latest` 的标签。

   ```console
   $ docker push YOUR-USER-NAME/getting-started
   ```

## 在新实例上运行镜像

现在您的镜像已构建并推送到注册表中，请尝试在从未见过此容器镜像的全新实例上运行您的应用程序。为此，您将使用 Play with Docker。

> [!NOTE]
>
> Play with Docker 使用 amd64 平台。如果您使用的是基于 ARM 的 Apple silicon Mac，则需要重建镜像以与 Play with Docker 兼容，并将新镜像推送到您的仓库。
>
> 要为 amd64 平台构建镜像，请使用 `--platform` 标志。
> ```console
> $ docker build --platform linux/amd64 -t YOUR-USER-NAME/getting-started .
> ```
>
> Docker buildx 亦支持构建多平台镜像。要了解更多信息，请参阅 [多平台镜像](/manuals/build/building/multi-platform.md)。


1. 打开浏览器访问 [Play with Docker](https://labs.play-with-docker.com/)。

2. 选择 **Login**（登录），然后从下拉列表中选择 **docker**。

3. 使用您的 Docker Hub 帐户登录，然后选择 **Start**（开始）。

4. 选择左侧边栏上的 **ADD NEW INSTANCE**（添加新实例）选项。如果您没有看到它，请让您的浏览器宽一点。几秒钟后，终端窗口会在您的浏览器中打开。

    ![Play with Docker add new instance](images/pwd-add-new-instance.webp)

5. 在终端中，启动您刚推送的应用程序。

   ```console
   $ docker run -dp 0.0.0.0:3000:3000 YOUR-USER-NAME/getting-started
   ```

    您应该看到镜像被拉取下来并最终启动。

    > [!TIP]
    >
    > 您可能已经注意到，此命令将端口映射绑定到不同的 IP 地址。之前的 `docker run` 命令将端口发布到主机上的 `127.0.0.1:3000`。这一次，您使用的是 `0.0.0.0`。
    >
    > 绑定到 `127.0.0.1` 仅将容器的端口暴露给环回接口。然而，绑定到 `0.0.0.0` 会将容器的端口暴露给主机的所有接口，使其可供外界访问。
    >
    > 有关端口映射工作原理的更多信息，请参阅 [网络](/manuals/engine/network/_index.md#published-ports)。

6. 当 3000 徽章出现时选择它。

   如果 3000 徽章没有出现，您可以选择 **Open Port**（打开端口）并指定 `3000`。

## 总结

在本节中，您学习了如何通过将镜像推送到注册表来共享镜像。然后，您转到一个全新的实例，并能够运行刚刚推送的镜像。这在 CI 管道中非常常见，管道将创建镜像并将其推送到注册表，然后生产环境可以使用最新版本的镜像。

相关信息：

 - [docker CLI 参考](/reference/cli/docker/)
 - [多平台镜像](/manuals/build/building/multi-platform.md)
 - [Docker Hub 概览](/manuals/docker-hub/_index.md)

## 下一步

在下一节中，您将学习如何在容器化应用程序中持久化数据。

{{< button text="持久化数据库" url="05_persisting_data.md" >}}