--- 
title: 使用容器进行 PHP 开发
linkTitle: 开发你的应用
weight: 20
keywords: php, development
description: 了解如何使用容器在本地开发 PHP 应用程序。
alias:
  - /language/php/develop/
  - /guides/language/php/develop/
---

## 先决条件

完成 [容器化 PHP 应用程序](containerize.md)。

## 概览

在本节中，你将学习如何为容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 添加 phpMyAdmin 以与数据库交互
- 配置 Compose 以在你编辑并保存代码时自动更新正在运行的 Compose 服务
- 创建一个包含开发依赖项的开发容器

## 添加本地数据库并持久化数据

你可以使用容器设置本地服务，例如数据库。
要为示例应用程序执行此操作，你需要执行以下操作：

- 更新 `Dockerfile` 以安装扩展来连接到数据库
- 更新 `compose.yaml` 文件以添加数据库服务和卷来持久化数据

### 更新 Dockerfile 以安装扩展

要安装 PHP 扩展，你需要更新 `Dockerfile`。在 IDE 或文本编辑器中打开你的 Dockerfile，然后更新内容。以下 `Dockerfile` 包含一行新代码，用于安装 `pdo` 和 `pdo_mysql` 扩展。所有注释均已删除。

```dockerfile {hl_lines=11}
# syntax=docker/dockerfile:1

FROM composer:lts as deps
WORKDIR /app
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM php:8.2-apache as final
RUN docker-php-ext-install pdo pdo_mysql
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=deps app/vendor/ /var/www/html/vendor
COPY ./src /var/www/html
USER www-data
```

