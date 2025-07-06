---
description: 了解如何在本地容器化数据库中运行、连接和持久化数据。
keywords: database, mysql
title: 使用容器化数据库
summary: |
  了解如何有效地运行和管理作为容器的数据库。
tags: [databases]
aliases:
  - /guides/use-case/databases/
params:
  time: 20 分钟
---

使用本地容器化数据库具有灵活性和易于设置的优点，
让您可以紧密地镜像生产环境，而无需
传统数据库安装的开销。Docker 简化了此过程，使您能够
通过几个命令在隔离的容器中部署、管理和扩展数据库。

在本指南中，您将学习如何：

- 运行本地容器化数据库
- 访问容器化数据库的 shell
- 从您的主机连接到容器化数据库
- 从另一个容器连接到容器化数据库
- 在卷中持久化数据库数据
- 构建自定义数据库镜像
- 使用 Docker Compose 运行数据库

本指南使用 MySQL 镜像作为示例，但这些概念可以应用于其他数据库镜像。

## 先决条件

要学习本指南，您必须安装 Docker。要安装 Docker，请参阅[获取 Docker](/get-started/get-docker.md)。

## 运行本地容器化数据库

大多数流行的数据库系统，包括 MySQL、PostgreSQL 和 MongoDB，都有
在 Docker Hub 上可用的 Docker 官方镜像。这些镜像是遵循最佳实践的精选
镜像集，确保您可以访问最新的
功能和安全更新。要开始使用，请访问
[Docker Hub](https://hub.docker.com) 并搜索您
感兴趣的数据库。每个镜像的页面都提供了有关如何运行
容器、自定义您的设置以及根据
您的需求配置数据库的详细说明。有关本指南中使用的 MySQL 镜像的更多信息，请参阅 Docker Hub [MySQL 镜像](https://hub.docker.com/_/mysql)页面。

要运行数据库容器，您可以使用 Docker Desktop GUI 或
CLI。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

要使用 CLI 运行容器，请在终端中运行以下命令：

```console
$ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -d mysql:latest
```

在此命令中：

- `--name my-mysql` 将名称 my-mysql 分配给您的容器，以便于
  引用。
- `-e MYSQL_ROOT_PASSWORD=my-secret-pw` 将 MySQL 的 root 密码设置为
  my-secret-pw。请将 my-secret-pw 替换为您选择的安全密码。
- `-e MYSQL_DATABASE=mydb` 可选地创建一个名为 mydb 的数据库。您可以
  将 mydb 更改为您想要的数据库名称。
- `-d` 以分离模式运行容器，这意味着它���后台运行。
- `mysql:latest` 指定您要使用最新版本的 MySQL
  镜像。

要验证您的容器正在运行，请在终端中运行 `docker ps`

{{< /tab >}}
{{< tab name="GUI" >}}

要使用 GUI 运行容器：

1. 在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。
2. 在搜索框中指定 `mysql`，如果尚未
   选择，请选择 `Images` 选项卡。
3. 将鼠标悬停在 `mysql` 镜像上，然后选择 `Run`。
   将出现 **运行新容器** 模式。
4. 展开 **可选设置**。
5. 在可选设置中，指定以下内容：

   - **容器名称**：`my-mysql`
   - **环境变量**：
     - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
     - `MYSQL_DATABASE`:`mydb`

   ![带有指定选项的可选设置屏幕。](images/databases-1.webp)

6. 选择 `Run`。
7. 在 Docker Desktop 仪表板中打开 **容器** 视图以验证您的
   容器正在运行。

{{< /tab >}}
{{< /tabs >}}

## 访问容器化数据库的 shell

当您在 Docker 容器内运行数据库时，您可能需要
访问其 shell 来管理数据库、执行命令或执行
管理任务。Docker 提供了一种使用
`docker exec` 命令的直接方法。此外，如果您更喜欢图形界面，您
可以使用 Docker Desktop 的 GUI。

如果您还没有运行数据��容器，请参阅
[运行本地容器化数据库](#run-a-local-containerized-database)。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

要使用 CLI 访问 MySQL 容器的终端，您可以使用
以下 `docker exec` 命令。

```console
$ docker exec -it my-mysql bash
```

在此命令中：

- `docker exec` 告诉 Docker 您要在正在运行的
  容器中执行命令。
- `-it` 确保您正在访问的终端是交互式的，因此您可以在其中
  键入命令。
- `my-mysql` 是您的 MySQL 容器的名称。如果您在运行时为容器指定了不同的名称
  ，请改用该名称。
- `bash` 是您要在容器内运行的命令。它会打开一个 bash
  shell，让您可以与容器的文件系统和已安装的
  应用程序进行交互。

执行此命令后，您将获得对 MySQL 容器内 bash shell 的访问权限
，您可以从中直接管理您的 MySQL 服务器。您可以
运行 `exit` 返回到您的终端。

{{< /tab >}}
{{< tab name="GUI" >}}

1. 打开 Docker Desktop 仪表板并选择 **容器** 视图。
2. 在容器的 **操作** 列中，选择 **显示容器
   操作**，然后选择 **在终端中打开**。

在此终端中，您可以访问 MySQL 容器内的 shell，您可以
从中直接管理您的 MySQL 服务器。

{{< /tab >}}
{{< /tabs >}}

一旦您访问了容器的终端，您就可以运行该容器中可用的任何工具
。以下示例显示了在容器中使用 `mysql` 来
列出数据库。

```console
# mysql -u root -p
Enter password: my-secret-pw

mysql> SHOW DATABASES;

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

## 从您的主机连接到容器化数据库

从您的主机连接到容器化数据库涉及将
容器内的端口映射到主机上的端口。此过程可确保
可以通过主机的
网络访问容器内的数据库。对于 MySQL，默认端口为 3306。通过公开此端口，您可以使用
主机上的各种数据库管理工具或应用程序
与您的 MySQL 数据库进行交互。

在开始之前，您必须删除您之前为此
指南运行的任何容器。要停止和删除容器，请执行以下任一操作：

- 在终端中，运行 `docker rm --force my-mysql` 以删除名为
  `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **容器** 视图中选择容器旁边的 **删除** 图标
  。

接下来，您可以使用 Docker Desktop GUI 或 CLI 来运行带有
端口映射的容器。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

在终端中运行以下命令。

```console
$ docker run -p 3307:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -d mysql:latest
```

在此命令中，`-p 3307:3306` 将主机上的端口 3307 映射到容器中的端口 3306。

要验证端口是否已映射，请运行以下命令。

```console
$ docker ps
```

您应该会看到类似以下的输出。

```console
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                               NAMES
6eb776cfd73c   mysql:latest   "docker-entrypoint.s…"   17 minutes ago   Up 17 minutes   33060/tcp, 0.0.0.0:3307->3306/tcp   my-mysql
```

{{< /tab >}}
{{< tab name="GUI" >}}

要使用 GUI 运行容器：

1. 在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。
2. 在搜索框中指定 `mysql`，如果尚未
   选择，请选择 `Images` 选项卡。
3. 将鼠标悬停在 `mysql` 镜像上，然后选择 `Run`。
   将出现 **运行新容器** 模式。
4. 展开 **可选设置**。
5. 在可选设置中，指定以下内容：

   - **容器名称**：`my-mysql`
   - **主机端口** 对于 **3306/tcp** 端口：`3307`
   - **环境变量**：
     - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
     - `MYSQL_DATABASE`:`mydb`

   ![带有指定选项的可选设置屏幕。](images/databases-2.webp)

6. 选择 `Run`。
7. 在 **容器** 视图中，验证端口是否在 **端口**
   列下映射。您应该会看到 **my-mysql**
   容器的 **3307:3306**。

{{< /tab >}}
{{< /tabs >}}

此时，在您的主机上运行的任何应用程序都可以在 `localhost:3307` 访问容器中的 MySQL 服务。

## 从另一个容器连接到容器化数据库

从另一个容器连接到容器化数据库是
微服务架构和开发过程中的常见
场景。
Docker 的网络功能使得建立此连接变得容易
，而无需将数据库暴露给主机网络。这是通过
将数据库容器和需要访问它的容器都放在
同一个 Docker 网络上实现的。

在开始之前，您必须删除您之前为此
指南运行的任何容器。要停止和删除容器，请执行以下任一操作：

- 在终端中，运行 `docker remove --force my-mysql` 以删除名为
  `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **容器** 视图中选择容器旁边的 **删除** 图标
  。

要创建网络并在其上运行容器：

1. 运行以下命令以创建名为 my-network 的 Docker 网络。

   ```console
   $ docker network create my-network
   ```

2. 运行您的数据库容器并使用 `--network`
   选项指定网络。这将在 my-network 网络上运行容器。

   ```console
   $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb --network my-network -d mysql:latest
   ```

3. 运行您的其他容器并使用 `--network`
   选项指定网络。对于此示例，您将运行一个可以连接
   到您的数据库的 phpMyAdmin 容器。

   1. 运行 phpMyAdmin 容器。使用 `--network` 选项指定
      网络，使用 `-p` 选项让您可以从主机
      访问容器，并使用 `-e` 选项指定此镜像
      所需的必需环境变量。

      ```console
      $ docker run --name my-phpmyadmin -d --network my-network -p 8080:80 -e PMA_HOST=my-mysql phpmyadmin
      ```

4. 验证容器可以通信。对于此示例，您将访问
   phpMyAdmin 并验证它是否连接到数据库。

   1. 打开 [http://localhost:8080](http://localhost:8080) 以访问您的 phpMyAdmin 容器。
   2. 使用 `root` 作为用户名和 `my-secret-pw` 作为密码登录。
      您应该连接到 MySQL 服务器并看到您的数据库列出。

此时，在您的 `my-network` 容器网络上运行的任何应用程序
都可以在 `my-mysql:3306` 访问容器中的 MySQL 服务。

## 在卷中持久化数据库数据

在 Docker 卷中持久化数据库数据对于确保您的
数据在容器重新启动和删除后仍然存在是必要的。Docker 卷可让您将
数据库文件存储在容器的可写层之外，从而可以
升级容器、切换基础并共享数据而不会丢失数据。以下是
如何使用 Docker CLI 或 Docker Desktop GUI 将卷附加到您的数据库容器。

在开始之前，您必须删除您之前为此
指南运行的任何容器。要停止和删除容器，请执行以下任一操作：

- 在终端中，运行 `docker remove --force my-mysql` 以删除名为
  `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **容器** 视图中选择容器旁边的 **删除** 图标
  。

接下来，您可以使用 Docker Desktop GUI 或 CLI 来运行带有卷的容器。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

要运行带有附加卷的数据库容器，请在您的 `docker run` 命令中包含 `-v` 选项
，并指定卷名和
数据库在容器内存储其数据的路径。如果卷不存在，
Docker 会自动为您创建它。

要运行带有附加卷的数据库容器，然后验证
数据是否持久化：

1. 运行容器并附加卷。

   ```console
   $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -v my-db-volume:/var/lib/mysql -d mysql:latest
   ```

   此命令将名为 `my-db-volume` 的卷挂载到容器中的 `/var/lib/mysql` 目录。

2. 在数据库中创建一些数据。使用 `docker exec` 命令在
   容器内运行 `mysql` 并创建一个表。

   ```console
   $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "CREATE TABLE IF NOT EXISTS mydb.mytable (column_name VARCHAR(255)); INSERT INTO mydb.mytable (column_name) VALUES ('value');"
   ```

   此命令使用容器中的 `mysql` 工具创建一个名为
   `mytable` 的表，其中包含一个名为 `column_name` 的列，最后插入一个
   `value` 的值。

3. 停止并删除容器。如果没有卷，您创建的表将在
   删除容器时丢失。

   ```console
   $ docker remove --force my-mysql
   ```

4. 启动一个带有附加卷的新容器。这一次，您不需要
   指定任何环境变量，因为配置已保存在
   卷中。

   ```console
   $ docker run --name my-mysql -v my-db-volume:/var/lib/mysql -d mysql:latest
   ```

5. 验证您创建的表仍然存在。再次使用 `docker exec` 命令
   在容器内运行 `mysql`。

   ```console
   $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "SELECT * FROM mydb.mytable;"
   ```

   此命令使用容器中的 `mysql` 工具从
   `mytable` 表中选择所有记录。

   您应该会看到类似以下的输出。

   ```console
   column_name
   value
   ```

{{< /tab >}}
{{< tab name="GUI" >}}

要运行带有附加卷的数据库容器，然后验证
数据是否持久化：

1. 运行带有附加卷的容器。

   1. 在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。
   2. 在搜索框中指定 `mysql`，如果尚未
      选择，请选择 **Images** 选项卡。
   3. 将鼠标悬停在 **mysql** 镜像上，然后选择 **Run**。
      将出现 **运行新容器** 模式。
   4. 展开 **可选设置**。
   5. 在可选设置中，指定以下内容：

      - **容器名称**：`my-mysql`
      - **环境变量**：
        - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
        - `MYSQL_DATABASE`:`mydb`
      - **卷**：
        - `my-db-volume`:`/var/lib/mysql`

      ![带有指定选项的可选设置屏幕。](images/databases-3.webp)

      在这里，卷的名称是 `my-db-volume`，它被挂载在
      容器中的 `/var/lib/mysql`。

   6. 选择 `Run`。

2. 在数据库中创建一些数据。

   1. 在 **容器** 视图中，在您的容器旁边选择 **显示
      容器操作** 图标，然后选择 **在终端中打开**。
   2. 在容器的终端中运���以下命令以添加一个表。

      ```console
      # mysql -u root -pmy-secret-pw -e "CREATE TABLE IF NOT EXISTS mydb.mytable (column_name VARCHAR(255)); INSERT INTO mydb.mytable (column_name) VALUES ('value');"
      ```

      此命令使用容器中的 `mysql` 工具创建一个名为
      `mytable` 的表，其中包含一个名为 `column_name` 的列，最后插入一个
      `value` 的值。

3. 在 **容器** 视图中，选择容器旁边的 **删除** 图标
   ，然后选择 **永久删除**。如果没有卷，您创建的表将在
   删除容器时丢失。
4. 运行带有附加卷的容器。

   1. 在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。
   2. 在搜索框中指定 `mysql`，如果尚未
      选择，请选择 **Images** 选项卡。
   3. 将鼠标悬停在 **mysql** 镜像上，然后选择 **Run**。
      将出现 **运行新容器** 模式。
   4. 展开 **可选设置**。
   5. 在可选设置中，指定以下内容：

      - **容器名称**：`my-mysql`
      - **环境变量**：
        - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
        - `MYSQL_DATABASE`:`mydb`
      - **卷**：
        - `my-db-volume`:`/var/lib/mysql`

      ![带有指定选项的可选设置屏幕。](images/databases-3.webp)

   6. 选择 `Run`。

5. 验证您创建的表仍然存在。

   1. 在 **容器** 视图中，在您的容器旁边选择 **显示
      容器操作** 图标，然后选择 **在终端中打开**。
   2. 在容器的终端中运行以下命令以验证您
      创建的表仍然存在。

      ```console
      # mysql -u root -pmy-secret-pw -e "SELECT * FROM mydb.mytable;"
      ```

      此命令使用容器中的 `mysql` 工具从
      `mytable` 表中选择所有记录。

      您应该会看到类似以下的输出。

      ```console
      column_name
      value
      ```

{{< /tab >}}
{{< /tabs >}}

此时，任何挂载 `my-db-volume` 的 MySQL 容器都将能够
访问和保存持久化数据。

## 构建自定义数据库镜像

自定义您的数据库镜像可让您在基础数据库服务器旁边包含其他配置、
脚本或工具。这对于
创建与您的特定开发或
生产环境需求相匹配的 Docker 镜像特别有用。以下示例概述了如何构建和
运行包含表初始化脚本的自定义 MySQL 镜像。

在开始之前，您必须删除您之前为此
指南运行的任何容器。要停止和删除容器，请执行以下任一操作：

- ��终端中，运行 `docker remove --force my-mysql` 以删除名为
  `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **容器** 视图中选择容器旁边的 **删除** 图标
  。

要构建和运行您的自定义镜像：

1. 创建一个 Dockerfile。

   1. 在您的项目目录中创建一个名为 `Dockerfile` 的文件。对于此
      示例，您可以在您选择的空目录中创建 `Dockerfile`
      。此文件将定义如何构建您的自定义 MySQL 镜像。
   2. 将以下内容添加到 `Dockerfile`。

      ```dockerfile
      # syntax=docker/dockerfile:1

      # 使用基础镜像 mysql:latest
      FROM mysql:latest

      # 设置环境变量
      ENV MYSQL_DATABASE mydb

      # 将自定义脚本或配置文件从您的主机复制到容器
      COPY ./scripts/ /docker-entrypoint-initdb.d/
      ```

      在此 Dockerfile 中，您已为 MySQL
      数据库名称设置了环境变量。您还可以使用 `COPY` 指令将自定义
      配置文件或脚本添加到容器中。在此
      示例中，您的主机的 `./scripts/` 目录中的文件被复制到
      容器的 `/docker-entrypoint-initdb.d/` 目录中。在此目录中，
      `.sh`、`.sql` 和 `.sql.gz` 脚本在容器
      首次启动时执行。有关 Dockerfile 的更多详细信息，��参阅
      [Dockerfile 参考](/reference/dockerfile/)。

   3. 创建一个脚本文件以在数据库中初始化一个表。在您的
      `Dockerfile` 所在的目录中，创建一个名为
      `scripts` 的子目录，然后创建一个名为 `create_table.sql` 的文件，其中包含
      以下内容。

   ```text
   CREATE TABLE IF NOT EXISTS mydb.myothertable (
     column_name VARCHAR(255)
   );

   INSERT INTO mydb.myothertable (column_name) VALUES ('other_value');
   ```

   您现在应该具有以下目录结构。

   ```text
   ├── your-project-directory/
   │ ├── scripts/
   │ │ └── create_table.sql
   │ └── Dockerfile
   ```

2. 构建您的镜像。

   1. 在终端中，将目录更改为您的 `Dockerfile`
      所在的目录。
   2. 运行以下命令以构建镜像。

      ```console
      $ docker build -t my-custom-mysql .
      ```

      在此命令中，`-t my-custom-mysql` 将您的新镜像标记（命名）为
      `my-custom-mysql`。命令末尾的句点 (.) 指定
      当前目录作为构建的上下文，Docker 在其中查找
      Dockerfile 和构建所需的任何其他文件。

3. 像在[运行本地容器化
   数据库](#run-a-local-containerized-database)中一样运行您的镜像。这一次，指定您的
   镜像���名称而不是 `mysql:latest`。此外，您不再需要指定
   `MYSQL_DATABASE` 环境变量，因为它现在由您的
   Dockerfile 定义。

   ```console
   $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d my-custom-mysql
   ```

4. 使用以下命令验证您的容器正在运行。

   ```console
   $ docker ps
   ```

   您应该会看到类似以下的输出。

   ```console
   CONTAINER ID   IMAGE              COMMAND                  CREATED        STATUS          PORTS                 NAMES
   f74dcfdb0e59   my-custom-mysql   "docker-entrypoint.s…"    2 hours ago    Up 51 minutes   3306/tcp, 33060/tcp   my-mysql
   ```

5. 验证您的初始化脚本已运行。在
   终端中运行以下命令以显示 `myothertable` 表的内容。

   ```console
   $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "SELECT * FROM mydb.myothertable;"
   ```

   您应该会看到类似以下的输出。

   ```console
   column_name
   other_value
   ```

使用您的 `my-custom-mysql` 镜像运行的任何容器都将在
首次启动时初始化该表。

## 使用 Docker Compose 运行数据库

Docker Compose 是一个用于定义和运行多容器 Docker
应用程序的工具。通过一个命令，您可以配置所有应用程序的
服务（如数据库、Web 应用程序��）并管理它们。在此示例中，
您将创建一个 Compose 文件并使用它来运行 MySQL 数据库容器和 phpMyAdmin 容器。

要使用 Docker Compose 运行您的容器：

1. 创建一个 Docker Compose 文件。

   1. 在您的项目目录中创建一个名为 `compose.yaml` 的文件。此文件
      将定义服务、网络和卷。
   2. 将以下内容添加到 `compose.yaml` 文件。

      ```yaml
      services:
        db:
          image: mysql:latest
          environment:
            MYSQL_ROOT_PASSWORD: my-secret-pw
            MYSQL_DATABASE: mydb
          ports:
            - 3307:3306
          volumes:
            - my-db-volume:/var/lib/mysql

        phpmyadmin:
          image: phpmyadmin/phpmyadmin:latest
          environment:
            PMA_HOST: db
            PMA_PORT: 3306
            MYSQL_ROOT_PASSWORD: my-secret-pw
          ports:
            - 8080:80
          depends_on:
            - db

      volumes:
        my-db-volume:
      ```

      对于数据库服务：

      - `db` 是服务的名称。
      - `image: mysql:latest` 指定该服务使用来自 Docker Hub 的最新 MySQL
        镜像。
      - `environment` 列出了 MySQL 用于
        初始化数据库的环境变量，例如 root 密码和数据库
        名称。
      - `ports` ���主机上的端口 3307 映射到容器中的端口 3306，
        允许您从主机连接到数据库。
      - `volumes` 将 `my-db-volume` 挂载到容器内的 `/var/lib/mysql`
        以持久化数据库数据。

      除了数据库服务之外，还有一个 phpMyAdmin 服务。默认情况下，Compose 会为您的应用程序设置一个单一网络。
      服务的每个容器都会加入默认网络，并且可以被该网络上的其他容器
      访问，并且可以通过服务名称发现。
      因此，在 `PMA_HOST` 环境变量中，您可以指定
      服务名称 `db`，以便连接到数据库服务。有关 Compose 的更多详细信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

2. 运行 Docker Compose。

   1. 打开一个终端并将目录更改为您的
      `compose.yaml` 文件所在的目录。
   2. 使用以下命令运行 Docker Compose。

      ```console
      $ docker compose up
      ```

      您现在可以在
      [http://localhost:8080](http://localhost:8080) 访问 phpMyAdmin 并使用
      `root` 作为用户名和 `my-secret-pw` 作为密码连接到您的
      数据库。

   3. 要停止容器，请在终端中按 `ctrl`+`c`。

现在，使用 Docker Compose，您可以通过一个命令启动您的数据库和应用程序、挂载卷��
配置网络等等。

## 总结

本指南向您介绍了使用容器化数据库（特别是
专注于 MySQL）的基本知识，以增强
开发环境的灵活性、易于设置和
一致性。
本指南中涵盖的用例不仅可以简化您的开发工作流程，还可以为您
准备更高级的数据库管理和部署方案，确保您的
数据驱动应用程序保持健壮和可扩展。

相关信息：

- [Docker Hub 数据库镜像](https://hub.docker.com/search?q=database&type=image)
- [Dockerfile 参考](/reference/dockerfile/)
- [Compose 文件参考](/reference/compose-file/)
- [CLI 参考](/reference/cli/docker/)
- [数据库示例](../../reference/samples/_index.md#databases)
