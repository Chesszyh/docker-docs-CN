---
title: 使用 Docker Compose
weight: 80
linkTitle: "第七部分：使用 Docker Compose"
keywords: '入门, 设置, 定向, 快速入门, 介绍, 概念, 容器, docker desktop'
description: 为多容器应用程序使用 Docker Compose
aliases:
 - /get-started/08_using_compose/
 - /guides/workshop/08_using_compose/
---

[Docker Compose](/manuals/compose/_index.md) 是一个可以帮助你定义和共享多容器应用程序的工具。使用 Compose，你可以创建一个 YAML 文件来定义服务，并且只需一个命令，你就可以启动所有服务或拆卸所有服务。

使用 Compose 的最大优势是，你可以在一个文件中定义你的应用程序堆栈，将其保存在你的项目存储库的根目录下（现在它已受版本控制），并轻松地让其他人为你的项目做出贡献。其他人只需要克隆你的存储库并使用 Compose 启动应用程序。事实上，你现在可能会在 GitHub/GitLab 上看到很多项目正是这样做的。

## 创建 Compose 文件

在 `getting-started-app` 目录中，创建一个名为 `compose.yaml` 的文件。

```text
├── getting-started-app/
│ ├── Dockerfile
│ ├── compose.yaml
│ ├── node_modules/
│ ├── package.json
│ ├── spec/
│ ├── src/
│ └── yarn.lock
```

## 定义应用程序服务

在[第六部分](./07_multi_container.md)中，你使用了以下命令来启动应用程序服务。

```console
$ docker run -dp 127.0.0.1:3000:3000 \
  -w /app -v "$(pwd):/app" \
  --network todo-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  node:18-alpine \
  sh -c "yarn install && yarn run dev"
```

你现在将在 `compose.yaml` 文件中定义此服务。

1. 在文本或代码编辑器中打开 `compose.yaml`，首先定义你想要作为应用程序一部分运行的第一个服务（或容器）的名称和镜像。该名称将自动成为网络别名，这在定义你的 MySQL 服务时将非常有用。

   ```yaml
   services:
     app:
       image: node:18-alpine
   ```

2. 通常，你会看到 `command` 靠近 `image` 定义，尽管没有排序要求。将 `command` 添加到你的 `compose.yaml` 文件中。

   ```yaml
   services:
     app:
       image: node:18-alpine
       command: sh -c "yarn install && yarn run dev"
   ```

3. 现在，通过定义服务的 `ports` 来迁移命令的 `-p 127.0.0.1:3000:3000` 部分。

   ```yaml
   services:
     app:
       image: node:18-alpine
       command: sh -c "yarn install && yarn run dev"
       ports:
         - 127.0.0.1:3000:3000
   ```

4. 接下来，通过使用 `working_dir` 和 `volumes` 定义来迁移工作目录 (`-w /app`) 和卷映射 (`-v "$(pwd):/app"`)。

    Docker Compose 卷定义的一个优点是你可以使用相对于当前目录的路径。

   ```yaml
   services:
     app:
       image: node:18-alpine
       command: sh -c "yarn install && yarn run dev"
       ports:
         - 127.0.0.1:3000:3000
       working_dir: /app
       volumes:
         - ./:/app
   ```

5. 最后，你需要使用 `environment` 键来迁移环境变量定义。

   ```yaml
   services:
     app:
       image: node:18-alpine
       command: sh -c "yarn install && yarn run dev"
       ports:
         - 127.0.0.1:3000:3000
       working_dir: /app
       volumes:
         - ./:/app
       environment:
         MYSQL_HOST: mysql
         MYSQL_USER: root
         MYSQL_PASSWORD: secret
         MYSQL_DB: todos
   ```

### 定义 MySQL 服务

现在，是时候定义 MySQL 服务了。你用于该容器的命令如下：

```console
$ docker run -d \
  --network todo-app --network-alias mysql \
  -v todo-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  mysql:8.0
```

1. 首先定义新服务并将其命名为 `mysql`，以便它自动获取网络别名。同时指定要使用的镜像。

   ```yaml

   services:
     app:
       # 应用程序服务定义
     mysql:
       image: mysql:8.0
   ```

