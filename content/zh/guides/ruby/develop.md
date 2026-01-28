---
title: 使用容器进行 Ruby on Rails 开发
linkTitle: 开发你的应用
weight: 40
keywords: ruby, local, development
description: 了解如何在本地开发你的 Ruby on Rails 应用程序。
aliases:
  - /language/ruby/develop/
  - /guides/language/ruby/develop/
---

## 先决条件

完成 [容器化 Ruby on Rails 应用程序](containerize.md)。

## 概述

在本节中，你将学习如何为你的容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose 以在你编辑和保存代码时自动更新正在运行的 Compose 服务

## 添加本地数据库并持久化数据

你可以使用容器来设置本地服务，例如数据库。在本节中，你将更新 `compose.yaml` 文件以定义数据库服务和用于持久化数据的卷。

在克隆的存储库目录中，在 IDE 或文本编辑器中打开 `compose.yaml` 文件。你需要将数据库密码文件作为环境变量添加到服务器服务，并指定要使用的密钥文件。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="07-25"}
services:
  web:
    build: .
    command: bundle exec rails s -b '0.0.0.0'
    ports:
      - "3000:3000"
    depends_on:
      - db
    environment:
      - RAILS_ENV=test
    env_file: "webapp.env"
  db:
    image: postgres:latest
    secrets:
      - db-password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
secrets:
  db-password:
    file: db/password.txt
```

> [!NOTE]
>
> 要了解有关 Compose 文件中指令的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

在使用 Compose 运行应用程序之前，请注意此 Compose 文件指定了一个 `password.txt` 文件来保存数据库的密码。你必须创建此文件，因为它不包含在源存储库中。

在克隆的存储库目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件，其中包含数据库的密码。使用你喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件中。

```text
mysecretpassword
```

保存并关闭 `password.txt` 文件。此外，在文件 `webapp.env` 中，你可以更改连接到数据库的密码。

你现在的 `docker-ruby-on-rails` 目录中应该有以下内容。

```text
.
├── Dockerfile
├── Gemfile
├── Gemfile.lock
├── README.md
├── Rakefile
├── app/
├── bin/
├── compose.yaml
├── config/
├── config.ru
├── db/
│   ├── development.sqlite3
│   ├── migrate
│   ├── password.txt
│   ├── schema.rb
│   └── seeds.rb
├── lib/
├── log/
├── public/
├── storage/
├── test/
├── tmp/
└── vendor
```

现在，运行以下 `docker compose up` 命令来启动你的应用程序。

```console
$ docker compose up --build
```

在 Ruby on Rails 中，`db:migrate` 是一个 Rake 任务，用于在数据库上运行迁移。迁移是一种随着时间的推移以一致且简单的方式更改数据库模式结构的方法。

```console
$ docker exec -it docker-ruby-on-rails-web-1 rake db:migrate RAILS_ENV=test
```

你会看到类似这样的消息：

`console
== 20240710193146 CreateWhales: migrating =====================================
-- create_table(:whales)
   -> 0.0126s
== 20240710193146 CreateWhales: migrated (0.0127s) ============================
`

在浏览器中刷新 <http://localhost:3000> 并添加 whales。

在终端中按 `ctrl+c` 停止你的应用程序，然后再次运行 `docker compose up`，whales 正在被持久化。

## 自动更新服务

使用 Compose Watch 在你编辑和保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开你的 `compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="13-16"}
services:
  web:
    build: .
    command: bundle exec rails s -b '0.0.0.0'
    ports:
      - "3000:3000"
    depends_on:
      - db
    environment:
      - RAILS_ENV=test
    env_file: "webapp.env"

    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:latest
    secrets:
      - db-password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
secrets:
  db-password:
    file: db/password.txt
```

运行以下命令以使用 Compose Watch 运行你的应用程序。

```console
$ docker compose watch
```

你本地机器上应用程序源文件的任何更改现在都将立即反映在正在运行的容器中。

在 IDE 或文本编辑器中打开 `docker-ruby-on-rails/app/views/whales/index.html.erb`，并通过添加感叹号更新 `Whales` 字符串。

```diff
-    <h1>Whales</h1>
+    <h1>Whales!</h1>
```

保存对 `index.html.erb` 的更改，然后等待几秒钟让应用程序重建。再次转到应用程序并验证是否显示了更新的文本。

在终端中按 `ctrl+c` 停止你的应用程序。

## 总结

在本节中，你了解了如何设置 Compose 文件以添加本地数据库并持久化数据。你还学习了如何在更新代码时使用 Compose Watch 自动重建并运行你的容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，你将学习如何在部署之前在 Kubernetes 上本地测试和调试你的工作负载。
