---
title: 构建、标记和发布镜像
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 此概念页面将教您如何构建、标记和发布镜像到 Docker Hub 或任何其他仓库
summary: |
  构建、标记和发布 Docker 镜像是
  容器化工作流程中的关键步骤。在本指南中，您将学习如何创建 Docker
  镜像、如何使用唯一标识符标记这些镜像以及如何将
  您的镜像发布到公共仓库。
weight: 3
aliases: 
 - /guides/docker-concepts/building-images/build-tag-and-publish-an-image/
---

{{< youtube-embed chiiGLlYRlY >}}

## 说明

在本指南中，您将学习以下内容：

- 构建镜像 - 基于 `Dockerfile` 构建镜像的过程
- 标记镜像 - 为镜像命名的过程，这也决定了镜像可以分发到哪里
- 发布镜像 - 使用容器仓库分发或共享新创建的镜像的过程

### 构建镜像

大多数情况下，镜像是使用 Dockerfile 构建的。最基本的 `docker build` 命令可能如下所示：

```bash
docker build .
```

命��中的最后一个 `.` 提供了[构建上下文](https://docs.docker.com/build/concepts/context/#what-is-a-build-context)的路径或 URL。在此位置，构建器将找到 `Dockerfile` 和其他引用的文件。

当您运行构建时，构建器会根据需要拉取基础镜像，然后运行 Dockerfile 中指定的指令。

使用前面的命令，镜像将没有名称，但输出将提供镜像的 ID。例如，前面的命令可能会产生以下输出：

```console
$ docker build .
[+] Building 3.5s (11/11) FINISHED                                              docker:desktop-linux
 => [internal] load build definition from Dockerfile                                            0.0s
 => => transferring dockerfile: 308B                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3.12                                  0.0s
 => [internal] load .dockerignore                                                               0.0s
 => => transferring context: 2B                                                                 0.0s
 => [1/6] FROM docker.io/library/python:3.12                                                    0.0s
 => [internal] load build context                                                               0.0s
 => => transferring context: 123B                                                               0.0s
 => [2/6] WORKDIR /usr/local/app                                                                0.0s
 => [3/6] RUN useradd app                                                                       0.1s
 => [4/6] COPY ./requirements.txt ./requirements.txt                                            0.0s
 => [5/6] RUN pip install --no-cache-dir --upgrade -r requirements.txt                          3.2s
 => [6/6] COPY ./app ./app                                                                      0.0s
 => exporting to image                                                                          0.1s
 => => exporting layers                                                                         0.1s
 => => writing image sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00    0.0s
```

使用前面的输出，您可以使用引用的镜像启动一个容器：

```console
docker run sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00
```

这个名字当然不好记，这就是标记变得有用的地方。


### 标记镜像

标记镜像是为镜像提供一个好记的名称的方法。但是，镜像的名称有一个结构。一个完整的镜像名称具有以下结构：

```text
[HOST[:PORT_NUMBER]/]PATH[:TAG]
```

- `HOST`：镜像所在的可选仓库主机名。如果未指定主机，则默认使用 Docker 的公共仓库 `docker.io`。
- `PORT_NUMBER`：如果提供了主机名，则为仓库端口号
- `PATH`：镜像的路径，由斜杠分隔的组件组成。对于 Docker Hub，格式遵循 `[NAMESPACE/]REPOSITORY`，其中命名空间是用户或组织的名称。如果未指定命名空间，则使用 `library`，这是 Docker 官方镜像的命名空间。
- `TAG`：一个自定义的、人类可读的标识符，通常用于识别镜像的不同版本或变体。如果未指定标签，则默认使用 `latest`。

一些镜像名称的示例如下：

- `nginx`，等同于 `docker.io/library/nginx:latest`：这将从 `docker.io` 仓库、`library` 命名空间、`nginx` 镜像存储库和 `latest` 标签中拉取一个镜像。
- `docker/welcome-to-docker`，等同于 `docker.io/docker/welcome-to-docker:latest`：这将从 `docker.io` 仓库、`docker` 命名空间、`welcome-to-docker` 镜像存储库和 `latest` 标签中拉取一个镜像
- `ghcr.io/dockersamples/example-voting-app-vote:pr-311`：这将从 GitHub 容器仓库、`dockersamples` 命名空间、`example-voting-app-vote` 镜像存储库和 `pr-311` 标签中拉取一个镜像

要在构建期间标���镜像，请添加 `-t` 或 `--tag` 标志：

```console
docker build -t my-username/my-image .
```

如果您已经构建了一个镜像，您可以使用 [`docker image tag`](https://docs.docker.com/engine/reference/commandline/image_tag/) 命令为镜像添加另一个标签：

```console
docker image tag my-username/my-image another-username/another-image:v1
```

### 发布镜像

一旦您构建并标记了镜像，就可以将其推送到仓库了。为此，请使用 [`docker push`](https://docs.docker.com/engine/reference/commandline/image_push/) 命令：

```console
docker push my-username/my-image
```

几秒钟之内，您镜像的所有层都将被推送到仓库。

> **需要身份验证**
>
> 在您能够将镜像推送到存储库之前，您需要进行身份验证。
> 为此，只需使用 [docker login](https://docs.docker.com/engine/reference/commandline/login/) 命令。
{ .information }

## 动手试试

在这个动手指南中，您将使用提供的 Dockerfile 构建一个简单的镜像并将其推送到 Docker Hub。

### 设置

1. 获取示例应用程序。

   如果您有 Git，您可以克隆示例应用程序的存储库。否则，您可以下载示例应用程序。选择以下选项之一。

   {{< tabs >}}
   {{< tab name="使用 git 克���" >}}

   在终端中使用以下命令克隆示例应用程序存储库。

   ```console
   $ git clone https://github.com/docker/getting-started-todo-app
   ```
   {{< /tab >}}
   {{< tab name="下载" >}}

   下载源代码并解压缩。

   {{< button url="https://github.com/docker/getting-started-todo-app/raw/cd61f824da7a614a8298db503eed6630eeee33a3/app.zip" text="下载源代码" >}}

   {{< /tab >}}
   {{< /tabs >}}


2. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

3. 如果您还没有 Docker 帐户，[立即创建一个](https://hub.docker.com/)。完成后，使用该帐户登录 Docker Desktop。


### 构建镜像

现在您在 Docker Hub 上有了一个存储库，是时候构建一个镜像并将其推送到该存储库了。

1. 在示例应用程序存储库的根目录下的终端中，运行以下命令。将 `YOUR_DOCKER_USERNAME` 替换为您的 Docker Hub 用户名：

    ```console
    $ docker build -t <YOUR_DOCKER_USERNAME>/concepts-build-image-demo .
    ```

    例如，如果您的用户名是 `mobywhale`，您将运行以下命令：

    ```console
    $ docker build -t mobywhale/concepts-build-image-demo .
    ```

2. 构建完成后，您可以使用以下命令查看���像：

    ```console
    $ docker image ls
    ```

    该命令将产生类似于以下内容的输出：

    ```plaintext
    REPOSITORY                             TAG       IMAGE ID       CREATED          SIZE
    mobywhale/concepts-build-image-demo    latest    746c7e06537f   24 seconds ago   354MB
    ```

3. 您实际上可以使用 [docker image history](/reference/cli/docker/image/history/) 命令查看历史记录（或镜像是如何创建的）：

    ```console
    $ docker image history mobywhale/concepts-build-image-demo
    ```

    然后您将看到类似于以下内容的输出：

    ```plaintext
    IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
    f279389d5f01   8 seconds ago   CMD ["node" "./src/index.js"]                   0B        buildkit.dockerfile.v0
    <missing>      8 seconds ago   EXPOSE map[3000/tcp:{}]                         0B        buildkit.dockerfile.v0 
    <missing>      8 seconds ago   WORKDIR /app                                    8.19kB    buildkit.dockerfile.v0
    <missing>      4 days ago      /bin/sh -c #(nop)  CMD ["node"]                 0B
    <missing>      4 days ago      /bin/sh -c #(nop)  ENTRYPOINT ["docker-entry…   0B
    <missing>      4 days ago      /bin/sh -c #(nop) COPY file:4d192565a7220e13…   20.5kB
    <missing>      4 days ago      /bin/sh -c apk add --no-cache --virtual .bui…   7.92MB
    <missing>      4 days ago      /bin/sh -c #(nop)  ENV YARN_VERSION=1.22.19     0B
    <missing>      4 days ago      /bin/sh -c addgroup -g 1000 node     && addu…   126MB
    <missing>      4 days ago      /bin/sh -c #(nop)  ENV NODE_VERSION=20.12.0     0B
    <missing>      2 months ago    /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
    <missing>      2 months ago    /bin/sh -c #(nop) ADD file:d0764a717d1e9d0af…   8.42MB
    ```

    此输出显示了镜像的层，突出显示了您添加的层和从基础镜像继承的层。

### 推送镜像

现在您已经构建了一个镜像，是时候将镜像推送到仓库了。

1. 使用 [docker push](/reference/cli/docker/image/push/) 命令推送镜像：

    ```console
    $ docker push <YOUR_DOCKER_USERNAME>/concepts-build-image-demo
    ```

    如果您收到 `requested access to the resource is denied`，请确保您已登录并且您的 Docker 用户名在镜像标签中是正确的。

    稍后，您的镜像应该会被推送到 Docker Hub。

## 其他资源

要了解有关构建、标记和发布镜像的更多信息，请访问以下资源：

* [什么是构建上下文？](/build/concepts/context/#what-is-a-build-context)
* [docker build 参考](/engine/reference/commandline/image_build/)
* [docker image tag 参考](/engine/reference/commandline/image_tag/)
* [docker push 参考](/engine/reference/commandline/image_push/)
* [什么是仓库？](/get-started/docker-concepts/the-basics/what-is-a-registry/)

## 后续步骤

现在您已经了解了构建和发布镜像，是时候学习如何使用 Docker 构建缓存来加快构建过程了。

{{< button text="使用构建缓存" url="using-the-build-cache" >}}


