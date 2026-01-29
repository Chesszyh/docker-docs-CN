---
title: Dockerfile 概览
weight: 20
description: 了解 Dockerfile 以及如何将其与 Docker 镜像配合使用来构建和打包您的软件
keywords: build, buildx, buildkit, 入门, dockerfile
---

## Dockerfile

这一切都始于 Dockerfile。

Docker 通过读取 Dockerfile 中的指令来构建镜像。Dockerfile 是一个文本文件，包含构建源代码所需的指令。Dockerfile 指令语法在 [Dockerfile 参考](/reference/dockerfile.md) 规范中定义。

以下是最常见的指令类型：

| 指令 | 描述 |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`FROM <镜像>`](/reference/dockerfile.md#from)           | 为您的镜像定义基础。                                                                                                                                                                           |
| [`RUN <命令>`](/reference/dockerfile.md#run)           | 在当前镜像顶部的层中执行任何命令，并提交结果。`RUN` 也有一个用于运行命令的 shell 形式。                                                               |
| [`WORKDIR <目录>`](/reference/dockerfile.md#workdir) | 为 Dockerfile 中其后的任何 `RUN`、`CMD`、`ENTRYPOINT`、`COPY` 和 `ADD` 指令设置工作目录。                                                                          |
| [`COPY <源> <目的>`](/reference/dockerfile.md#copy)      | 从 `<源>` 复制新文件或目录，并将其添加到容器文件系统的 `<目的>` 路径下。                                                                                      |
| [`CMD <命令>`](/reference/dockerfile.md#cmd)           | 允许您定义基于此镜像启动容器后运行的默认程序。每个 Dockerfile 只能有一个 `CMD`，如果存在多个，则只有最后一个 `CMD` 实例有效。 |

Dockerfile 是镜像构建的关键输入，可以根据您的独特配置实现自动化的多层镜像构建。Dockerfile 可以从简单开始，并随着您的需求增长以支持更复杂的场景。

### 文件名

Dockerfile 的默认文件名为 `Dockerfile`，不带文件扩展名。使用默认名称允许您运行 `docker build` 命令，而无需指定额外的命令标志。

某些项目可能需要用于特定目的的不同 Dockerfile。常见的做法是将其命名为 `<something>.Dockerfile`。您可以使用 `docker build` 命令的 `--file` 标志指定 Dockerfile 文件名。请参阅 [`docker build` CLI 参考](/reference/cli/docker/buildx/build.md#file) 了解 `--file` 标志。

> [!NOTE]
>
> 我们建议为项目的主 Dockerfile 使用默认名称 (`Dockerfile`)。

## Docker 镜像

Docker 镜像由层（layers）组成。每一层都是 Dockerfile 中一条构建指令的结果。层按顺序堆叠，每一层都是一个增量，代表对前一层应用的更改。

### 示例

以下是使用 Docker 构建应用程序的典型工作流。

以下示例代码展示了一个使用 Flask 框架编写的 Python 简单 "Hello World" 应用程序。

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

为了在不使用 Docker Build 的情况下交付和部署此应用程序，您需要确保：

- 服务器上安装了所需的运行时依赖项
- Python 代码被上传到服务器的文件系统中
- 服务器使用必要的参数启动您的应用程序

以下 Dockerfile 会创建一个容器镜像，该镜像已安装所有依赖项并会自动启动您的应用程序。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# 安装应用依赖项
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==3.0.*

# 安装应用
COPY hello.py /

# 最终配置
ENV FLASK_APP=hello
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

以下是此 Dockerfile 的功能分解：

- [Dockerfile 语法](#dockerfile-语法)
- [基础镜像](#基础镜像)
- [环境设置](#环境设置)
- [注释](#注释)
- [安装依赖项](#安装依赖项)
- [复制文件](#复制文件)
- [设置环境变量](#设置环境变量)
- [暴露端口](#暴露端口)
- [启动应用程序](#启动应用程序)

### Dockerfile 语法

添加到 Dockerfile 的第一行应为 [`# syntax` 解析器指令](/reference/dockerfile.md#syntax)。虽然它是可选的，但该指令会指示 Docker 构建器在解析 Dockerfile 时使用哪种语法，并允许 [启用了 BuildKit](../buildkit/_index.md#快速入门) 的旧版本 Docker 在开始构建之前使用特定的 [Dockerfile 前端](../buildkit/frontend.md)。[解析器指令](/reference/dockerfile.md#解析器指令) 必须出现在 Dockerfile 中的任何其他注释、空白或指令之前，并且应该是 Dockerfile 的第一行。

```dockerfile
# syntax=docker/dockerfile:1
```

> [!TIP]
>
> 我们建议使用 `docker/dockerfile:1`，它始终指向版本 1 语法的最新发行版。BuildKit 会在构建前自动检查语法更新，确保您使用的是最新版本。

### 基础镜像

语法指令之后的行定义了要使用的基础镜像：

```dockerfile
FROM ubuntu:22.04
```

[`FROM` 指令](/reference/dockerfile.md#from) 将您的基础镜像设置为 Ubuntu 的 22.04 版本。随后所有的指令都在这个基础镜像（一个 Ubuntu 环境）中执行。`ubuntu:22.04` 这种记法遵循 Docker 镜像命名的 `name:tag` 标准。构建镜像时，您使用此记法为镜像命名。您可以在项目中使用许多公共镜像，方法是通过 Dockerfile 的 `FROM` 指令将它们导入到构建步骤中。

[Docker Hub](https://hub.docker.com/search?image_filter=official&q=&type=image) 包含大量官方镜像供您使用。

### 环境设置

以下行在基础镜像内部执行构建命令。

```dockerfile
# 安装应用依赖项
RUN apt-get update && apt-get install -y python3 python3-pip
```

此 [`RUN` 指令](/reference/dockerfile.md#run) 在 Ubuntu 中执行一个 shell，用于更新 APT 软件包索引并在容器中安装 Python 工具。

### 注释

请注意 `# install app dependencies` 这一行。这是一个注释。Dockerfile 中的注释以 `#` 符号开头。随着 Dockerfile 的演进，注释对于记录 Dockerfile 的工作方式非常有帮助，方便未来的读者和编辑者（包括未来的您自己）理解！

> [!NOTE]
>
> 您可能已经注意到，注释使用的符号与文件第一行的 [语法指令](#dockerfile-语法) 相同。该符号只有在匹配指令模式且出现在 Dockerfile 开头时才会被解释为指令。否则，它会被视为注释。

### 安装依赖项

第二条 `RUN` 指令安装 Python 应用程序所需的 `flask` 依赖项。

```dockerfile
RUN pip install flask==3.0.*
```

此指令的前提条件是将 `pip` 安装到构建容器中。第一条 `RUN` 命令安装了 `pip` ，确保我们可以使用该命令来安装 Flask Web 框架。

### 复制文件

下一条指令使用 [`COPY` 指令](/reference/dockerfile.md#copy) 将本地构建上下文中的 `hello.py` 文件复制到镜像的根目录中。 

```dockerfile
COPY hello.py /
```

[构建上下文](./context.md) 是您在 `COPY` 和 `ADD` 等 Dockerfile 指令中可以访问的文件集。

在 `COPY` 指令执行后，`hello.py` 文件被添加到构建容器的文件系统中。

### 设置环境变量

如果您的应用程序使用环境变量，可以使用 [`ENV` 指令](/reference/dockerfile.md#env) 在 Docker 构建中设置环境变量。

```dockerfile
ENV FLASK_APP=hello
```

这设置了一个我们稍后需要的 Linux 环境变量。本示例中使用的 Flask 框架使用此变量启动应用程序。如果没有它，Flask 就不知道在哪里可以找到并运行我们的应用程序。

### 暴露端口

[`EXPOSE` 指令](/reference/dockerfile.md#expose) 标记我们的最终镜像有一个服务在监听端口 `8000`。

```dockerfile
EXPOSE 8000
```

此指令不是必需的，但它是一个很好的实践，有助于工具和团队成员了解此应用程序正在执行的操作。

### 启动应用程序

最后，[`CMD` 指令](/reference/dockerfile.md#cmd) 设置了用户基于此镜像启动容器时运行的命令。

```dockerfile
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

此命令启动 Flask 开发服务器，监听端口 `8000` 上的所有地址。此处的示例使用了 `CMD` 的 "exec 形式" 版本。也可以使用 "shell 形式"：

```dockerfile
CMD flask run --host 0.0.0.0 --port 8000
```

这两个版本之间存在细微差别，例如它们如何捕获 `SIGTERM` 和 `SIGKILL` 等信号。有关这些差别的更多信息，请参阅 [Shell 形式和 exec 形式](/reference/dockerfile.md#shell-形式和-exec-形式)。

## 构建

要使用 [上一节](#示例) 中的 Dockerfile 示例构建容器镜像，请使用 `docker build` 命令：

```console
$ docker build -t test:latest .
```

`-t test:latest` 选项指定了镜像的名称和标签。

命令末尾的单个点 (`.`) 将 [构建上下文](./context.md) 设置为当前目录。这意味着构建过程预期在调用命令的目录中找到 Dockerfile 和 `hello.py` 文件。如果这些文件不存在，构建将失败。

镜像构建完成后，您可以使用 `docker run` 并指定镜像名称来将应用程序作为容器运行：

```console
$ docker run -p 127.0.0.1:8000:8000 test:latest
```

这会将容器的 8000 端口发布到 Docker 宿主机的 `http://localhost:8000`。

> [!TIP]
>
> 想要在 VS Code 中获得更好的 Dockerfile 编辑体验吗？
> 请查看 [Docker VS Code 扩展 (Beta)](https://marketplace.visualstudio.com/items?itemName=docker.docker)，它支持 lint、代码导航和漏洞扫描。
