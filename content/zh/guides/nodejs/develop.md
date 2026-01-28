---
title: 使用容器进行 Node.js 开发
linkTitle: 开发你的应用
weight: 20
keywords: node, node.js, development
description: 学习如何使用容器在本地开发你的 Node.js 应用程序。
aliases:
  - /get-started/nodejs/develop/
  - /language/nodejs/develop/
  - /guides/language/nodejs/develop/
---

## 前提条件

完成[容器化 Node.js 应用程序](containerize.md)。

## 概述

在本节中，你将学习如何为容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置容器以运行开发环境
- 调试容器化应用程序

## 添加本地数据库并持久化数据

你可以使用容器来设置本地服务，比如数据库。在本节中，你将更新 `compose.yaml` 文件以定义数据库服务和用于持久化数据的卷。

1. 在 IDE 或文本编辑器中打开你的 `compose.yaml` 文件。
2. 取消注释与数据库相关的指令。以下是更新后的 `compose.yaml` 文件。

   > [!IMPORTANT]
   >
   > 在本节中，在收到指示之前不要运行 `docker compose up`。在中间步骤运行该命令可能会错误地初始化你的数据库。

   ```yaml {hl_lines="26-51",collapse=true,title=compose.yaml}
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
       environment:
         NODE_ENV: production
       ports:
         - 3000:3000

       # The commented out section below is an example of how to define a PostgreSQL
       # database that your application can use. `depends_on` tells Docker Compose to
       # start the database before your application. The `db-data` volume persists the
       # database data between container restarts. The `db-password` secret is used
       # to set the database password. You must create `db/password.txt` and add
       # a password of your choosing to it before running `docker compose up`.

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

3. 在 IDE 或文本编辑器中打开 `src/persistence/postgres.js`。你会注意到这个应用程序使用 Postgres 数据库，需要一些环境变量才能连接到数据库。`compose.yaml` 文件还没有定义这些变量。
4. 添加指定数据库配置的环境变量。以下是更新后的 `compose.yaml` 文件。

   ```yaml {hl_lines="16-19",collapse=true,title=compose.yaml}
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
       environment:
         NODE_ENV: production
         POSTGRES_HOST: db
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD_FILE: /run/secrets/db-password
         POSTGRES_DB: example
       ports:
         - 3000:3000

       # The commented out section below is an example of how to define a PostgreSQL
       # database that your application can use. `depends_on` tells Docker Compose to
       # start the database before your application. The `db-data` volume persists the
       # database data between container restarts. The `db-password` secret is used
       # to set the database password. You must create `db/password.txt` and add
       # a password of your choosing to it before running `docker compose up`.

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

