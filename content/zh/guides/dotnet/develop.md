---
title: 使用容器进行 .NET 开发
linkTitle: 开发你的应用
weight: 20
keywords: .net, 开发
description: 学习如何使用容器在本地开发 .NET 应用程序。
aliases:
  - /language/dotnet/develop/
  - /guides/language/dotnet/develop/
---

## 前提条件

完成[容器化 .NET 应用程序](containerize.md)。

## 概述

在本节中，你将学习如何为容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose 以便在你编辑和保存代码时自动更新正在运行的 Compose 服务
- 创建一个包含 .NET Core SDK 工具和依赖项的开发容器

## 更新应用程序

本节使用 `docker-dotnet-sample` 仓库的不同分支，其中包含更新的 .NET 应用程序。更新的应用程序位于你在[容器化 .NET 应用程序](containerize.md)中克隆的仓库的 `add-db` 分支上。

要获取更新的代码，你需要切换到 `add-db` 分支。对于你在[容器化 .NET 应用程序](containerize.md)中所做的更改，在本节中你可以将它们暂存。在终端中，在 `docker-dotnet-sample` 目录中运行以下命令。

1. 暂存之前的任何更改。

   ```console
   $ git stash -u
   ```

2. 切换到包含更新应用程序的新分支。

   ```console
   $ git checkout add-db
   ```

在 `add-db` 分支中，只有 .NET 应用程序被更新了。Docker 资源尚未更新。

现在你的 `docker-dotnet-sample` 目录中应该有以下内容。

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── src/
│ │ ├── Data/
│ │ ├── Models/
│ │ ├── Pages/
│ │ ├── Properties/
│ │ ├── wwwroot/
│ │ ├── appsettings.Development.json
│ │ ├── appsettings.json
│ │ ├── myWebApp.csproj
│ │ └── Program.cs
│ ├── tests/
│ │ ├── tests.csproj
│ │ ├── UnitTest1.cs
│ │ └── Usings.cs
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

## 添加本地数据库并持久化数据

你可以使用容器来设置本地服务，如数据库。在本节中，你将更新 `compose.yaml` 文件以定义数据库服务和用于持久化数据的卷。

在 IDE 或文本编辑器中打开 `compose.yaml` 文件。你会注意到它已经包含了被注释掉的 PostgreSQL 数据库和卷的说明。

在 IDE 或文本编辑器中打开 `docker-dotnet-sample/src/appsettings.json`。你会注意到包含所有数据库信息的连接字符串。`compose.yaml` 已经包含此信息，但它被注释掉了。取消 `compose.yaml` 文件中数据库说明的注释。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="8-33"}
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
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
> 要了解更多关于 Compose 文件中指令的信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用程序之前，请注意此 Compose 文件使用 `secrets` 并指定了一个 `password.txt` 文件来保存数据库密码。你必须创建此文件，因为它不包含在源仓库中。

在 `docker-dotnet-sample` 目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件。在 IDE 或文本编辑器中打开 `password.txt` 并添加以下密码。密码必须在单独一行上，文件中不能有其他行。

```text
example
```

保存并关闭 `password.txt` 文件。

现在你的 `docker-dotnet-sample` 目录中应该有以下内容。

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

运行以下命令启动你的应用程序。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。你应该能看到一个简单的 Web 应用程序，显示文本 `Student name is`。

应用程序没有显示名字，因为数据库是空的。对于此应用程序，你需要访问数据库然后添加记录。

## 向数据库添加记录

对于示例应用程序，你必须直接访问数据库来创建示例记录。

你可以使用 `docker exec` 命令在数据库容器内运行命令。在运行该命令之前，你必须获取数据库容器的 ID。打开一个新的终端窗口并运行以下命令列出所有正在运行的容器。

```console
$ docker container ls
```

你应该看到类似以下的输出。