2. 接下来，定义卷映射。当你使用 `docker run` 运行容器时，Docker 会自动创建命名卷。但是，使用 Compose 运行时不会发生这种情况。你需要在顶级的 `volumes:` 部分定义卷，然后在服务配置中指定挂载点。只需提供卷名，就会使用默认选项。

   ```yaml
   services:
     app:
       # 应用程序服务定义
     mysql:
       image: mysql:8.0
       volumes:
         - todo-mysql-data:/var/lib/mysql

   volumes:
     todo-mysql-data:
   ```

3. 最后，你需要指定环境变量。

   ```yaml
   services:
     app:
       # 应用程序服务定义
     mysql:
       image: mysql:8.0
       volumes:
         - todo-mysql-data:/var/lib/mysql
       environment:
         MYSQL_ROOT_PASSWORD: secret
         MYSQL_DATABASE: todos

   volumes:
     todo-mysql-data:
   ```

此时，你完整的 `compose.yaml` 应该如下所示：


```yaml
services:
  app:
    image: node:18-alpine
    command: sh -c "yarn install && yarn run dev"
    ports:
      - 127.0.0.1:3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos

  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:
```

## 运行应用程序堆栈

现在你有了 `compose.yaml` 文件，你可以启动你的应用程序了。

1. 首先确保没有其他容器副本正在运行。使用 `docker ps` 列出容器，并使用 `docker rm -f <ids>` 删除它们。

2. 使用 `docker compose up` 命令启动应用程序堆栈。添加 `-d` 标志以在后台运行所有内容。

   ```console
   $ docker compose up -d
   ```

    当你运行前面的命令时，你应该看到如下所示的输出：

   ```plaintext
   Creating network "app_default" with the default driver
   Creating volume "app_todo-mysql-data" with default driver
   Creating app_app_1   ... done
   Creating app_mysql_1 ... done
   ```

    你会注意到 Docker Compose 创建了卷以及一个网络。默认情况下，Docker Compose 会自动为应用程序堆栈创建一个专用的网络（这就是为什么你没有在 Compose 文件中定义一个）。

3. 使用 `docker compose logs -f` 命令查看日志。你会看到来自每个服务的日志交错地显示在一个流中。当你想观察与时间相关的问题时，这非常有用。`-f` 标志会跟踪日志，因此会为你提供实时的输出。

    如果你已经运行了该命令，你会看到如下所示的输出：

    ```plaintext
    mysql_1  | 2019-10-03T03:07:16.083639Z 0 [Note] mysqld: ready for connections.
    mysql_1  | Version: '8.0.31'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
    app_1    | Connected to mysql db at host mysql
    app_1    | Listening on port 3000
    ```

    服务名称显示在行的开头（通常是彩色的），以帮助区分消息。如果你想查看特定服务的日志，你可以在日志命令的末尾添加服务名称（例如，`docker compose logs -f app`）。

4. 此时，你应该能够在浏览器中打开你的应用程序 [http://localhost:3000](http://localhost:3000) 并看到它正在运行。

## 在 Docker Desktop 仪表板中查看应用程序堆栈

如果你查看 Docker Desktop 仪表板，你会看到一个名为 **getting-started-app** 的组。这是 Docker Compose 的项目名称，用于将容器组合在一起。默认情况下，项目名称就是 `compose.yaml` 所在目录的名称。

如果你展开该堆栈，你会看到你在 Compose 文件中定义的两个容器。名称也更具描述性，因为它们遵循 `<service-name>-<replica-number>` 的模式。因此，很容易快速地看到哪个容器是你的应用程序，哪个容器是 mysql 数据库。

## 拆卸所有服务

当你准备好拆卸所有服务时，只需运行 `docker compose down` 或在 Docker Desktop 仪表板上点击整个应用程序的垃圾桶图标。容器将停止，网络将被移除。

> [!WARNING]
>
> 默认情况下，当你运行 `docker compose down` 时，Compose 文件中的命名卷不会被移除。如果你想移除卷，你需要添加 `--volumes` 标志。
>
> 当你删除应用程序堆栈时，Docker Desktop 仪表板不会移除卷。

## 总结

在本节中，你了解了 Docker Compose 以及它如何帮助你简化定义和共享多服务应用程序的方式。

相关信息：
 - [Compose 概述](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Compose CLI 参考](/reference/cli/docker/compose/_index.md)

## 下一步

接下来，你将学习一些可以用来改进 Dockerfile 的最佳实践。

{{< button text="镜像构建最佳实践" url="09_image_best.md" >}}

```