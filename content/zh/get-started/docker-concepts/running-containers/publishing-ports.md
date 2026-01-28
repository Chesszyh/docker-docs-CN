---
title: 发布和暴露端口
keywords: concepts, build, images, container, docker desktop
description: 此概念页面将教您在 Docker 中发布和暴露端口的重要性
weight: 1
aliases: 
 - /guides/docker-concepts/running-containers/publishing-ports/
---

{{< youtube-embed 9JnqOmJ96ds >}}

## 说明

如果您一直关注本指南，您就会明白容器为应用程序的每个组件提供了隔离的进程。每个组件——React 前端、Python API 和 Postgres 数据库——都在其自己的沙盒环境中运行，与主机上的其他所有内容完全隔离。这种隔离非常适合安全性和管理依赖项，但也意味着您无法直接访问它们。例如，您无法在浏览器中访问 Web 应用程序。

这就是端口发布（port publishing）发挥作用的地方。

### 发布端口

发布端口提供了通过设置转发规则来突破一点网络隔离的能力。例如，您可以指示将主机端口 `8080` 上的请求转发到容器的端口 `80`。发布端口发生在容器创建期间，使用 `docker run` 的 `-p`（或 `--publish`）标志。语法是：

```console
$ docker run -d -p HOST_PORT:CONTAINER_PORT nginx
```

- `HOST_PORT`: 您希望在主机上接收流量的端口号
- `CONTAINER_PORT`: 容器内正在侦听连接的端口号

例如，要将容器的端口 `80` 发布到主机端口 `8080`：

```console
$ docker run -d -p 8080:80 nginx
```

现在，发送到主机端口 `8080` 的任何流量都将转发到容器内的端口 `80`。

> [!IMPORTANT]
>
> 当端口发布时，默认情况下它会发布到所有网络接口。这意味着任何可以访问您机器的流量都可以访问已发布的应用程序。请注意发布数据库或任何敏感信息。[在此处了解有关已发布端口的更多信息](/engine/network/#published-ports)。

### 发布到临时端口

有时，您可能只想发布端口，但不关心使用哪个主机端口。在这些情况下，您可以让 Docker 为您选择端口。为此，只需省略 `HOST_PORT` 配置。

例如，以下命令会将容器的端口 `80` 发布到主机上的临时端口：

```console
$ docker run -p 80 nginx
```
 
容器运行后，使用 `docker ps` 将显示所选端口：

```console
docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                    NAMES
a527355c9c53   nginx         "/docker-entrypoint.…"   4 seconds ago    Up 3 seconds    0.0.0.0:54772->80/tcp    romantic_williamson
```

在此示例中，应用程序暴露在主机的端口 `54772` 上。

### 发布所有端口

创建容器镜像时，`EXPOSE` 指令用于指示打包的应用程序将使用指定的端口。默认情况下不发布这些端口。

使用 `-P` 或 `--publish-all` 标志，您可以自动将所有暴露的端口发布到临时端口。当您试图避免开发或测试环境中的端口冲突时，这非常有用。

例如，以下命令将发布镜像配置的所有暴露端口：

```console
$ docker run -P nginx
```

## 试一试

在这个动手指南中，您将学习如何使用 CLI 和 Docker Compose 发布容器端口以部署 Web 应用程序。

### 使用 Docker CLI

在此步骤中，您将运行一个容器并使用 Docker CLI 发布其端口。

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 在终端中，运行以下命令以启动一个新容器：

    ```console
    $ docker run -d -p 8080:80 docker/welcome-to-docker
    ```

    第一个 `8080` 指的是主机端口。这是您本地机器上用于访问容器内运行的应用程序的端口。第二个 `80` 指的是容器端口。这是容器内的应用程序侦听传入连接的端口。因此，该命令将主机的端口 `8080` 绑定到容器系统的端口 `80`。

3. 通过转到 Docker Desktop Dashboard 的 **Containers** 视图来验证已发布的端口。

   ![A screenshot of Docker Desktop Dashboard showing the published port](images/published-ports.webp?w=5000&border=true)

4. 通过选择容器 **Port(s)** 列中的链接或在浏览器中访问 [http://localhost:8080](http://localhost:8080) 来打开网站。

   ![A screenshot of the landing page of the Nginx web server running in a container](/get-started/docker-concepts/the-basics/images/access-the-frontend.webp?border=true)


### 使用 Docker Compose

此示例将使用 Docker Compose 启动相同的应用程序：

1. 创建一个新目录，并在该目录中创建一个包含以下内容的 `compose.yml` 文件：

    ```yaml
    services:
      app:
        image: docker/welcome-to-docker
        ports:
          - 8080:80
    ```

    `ports` 配置接受几种不同形式的端口定义语法。在这种情况下，您使用的是与 `docker run` 命令中相同的 `HOST_PORT:CONTAINER_PORT`。

2. 打开终端并导航到您在上一步中创建的目录。

3. 使用 `docker compose up` 命令启动应用程序。

4. 打开浏览器访问 [http://localhost:8080](http://localhost:8080)。

## 其他资源

如果您想深入了解此主题，请务必查看以下资源：

* [`docker container port` CLI 参考](/reference/cli/docker/container/port/)
* [已发布端口](/engine/network/#published-ports)

## 下一步

既然您已了解如何发布和暴露端口，是时候学习如何使用 `docker run` 命令覆盖容器默认值了。

{{< button text="覆盖容器默认值" url="overriding-container-defaults" >}}