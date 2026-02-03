---
description: 按照此实践教程，学习如何使用 Docker Compose，从定义应用程序依赖项到尝试使用各种命令。
keywords: docker compose 示例, docker compose 教程, 如何使用 docker compose, 运行 docker compose, 如何运行 docker compose, docker compose 构建镜像, docker compose 命令示例, 运行 docker compose 文件, 如何创建 docker compose 文件, 运行 docker compose 文件
title: Docker Compose 快速入门
linkTitle: 快速入门
weight: 30
---

本教程旨在通过引导您开发一个基础的 Python Web 应用程序，来介绍 Docker Compose 的基本概念。

该应用程序使用 Flask 框架，并在 Redis 中实现了一个点击计数器，为 Docker Compose 在 Web 开发场景中的应用提供了一个实际示例。

即使您不熟悉 Python，这里演示的概念也应该是易于理解的。

这是一个非规范性的示例，旨在演示 Compose 的核心功能。

## 前提条件

确保您已：

- [安装了最新版本的 Docker Compose](/manuals/compose/install/_index.md)
- 对 Docker 概念及 Docker 的工作原理有基本了解

## 第一步：环境设置

1. 为项目创建一个目录：

   ```console
   $ mkdir composetest
   $ cd composetest
   ```

2. 在您的项目目录中创建一个名为 `app.py` 的文件，并将以下代码粘贴进去：

   ```python
   import time

   import redis
   from flask import Flask

   app = Flask(__name__)
   cache = redis.Redis(host='redis', port=6379)

   def get_hit_count():
       retries = 5
       while True:
           try:
               return cache.incr('hits')
           except redis.exceptions.ConnectionError as exc:
               if retries == 0:
                   raise exc
               retries -= 1
               time.sleep(0.5)

   @app.route('/')
   def hello():
       count = get_hit_count()
       return f'Hello World! I have been seen {count} times.\n'
    ```

   在此示例中，`redis` 是应用程序网络上 redis 容器的主机名，并使用了默认端口 `6379`。

   > [!NOTE]
   > 
   > 请注意 `get_hit_count` 函数的编写方式。如果 Redis 服务不可用，这个基本的重试循环会尝试多次请求。这在应用程序启动且 Redis 尚未完全上线时非常有用，同时也使应用程序在 Redis 服务需要重启的任何时候都更具韧性。在集群环境中，这也有助于处理节点间瞬间的连接中断。

3. 在您的项目目录中创建另一个名为 `requirements.txt` 的文件，并将以下代码粘贴进去：

   ```text
   flask
   redis
   ```

4. 创建一个 `Dockerfile` 并粘贴以下代码：

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM python:3.10-alpine
   WORKDIR /code
   ENV FLASK_APP=app.py
   ENV FLASK_RUN_HOST=0.0.0.0
   RUN apk add --no-cache gcc musl-dev linux-headers
   COPY requirements.txt requirements.txt
   RUN pip install -r requirements.txt
   EXPOSE 5000
   COPY . .
   CMD ["flask", "run", "--debug"]
   ```

   {{< accordion title="理解该 Dockerfile" >}}

   这告知 Docker 执行以下操作：

   * 从 Python 3.10 镜像开始构建镜像。
   * 将工作目录设置为 `/code`。
   * 设置 `flask` 命令使用的环境变量。
   * 安装 gcc 和其他依赖项。
   * 复制 `requirements.txt` 并安装 Python 依赖项。
   * 为镜像添加元数据，描述容器正在监听 5000 端口。
   * 将项目中的当前目录 `.` 复制到镜像中的工作目录 `.`。
   * 将容器的默认命令设置为 `flask run --debug`。

   {{< /accordion >}}

   > [!IMPORTANT]
   > 
   > 检查 `Dockerfile` 是否没有类似 `.txt` 的文件扩展名。某些编辑器可能会自动附加此扩展名，导致您在运行应用程序时出错。

   有关如何编写 Dockerfile 的更多信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

## 第二步：在 Compose 文件中定义服务

Compose 简化了对整个应用程序栈的控制，使您可以通过单个、易于理解的 YAML 配置文件来管理服务、网络和卷。

在您的项目目录中创建一个名为 `compose.yaml` 的文件，并粘贴以下内容：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:5000"
  redis:
    image: "redis:alpine"
```

