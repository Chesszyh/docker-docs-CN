---
title: Dockerfile 概览
weight: 20
description: 了解 Dockerfile 以及如何配合 Docker 镜像来构建并打包您的软件
keywords: build, buildx, buildkit, getting started, dockerfile, 构建, 入门
aliases:
- /build/hellobuild/
- /build/building/packaging/
---

## Dockerfile

一切都始于 Dockerfile。

Docker 通过读取 Dockerfile 中的指令来构建镜像。Dockerfile 是一个包含构建源码所需指令的文本文件。Dockerfile 指令的语法规范在 [Dockerfile 参考](/reference/dockerfile.md) 中有详细定义。

以下是一些最常用的指令类型：

| 指令 | 说明 |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`FROM <镜像名>`](/reference/dockerfile.md#from) | 为您的镜像定义基础镜像。 |
| [`RUN <命令>`](/reference/dockerfile.md#run) | 在当前镜像顶部的全新层中执行命令并提交结果。`RUN` 也有用于运行命令的 shell 形式。 |
| [`WORKDIR <目录>`](/reference/dockerfile.md#workdir) | 为 Dockerfile 中其后的 `RUN`、`CMD`、`ENTRYPOINT`、`COPY` 和 `ADD` 指令设置工作目录。 |
| [`COPY <源> <目标>`](/reference/dockerfile.md#copy) | 从 `<源>` 复制新文件或目录，并将其添加到容器文件系统的 `<目标>` 路径下。 |
| [`CMD <命令>`](/reference/dockerfile.md#cmd) | 允许您定义启动基于此镜像的容器时默认运行的程序。每个 Dockerfile 只能有一个 `CMD`，如果存在多个，则仅最后一次出现的 `CMD` 生效。 |

Dockerfile 是镜像构建的关键输入，可以根据您的独特配置实现自动化的多层镜像构建。Dockerfile 可以从简单开始，并随您的需求增长以支持更复杂的场景。

### 文件名

Dockerfile 的默认文件名是 `Dockerfile`（无文件扩展名）。使用默认名称允许您在运行 `docker build` 命令时无需指定额外的命令标志。

某些项目可能需要针对特定目的使用不同的 Dockerfile。通用的做法是将其命名为 `<名称>.Dockerfile`。您可以使用 `docker build` 命令的 `--file` 标志来指定 Dockerfile 的文件名。参考 [`docker build` CLI 参考](/reference/cli/docker/buildx/build.md#file) 了解关于 `--file` 标志的更多信息。

> [!NOTE]
>
> 建议为您项目的主要 Dockerfile 使用默认名称 (`Dockerfile`)。

## Docker 镜像 (Docker images)

Docker 镜像由多个层 (layers) 组成。每一层都是 Dockerfile 中一条构建指令的执行结果。这些层按顺序堆叠，每一层都是代表对上一层所做更改的增量 (delta)。

### 示例

以下是使用 Docker 构建应用程序的典型工作流示例。

下面的示例代码展示了一个用 Python 编写、使用 Flask 框架的简单 "Hello World" 应用程序。

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

为了在没有 Docker Build 的情况下交付和部署此应用程序，您需要确保：

- 服务器上安装了所需的运行时依赖项
- Python 代码已上传到服务器的文件系统
- 服务器使用必要的参数启动您的应用程序

以下 Dockerfile 创建了一个容器镜像，该镜像已安装所有依赖项并能自动启动您的应用程序。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# 安装应用依赖
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==3.0.*

# 安装应用
COPY hello.py /

# 最终配置
ENV FLASK_APP=hello
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

以下是该 Dockerfile 的功能分解：

- [Dockerfile 语法](#dockerfile-语法)
- [基础镜像](#基础镜像)
- [环境设置](#环境设置)
- [注释](#注释)
- [安装依赖项](#安装依赖项)
- [复制文件](#复制文件)
- [设置环境变量](#设置环境变量)
- [公开端口](#公开端口)
- [启动应用程序](#启动应用程序)

### Dockerfile 语法

Dockerfile 的第一行应添加 [`# syntax` 解析器指令](/reference/dockerfile.md#syntax)。虽然是可选的，但该指令会告知 Docker 构建器在解析 Dockerfile 时使用哪种语法，并允许开启了 [BuildKit](../buildkit/_index.md#快速入门) 的旧版 Docker 在开始构建前使用特定的 [Dockerfile 前端](../buildkit/frontend.md)。[解析器指令](/reference/dockerfile.md#parser-directives) 必须出现在 Dockerfile 中任何其他注释、空白行或 Dockerfile 指令之前，且应作为 Dockerfile 的第一行。

```dockerfile
# syntax=docker/dockerfile:1
```

> [!TIP]
>
> 建议使用 `docker/dockerfile:1`，它始终指向版本 1 语法的最新发布。BuildKit 在构建前会自动检查语法更新，确保您使用的是最新版本。

### 基础镜像 (Base image)

语法指令后的下一行定义了要使用的基础镜像：

```dockerfile
FROM ubuntu:22.04
```

[`FROM` 指令](/reference/dockerfile.md#from) 将您的基础镜像设置为 Ubuntu 的 22.04 发行版。后续的所有指令都在此基础镜像（即 Ubuntu 环境）中执行。`ubuntu:22.04` 这种记法遵循了 Docker 镜像命名的 `名称:标签` 标准。当您构建镜像时，也使用这种记法为镜像命名。您可以利用许多现有的公共镜像，通过 Dockerfile 的 `FROM` 指令将它们导入到您的构建步骤中。

[Docker Hub](https://hub.docker.com/search?image_filter=official&q=&type=image) 包含大量可供使用的官方镜像。

### 环境设置

下一行在基础镜像内部执行构建命令。

```dockerfile
# 安装应用依赖
RUN apt-get update && apt-get install -y python3 python3-pip
```

此 [`RUN` 指令](/reference/dockerfile.md#run) 在 Ubuntu 中执行 shell，用于更新 APT 软件包索引并在容器中安装 Python 工具。

### 注释

请注意 `# 安装应用依赖` 这一行。这是一个注释。Dockerfile 中的注释以 `#` 符号开头。随着 Dockerfile 的演进，注释对于记录 Dockerfile 的工作方式非常有帮助，方便未来的读者和编辑者（包括未来的您自己）阅读。

> [!NOTE]
>
> 您可能已经注意到，注释所使用的符号与文件第一行的 [语法指令](#dockerfile-语法) 相同。只有当模式匹配特定指令且出现在 Dockerfile 开头时，该符号才会被解释为指令。否则，它将被视为注释。

### 安装依赖项

第二条 `RUN` 指令安装 Python 应用程序所需的 `flask` 依赖。

```dockerfile
RUN pip install flask==3.0.*
```

此指令的前提是构建容器中已安装 `pip`。第一条 `RUN` 命令安装了 `pip`，从而确保我们可以使用该命令来安装 flask Web 框架。

### 复制文件

下一条指令使用 [`COPY` 指令](/reference/dockerfile.md#copy) 将本地构建上下文中的 `hello.py` 文件复制到镜像的根目录下。

```dockerfile
COPY hello.py /
```

[构建上下文 (build context)](./context.md) 是指您在 Dockerfile 指令（如 `COPY` 和 `ADD`）中可以访问的一组文件。

执行 `COPY` 指令后，`hello.py` 文件就被添加到了构建容器的文件系统中。

### 设置环境变量

如果您的应用程序使用环境变量，您可以使用 [`ENV` 指令](/reference/dockerfile.md#env) 在 Docker 构建中设置环境变量。

```dockerfile
ENV FLASK_APP=hello
```

这设置了一个我们稍后需要的 Linux 环境变量。本示例中使用的 Flask 框架利用此变量来启动应用程序。如果没有这个变量，flask 就不知道去哪里寻找并运行我们的应用程序。

### 公开端口

[`EXPOSE` 指令](/reference/dockerfile.md#expose) 标记了我们的最终镜像有一个服务在监听 `8000` 端口。

```dockerfile
EXPOSE 8000
```

此指令并非强制要求，但是一种良好的实践，有助于工具和团队成员理解该应用程序的功能。

### 启动应用程序

最后，[`CMD` 指令](/reference/dockerfile.md#cmd) 设置了当用户启动基于此镜像的容器时所运行的命令。

```dockerfile
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

此命令启动 flask 开发服务器，监听所有地址上的 `8000` 端口。此处的示例使用了 `CMD` 的 "exec 形式 (exec form)"。也可以使用 "shell 形式 (shell form)"：

```dockerfile
CMD flask run --host 0.0.0.0 --port 8000
```

这两个版本之间存在细微差异，例如在它们捕获 `SIGTERM` 和 `SIGKILL` 等信号的方式上。欲了解更多关于这些差异的信息，请参阅 [Shell 和 exec 形式](/reference/dockerfile.md#shell-and-exec-form)。

## 执行构建

要使用[前一节](#示例)中的 Dockerfile 示例构建容器镜像，请使用 `docker build` 命令：

```console
$ docker build -t test:latest .
```

`-t test:latest` 选项指定了镜像的名称和标签。

命令末尾的单个点 (`.`) 将 [构建上下文](./context.md) 设置为当前目录。这意味着构建过程预期在调用命令的目录下找到 Dockerfile 和 `hello.py` 文件。如果这些文件不在那里，构建将失败。

镜像构建完成后，您可以使用 `docker run` 并指定镜像名称来将应用程序作为容器运行：

```console
$ docker run -p 127.0.0.1:8000:8000 test:latest
```

这会将容器的 8000 端口发布到 Docker 宿主机的 `http://localhost:8000`。

> [!TIP]
>
> 想要在 VS Code 中获得更好的 Dockerfile 编辑体验？
> 请查看 [Docker VS Code 扩展 (Beta)](https://marketplace.visualstudio.com/items?itemName=docker.docker)，它支持 linting、代码导航和漏洞扫描。