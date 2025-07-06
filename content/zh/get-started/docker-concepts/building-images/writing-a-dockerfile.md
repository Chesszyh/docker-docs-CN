---
title: 编写 Dockerfile
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 此概念页面将教您如何使用 Dockerfile 创建镜像。
summary: |
  掌握 Dockerfile 实践对于有效利用容器技术、
  增强应用程序可靠性以及支持 DevOps 和
  CI/CD 方法至关重要。在本指南中，您将学习如何编写 Dockerfile、
  如何定义基础镜像和设置指令，包括软件
  安装和复制必要的文件。
weight: 2
aliases: 
 - /guides/docker-concepts/building-images/writing-a-dockerfile/
---

{{< youtube-embed Jx8zoIhiP4c >}}

## 说明

Dockerfile 是一个基于文本的文档，用于创建容器镜像。它向镜像构建器提供有关要运行的命令、要复制的文件、启动命令等的指令。

例如，以下 Dockerfile 将生成一个可随时运行的 Python 应用程序：

```dockerfile
FROM python:3.12
WORKDIR /usr/local/app

# 安装应用程序依赖项
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src ./src
EXPOSE 5000

# 设置一个应用程序用户，以便容器不以 root 用户身份运行
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 常用指令

`Dockerfile` 中一些最常见的指令包括：

- `FROM <image>` - 这指定了构建将扩展的基础镜像。
- `WORKDIR <path>` - 此指令指定“工作目录”或镜像中将复制文件和执行命令的路径。
- `COPY <host-path> <image-path>` - 此指令告诉构建器从主机复制文件并将其放入容器镜像中。
- `RUN <command>` - 此指令告诉构建器运行指定的命令。
- `ENV <name> <value>` - 此指令设置正在运行的容器将使用的环境变量。
- `EXPOSE <port-number>` - 此指令在镜像上设置配置，指示镜像希望公开的端口。
- `USER <user-or-uid>` - 此指令为所有后续指令设置默认用户。
- `CMD ["<command>", "<arg1>"]` - 此指令设置使用此镜像的容器将运行的默认命令。


要通读所有指令或了解更多详细信息，请查看 [Dockerfile 参考](https://docs.docker.com/engine/reference/builder/)。

## 动手试试

正如您在前面的示例中看到的那样，Dockerfile 通常遵循以下步骤：

1. 确定您的基础镜像
2. 安装应用程序依赖项
3. 复制任何相关的源代码和/或二进制文件
4. 配置最终镜像

在这个快速��动手指南中，您将编写一个构建简单 Node.js 应用程序的 Dockerfile。如果您不熟悉基于 JavaScript 的应用程序，请不要担心。这对于学习本指南不是必需的。

### 设置

[下载此 ZIP 文件](https://github.com/docker/getting-started-todo-app/raw/build-image-from-scratch/app.zip) 并将其内容解压缩到您机器上的一个目录中。

### 创建 Dockerfile

现在您有了项目，就可以创建 `Dockerfile` 了。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 在与 `package.json` 文件相同的文件夹中创建一个名为 `Dockerfile` 的文件。

    > **Dockerfile 文件扩展名**
    >
    > 重要的是要注意 `Dockerfile` *没有* 文件扩展名。一些编辑器
    > 会自动向文件添加扩展名（或抱怨它没有扩展名）。

3. 在 `Dockerfile` 中，通过添加以下行来定义您的基础镜像：

    ```dockerfile
    FROM node:20-alpine
    ```

4. 现在，使用 `WORKDIR` 指令定义工作目录。这将指定将来命令将在何处运行以及文件将复制到容器镜像内的目录。

    ```dockerfile
    WORKDIR /app
    ```

5. 使用 `COPY` 指令将项目中的所有文件从您的机器复制到容器镜像中：

    ```dockerfile
    COPY . .
    ```

6. 使用 `yarn` CLI 和包管理器安装应用程序的依赖项。为此，请使用 `RUN` 指令运行一个命令：

    ```dockerfile
    RUN yarn install --production
    ```

7. 最后，使用 `CMD` 指令指定要运行的默认命令：

    ```dockerfile
    CMD ["node", "./src/index.js"]
    ```
    这样，您应该有以下 Dockerfile：


    ```dockerfile
    FROM node:20-alpine
    WORKDIR /app
    COPY . .
    RUN yarn install --production
    CMD ["node", "./src/index.js"]
    ```

> **此 Dockerfile 尚未准备好用于生产**
>
> 重要的是要注意，此 Dockerfile *尚未* 遵循所有
> 最佳实践（这是设计使然）。它将构建应用程序，但
> 构建速度不会像它们可能的那样快，或者镜像也不会像它们可能的那样安全。
>
> 继续阅读以了解有关如何使镜像最大化
> 构建缓存、以非 root 用户身份运行以及多阶段构建的更多信息。


> **使用 `docker init` 快速容器化新项目**
>
> `docker init` 命令将分析您的项目并快速创建
> 一个 Dockerfile、一个 `compose.yaml` 和一个 `.dockerignore`，帮助您
> 启动并运行。由于您在这里专门学习 Dockerfile，
> 所以现在不会使用它。但是，[在此处了��有关它的更多信息](/engine/reference/commandline/init/)。

## 其他资源

要了解有关编写 Dockerfile 的更多信息，请访问以下资源：

* [Dockerfile 参考](/reference/dockerfile/)
* [Dockerfile 最佳实践](/develop/develop-images/dockerfile_best-practices/)
* [基础镜像](/build/building/base-images/)
* [Docker Init 入门](/reference/cli/docker/init/)

## 后续步骤

现在您已经创建了一个 Dockerfile 并学习了基础知识，是时候学习构建、标记和推送镜像了。

{{< button text="构建、标记和发布镜像" url="build-tag-and-publish-an-image" >}}

