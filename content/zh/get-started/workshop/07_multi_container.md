---
title: 多容器应用程序
weight: 70
linkTitle: "第六部分：多容器应用程序"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers,
  docker desktop, 入门, 设置, 概览, 快速入门, 简介, 概念, 容器
description: 在您的应用程序中使用多个容器
aliases:
 - /get-started/07_multi_container/
 - /guides/workshop/07_multi_container/
---

到目前为止，您一直在使用单容器应用程序。但是，现在您将把 MySQL 添加到应用程序堆栈中。经常会出现以下问题 - “MySQL 将在哪里运行？将其安装在同一个容器中还是单独运行？”通常，每个容器应该做一件事并做好它。以下是单独运行容器的几个原因：

- 您很有可能需要以不同于数据库的方式扩展 API 和前端。
- 单独的容器允许您隔离地对版本进行版本控制和更新。
- 虽然您可以在本地使用容器作为数据库，但您可能希望在生产环境中使用数据库的托管服务。那样您就不希望将数据库引擎随应用程序一起发布。
- 运行多个进程将需要一个进程管理器（容器只启动一个进程），这增加了容器启动/关闭的复杂性。

还有更多原因。因此，如下图所示，最好在多个容器中运行您的应用程序。

![连接到 MySQL 容器的待办事项应用程序](images/multi-container.webp?w=350h=250)


## 容器网络

请记住，默认情况下，容器是隔离运行的，并且不知道同一台机器上的其他进程或容器。那么，如何允许一个容器与另一个容器通信呢？答案是网络。如果将两个容器放在同一个网络上，它们就可以相互通信。

## 启动 MySQL

有两种方法可以将容器放在网络上：
 - 启动容器时分配网络。
 - 将已运行的容器连接到网络。

在以下步骤中，您将首先创建网络，然后在启动时附加 MySQL 容器。

1. 创建网络。

   ```console
   $ docker network create todo-app
   ```

