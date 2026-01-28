---
title: 使用容器进行 Python 开发
linkTitle: 开发您的应用
weight: 15
keywords: python, local, development
description: 学习如何在本地开发您的 Python 应用程序。
aliases:
  - /language/python/develop/
  - /guides/language/python/develop/
---

## 前提条件

完成[容器化 Python 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何为容器化应用程序搭建开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose 在您编辑和保存代码时自动更新正在运行的 Compose 服务

## 获取示例应用程序

您需要克隆一个新的仓库来获取包含数据库连接逻辑的示例应用程序。

1. 切换到您想要克隆仓库的目录，然后运行以下命令。

   ```console
   $ git clone https://github.com/estebanx64/python-docker-dev-example
   ```

2. 在克隆的仓库目录中，手动创建 Docker 资源或运行 `docker init` 来创建必要的 Docker 资源。

   {{< tabs >}}
   {{< tab name="Use Docker Init" >}}

   在克隆的仓库目录中，运行 `docker init`。参考以下示例回答 `docker init` 的提示。

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
   ? What port do you want your app to listen on? 8001
   ? What is the command to run your app? python3 -m uvicorn app:app --host=0.0.0.0 --port=8001
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

   # Want to help us make this template better? Share your feedback here: https://   forms.gle/ybq9Krt8jtBL3iCk7

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

   # Download dependencies as a separate step to take advantage of Docker's    caching.
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
   EXPOSE 8001

   # Run the application.
   CMD ["python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8001"]
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
         - 8001:8001
   # The commented out section below is an example of how to define a PostgreSQL
   # database that your application can use. `depends_on` tells Docker Compose to
   # start the database before your application. The `db-data` volume persists the
   # database data between container restarts. The `db-password` secret is used
   # to set the database password. You must create `db/password.txt` and add
   # a password of your choosing to it before running `docker compose up`.
   #     depends_on:
   #       db:
   #         condition: service_healthy
   #   db:
   #     image: postgres
   #     restart: always
   #     user: postgres
   #     secrets:
   #       - db-password
   #     volumes:
   #       - db-data:/var/lib/postgresql/data
   #     environment:
   #       - POSTGRES_DB=example
   #       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
   #     expose:
   #       - 5432
   #     healthcheck:
   #       test: [ "CMD", "pg_isready" ]
   #       interval: 10s
   #       timeout: 5s
   #       retries: 5
   # volumes:
   #   db-data:
   # secrets:
   #   db-password:
   #     file: db/password.txt
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

## 添加本地数据库并持久化数据

您可以使用容器来设置本地服务，如数据库。在本节中，您将更新 `compose.yaml` 文件来定义数据库服务和用于持久化数据的卷。

在克隆的仓库目录中，用 IDE 或文本编辑器打开 `compose.yaml` 文件。`docker init` 已经处理了大部分指令的创建，但您需要根据您的特定应用程序进行更新。

在 `compose.yaml` 文件中，您需要取消所有数据库指令的注释。此外，您需要将数据库密码文件作为环境变量添加到 server 服务，并指定要使用的 secret 文件。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="7-43"}
services:
  server:
    build:
      context: .
    ports:
      - 8001:8001
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
  db:
    image: postgres
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

> [!NOTE]
>
> 要了解更多关于 Compose 文件中指令的信息，请参阅 [Compose 文件
> 参考](/reference/compose-file/)。

在使用 Compose 运行应用程序之前，请注意此 Compose 文件指定了一个 `password.txt` 文件来保存数据库密码。您必须创建此文件，因为它不包含在源代码仓库中。

在克隆的仓库目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件，包含数据库的密码。使用您喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件中。

```text
mysecretpassword
```

保存并关闭 `password.txt` 文件。

现在您的 `python-docker-dev-example` 目录中应该包含以下内容。

```text
├── python-docker-dev-example/
│ ├── db/
│ │ └── password.txt
│ ├── app.py
│ ├── config.py
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

现在，运行以下 `docker compose up` 命令来启动您的应用程序。

```console
$ docker compose up --build
```

现在测试您的 API 端点。打开一个新终端，然后使用 curl 命令向服务器发送请求：

让我们使用 POST 方法创建一个对象

```console
$ curl -X 'POST' \
  'http://localhost:8001/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}'
```

您应该收到以下响应：

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

让我们使用下一个 curl 命令发出 GET 请求：

```console
curl -X 'GET' \
  'http://localhost:8001/heroes/' \
  -H 'accept: application/json'
```

您应该收到与上面相同的响应，因为这是我们数据库中唯一的对象。

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

在终端中按 `ctrl+c` 停止应用程序。

## 自动更新服务

使用 Compose Watch 在您编辑和保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详情，请参阅[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开 `compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="17-20"}
services:
  server:
    build:
      context: .
    ports:
      - 8001:8001
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

运行以下命令以使用 Compose Watch 运行您的应用程序。

```console
$ docker compose watch
```

在终端中，curl 应用程序以获取响应。

```console
$ curl http://localhost:8001
Hello, Docker!
```

您在本地机器上对应用程序源文件的任何更改现在都会立即反映在正在运行的容器中。

在 IDE 或文本编辑器中打开 `python-docker-dev-example/app.py`，通过添加几个感叹号来更新 `Hello, Docker!` 字符串。

```diff
-    return 'Hello, Docker!'
+    return 'Hello, Docker!!!'
```

保存对 `app.py` 的更改，然后等待几秒钟让应用程序重建。再次 curl 应用程序并验证更新后的文本是否出现。

```console
$ curl http://localhost:8001
Hello, Docker!!!
```

在终端中按 `ctrl+c` 停止应用程序。

## 总结

在本节中，您了解了如何设置 Compose 文件来添加本地数据库和持久化数据。您还学习了如何使用 Compose Watch 在更新代码时自动重建和运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，您将学习如何设置代码检查、格式化和类型检查，以遵循 Python 应用程序的最佳实践。
