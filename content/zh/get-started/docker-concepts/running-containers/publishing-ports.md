---
title: 发布并公开端口
keywords: concepts, build, images, container, docker desktop, 概念, 构建, 镜像, 容器
description: 此概念页面将向您介绍 Docker 中发布和公开端口的重要性
weight: 1
aliases: 
 - /guides/docker-concepts/running-containers/publishing-ports/
---

{{< youtube-embed 9JnqOmJ96ds >}}

## 解释

如果您一直关注本指南，就会明白容器为您应用程序的每个组件提供了隔离的进程。每个组件——React 前端、Python API 和 Postgres 数据库——都在其各自的沙盒环境中运行，与您主机机器上的其他一切完全隔离。这种隔离对于安全和管理依赖项非常有用，但也意味着您无法直接访问它们。例如，您无法在浏览器中访问该 Web 应用程序。

这就是端口发布 (port publishing) 的用武之地。

### 发布端口

发布端口通过建立转发规则提供了突破一点网络隔离的能力。例如，您可以指定将发往主机端口 `8080` 的请求转发到容器的端口 `80`。发布端口发生在创建容器期间，在 `docker run` 中使用 `-p`（或 `--publish`）标志。语法为：

```console
$ docker run -d -p HOST_PORT:CONTAINER_PORT nginx
```

- `HOST_PORT`：您希望在主机机器上接收流量的端口号
- `CONTAINER_PORT`：容器内正在监听连接的端口号

例如，要将容器的端口 `80` 发布到主机端口 `8080`：

```console
$ docker run -d -p 8080:80 nginx
```

现在，发送到主机机器端口 `8080` 的任何流量都将被转发到容器内的端口 `80`。

> [!IMPORTANT]
>
> 默认情况下，端口发布后会发布到所有网络接口。这意味着任何能够到达您机器的流量都可以访问已发布的应用程序。在发布数据库或任何敏感信息时请务必小心。[在此处了解有关已发布端口的更多信息](/engine/network/#published-ports)。

### 发布到临时端口

有时，您可能只想发布端口，但不在乎使用哪个主机端口。在这些情况下，您可以让 Docker 为您选择端口。为此，只需省略 `HOST_PORT` 配置即可。

例如，以下命令将容器的端口 `80` 发布到主机上的一个临时端口 (ephemeral port)：

```console
$ docker run -p 80 nginx
```
 
容器运行后，使用 `docker ps` 将显示所选的端口：

```console
docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                    NAMES
a527355c9c53   nginx         "/docker-entrypoint.…"   4 seconds ago    Up 3 seconds    0.0.0.0:54772->80/tcp    romantic_williamson
```

在这个例子中，应用程序在主机的 `54772` 端口暴露。

### 发布所有端口

创建容器镜像时，使用 `EXPOSE` 指令来指示打包的应用程序将使用指定的端口。这些端口默认情况下不会被发布。

使用 `-P` 或 `--publish-all` 标志，您可以自动将所有公开的端口发布到临时端口。这在您尝试避免开发或测试环境中的端口冲突时非常有用。

例如，以下命令将发布镜像配置的所有公开端口：

```console
$ docker run -P nginx
```

## 试一试

在本实践指南中，您将学习如何使用命令行和 Docker Compose 来发布容器端口以部署 Web 应用程序。

### 使用 Docker 命令行

在此步骤中，您将使用 Docker 命令行运行一个容器并发布其端口。

1. [下载并安装](/get-started/get-docker/) Docker Desktop。

2. 在终端中运行以下命令以启动一个新容器：

    ```console
    $ docker run -d -p 8080:80 docker/welcome-to-docker
    ```

    第一个 `8080` 指的是主机端口。这是您本地机器上用于访问容器内运行的应用程序的端口。第二个 `80` 指的是容器端口。这是容器内应用程序监听传入连接的端口。因此，该命令将主机的 `8080` 端口绑定到容器系统的 `80` 端口。

3. 通过转到 Docker Desktop Dashboard 的 **Containers**（容器）视图来验证已发布的端口。

   ![Docker Desktop Dashboard 截图，显示已发布的端口](images/published-ports.webp?w=5000&border=true)

4. 通过选择容器 **Port(s)** 列中的链接或在浏览器中访问 [http://localhost:8080](http://localhost:8080) 来打开网站。

   ![在容器中运行的 Nginx Web 服务器着陆页截图](/get-started/docker-concepts/the-basics/images/access-the-frontend.webp?border=true)


### 使用 Docker Compose

此示例将使用 Docker Compose 启动相同的应用程序：

1. 创建一个新目录，并在该目录内创建一个具有以下内容的 `compose.yaml` 文件：

    ```yaml
    services:
      app:
        image: docker/welcome-to-docker
        ports:
          - 8080:80
    ```

    `ports` 配置接受几种不同形式的端口定义语法。在这种情况下，您使用的是在 `docker run` 命令中使用的相同 `HOST_PORT:CONTAINER_PORT`。

2. 打开终端并导航到您在上一步中创建的目录。

3. 使用 `docker compose up` 命令启动应用程序。

4. 打开浏览器并访问 [http://localhost:8080](http://localhost:8080)。

## 其他资源

如果您想更深入地了解此主题，请务必查看以下资源：

* [`docker container port` 命令行参考](/reference/cli/docker/container/port/)
* [已发布端口](/engine/network/#published-ports)

## 下一步

现在您已经了解了如何发布和公开端口，您可以开始学习如何使用 `docker run` 命令来覆盖容器默认值了。

{{< button text="覆盖容器默认值" url="overriding-container-defaults" >}}