2. 启动一个 MySQL 容器并将其附加到网络。您还将定义一些环境变量，数据库将使用这些变量来初始化数据库。要了解有关 MySQL 环境变量的更多信息，请参阅 [MySQL Docker Hub 列表](https://hub.docker.com/_/mysql/)中的“环境变量”部分。

   {{< tabs >}}
   {{< tab name="Mac / Linux / Git Bash" >}}
   
   ```console
   $ docker run -d \
       --network todo-app --network-alias mysql \
       -v todo-mysql-data:/var/lib/mysql \
       -e MYSQL_ROOT_PASSWORD=secret \
       -e MYSQL_DATABASE=todos \
       mysql:8.0
   ```

   {{< /tab >}}
   {{< tab name="PowerShell" >}}

   ```powershell
   $ docker run -d ` \
       --network todo-app --network-alias mysql \
       -v todo-mysql-data:/var/lib/mysql \
       -e MYSQL_ROOT_PASSWORD=secret \
       -e MYSQL_DATABASE=todos \
       mysql:8.0
   ```
   
   {{< /tab >}}
   {{< tab name="Command Prompt" >}}

   ```console
   $ docker run -d ^ \
       --network todo-app --network-alias mysql ^
       -v todo-mysql-data:/var/lib/mysql ^
       -e MYSQL_ROOT_PASSWORD=secret ^
       -e MYSQL_DATABASE=todos ^
       mysql:8.0
   ```
   
   {{< /tab >}}
   {{< /tabs >}}
   
   在前面的命令中，您可以看到 `--network-alias` 标志。在后面的部分中，您将了解有关此标志的更多信息。

   > [!TIP]
   > 
   > 您会注意到上述命令中名为 `todo-mysql-data` 的卷挂载在 `/var/lib/mysql`，这是 MySQL 存储其数据的地方。但是，您从未运行过 `docker volume create` 命令。Docker 识别出您想要使用命名卷，并自动为您创建一个。

3. 要确认为数据库已启动并正在运行，请连接到数据库并验证其是否连接。

   ```console
   $ docker exec -it <mysql-container-id> mysql -u root -p
   ```

   当出现密码提示时，输入 `secret`。在 MySQL shell 中，列出数据库并验证您是否看到 `todos` 数据库。

   ```console
   mysql> SHOW DATABASES;
   ```

   您应该看到如下所示的输出：

   ```plaintext
   +--------------------+
   | Database           |
   +--------------------+
   | information_schema |
   | mysql              |
   | performance_schema |
   | sys                |
   | todos              |
   +--------------------+
   5 rows in set (0.00 sec)
   ```

4. 退出 MySQL shell 以返回到机器上的 shell。

   ```console
   mysql> exit
   ```

   您现在有一个 `todos` 数据库，随时可以使用。

## 连接到 MySQL

现在您知道 MySQL 已启动并正在运行，您可以使用它了。但是，如何使用它？如果在同一个网络上运行另一个容器，如何找到该容器？请记住，每个容器都有自己的 IP 地址。

为了回答上述问题并更好地理解容器网络，您将使用 [nicolaka/netshoot](https://github.com/nicolaka/netshoot) 容器，它附带了许多用于故障排除或调试网络问题的有用工具。

1. 使用 nicolaka/netshoot 镜像启动一个新容器。确保将其连接到同一个网络。

   ```console
   $ docker run -it --network todo-app nicolaka/netshoot
   ```

2. 在容器内部，您将使用 `dig` 命令，这是一个有用的 DNS 工具。您将查找主机名 `mysql` 的 IP 地址。

   ```console
   $ dig mysql
   ```

   您应该得到类似以下的输出。

   ```text
   ; <<>> DiG 9.18.8 <<>> mysql
   ;; global options: +cmd
   ;; Got answer:
   ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32162
   ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

   ;; QUESTION SECTION:
   ;mysql.			IN	A

   ;; ANSWER SECTION:
   mysql.			600	IN	A	172.23.0.2

   ;; Query time: 0 msec
   ;; SERVER: 127.0.0.11#53(127.0.0.11)
   ;; WHEN: Tue Oct 01 23:47:24 UTC 2019
   ;; MSG SIZE  rcvd: 44
   ```

   在“ANSWER SECTION”（应答部分）中，您将看到 `mysql` 的 `A` 记录解析为 `172.23.0.2`（您的 IP 地址很可能具有不同的值）。虽然 `mysql` 通常不是有效的主机名，但 Docker 能够将其解析为具有该网络别名的容器的 IP 地址。请记住，您之前使用了 `--network-alias`。

   这意味着您的应用程序只需要简单地连接到名为 `mysql` 的主机，它就会与数据库通信。

## 使用 MySQL 运行您的应用程序

待办事项应用程序支持设置一些环境变量来指定 MySQL 连接设置。它们是：

- `MYSQL_HOST` - 正在运行的 MySQL 服务器的主机名
- `MYSQL_USER` - 用于连接的用户名
- `MYSQL_PASSWORD` - 用于连接的密码
- `MYSQL_DB` - 连接后使用的数据库

> [!NOTE]
> 
> 虽然使用环境变量设置连接设置在开发中通常是可以接受的，但在生产环境中运行应用程序时，强烈不建议这样做。Diogo Monica，Docker 的前安全主管，[写了一篇精彩的博客文章](https://diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/)解释了原因。
> 
> 更安全的机制是使用容器编排框架提供的机密支持。在大多数情况下，这些机密作为文件挂载在正在运行的容器中。您会看到许多应用程序（包括 MySQL 镜像和待办事项应用程序）也支持带有 `_FILE` 后缀的环境变量，以指向包含该变量的文件。
> 
> 例如，设置 `MYSQL_PASSWORD_FILE` 变量将导致应用程序使用引用文件的内容作为连接密码。Docker 不做任何事情来支持这些环境变量。您的应用程序需要知道查找该变量并获取文件内容。

您现在可以启动开发就绪容器。

1. 指定之前的每个环境变量，并将容器连接到您的应用程序网络。运行此命令时，请确保您位于 `getting-started-app` 目录中。

   {{< tabs >}}
   {{< tab name="Mac / Linux" >}}

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
   
   {{< /tab >}}
   {{< tab name="PowerShell" >}}
   在 Windows 中，在 PowerShell 中运行此命令。

   ```powershell
   $ docker run -dp 127.0.0.1:3000:3000 ` \
     -w /app -v "$(pwd):/app" ` \
     --network todo-app ` \
     -e MYSQL_HOST=mysql ` \
     -e MYSQL_USER=root ` \
     -e MYSQL_PASSWORD=secret ` \
     -e MYSQL_DB=todos ` \
     node:18-alpine ` \
     sh -c "yarn install && yarn run dev"
   ```

   {{< /tab >}}
   {{< tab name="Command Prompt" >}}
   在 Windows 中，在命令提示符中运行此命令。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 ^ \
     -w /app -v "%cd%:/app" ^
     --network todo-app ^
     -e MYSQL_HOST=mysql ^
     -e MYSQL_USER=root ^
     -e MYSQL_PASSWORD=secret ^
     -e MYSQL_DB=todos ^
     node:18-alpine ^
     sh -c "yarn install && yarn run dev"
   ```

   {{< /tab >}}
   {{< tab name="Git Bash" >}}

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
     -w //app -v "/$(pwd):/app" \
     --network todo-app \
     -e MYSQL_HOST=mysql \
     -e MYSQL_USER=root \
     -e MYSQL_PASSWORD=secret \
     -e MYSQL_DB=todos \
     node:18-alpine \
     sh -c "yarn install && yarn run dev"
   ```
   
   {{< /tab >}}
   {{< /tabs >}}

2. 如果您查看容器的日志 (`docker logs -f <container-id>`)，您应该看到类似以下的消息，表明它正在使用 mysql 数据库。

   ```console
   $ nodemon src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching dir(s): *.*
   [nodemon] starting `node src/index.js`
   Connected to mysql db at host mysql
   Listening on port 3000
   ```

3. 在浏览器中打开应用程序，并将一些项目添加到待办事项列表中。

4. 连接到 mysql 数据库并证明项目正在写入数据库。记住，密码是 `secret`。

   ```console
   $ docker exec -it <mysql-container-id> mysql -p todos
   ```

   在 mysql shell 中，运行以下命令：

   ```console
   mysql> select * from todo_items;
   +--------------------------------------+--------------------+-----------+
   | id                                   | name               | completed |
   +--------------------------------------+--------------------+-----------+
   | c906ff08-60e6-44e6-8f49-ed56a0853e85 | Do amazing things! |         0 |
   | 2912a79e-8486-4bc3-a4c5-460793a575ab | Be awesome!        |         0 |
   +--------------------------------------+--------------------+-----------+
   ```

   您的表看起来会有所不同，因为它包含您的项目。但是，您应该看到它们存储在那里。

## 总结

此时，您拥有一个应用程序，该应用程序现在将其数据存储在单独容器中运行的外部数据库中。您了解了一些关于容器网络和使用 DNS 进行服务发现的知识。

相关信息：
 - [docker CLI 参考](/reference/cli/docker/)
 - [网络概览](/manuals/engine/network/_index.md)

## 下一步

很有可能您开始对启动此应用程序所需做的一切感到有点不知所措。您必须创建网络、启动容器、指定所有环境变量、公开端口等等。这需要记住很多东西，而且肯定会让将事情传递给其他人变得更加困难。

在下一节中，您将学习 Docker Compose。使用 Docker Compose，您可以以更简单的方式共享您的应用程序堆栈，并让其他人通过一个简单的命令启动它们。

{{< button text="使用 Docker Compose" url="08_using_compose.md" >}}