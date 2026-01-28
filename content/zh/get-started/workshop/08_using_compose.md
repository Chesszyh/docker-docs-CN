---
title: 使用 Docker Compose
weight: 80
linkTitle: "第七部分：使用 Docker Compose"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers,
  docker desktop, 入门, 设置, 概览, 快速入门, 简介, 概念, 容器
description: 将 Docker Compose 用于多容器应用程序
aliases:
 - /get-started/08_using_compose/
 - /guides/workshop/08_using_compose/
---

[Docker Compose](/manuals/compose/_index.md) 是一个帮助您定义和共享多容器应用程序的工具。使用 Compose，您可以创建一个 YAML 文件来定义服务，只需一个命令，您就可以启动所有内容或将其全部拆除。

使用 Compose 的最大好处是您可以在文件中定义应用程序堆栈，将其保留在项目仓库的根目录中（现在受版本控制），并轻松让其他人为您的项目做出贡献。其他人只需要克隆您的仓库并使用 Compose 启动应用程序。事实上，您可能会在 GitHub/GitLab 上看到很多项目现在正是这样做的。

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

在[第六部分](./07_multi_container.md)中，您使用了以下命令来启动应用程序服务。

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

您现在将在 `compose.yaml` 文件中定义此服务。

1. 在文本或代码编辑器中打开 `compose.yaml`，首先定义您想要作为应用程序一部分运行的第一个服务（或容器）的名称和镜像。
   该名称将自动成为网络别名，这在定义 MySQL 服务时非常有用。

   ```yaml
   services:
     app:
       image: node:18-alpine
   ```

2. 通常，您会看到 `command` 靠近 `image` 定义，尽管对顺序没有要求。将 `command` 添加到您的 `compose.yaml` 文件中。

   ```yaml
   services:
     app:
       image: node:18-alpine
       command: sh -c "yarn install && yarn run dev"
   ```

3. 现在通过定义服务的 `ports` 来迁移命令的 `-p 127.0.0.1:3000:3000` 部分。

   ```yaml
   services:
     app:
       image: node:18-alpine
       command: sh -c "yarn install && yarn run dev"
       ports:
         - 127.0.0.1:3000:3000
   ```

4. 接下来，通过使用 `working_dir` 和 `volumes` 定义迁移工作目录 (`-w /app`) 和卷映射 (`-v "$(pwd):/app"`)。

    Docker Compose 卷定义的一个优点是您可以使用相对于当前目录的路径。

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

5. 最后，您需要使用 `environment` 键迁移环境变量定义。

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

现在，是时候定义 MySQL 服务了。您用于该容器的命令如下：

```console
$ docker run -d \
  --network todo-app --network-alias mysql \
  -v todo-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  mysql:8.0
```

1. 首先定义新服务并将其命名为 `mysql`，以便它自动获得网络别名。同时指定要使用的镜像。

   ```yaml

   services:
     app:
       # 应用程序服务定义
     mysql:
       image: mysql:8.0
   ```

2. 接下来，定义卷映射。当您使用 `docker run` 运行容器时，Docker 会自动创建命名卷。但是，使用 Compose 运行时不会发生这种情况。您需要在顶级 `volumes:` 部分定义卷，然后在服务配置中指定挂载点。通过仅提供卷名称，将使用默认选项。

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

3. 最后，您需要指定环境变量。

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

此时，您完整的 `compose.yaml` 应该如下所示：


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

现在您有了 `compose.yaml` 文件，可以启动您的应用程序了。

1. 首先确保没有其他容器副本正在运行。使用 `docker ps` 列出容器，并使用 `docker rm -f <ids>` 删除它们。

2. 使用 `docker compose up` 命令启动应用程序堆栈。添加 `-d` 标志以在后台运行所有内容。

   ```console
   $ docker compose up -d
   ```

    运行上一条命令时，您应该看到类似以下的输出：

   ```plaintext
   Creating network "app_default" with the default driver
   Creating volume "app_todo-mysql-data" with default driver
   Creating app_app_1   ... done
   Creating app_mysql_1 ... done
   ```

    您会注意到 Docker Compose 创建了卷和网络。默认情况下，Docker Compose 会为应用程序堆栈创建一个专用网络（这就是您没有在 Compose 文件中定义网络的原因）。

3. 使用 `docker compose logs -f` 命令查看日志。您将看到来自每个服务的日志交错在单个流中。当您想要监视与时间相关的问题时，这非常有用。`-f` 标志跟随日志，因此将在生成实时输出时提供。

    如果您已经运行了命令，您将看到类似以下的输出：

    ```plaintext
    mysql_1  | 2019-10-03T03:07:16.083639Z 0 [Note] mysqld: ready for connections.
    mysql_1  | Version: '8.0.31'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
    app_1    | Connected to mysql db at host mysql
    app_1    | Listening on port 3000
    ```

    服务名称显示在行首（通常是彩色的），以帮助区分消息。如果您想查看特定服务的日志，可以将服务名称添加到日志命令的末尾（例如，`docker compose logs -f app`）。

4. 此时，您应该能够在浏览器中打开 [http://localhost:3000](http://localhost:3000) 上的应用程序并看到它正在运行。

## 在 Docker Desktop Dashboard 中查看应用程序堆栈

如果您查看 Docker Desktop Dashboard，您会看到有一个名为 **getting-started-app** 的组。这是来自 Docker Compose 的项目名称，用于将容器组合在一起。默认情况下，项目名称只是 `compose.yaml` 所在目录的名称。

如果您展开堆栈，您将看到在 Compose 文件中定义的两个容器。名称也更具描述性，因为它们遵循 `<service-name>-<replica-number>` 的模式。因此，很容易快速查看哪个容器是您的应用程序，哪个容器是 mysql 数据库。

## 全部拆除

当您准备好全部拆除时，只需运行 `docker compose down` 或在 Docker Desktop Dashboard 上点击整个应用程序的垃圾桶图标。容器将停止，网络将被删除。

> [!WARNING]
> 
> 默认情况下，当您运行 `docker compose down` 时，不会删除 compose 文件中的命名卷。如果您想删除卷，您需要添加 `--volumes` 标志。
> 
> 删除应用程序堆栈时，Docker Desktop Dashboard 不会删除卷。

## 总结

在本节中，您了解了 Docker Compose 以及它如何帮助您简化定义和共享多服务应用程序的方式。

相关信息：
 - [Compose 概览](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Compose CLI 参考](/reference/cli/docker/compose/_index.md)

## 下一步

接下来，您将学习一些可用于改进 Dockerfile 的最佳实践。

{{< button text="镜像构建最佳实践" url="09_image_best.md" >}}