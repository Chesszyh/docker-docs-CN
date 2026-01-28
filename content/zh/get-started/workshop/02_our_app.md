---
title: 容器化应用程序
weight: 20
linkTitle: "第一部分：容器化应用程序"
keywords: |
  dockerfile example, Containerize an application, run docker file, running
  docker file, how to run dockerfile, example dockerfile, how to create a docker container,
  create dockerfile, simple dockerfile, creating containers, dockerfile 示例, 容器化应用程序, 运行 docker file, 运行 dockerfile, 如何运行 dockerfile, 示例 dockerfile, 如何创建 docker 容器, 创建 dockerfile, 简单 dockerfile, 创建容器
description: |
  按照此分步指南学习如何使用 Docker 创建和运行容器化应用程序
aliases:
  - /get-started/part2/
  - /get-started/02_our_app/
  - /guides/workshop/02_our_app/
  - /guides/walkthroughs/containerize-your-app/
---

在本指南的其余部分，您将使用一个在 Node.js 上运行的简单待办事项列表管理器。如果您不熟悉 Node.js，请不要担心。本指南不需要任何 JavaScript 的先前经验。

## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您已安装 [Git 客户端](https://git-scm.com/downloads)。
- 您有一个 IDE 或文本编辑器来编辑文件。Docker 建议使用 [Visual Studio Code](https://code.visualstudio.com/)。

## 获取应用程序

在运行应用程序之前，您需要将应用程序源代码获取到您的机器上。

1. 使用以下命令克隆 [getting-started-app 仓库](https://github.com/docker/getting-started-app/tree/main)：

   ```console
   $ git clone https://github.com/docker/getting-started-app.git
   ```

2. 查看克隆仓库的内容。您应该看到以下文件和子目录。

   ```text
   ├── getting-started-app/
   │ ├── .dockerignore
   │ ├── package.json
   │ ├── README.md
   │ ├── spec/
   │ ├── src/
   │ └── yarn.lock
   ```

## 构建应用程序的镜像

要构建镜像，您需要使用 Dockerfile。Dockerfile 只是一个没有文件扩展名的基于文本的文件，其中包含指令脚本。Docker 使用此脚本来构建容器镜像。

1. 在 `getting-started-app` 目录中，即 `package.json` 文件所在的同一位置，创建一个名为 `Dockerfile` 的文件，内容如下：

   ```dockerfile
   # syntax=docker/dockerfile:1

   FROM node:lts-alpine
   WORKDIR /app
   COPY . .
   RUN yarn install --production
   CMD ["node", "src/index.js"]
   EXPOSE 3000
   ```

   此 Dockerfile 以 `node:lts-alpine` 基础镜像开始，这是一个轻量级的 Linux 镜像，预装了 Node.js 和 Yarn 包管理器。它将所有源代码复制到镜像中，安装必要的依赖项，并启动应用程序。

2. 使用以下命令构建镜像：

   在终端中，确保您位于 `getting-started-app` 目录中。将 `/path/to/getting-started-app` 替换为您的 `getting-started-app` 目录的路径。

   ```console
   $ cd /path/to/getting-started-app
   ```

   构建镜像。

   ```console
   $ docker build -t getting-started .
   ```

   `docker build` 命令使用 Dockerfile 构建新镜像。您可能已经注意到 Docker 下载了很多“层”。这是因为您指示构建器要从 `node:lts-alpine` 镜像开始。但是，由于您的机器上没有该镜像，Docker 需要下载该镜像。

   Docker 下载镜像后，Dockerfile 中的指令复制了您的应用程序，并使用 `yarn` 安装了应用程序的依赖项。`CMD` 指令指定了从此镜像启动容器时运行的默认命令。

   最后，`-t` 标志标记了您的镜像。将其视为最终镜像的人类可读名称。由于您将镜像命名为 `getting-started`，因此可以在运行容器时引用该镜像。

   `docker build` 命令末尾的 `.` 告诉 Docker 它应该在当前目录中查找 `Dockerfile`。

## 启动应用程序容器

现在您有了一个镜像，可以使用 `docker run` 命令在容器中运行应用程序。

1. 使用 `docker run` 命令运行您的容器并指定您刚刚创建的镜像名称：

   ```console
   $ docker run -d -p 127.0.0.1:3000:3000 getting-started
   ```

   `-d` 标志（`--detach` 的缩写）在后台运行容器。
   这意味着 Docker 启动您的容器并使您返回到终端提示符。此外，它不会在终端中显示日志。

   `-p` 标志（`--publish` 的缩写）在主机和容器之间创建端口映射。`-p` 标志采用 `HOST:CONTAINER` 格式的字符串值，其中 `HOST` 是主机上的地址，`CONTAINER` 是容器上的端口。该命令将容器的端口 3000 发布到主机上的 `127.0.0.1:3000` (`localhost:3000`)。如果没有端口映射，您将无法从主机访问应用程序。

2. 几秒钟后，在您的 Web 浏览器中打开 [http://localhost:3000](http://localhost:3000)。
   您应该会看到您的应用程序。

   ![空待办事项列表](images/todo-list-empty.webp)

3. 添加一两个项目，看看它是否按预期工作。您可以将项目标记为完成并将其删除。您的前端已成功将项目存储在后端。

此时，您有一个正在运行的待办事项列表管理器，其中包含一些项目。

如果您快速查看一下您的容器，应该会看到至少有一个容器正在运行，它使用 `getting-started` 镜像并位于端口 `3000` 上。要查看您的容器，可以使用 CLI 或 Docker Desktop 的图形界面。

{{< tabs >}}
{{< tab name="CLI" >}}

在终端中运行 `docker ps` 命令以列出您的容器。

```console
$ docker ps
```

应该会出现类似以下的输出。

```console
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
df784548666d        getting-started     "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes        127.0.0.1:3000->3000/tcp   priceless_mcclintock
```

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

在 Docker Desktop 中，选择 **Containers**（容器）选项卡以查看您的容器列表。

![Docker Desktop 中运行着 get-started 容器](images/dashboard-two-containers.webp)

{{< /tab >}}
{{< /tabs >}}

## 总结

在本节中，您了解了有关创建 Dockerfile 以构建镜像的基础知识。构建镜像后，您启动了一个容器并看到了正在运行的应用程序。

相关信息：

- [Dockerfile 参考](/reference/dockerfile/)
- [docker CLI 参考](/reference/cli/docker/)

## 下一步

接下来，您将对应用程序进行修改，并学习如何使用新镜像更新正在运行的应用程序。在此过程中，您将学习其他一些有用的命令。

{{< button text="更新应用程序" url="03_updating_app.md" >}}