5. 在 `server` 服务下添加 `secrets` 部分，以便你的应用程序安全地处理数据库密码。以下是更新后的 `compose.yaml` 文件。

   ```yaml {hl_lines="33-34",collapse=true,title=compose.yaml}
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
       environment:
         NODE_ENV: production
         POSTGRES_HOST: db
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD_FILE: /run/secrets/db-password
         POSTGRES_DB: example
       ports:
         - 3000:3000

       # The commented out section below is an example of how to define a PostgreSQL
       # database that your application can use. `depends_on` tells Docker Compose to
       # start the database before your application. The `db-data` volume persists the
       # database data between container restarts. The `db-password` secret is used
       # to set the database password. You must create `db/password.txt` and add
       # a password of your choosing to it before running `docker compose up`.

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

6. 在 `docker-nodejs-sample` 目录中，创建一个名为 `db` 的目录。
7. 在 `db` 目录中，创建一个名为 `password.txt` 的文件。这个文件将包含你的数据库密码。

   你的 `docker-nodejs-sample` 目录现在应该至少包含以下内容。

   ```text
   ├── docker-nodejs-sample/
   │ ├── db/
   │ │ └── password.txt
   │ ├── spec/
   │ ├── src/
   │ ├── .dockerignore
   │ ├── .gitignore
   │ ├── compose.yaml
   │ ├── Dockerfile
   │ ├── package-lock.json
   │ ├── package.json
   │ └── README.md
   ```

8. 在 IDE 或文本编辑器中打开 `password.txt` 文件，并指定你选择的密码。你的密码必须在单行上，文件中不能有其他额外的行。确保文件不包含任何换行符或其他隐藏字符。
9. 确保保存对所有修改过的文件的更改。
10. 运行以下命令启动你的应用程序。

    ```console
    $ docker compose up --build
    ```

11. 打开浏览器，在 [http://localhost:3000](http://localhost:3000) 验证应用程序正在运行。
12. 向待办事项列表添加一些项目以测试数据持久化。
13. 向待办事项列表添加一些项目后，在终端中按 `ctrl+c` 停止你的应用程序。
14. 在终端中，运行 `docker compose rm` 删除你的容器。

    ```console
    $ docker compose rm
    ```

15. 运行 `docker compose up` 再次运行你的应用程序。

    ```console
    $ docker compose up --build
    ```

16. 在浏览器中刷新 [http://localhost:3000](http://localhost:3000)，验证待办事项仍然存在，即使容器被删除并重新运行。

## 配置和运行开发容器

你可以使用绑定挂载将源代码挂载到容器中。这样容器可以立即看到你对代码所做的更改，只要你保存文件。这意味着你可以在容器中运行 nodemon 等进程，监视文件系统更改并对其做出响应。要了解更多关于绑定挂载的信息，请参阅[存储概述](/manuals/engine/storage/_index.md)。

除了添加绑定挂载外，你还可以配置 Dockerfile 和 `compose.yaml` 文件来安装开发依赖项并运行开发工具。

### 更新 Dockerfile 以用于开发

在 IDE 或文本编辑器中打开 Dockerfile。注意 Dockerfile 没有安装开发依赖项，也没有运行 nodemon。你需要更新 Dockerfile 来安装开发依赖项并运行 nodemon。

与其为生产环境创建一个 Dockerfile，为开发环境创建另一个 Dockerfile，不如使用一个多阶段 Dockerfile 来同时处理这两种情况。

将你的 Dockerfile 更新为以下多阶段 Dockerfile。

```dockerfile {hl_lines="5-26",collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

ARG NODE_VERSION=18.0.0

FROM node:${NODE_VERSION}-alpine as base
WORKDIR /usr/src/app
EXPOSE 3000

FROM base as dev
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --include=dev
USER node
COPY . .
CMD npm run dev

FROM base as prod
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev
USER node
COPY . .
CMD node src/index.js
```

在 Dockerfile 中，你首先在 `FROM node:${NODE_VERSION}-alpine` 语句后添加一个标签 `as base`。这让你可以在其他构建阶段引用这个构建阶段。接下来，你添加一个名为 `dev` 的新构建阶段来安装开发依赖项，并使用 `npm run dev` 启动容器。最后，你添加一个名为 `prod` 的阶段，它省略开发依赖项并使用 `node src/index.js` 运行应用程序。要了解更多关于多阶段构建的信息，请参阅[多阶段构建](/manuals/build/building/multi-stage.md)。

接下来，你需要更新 Compose 文件以使用新阶段。

### 更新 Compose 文件以用于开发

要使用 Compose 运行 `dev` 阶段，你需要更新 `compose.yaml` 文件。在 IDE 或文本编辑器中打开 `compose.yaml` 文件，然后添加 `target: dev` 指令以从多阶段 Dockerfile 中指向 `dev` 阶段。

此外，为服务器服务添加一个新的卷用于绑定挂载。对于这个应用程序，你将把本地机器上的 `./src` 挂载到容器中的 `/usr/src/app/src`。

最后，发布端口 `9229` 用于调试。

以下是更新后的 Compose 文件。所有注释已被删除。

```yaml {hl_lines=[5,8,20,21],collapse=true,title=compose.yaml}
services:
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
      - 9229:9229
    environment:
      NODE_ENV: production
      POSTGRES_HOST: db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD_FILE: /run/secrets/db-password
      POSTGRES_DB: example
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    volumes:
      - ./src:/usr/src/app/src
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

### 运行开发容器并调试应用程序

运行以下命令，使用对 `Dockerfile` 和 `compose.yaml` 文件的新更改来运行应用程序。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 验证应用程序正在运行。

你在本地机器上对应用程序源文件所做的任何更改现在都会立即反映在运行的容器中。

在 IDE 或文本编辑器中打开 `docker-nodejs-sample/src/static/js/app.js`，将第 109 行的按钮文本从 `Add Item` 更新为 `Add`。

```diff
+                         {submitting ? 'Adding...' : 'Add'}
-                         {submitting ? 'Adding...' : 'Add Item'}
```

在浏览器中刷新 [http://localhost:3000](http://localhost:3000)，验证更新后的文本是否出现。

你现在可以将检查器客户端连接到应用程序进行调试。有关检查器客户端的更多详细信息，请参阅 [Node.js 文档](https://nodejs.org/en/docs/guides/debugging-getting-started)。

## 总结

在本节中，你学习了如何设置 Compose 文件以添加模拟数据库并持久化数据。你还学习了如何创建多阶段 Dockerfile 并为开发设置绑定挂载。

相关信息：

- [卷顶级元素](/reference/compose-file/volumes/)
- [服务顶级元素](/reference/compose-file/services/)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，你将学习如何使用 Docker 运行单元测试。
