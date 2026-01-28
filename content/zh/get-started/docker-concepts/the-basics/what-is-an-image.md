---
title: 什么是镜像？
weight: 20
keywords: concepts, build, images, container, docker desktop
description: 什么是镜像
aliases:
  - /guides/docker-concepts/the-basics/what-is-an-image/
  - /get-started/run-docker-hub-images/
---

{{< youtube-embed NyvT9REqLe4 >}}

## 概念解释

既然[容器](./what-is-a-container.md)是一个隔离的进程，那么它的文件和配置从何而来？您如何共享这些环境？

这就是容器镜像的作用所在。容器镜像是一个标准化的包，包含运行容器所需的所有文件、二进制文件、库和配置。

对于 [PostgreSQL](https://hub.docker.com/_/postgres) 镜像，该镜像将打包数据库二进制文件、配置文件和其他依赖项。对于 Python Web 应用程序，它将包含 Python 运行时、您的应用程序代码及其所有依赖项。

镜像有两个重要原则：

1. 镜像是不可变的。一旦创建了镜像，就无法修改。您只能创建新镜像或在其之上添加更改。

2. 容器镜像由层组成。每一层代表一组添加、删除或修改文件的文件系统更改。

这两个原则使您能够扩展或添加到现有镜像。例如，如果您正在构建 Python 应用程序，可以从 [Python 镜像](https://hub.docker.com/_/python)开始，添加额外的层来安装应用程序的依赖项并添加您的代码。这使您可以专注于您的应用程序，而不是 Python 本身。

### 查找镜像

[Docker Hub](https://hub.docker.com) 是用于存储和分发镜像的默认全球市场。它拥有超过 100,000 个由开发人员创建的镜像，您可以在本地运行。您可以搜索 Docker Hub 镜像并直接从 Docker Desktop 运行它们。

Docker Hub 提供各种 Docker 支持和认可的镜像，称为 Docker 可信内容（Docker Trusted Content）。这些提供完全托管的服务或为您自己的镜像提供出色的起点。包括：

- [Docker 官方镜像](https://hub.docker.com/search?q=&type=image&image_filter=official) - 精选的 Docker 仓库集合，是大多数用户的起点，也是 Docker Hub 上最安全的镜像之一
- [Docker 认证发布者](https://hub.docker.com/search?q=&image_filter=store) - 经 Docker 验证的商业发布者提供的高质量镜像
- [Docker 赞助的开源项目](https://hub.docker.com/search?q=&image_filter=open_source) - 通过 Docker 开源计划由 Docker 赞助的开源项目发布和维护的镜像

例如，[Redis](https://hub.docker.com/_/redis) 和 [Memcached](https://hub.docker.com/_/memcached) 是几个流行的即用型 Docker 官方镜像。您可以下载这些镜像，并在几秒钟内启动这些服务。还有基础镜像，如 [Node.js](https://hub.docker.com/_/node) Docker 镜像，您可以将其用作起点，并添加您自己的文件和配置。

## 动手实践

{{< tabs group=concept-usage persist=true >}}
{{< tab name="Using the GUI" >}}

在本动手实践中，您将学习如何使用 Docker Desktop GUI 搜索和拉取容器镜像。

### 搜索和下载镜像

1. 打开 Docker Desktop 仪表板，在左侧导航菜单中选择 **Images** 视图。

   ![Docker Desktop 仪表板的截图，显示左侧边栏中的镜像视图](images/click-image.webp?border=true&w=1050&h=400)

2. 选择 **Search images to run** 按钮。如果看不到它，请选择屏幕顶部的 _全局搜索栏_。

   ![Docker Desktop 仪表板的截图，显示搜索选项卡](images/search-image.webp?border)

3. 在 **Search** 字段中，输入 "welcome-to-docker"。搜索完成后，选择 `docker/welcome-to-docker` 镜像。

   ![Docker Desktop 仪表板的截图，显示 docker/welcome-to-docker 镜像的搜索结果](images/select-image.webp?border=true&w=1050&h=400)

4. 选择 **Pull** 下载镜像。

### 了解镜像信息

下载镜像后，您可以通过 GUI 或 CLI 了解有关镜像的很多详细信息。

1. 在 Docker Desktop 仪表板中，选择 **Images** 视图。

2. 选择 **docker/welcome-to-docker** 镜像以打开有关该镜像的详细信息。

   ![Docker Desktop 仪表板的截图，显示镜像视图，箭头指向 docker/welcome-to-docker 镜像](images/pulled-image.webp?border=true&w=1050&h=400)

3. 镜像详细信息页面向您展示有关镜像层、镜像中安装的包和库以及任何发现的漏洞的信息。

   ![docker/welcome-to-docker 镜像详细信息视图的截图](images/image-layers.webp?border=true&w=1050&h=400)

{{< /tab >}}

{{< tab name="Using the CLI" >}}

按照说明使用 CLI 搜索和拉取 Docker 镜像以查看其层。

### 搜索和下载镜像

1. 打开终端，使用 [`docker search`](/reference/cli/docker/search.md) 命令搜索镜像：

   ```console
   docker search docker/welcome-to-docker
   ```

   您将看到类似以下的输出：

   ```console
   NAME                       DESCRIPTION                                     STARS     OFFICIAL
   docker/welcome-to-docker   Docker image for new users getting started w…   20
   ```

   此输出显示 Docker Hub 上可用的相关镜像信息。

2. 使用 [`docker pull`](/reference/cli/docker/image/pull.md) 命令拉取镜像。

   ```console
   docker pull docker/welcome-to-docker
   ```

   您将看到类似以下的输出：

   ```console
   Using default tag: latest
   latest: Pulling from docker/welcome-to-docker
   579b34f0a95b: Download complete
   d11a451e6399: Download complete
   1c2214f9937c: Download complete
   b42a2f288f4d: Download complete
   54b19e12c655: Download complete
   1fb28e078240: Download complete
   94be7e780731: Download complete
   89578ce72c35: Download complete
   Digest: sha256:eedaff45e3c78538087bdd9dc7afafac7e110061bbdd836af4104b10f10ab693
   Status: Downloaded newer image for docker/welcome-to-docker:latest
   docker.io/docker/welcome-to-docker:latest
   ```

   每一行代表镜像的一个不同的已下载层。请记住，每一层都是一组文件系统更改，提供镜像的功能。

### 了解镜像信息

1. 使用 [`docker image ls`](/reference/cli/docker/image/ls.md) 命令列出已下载的镜像：

   ```console
   docker image ls
   ```

   您将看到类似以下的输出：

   ```console
   REPOSITORY                 TAG       IMAGE ID       CREATED        SIZE
   docker/welcome-to-docker   latest    eedaff45e3c7   4 months ago   29.7MB
   ```

   该命令显示系统上当前可用的 Docker 镜像列表。`docker/welcome-to-docker` 的总大小约为 29.7MB。

   > **镜像大小**
   >
   > 此处显示的镜像大小反映的是镜像的未压缩大小，而不是层的下载大小。

2. 使用 [`docker image history`](/reference/cli/docker/image/history.md) 命令列出镜像的层：

   ```console
   docker image history docker/welcome-to-docker
   ```

   您将看到类似以下的输出：

   ```console
   IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
   648f93a1ba7d   4 months ago   COPY /app/build /usr/share/nginx/html # buil…   1.6MB     buildkit.dockerfile.v0
   <missing>      5 months ago   /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon…   0B
   <missing>      5 months ago   /bin/sh -c #(nop)  STOPSIGNAL SIGQUIT           0B
   <missing>      5 months ago   /bin/sh -c #(nop)  EXPOSE 80                    0B
   <missing>      5 months ago   /bin/sh -c #(nop)  ENTRYPOINT ["/docker-entr…   0B
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:9e3b2b63db9f8fc7…   4.62kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:57846632accc8975…   3.02kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:3b1b9915b7dd898a…   298B
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:caec368f5a54f70a…   2.12kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:01e75c6dd0ce317d…   1.62kB
   <missing>      5 months ago   /bin/sh -c set -x     && addgroup -g 101 -S …   9.7MB
   <missing>      5 months ago   /bin/sh -c #(nop)  ENV PKG_RELEASE=1            0B
   <missing>      5 months ago   /bin/sh -c #(nop)  ENV NGINX_VERSION=1.25.3     0B
   <missing>      5 months ago   /bin/sh -c #(nop)  LABEL maintainer=NGINX Do…   0B
   <missing>      5 months ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      5 months ago   /bin/sh -c #(nop) ADD file:ff3112828967e8004…   7.66MB
   ```

   此输出显示所有层、它们的大小以及用于创建该层的命令。

   > **查看完整命令**
   >
   > 如果在命令中添加 `--no-trunc` 标志，您将看到完整的命令。请注意，由于输出是表格格式，较长的命令会使输出非常难以浏览。

{{< /tab >}}
{{< /tabs >}}

在本实践中，您搜索并拉取了一个 Docker 镜像。除了拉取 Docker 镜像外，您还了解了 Docker 镜像的层。

## 其他资源

以下资源将帮助您进一步了解探索、查找和构建镜像：

- [Docker 可信内容](/manuals/docker-hub/image-library/trusted-content.md)
- [在 Docker Desktop 中探索镜像视图](/manuals/desktop/use-desktop/images.md)
- [Docker Build 概述](/manuals/build/concepts/overview.md)
- [Docker Hub](https://hub.docker.com)

## 后续步骤

现在您已经了解了镜像的基础知识，是时候学习通过镜像仓库分发镜像了。

{{< button text="什么是镜像仓库？" url="what-is-a-registry" >}}
