---
description: 如何向 Swarm 部署 stack (栈)
keywords: guide, swarm mode, composefile, stack, compose, deploy, 部署, 栈
title: 向 Swarm 部署 stack
---

在以 Swarm 模式运行 Docker Engine 时，您可以使用 `docker stack deploy` 向 Swarm 部署一个完整的应用程序 stack。`deploy` 命令接受以 [Compose 文件](/reference/compose-file/legacy-versions.md) 形式提供的 stack 描述。

{{% include "swarm-compose-compat.md" %}}

要完成本教程，您需要：

1.  一个以 [Swarm 模式](swarm-mode.md) 运行的 Docker Engine。如果您不熟悉 Swarm 模式，可能需要阅读 [Swarm 模式核心概念](key-concepts.md) 和 [服务如何工作](how-swarm-mode-works/services.md)。

    > [!NOTE]
    > 
    > 如果您在本地开发环境中进行尝试，可以使用 `docker swarm init` 将您的 Engine 置于 Swarm 模式。
    > 
    > 如果您已经有一个正在运行的多节点 Swarm，请记住所有的 `docker stack` 和 `docker service` 命令都必须从管理节点运行。

2.  当前版本的 [Docker Compose](/manuals/compose/install/_index.md)。

## 设置 Docker 注册表 (Registry)