```console
CONTAINER ID   IMAGE                  COMMAND                  CREATED              STATUS                        PORTS                    NAMES
cb36e310aa7e   docker-dotnet-server   "dotnet myWebApp.dll"    About a minute ago   Up About a minute             0.0.0.0:8080->8080/tcp   docker-dotnet-server-1
39fdcf0aff7b   postgres               "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   5432/tcp                 docker-dotnet-db-1
```

在前面的示例中，容器 ID 是 `39fdcf0aff7b`。运行以下命令连接到容器中的 postgres 数据库。将容器 ID 替换为你自己的容器 ID。

```console
$ docker exec -it 39fdcf0aff7b psql -d example -U postgres
```

最后，向数据库插入一条记录。

```console
example=# INSERT INTO "Students" ("ID", "LastName", "FirstMidName", "EnrollmentDate") VALUES (DEFAULT, 'Whale', 'Moby', '2013-03-20');
```

你应该看到类似以下的输出。

```console
INSERT 0 1
```

运行 `exit` 关闭数据库连接并退出容器 shell。

```console
example=# exit
```

## 验证数据在数据库中持久化

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。你应该能看到一个简单的 Web 应用程序，显示文本 `Student name is Whale Moby`。

在终端中按 `ctrl+c` 停止你的应用程序。

在终端中，运行 `docker compose rm` 删除你的容器，然后运行 `docker compose up` 再次运行你的应用程序。

```console
$ docker compose rm
$ docker compose up --build
```

在浏览器中刷新 [http://localhost:8080](http://localhost:8080)，验证学生名字仍然存在，即使容器被删除并再次运行。

在终端中按 `ctrl+c` 停止你的应用程序。

## 自动更新服务

使用 Compose Watch 在你编辑和保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开 `compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="11-14"}
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
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

运行以下命令以使用 Compose Watch 运行你的应用程序。

```console
$ docker compose watch
```

打开浏览器并验证应用程序在 [http://localhost:8080](http://localhost:8080) 上运行。

现在，对本地机器上应用程序源文件的任何更改都将立即反映在正在运行的容器中。

在 IDE 或文本编辑器中打开 `docker-dotnet-sample/src/Pages/Index.cshtml`，并将第 13 行的学生名字文本从 `Student name is` 更新为 `Student name:`。

```diff
-    <p>Student Name is @Model.StudentName</p>
+    <p>Student name: @Model.StudentName</p>
```

保存对 `Index.cshmtl` 的更改，然后等待几秒钟让应用程序重建。在浏览器中刷新 [http://localhost:8080](http://localhost:8080)，验证更新后的文本是否出现。

在终端中按 `ctrl+c` 停止你的应用程序。

## 创建开发容器

此时，当你运行容器化应用程序时，它使用的是 .NET 运行时镜像。虽然这个小镜像适合生产环境，但它缺少开发时可能需要的 SDK 工具和依赖项。此外，在开发期间，你可能不需要运行 `dotnet publish`。你可以使用多阶段构建在同一个 Dockerfile 中构建用于开发和生产的阶段。有关更多详细信息，请参阅[多阶段构建](/manuals/build/building/multi-stage.md)。

向你的 Dockerfile 添加一个新的开发阶段，并更新你的 `compose.yaml` 文件以使用此阶段进行本地开发。

以下是更新后的 Dockerfile。

```Dockerfile {hl_lines="10-13"}
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
WORKDIR /app
COPY --from=build /app .
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines=[5,15,16]}
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: rebuild
          path: .
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
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

你的容器化应用程序现在将使用 `mcr.microsoft.com/dotnet/sdk:8.0-alpine` 镜像，其中包含开发工具如 `dotnet test`。继续下一节了解如何运行 `dotnet test`。

## 总结

在本节中，你了解了如何设置 Compose 文件以添加本地数据库并持久化数据。你还学习了如何使用 Compose Watch 在更新代码时自动重建和运行容器。最后，你学习了如何创建包含开发所需 SDK 工具和依赖项的开发容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，你将学习如何使用 Docker 运行单元测试。
