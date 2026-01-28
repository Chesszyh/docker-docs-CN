---
title: Dockerfile 概述
weight: 20
description: 了解 Dockerfile 以及如何将它们与 Docker 镜像一起使用来构建和打包您的软件
keywords: build, buildx, buildkit, getting started, dockerfile
aliases:
- /build/hellobuild/
- /build/building/packaging/
---

## Dockerfile

一切从 Dockerfile 开始。

Docker 通过读取 Dockerfile 中的指令来构建镜像。Dockerfile 是一个包含构建源代码指令的文本文件。Dockerfile 指令语法由 [Dockerfile 参考](/reference/dockerfile.md) 中的规范定义。

以下是最常见的指令类型：

| 指令                                                        | 描述                                                                                                                                                                                              |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`FROM <image>`](/reference/dockerfile.md#from)           | 定义镜像的基础。                                                                                                                                                                           |
| [`RUN <command>`](/reference/dockerfile.md#run)           | 在当前镜像之上的新层中执行任何命令并提交结果。`RUN` 还有一个 shell 形式用于运行命令。                                                               |
| [`WORKDIR <directory>`](/reference/dockerfile.md#workdir) | 为 Dockerfile 中后续的 `RUN`、`CMD`、`ENTRYPOINT`、`COPY` 和 `ADD` 指令设置工作目录。                                                                          |
| [`COPY <src> <dest>`](/reference/dockerfile.md#copy)      | 从 `<src>` 复制新文件或目录，并将它们添加到容器文件系统的 `<dest>` 路径中。                                                                                      |
| [`CMD <command>`](/reference/dockerfile.md#cmd)           | 允许您定义基于此镜像启动容器后运行的默认程序。每个 Dockerfile 只有一个 `CMD`，当存在多个时，只有最后一个 `CMD` 实例会生效。 |

Dockerfile 是镜像构建的关键输入，可以根据您的独特配置实现自动化的多层镜像构建。Dockerfile 可以从简单开始，随着您的需求增长以支持更复杂的场景。

### 文件名

Dockerfile 使用的默认文件名是 `Dockerfile`，没有文件扩展名。使用默认名称允许您运行 `docker build` 命令而无需指定额外的命令标志。

某些项目可能需要针对特定目的使用不同的 Dockerfile。一个常见的约定是将这些文件命名为 `<something>.Dockerfile`。您可以使用 `docker build` 命令的 `--file` 标志指定 Dockerfile 文件名。请参阅 [`docker build` CLI 参考](/reference/cli/docker/buildx/build.md#file) 了解 `--file` 标志的信息。

> [!NOTE]
>
> 我们建议为项目的主要 Dockerfile 使用默认名称 (`Dockerfile`)。

## Docker 镜像

Docker 镜像由层组成。每个层是 Dockerfile 中构建指令的结果。层按顺序堆叠，每个层都是表示应用于前一层的更改的增量。

### 示例

以下是使用 Docker 构建应用程序的典型工作流程。

以下示例代码显示了一个使用 Flask 框架用 Python 编写的小型 "Hello World" 应用程序。

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

为了在没有 Docker Build 的情况下发布和部署此应用程序，您需要确保：

- 服务器上安装了所需的运行时依赖项
- Python 代码上传到服务器的文件系统
- 服务器使用必要的参数启动您的应用程序

以下 Dockerfile 创建一个容器镜像，其中安装了所有依赖项并自动启动您的应用程序。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==3.0.*

# install app
COPY hello.py /

# final configuration
ENV FLASK_APP=hello
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

以下是此 Dockerfile 的功能分解：

- [Dockerfile 语法](#dockerfile-syntax)
- [基础镜像](#base-image)
- [环境设置](#environment-setup)
- [注释](#comments)
- [安装依赖项](#installing-dependencies)
- [复制文件](#copying-files)
- [设置环境变量](#setting-environment-variables)
- [暴露端口](#exposed-ports)
- [启动应用程序](#starting-the-application)

### Dockerfile 语法 {#dockerfile-syntax}

添加到 Dockerfile 的第一行是 [`# syntax` 解析器指令](/reference/dockerfile.md#syntax)。虽然这是可选的，但此指令指示 Docker 构建器在解析 Dockerfile 时使用什么语法，并允许[启用了 BuildKit](../buildkit/_index.md#getting-started) 的旧版 Docker 在开始构建之前使用特定的 [Dockerfile 前端](../buildkit/frontend.md)。[解析器指令](/reference/dockerfile.md#parser-directives) 必须出现在 Dockerfile 中任何其他注释、空白或 Dockerfile 指令之前，并且应该是 Dockerfile 的第一行。

```dockerfile
# syntax=docker/dockerfile:1
```

> [!TIP]
>
> 我们建议使用 `docker/dockerfile:1`，它始终指向版本 1 语法的最新版本。BuildKit 在构建之前会自动检查语法更新，确保您使用的是最新版本。

### 基础镜像 {#base-image}

语法指令之后的行定义要使用的基础镜像：

```dockerfile
FROM ubuntu:22.04
```

[`FROM` 指令](/reference/dockerfile.md#from) 将您的基础镜像设置为 Ubuntu 的 22.04 版本。后续的所有指令都在此基础镜像中执行：即 Ubuntu 环境。`ubuntu:22.04` 表示法遵循命名 Docker 镜像的 `name:tag` 标准。当您构建镜像时，您使用此表示法来命名您的镜像。有许多公共镜像可以在项目中使用，通过使用 Dockerfile 的 `FROM` 指令将它们导入到构建步骤中。

[Docker Hub](https://hub.docker.com/search?image_filter=official&q=&type=image) 包含大量可用于此目的的官方镜像。

### 环境设置 {#environment-setup}

以下行在基础镜像中执行构建命令。

```dockerfile
# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
```

此 [`RUN` 指令](/reference/dockerfile.md#run) 在 Ubuntu 中执行 shell，更新 APT 包索引并在容器中安装 Python 工具。

### 注释 {#comments}

请注意 `# install app dependencies` 行。这是一个注释。Dockerfile 中的注释以 `#` 符号开头。随着 Dockerfile 的发展，注释对于为文件的任何未来读者和编辑者（包括未来的您自己！）记录 Dockerfile 的工作方式非常有帮助。

> [!NOTE]
>
> 您可能已经注意到注释使用与文件第一行的[语法指令](#dockerfile-syntax)相同的符号。只有当模式与指令匹配并出现在 Dockerfile 开头时，该符号才被解释为指令。否则，它被视为注释。

### 安装依赖项 {#installing-dependencies}

第二个 `RUN` 指令安装 Python 应用程序所需的 `flask` 依赖项。

```dockerfile
RUN pip install flask==3.0.*
```

此指令的前提是 `pip` 已安装到构建容器中。第一个 `RUN` 命令安装了 `pip`，这确保我们可以使用该命令安装 flask Web 框架。

### 复制文件 {#copying-files}

下一个指令使用 [`COPY` 指令](/reference/dockerfile.md#copy) 将本地构建上下文中的 `hello.py` 文件复制到镜像的根目录。

```dockerfile
COPY hello.py /
```

[构建上下文](./context.md)是您可以在 `COPY` 和 `ADD` 等 Dockerfile 指令中访问的文件集合。

在 `COPY` 指令之后，`hello.py` 文件被添加到构建容器的文件系统中。

### 设置环境变量 {#setting-environment-variables}

如果您的应用程序使用环境变量，您可以使用 [`ENV` 指令](/reference/dockerfile.md#env) 在 Docker 构建中设置环境变量。

```dockerfile
ENV FLASK_APP=hello
```

这设置了一个我们稍后需要的 Linux 环境变量。Flask（本示例中使用的框架）使用此变量来启动应用程序。没有这个，flask 不知道在哪里找到我们的应用程序以便能够运行它。

### 暴露端口 {#exposed-ports}

[`EXPOSE` 指令](/reference/dockerfile.md#expose) 标记我们的最终镜像有一个服务在端口 `8000` 上监听。

```dockerfile
EXPOSE 8000
```

此指令不是必需的，但它是一个好的实践，有助于工具和团队成员了解此应用程序在做什么。

### 启动应用程序 {#starting-the-application}

最后，[`CMD` 指令](/reference/dockerfile.md#cmd) 设置用户基于此镜像启动容器时运行的命令。

```dockerfile
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

此命令启动 flask 开发服务器，在端口 `8000` 上监听所有地址。这里的示例使用 `CMD` 的 "exec form" 版本。也可以使用 "shell form"：

```dockerfile
CMD flask run --host 0.0.0.0 --port 8000
```

这两个版本之间存在微妙的差异，例如它们如何捕获 `SIGTERM` 和 `SIGKILL` 等信号。有关这些差异的更多信息，请参阅 [Shell 和 exec 形式](/reference/dockerfile.md#shell-and-exec-form)

## 构建

要使用[上一节](#example)中的 Dockerfile 示例构建容器镜像，请使用 `docker build` 命令：

```console
$ docker build -t test:latest .
```

`-t test:latest` 选项指定镜像的名称和标签。

命令末尾的单个点 (`.`) 将[构建上下文](./context.md)设置为当前目录。这意味着构建期望在调用命令的目录中找到 Dockerfile 和 `hello.py` 文件。如果这些文件不在那里，构建将失败。

镜像构建完成后，您可以使用 `docker run` 将应用程序作为容器运行，指定镜像名称：

```console
$ docker run -p 127.0.0.1:8000:8000 test:latest
```

这会将容器的端口 8000 发布到 Docker 主机上的 `http://localhost:8000`。

> [!TIP]
>
> 想要在 VS Code 中获得更好的 Dockerfile 编辑体验吗？
> 查看 [Docker VS Code 扩展（Beta）](https://marketplace.visualstudio.com/items?itemName=docker.docker)，它提供代码检查、代码导航和漏洞扫描功能。
