---
title: 容器化 Python 应用程序
linkTitle: 容器化您的应用
weight: 10
keywords: python, flask, containerize, initialize
description: 学习如何容器化 Python 应用程序。
aliases:
  - /language/python/build-images/
  - /language/python/run-containers/
  - /language/python/containerize/
  - /guides/language/python/containerize/
---

## 前提条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您有一个 [git 客户端](https://git-scm.com/downloads)。本节示例使用命令行 git 客户端，但您可以使用任何客户端。

## 概述

本节将引导您完成 Python 应用程序的容器化和运行。

## 获取示例应用程序

示例应用程序使用流行的 [FastAPI](https://fastapi.tiangolo.com) 框架。

克隆示例应用程序以配合本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/estebanx64/python-docker-example && cd python-docker-example
```

## 初始化 Docker 资源

现在您有了应用程序，可以创建必要的 Docker 资源来容器化您的应用程序。您可以使用 Docker Desktop 内置的 Docker Init 功能来简化流程，也可以手动创建这些资源。

{{< tabs >}}
{{< tab name="Use Docker Init" >}}

在 `python-docker-example` 目录中，运行 `docker init` 命令。`docker init` 提供一些默认配置，但您需要回答一些关于应用程序的问题。例如，此应用程序使用 FastAPI 运行。参考以下示例回答 `docker init` 的提示，并为您的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Python
? What version of Python do you want to use? 3.12
? What port do you want your app to listen on? 8000
? What is the command to run your app? python3 -m uvicorn app:app --host=0.0.0.0 --port=8000
```

创建一个名为 `.gitignore` 的文件，包含以下内容。

```text {collapse=true,title=".gitignore"}
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

{{< /tab >}}
{{< tab name="Manually create assets" >}}

如果您没有安装 Docker Desktop 或偏好手动创建资源，您可以在项目目录中创建以下文件。

创建一个名为 `Dockerfile` 的文件，包含以下内容。

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

创建一个名为 `compose.yaml` 的文件，包含以下内容。

```yaml {collapse=true,title=compose.yaml}
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
```

创建一个名为 `.dockerignore` 的文件，包含以下内容。

```text {collapse=true,title=".dockerignore"}
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

**/.DS_Store
**/__pycache__
**/.venv
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/bin
**/charts
**/docker-compose*
**/compose.y*ml
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
```

创建一个名为 `.gitignore` 的文件，包含以下内容。

```text {collapse=true,title=".gitignore"}
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

{{< /tab >}}
{{< /tabs >}}

现在您的 `python-docker-example` 目录中应该包含以下内容。

```text
├── python-docker-example/
│ ├── app.py
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

要了解更多关于这些文件的信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [.gitignore](https://git-scm.com/docs/gitignore)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `python-docker-example` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。您应该能看到一个简单的 FastAPI 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项使应用程序在后台运行，脱离终端。在 `python-docker-example` 目录中，在终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，访问 [http://localhost:8000](http://localhost:8000)。

要查看 OpenAPI 文档，您可以访问 [http://localhost:8000/docs](http://localhost:8000/docs)。

您应该能看到一个简单的 FastAPI 应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI
参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化并运行 Python 应用程序。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，您将了解如何使用 Docker 容器搭建本地开发环境。
