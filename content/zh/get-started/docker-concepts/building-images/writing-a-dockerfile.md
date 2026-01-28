---
title: 编写 Dockerfile
keywords: concepts, build, images, container, docker desktop
description: 本概念页面将教您如何使用 Dockerfile 创建镜像。
summary: |
  掌握 Dockerfile 实践对于有效利用容器技术、增强应用程序可靠性以及支持 DevOps 和 CI/CD 方法论至关重要。在本指南中，您将学习如何编写 Dockerfile、如何定义基础镜像和设置指令，包括软件安装和复制必要的文件。
weight: 2
aliases:
 - /guides/docker-concepts/building-images/writing-a-dockerfile/
---

{{< youtube-embed Jx8zoIhiP4c >}}

## 概念解释

Dockerfile 是一个基于文本的文档，用于创建容器镜像。它向镜像构建器提供要运行的命令、要复制的文件、启动命令等指令。

例如，以下 Dockerfile 将生成一个可立即运行的 Python 应用程序：

```dockerfile
FROM python:3.12
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 常用指令

`Dockerfile` 中一些最常见的指令包括：

- `FROM <image>` - 指定构建将扩展的基础镜像。
- `WORKDIR <path>` - 此指令指定"工作目录"或镜像中文件将被复制和命令将被执行的路径。
- `COPY <host-path> <image-path>` - 此指令告诉构建器从主机复制文件并将它们放入容器镜像中。
- `RUN <command>` - 此指令告诉构建器运行指定的命令。
- `ENV <name> <value>` - 此指令设置运行中的容器将使用的环境变量。
- `EXPOSE <port-number>` - 此指令在镜像上设置配置，指示镜像希望暴露的端口。
- `USER <user-or-uid>` - 此指令为所有后续指令设置默认用户。
- `CMD ["<command>", "<arg1>"]` - 此指令设置使用此镜像的容器将运行的默认命令。


要阅读所有指令或了解更多详情，请查看 [Dockerfile 参考](https://docs.docker.com/engine/reference/builder/)。

## 动手实践

正如您在前面的示例中看到的，Dockerfile 通常遵循以下步骤：

1. 确定您的基础镜像
2. 安装应用程序依赖项
3. 复制任何相关的源代码和/或二进制文件
4. 配置最终镜像

在这个快速动手指南中，您将编写一个构建简单 Node.js 应用程序的 Dockerfile。如果您不熟悉基于 JavaScript 的应用程序，不用担心。按照本指南操作并不需要这些知识。

### 设置

[下载此 ZIP 文件](https://github.com/docker/getting-started-todo-app/raw/build-image-from-scratch/app.zip)并将内容解压到您机器上的一个目录中。

### 创建 Dockerfile

现在您有了项目，您可以准备创建 `Dockerfile` 了。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 在与 `package.json` 文件相同的文件夹中创建一个名为 `Dockerfile` 的文件。

    > **Dockerfile 文件扩展名**
    >
    > 需要注意的是，`Dockerfile` _没有_ 文件扩展名。某些编辑器会自动向文件添加扩展名（或抱怨它没有扩展名）。

3. 在 `Dockerfile` 中，通过添加以下行来定义您的基础镜像：

    ```dockerfile
    FROM node:20-alpine
    ```

4. 现在，使用 `WORKDIR` 指令定义工作目录。这将指定未来命令将在哪里运行，以及文件将被复制到容器镜像中的哪个目录。

    ```dockerfile
    WORKDIR /app
    ```

5. 使用 `COPY` 指令将项目中的所有文件从您的机器复制到容器镜像中：

    ```dockerfile
    COPY . .
    ```

6. 使用 `yarn` CLI 和包管理器安装应用程序的依赖项。为此，使用 `RUN` 指令运行命令：

    ```dockerfile
    RUN yarn install --production
    ```

7. 最后，使用 `CMD` 指令指定要运行的默认命令：

    ```dockerfile
    CMD ["node", "./src/index.js"]
    ```
    这样，您应该得到以下 Dockerfile：


    ```dockerfile
    FROM node:20-alpine
    WORKDIR /app
    COPY . .
    RUN yarn install --production
    CMD ["node", "./src/index.js"]
    ```

> **此 Dockerfile 还不适合生产环境**
>
> 需要注意的是，此 Dockerfile _尚未_ 遵循所有最佳实践（这是有意为之）。它可以构建应用程序，但构建速度不会那么快，镜像也不会那么安全。
>
> 继续阅读以了解更多关于如何最大化构建缓存、以非 root 用户运行以及多阶段构建的信息。


> **使用 `docker init` 快速容器化新项目**
>
> `docker init` 命令将分析您的项目并快速创建 Dockerfile、`compose.yaml` 和 `.dockerignore`，帮助您快速启动。由于您在这里专门学习 Dockerfile，所以现在不会使用它。但是，[在此处了解更多信息](/engine/reference/commandline/init/)。

## 其他资源

要了解更多关于编写 Dockerfile 的信息，请访问以下资源：

* [Dockerfile 参考](/reference/dockerfile/)
* [Dockerfile 最佳实践](/develop/develop-images/dockerfile_best-practices/)
* [基础镜像](/build/building/base-images/)
* [Docker Init 入门](/reference/cli/docker/init/)

## 后续步骤

现在您已经创建了 Dockerfile 并学习了基础知识，是时候学习构建、标记和推送镜像了。

{{< button text="构建、标记和发布镜像" url="build-tag-and-publish-an-image" >}}