有关安装 PHP 扩展的更多详细信息，请参阅 [PHP 官方 Docker 镜像](https://hub.docker.com/_/php)。

### 更新 compose.yaml 文件以添加 db 并持久化数据

在 IDE 或文本编辑器中打开 `compose.yaml` 文件。你会注意到它已经包含用于 PostgreSQL 数据库和卷的注释掉的指令。对于此应用程序，你将使用 MariaDB。有关 MariaDB 的更多详细信息，请参阅 [MariaDB 官方 Docker 镜像](https://hub.docker.com/_/mariadb)。

在 IDE 或文本编辑器中打开 `src/database.php` 文件。你会注意到它读取环境变量以便连接到数据库。

在 `compose.yaml` 文件中，你需要更新以下内容：

1. 取消注释并更新 MariaDB 的数据库指令。
2. 向 server 服务添加一个 secret（机密）以传入数据库密码。
3. 将数据库连接环境变量添加到 server 服务。
4. 取消注释卷指令以持久化数据。

以下是更新后的 `compose.yaml` 文件。所有注释均已删除。

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data: []
secrets:
  db-password:
    file: db/password.txt
```

> [!NOTE]
> 
> 要了解有关 Compose 文件中指令的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用程序之前，请注意此 Compose 文件使用 `secrets` 并指定 `password.txt` 文件来保存数据库的密码。你必须创建此文件，因为它不包含在源存储库中。

在 `docker-php-sample` 目录中，创建一个名为 `db` 的新目录，并在该目录内创建一个名为 `password.txt` 的文件。在 IDE 或文本编辑器中打开 `password.txt` 并添加以下密码。密码必须在单行上，文件中没有其他行。

```text
example
```

保存并关闭 `password.txt` 文件。

现在你的 `docker-php-sample` 目录中应该有以下内容。

```text
├── docker-php-sample/
│ ├── .git/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── composer.json
│ ├── composer.lock
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

运行以下命令来启动你的应用程序。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:9000/database.php](http://localhost:9000/database.php) 查看应用程序。你应该看到一个简单的 Web 应用程序，其中包含文本和每次刷新都会增加的计数器。

在终端中按 `ctrl+c` 停止应用程序。

## 验证数据是否持久保存在数据库中

在终端中，运行 `docker compose rm` 删除你的容器，然后运行 `docker compose up` 再次运行你的应用程序。

```console
$ docker compose rm
$ docker compose up --build
```

在浏览器中刷新 [http://localhost:9000/database.php](http://localhost:9000/database.php) 并验证先前的计数是否仍然存在。如果没有卷，删除容器后数据库数据将不会持久存在。

在终端中按 `ctrl+c` 停止应用程序。

## 添加 phpMyAdmin 以与数据库交互

你可以通过更新 `compose.yaml` 文件轻松地将服务添加到你的应用程序栈。

更新你的 `compose.yaml` 以添加一个新的 phpMyAdmin 服务。有关更多详细信息，请参阅 [phpMyAdmin 官方 Docker 镜像](https://hub.docker.com/_/phpmyadmin)。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="42-49"}
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
  phpmyadmin:
    image: phpmyadmin
    ports:
      - 8080:80
    depends_on:
      - db
    environment:
      - PMA_HOST=db
volumes:
  db-data: []
secrets:
  db-password:
    file: db/password.txt
```

在终端中，运行 `docker compose up` 以再次运行你的应用程序。

```console
$ docker compose up --build
```

在浏览器中打开 [http://localhost:8080](http://localhost:8080) 以访问 phpMyAdmin。使用 `root` 作为用户名并使用 `example` 作为密码登录。你现在可以通过 phpMyAdmin 与数据库进行交互。

在终端中按 `ctrl+c` 停止应用程序。

## 自动更新服务

使用 Compose Watch 在你编辑并保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开你的 `compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="17-21"}
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
    develop:
      watch:
        - action: sync
          path: ./src
          target: /var/www/html
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
  phpmyadmin:
    image: phpmyadmin
    ports:
      - 8080:80
    depends_on:
      - db
    environment:
      - PMA_HOST=db
volumes:
  db-data: []
secrets:
  db-password:
    file: db/password.txt
```

运行以下命令以使用 Compose Watch 运行你的应用程序。

```console
$ docker compose watch
```

打开浏览器并验证应用程序正在 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 运行。

现在，对本地计算机上应用程序源文件的任何更改都将立即反映在正在运行的容器中。

在 IDE 或文本编辑器中打开 `hello.php` 并将字符串 `Hello, world!` 更新为 `Hello, Docker!`。

保存对 `hello.php` 的更改，然后等待几秒钟让应用程序同步。在浏览器中刷新 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 并验证是否显示更新后的文本。

在终端中按 `ctrl+c` 停止 Compose Watch。在终端中运行 `docker compose down` 以停止应用程序。

## 创建开发容器

此时，当你运行容器化应用程序时，Composer 不会安装开发依赖项。虽然这个小镜像非常适合生产，但它缺少你在开发时可能需要的工具和依赖项，并且不包含 `tests` 目录。你可以使用多阶段构建在同一个 Dockerfile 中构建开发和生产阶段。有关更多详细信息，请参阅 [多阶段构建](/manuals/build/building/multi-stage.md)。

在 `Dockerfile` 中，你需要更新以下内容：

1. 将 `deps` 阶段拆分为两个阶段。一个阶段用于生产 (`prod-deps`)，一个阶段 (`dev-deps`) 用于安装开发依赖项。
2. 创建一个通用的 `base` 阶段。
3. 创建一个新的 `development` 阶段用于开发。
4. 更新 `final` 阶段以从新的 `prod-deps` 阶段复制依赖项。

以下是更改前后的 `Dockerfile`。

{{< tabs >}}
{{< tab name="Before" >}}

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as deps
WORKDIR /app
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM php:8.2-apache as final
RUN docker-php-ext-install pdo pdo_mysql
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=deps app/vendor/ /var/www/html/vendor
COPY ./src /var/www/html
USER www-data
```

{{< /tab >}}
{{< tab name="After" >}}

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as prod-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM composer:lts as dev-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-interaction

FROM php:8.2-apache as base
RUN docker-php-ext-install pdo pdo_mysql
COPY ./src /var/www/html

FROM base as development
COPY ./tests /var/www/html/tests
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
COPY --from=dev-deps app/vendor/ /var/www/html/vendor

FROM base as final
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=prod-deps app/vendor/ /var/www/html/vendor
USER www-data
```

{{< /tab >}}
{{< /tabs >}}

通过添加针对开发阶段的指令来更新你的 `compose.yaml` 文件。

以下是 `compose.yaml` 文件的更新部分。

```yaml {hl_lines=5}
services:
  server:
    build:
      context: .
      target: development
      # ...
```

你的容器化应用程序现在将安装开发依赖项。

运行以下命令来启动你的应用程序。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:9000/hello.php](http://localhost:9000/hello.php) 查看应用程序。你应该仍然看到简单的 "Hello, Docker!" 应用程序。

在终端中按 `ctrl+c` 停止应用程序。

虽然应用程序看起来是一样的，但你现在可以使用开发依赖项。继续下一节以了解如何使用 Docker 运行测试。

## 总结

在本节中，你了解了如何设置 Compose 文件以添加本地数据库并持久化数据。你还学习了如何使用 Compose Watch 在更新代码时自动同步应用程序。最后，你学习了如何创建一个包含开发所需依赖项的开发容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件 watch](/manuals/compose/how-tos/file-watch.md)
- [Dockerfile 参考](/reference/dockerfile.md)
- [PHP 官方 Docker 镜像](https://hub.docker.com/_/php)

## 后续步骤

在下一节中，你将学习如何使用 Docker 运行单元测试。