由于 Swarm 由多个 Docker Engine 组成，因此需要一个注册表将镜像分发到所有节点。您可以使用 [Docker Hub](https://hub.docker.com) 或维护您自己的注册表。以下是创建一个临时注册表的方法，您可以在完成后将其丢弃。

1.  在您的 Swarm 上将注册表作为服务启动：

    ```console
    $ docker service create --name registry --publish published=5000,target=5000 registry:2
    ```

2.  使用 `docker service ls` 检查其状态：

    ```console
    $ docker service ls

    ID            NAME      REPLICAS  IMAGE                                                                               COMMAND
    l7791tpuwkco  registry  1/1       registry:2@sha256:1152291c7f93a4ea2ddc95e46d142c31e743b6dd70e194af9e6ebe530f782c17
    ```

    一旦 `REPLICAS` 下显示 `1/1`，它就运行起来了。如果显示 `0/1`，可能还在拉取镜像。

3.  使用 `curl` 检查它是否正在工作：

    ```console
    $ curl http://127.0.0.1:5000/v2/

    {}
    ```

## 创建示例应用程序

本指南中使用的应用基于 [Docker Compose 入门](/manuals/compose/gettingstarted.md) 指南中的点击计数器应用。它由一个 Python 应用组成，该应用在 Redis 实例中维护一个计数器，并在您每次访问时递增该计数器。

1.  为项目创建一个目录：

    ```console
    $ mkdir stackdemo
    $ cd stackdemo
    ```

2.  在项目目录中创建一个名为 `app.py` 的文件，并粘贴以下内容：

    ```python
    from flask import Flask
    from redis import Redis

    app = Flask(__name__)
    redis = Redis(host='redis', port=6379)

    @app.route('/')
    def hello():
        count = redis.incr('hits')
        return 'Hello World! I have been seen {} times.\n'.format(count)

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8000, debug=True)
    ```

3.  创建一个名为 `requirements.txt` 的文件，并粘贴以下两行内容：

    ```none
    flask
    redis
    ```

4.  创建一个名为 `Dockerfile` 的文件，并粘贴以下内容：

    ```dockerfile
    # syntax=docker/dockerfile:1
    FROM python:3.4-alpine
    ADD . /code
    WORKDIR /code
    RUN pip install -r requirements.txt
    CMD ["python", "app.py"]
    ```

5.  创建一个名为 `compose.yaml` 的文件，并粘贴以下内容：

    ```yaml
      services:
        web:
          image: 127.0.0.1:5000/stackdemo
          build: .
          ports:
            - "8000:8000"
        redis:
          image: redis:alpine
    ```

    Web 应用的镜像使用上面定义的 Dockerfile 构建。它还被打上了 `127.0.0.1:5000` 标签 —— 即之前创建的注册表的地址。这在将应用分发到 Swarm 时非常重要。


## 使用 Compose 测试应用

1.  使用 `docker compose up` 启动应用。这将构建 Web 应用镜像，如果您尚未拥有 Redis 镜像则拉取它，并创建两个容器。

    您会看到一条关于 Engine 处于 Swarm 模式的警告。这是因为 Compose 不利用 Swarm 模式，而是将所有内容部署到单个节点。您可以安全地忽略此警告。

    ```console
    $ docker compose up -d

    WARNING: The Docker Engine you're using is running in swarm mode.

    Compose does not use swarm mode to deploy services to multiple nodes in
    a swarm. All containers are scheduled on the current node.

    To deploy your application across the swarm, use `docker stack deploy`.

    Creating network "stackdemo_default" with the default driver
    Building web
    ...(构建输出)...
    Creating stackdemo_redis_1
    Creating stackdemo_web_1
    ```

2.  使用 `docker compose ps` 检查应用是否正在运行：

    ```console
    $ docker compose ps

          Name                     Command               State           Ports
    -----------------------------------------------------------------------------------
    stackdemo_redis_1   docker-entrypoint.sh redis ...   Up      6379/tcp
    stackdemo_web_1     python app.py                    Up      0.0.0.0:8000->8000/tcp
    ```

    您可以使用 `curl` 测试应用：

    ```console
    $ curl http://localhost:8000
    Hello World! I have been seen 1 times.

    $ curl http://localhost:8000
    Hello World! I have been seen 2 times.

    $ curl http://localhost:8000
    Hello World! I have been seen 3 times.
    ```

3.  停止并移除应用：

    ```console
    $ docker compose down --volumes

    Stopping stackdemo_web_1 ... done
    Stopping stackdemo_redis_1 ... done
    Removing stackdemo_web_1 ... done
    Removing stackdemo_redis_1 ... done
    Removing network stackdemo_default
    ```


## 将生成的镜像推送到注册表

为了在 Swarm 中分发 Web 应用的镜像，需要将其推送到您之前设置的注册表中。使用 Compose 执行此操作非常简单：

```console
$ docker compose push

Pushing web (127.0.0.1:5000/stackdemo:latest)...
The push refers to repository [127.0.0.1:5000/stackdemo]
5b5a49501a76: Pushed
be44185ce609: Pushed
bd7330a79bcf: Pushed
c9fc143a069a: Pushed
011b303988d2: Pushed
latest: digest: sha256:a81840ebf5ac24b42c1c676cbda3b2cb144580ee347c07e1bc80e35e5ca76507 size: 1372
```

现在 stack 已经准备好部署了。


## 向 Swarm 部署 stack

1.  使用 `docker stack deploy` 创建 stack：

    ```console
    $ docker stack deploy --compose-file compose.yaml stackdemo

    Ignoring unsupported options: build

    Creating network stackdemo_default
    Creating service stackdemo_web
    Creating service stackdemo_redis
    ```

    最后一个参数是 stack 的名称。每个网络、卷和服务名称都会加上 stack 名称作为前缀。

2.  使用 `docker stack services stackdemo` 检查它是否正在运行：

    ```console
    $ docker stack services stackdemo

    ID            NAME             MODE        REPLICAS  IMAGE
    orvjk2263y1p  stackdemo_redis  replicated  1/1       redis:3.2-alpine@sha256:f1ed3708f538b537eb9c2a7dd50dc90a706f7debd7e1196c9264edeea521a86d
    s1nf0xy8t1un  stackdemo_web    replicated  1/1       127.0.0.1:5000/stackdemo@sha256:adb070e0805d04ba2f92c724298370b7a4eb19860222120d43e0f6351ddbc26f
    ```

    一旦运行起来，您应该在两个服务的 `REPLICAS` 下看到 `1/1`。如果您有一个多节点 Swarm，由于需要拉取镜像，这可能需要一些时间。

    和之前一样，您可以使用 `curl` 测试应用：

    ```console
    $ curl http://localhost:8000
    Hello World! I have been seen 1 times.

    $ curl http://localhost:8000
    Hello World! I have been seen 2 times.

    $ curl http://localhost:8000
    Hello World! I have been seen 3 times.
    ```

    借助 Docker 内置的路由网格 (routing mesh)，您可以访问 Swarm 中的任何节点上的 `8000` 端口，并被路由到该应用：

    ```console
    $ curl http://其他节点的地址:8000
    Hello World! I have been seen 4 times.
    ```

3.  使用 `docker stack rm` 停止并移除 stack：

    ```console
    $ docker stack rm stackdemo

    Removing service stackdemo_web
    Removing service stackdemo_redis
    Removing network stackdemo_default
    ```

4.  使用 `docker service rm` 停止注册表服务：

    ```console
    $ docker service rm registry
    ```

5.  如果您只是在本地机器上测试，并希望将 Docker Engine 退出 Swarm 模式，使用 `docker swarm leave`：

    ```console
    $ docker swarm leave --force

    Node left the swarm.
    ```