此 Compose 文件定义了两个服务：`web` 和 `redis`。

`web` 服务使用从当前目录下的 `Dockerfile` 构建的镜像。然后，它将容器和宿主机绑定到暴露的端口 `8000`。该示例服务使用了 Flask Web 服务器的默认端口 `5000`。

`redis` 服务使用从 Docker Hub 注册表拉取的公共 [Redis](https://registry.hub.docker.com/_/redis/) 镜像。

有关 `compose.yaml` 文件的更多信息，请参阅 [Compose 的工作原理](compose-application-model.md)。

## 第三步：使用 Compose 构建并运行您的应用

只需一条命令，即可根据您的配置文件创建并启动所有服务。

1. 在您的项目目录中，运行 `docker compose up` 启动应用程序。

   ```console
   $ docker compose up

   Creating network "composetest_default" with the default driver
   Creating composetest_web_1 ...
   Creating composetest_redis_1 ...
   Creating composetest_web_1
   Creating composetest_redis_1 ... done
   Attaching to composetest_web_1, composetest_redis_1
   web_1    |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
   redis_1  | 1:C 17 Aug 22:11:10.480 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
   redis_1  | 1:C 17 Aug 22:11:10.480 # Redis version=4.0.1, bits=64, commit=00000000, modified=0, pid=1, just started
   redis_1  | 1:C 17 Aug 22:11:10.480 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
   web_1    |  * Restarting with stat
   redis_1  | 1:M 17 Aug 22:11:10.483 * Running mode=standalone, port=6379.
   redis_1  | 1:M 17 Aug 22:11:10.483 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
   web_1    |  * Debugger is active!
   redis_1  | 1:M 17 Aug 22:11:10.483 # Server initialized
   redis_1  | 1:M 17 Aug 22:11:10.483 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
   web_1    |  * Debugger PIN: 330-787-903
   redis_1  | 1:M 17 Aug 22:11:10.483 * Ready to accept connections
   ```

   Compose 会拉取 Redis 镜像，为您自己的代码构建一个镜像，并启动您定义的服务。在此案例中，代码是在构建时静态复制到镜像中的。

2. 在浏览器中输入 `http://localhost:8000/` 以查看正在运行的应用程序。

   如果无法解析，您也可以尝试 `http://127.0.0.1:8000`。

   您应该在浏览器中看到一条消息：

   ```text
   Hello World! I have been seen 1 times.
   ```

   ![浏览器中的 hello world](images/quick-hello-world-1.png)

3. 刷新页面。

   数字应该会增加。

   ```text
   Hello World! I have been seen 2 times.
   ```

   ![浏览器中的 hello world](images/quick-hello-world-2.png)

4. 切换到另一个终端窗口，输入 `docker image ls` 列出本地镜像。

   此时列出镜像应返回 `redis` 和 `web`。

   ```console
   $ docker image ls

   REPOSITORY        TAG           IMAGE ID      CREATED        SIZE
   composetest_web   latest        e2c21aa48cc1  4 minutes ago  93.8MB
   python            3.4-alpine    84e6077c7ab6  7 days ago     82.5MB
   redis             alpine        9d8fa9aa0e5b  3 weeks ago    27.5MB
   ```

   您可以使用 `docker inspect <标签或ID>` 检查镜像。

5. 停止应用程序，既可以在第二个终端的项目目录内运行 `docker compose down`，也可以在启动应用的原始终端中按 `CTRL+C`。

## 第四步：修改 Compose 文件以使用 Compose Watch

修改项目目录中的 `compose.yaml` 文件以使用 `watch` 功能，这样您就可以实时预览运行中的 Compose 服务，并在编辑并保存代码时自动更新：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:5000"
    develop:
      watch:
        - action: sync
          path: .
          target: /code
  redis:
    image: "redis:alpine"
```

每当文件发生更改时，Compose 都会将该文件同步到容器内部 `/code` 下的相应位置。复制完成后，打包工具会在不重启的情况下更新运行中的应用程序。

有关 Compose Watch 工作原理的更多信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。或者参阅 [在容器中管理数据](/manuals/engine/storage/volumes.md) 了解其他选项。

> [!NOTE]
> 
> 为了使本示例生效，在 `Dockerfile` 中添加了 `--debug` 选项。Flask 中的 `--debug` 选项开启了代码自动重载功能，使得在不重启或重新构建容器的情况下，对后端 API 进行开发成为可能。修改 `.py` 文件后，随后的 API 调用将使用新代码，但在这个小示例中，浏览器 UI 不会自动刷新。大多数前端开发服务器都包含能与 Compose 配合使用的原生热重载支持。

## 第五步：使用 Compose 重新构建并运行应用

在您的项目目录中，输入 `docker compose watch` 或 `docker compose up --watch` 来构建、启动应用并开启文件监视模式。

```console
$ docker compose watch
[+] Running 2/2
 ✔ Container docs-redis-1 Created                                                                                                                                                                                                        0.0s
 ✔ Container docs-web-1    Recreated                                                                                                                                                                                                      0.1s
Attaching to redis-1, web-1
         ⦿ watch enabled
...
```

再次在 Web 浏览器中检查 `Hello World` 消息，并刷新以查看计数增加。

## 第六步：更新应用程序

要查看 Compose Watch 的实际效果：

1. 更改 `app.py` 中的问候语并保存。例如，将 `Hello World!` 更改为 `Hello from Docker!`：

   ```python
   return f'Hello from Docker! I have been seen {count} times.\n'
   ```

2. 在浏览器中刷新应用。问候语应该已更新，且计数器应仍在递增。

   ![浏览器中的 hello world](images/quick-hello-world-3.png)

3. 完成后，运行 `docker compose down`。

## 第七步：拆分服务

使用多个 Compose 文件允许您为不同的环境或工作流自定义 Compose 应用程序。这对于可能使用数十个容器、且所有权分散在多个团队的大型应用程序非常有用。

1. 在您的项目文件夹中，创建一个名为 `infra.yaml` 的新 Compose 文件。

2. 将 Redis 服务从您的 `compose.yaml` 文件剪切并粘贴到新的 `infra.yaml` 文件中。确保在文件顶部添加了 `services` 顶级属性。您的 `infra.yaml` 文件现在应如下所示：

   ```yaml
   services:
     redis:
       image: "redis:alpine"
   ```

3. 在您的 `compose.yaml` 文件中，添加 `include` 顶级属性以及指向 `infra.yaml` 文件的路径。

   ```yaml
   include:
      - infra.yaml
   services:
     web:
       build: .
       ports:
         - "8000:5000"
       develop:
         watch:
           - action: sync
             path: .
             target: /code
   ```

4. 运行 `docker compose up` 使用更新后的 Compose 文件构建并运行应用。您应该在浏览器中看到 `Hello world` 消息。

这是一个简化的示例，但它演示了 `include` 的基本原则，以及它如何使复杂应用程序更容易地模块化为子 Compose 文件。有关 `include` 及使用多个 Compose 文件的更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

## 第八步：尝试使用其他命令

- 如果您想在后台运行服务，可以为 `docker compose up` 传递 `-d` 标志（表示“分离 (detached)”模式），并使用 `docker compose ps` 查看当前正在运行的内容：

   ```console
   $ docker compose up -d

   Starting composetest_redis_1...
   Starting composetest_web_1...

   $ docker compose ps

          Name                      Command               State           Ports         
   -------------------------------------------------------------------------------------
   composetest_redis_1   docker-entrypoint.sh redis ...   Up      6379/tcp              
   composetest_web_1     flask run                        Up      0.0.0.0:8000->5000/tcp
   ```

- 运行 `docker compose --help` 查看其他可用命令。

- 如果您使用 `docker compose up -d` 启动了 Compose，请在完成后停止您的服务：

   ```console
   $ docker compose stop
   ```

- 您可以使用 `docker compose down` 命令停止并移除所有容器。

## 接下来去哪里

- 尝试 [使用 Compose 的示例应用](https://github.com/docker/awesome-compose)
- [探索完整的 Compose 命令列表](/reference/cli/docker/compose.md)
- [探索 Compose 文件参考](/reference/compose-file/_index.md)
- [在 LinkedIn Learning 上查看 Docker Compose 学习视频](https://www.linkedin.com/learning/learning-docker-compose/)