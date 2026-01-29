---
description: 了解合并 Compose 文件的工作原理
keywords: compose, docker, 合并, compose 文件
title: 合并 Compose 文件
linkTitle: 合并 (Merge)
weight: 10
aliases:
- /compose/multiple-compose-files/merge/
---

Docker Compose 允许您将一组 Compose 文件合并并覆盖，以创建一个复合的 Compose 文件。

默认情况下，Compose 会读取两个文件：`compose.yaml` 和可选的 `compose.override.yaml` 文件。按照惯例，`compose.yaml` 包含基础配置。覆盖文件可以包含对现有服务的配置覆盖，或者是全新的服务。

如果两个文件中都定义了同一个服务，Compose 会使用下文以及 [Compose 规范](/reference/compose-file/merge.md) 中描述的规则来合并配置。

## 如何合并多个 Compose 文件

要使用多个覆盖文件，或具有不同名称的覆盖文件，您可以使用预定义的 [COMPOSE_FILE](../environment-variables/envvars.md#compose_file) 环境变量，或者使用 `-f` 选项指定文件列表。 

Compose 按照在命令行中指定的顺序合并文件。后续文件可以合并、覆盖或补充其前面的文件。

例如：

```console
$ docker compose -f compose.yaml -f compose.admin.yaml run backup_db
```

`compose.yaml` 文件可能指定了一个 `webapp` 服务。

```yaml
webapp:
  image: examples/web
  ports:
    - "8000:8000"
  volumes:
    - "/data"
```

`compose.admin.yaml` 也可能指定这个相同的服务： 

```yaml
webapp:
  environment:
    - DEBUG=1
```

任何匹配的字段都会覆盖前一个文件。新的值则会添加到 `webapp` 服务配置中：

```yaml
webapp:
  image: examples/web
  ports:
    - "8000:8000"
  volumes:
    - "/data"
  environment:
    - DEBUG=1
```

## 合并规则 

- 路径相对于基础文件进行评估。当您使用多个 Compose 文件时，必须确保文件中的所有路径都相对于基础 Compose 文件（即使用 `-f` 指定的第一个 Compose 文件）。这是必要的，因为覆盖文件不一定是完整的有效 Compose 文件。覆盖文件可以包含配置的小片段。跟踪服务的哪个片段相对于哪个路径是困难且容易混淆的，因此为了使路径易于理解，所有路径都必须相对于基础文件定义。

   >[!TIP]
   >
   > 您可以使用 `docker compose config` 来查看合并后的配置，从而避免路径相关的问题。

- Compose 将配置从原始服务复制到本地服务。如果一个配置选项在原始服务和本地服务中都有定义，则本地的值会替换或扩展原始值。

   - 对于 `image`、`command` 或 `mem_limit` 等单值选项，新值会替换旧值。

      原始服务：

      ```yaml
      services:
        myservice:
          # ...
          command: python app.py
      ```

      本地服务：

      ```yaml
      services:
        myservice:
          # ...
          command: python otherapp.py
      ```

      结果：

      ```yaml
      services:
        myservice:
          # ...
          command: python otherapp.py
      ```

   - 对于多值选项 `ports`、`expose`、`external_links`、`dns`、`dns_search` 和 `tmpfs` ，Compose 会将两组值连接起来：

      原始服务：

      ```yaml
      services:
        myservice:
          # ...
          expose:
            - "3000"
      ```

      本地服务：

      ```yaml
      services:
        myservice:
          # ...
          expose:
            - "4000"
            - "5000"
      ```

      结果：

      ```yaml
      services:
        myservice:
          # ...
          expose:
            - "3000"
            - "4000"
            - "5000"
      ```

   - 对于 `environment`、`labels`、`volumes` 和 `devices` ，Compose 会将条目“合并”在一起，且本地定义的值具有优先级。对于 `environment` 和 `labels` ，由环境变量名或标签名决定使用哪个值：

      原始服务：

      ```yaml
      services:
        myservice:
          # ...
          environment:
            - FOO=original
            - BAR=original
      ```

      本地服务：

      ```yaml
      services:
        myservice:
          # ...
          environment:
            - BAR=local
            - BAZ=local
      ```

     结果：

      ```yaml
      services:
        myservice:
          # ...
          environment:
            - FOO=original
            - BAR=local
            - BAZ=local
      ```

   - `volumes` 和 `devices` 的条目根据容器内的挂载路径进行合并：

      原始服务：

      ```yaml
      services:
        myservice:
          # ...
          volumes:
            - ./original:/foo
            - ./original:/bar
      ```

      本地服务：

      ```yaml
      services:
        myservice:
          # ...
          volumes:
            - ./local:/bar
            - ./local:/baz
      ```

      结果：

      ```yaml
      services:
        myservice:
          # ...
          volumes:
            - ./original:/foo
            - ./local:/bar
            - ./local:/baz
      ```

有关更多合并规则，请参阅 Compose 规范中的 [合并与覆盖 (Merge and override)](/reference/compose-file/merge.md)。 

### 补充信息

- 使用 `-f` 是可选的。如果未提供，Compose 会在工作目录及其父目录中搜索 `compose.yaml` 和 `compose.override.yaml` 文件。您必须至少提供 `compose.yaml` 文件。如果这两个文件存在于同一级目录中，Compose 会将它们组合成一个单一的配置。

- 您可以使用带有连字符 `-` 的 `-f` 作为文件名，以从 `stdin`（标准输入）读取配置。例如： 
   ```console
   $ docker compose -f - <<EOF
     webapp:
       image: examples/web
       ports:
        - "8000:8000"
       volumes:
        - "/data"
       environment:
        - DEBUG=1
     EOF
   ```
   
   使用 `stdin` 时，配置中的所有路径都相对于当前工作目录。
   
- 您可以使用 `-f` 标志来指定不在当前目录中的 Compose 文件的路径，既可以在命令行中指定，也可以通过在 shell 或环境文件中设置 [COMPOSE_FILE 环境变量](../environment-variables/envvars.md#compose_file) 来实现。

   例如，如果您正在运行 [Compose Rails 示例](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/rails/README.md)，并且在名为 `sandbox/rails` 的目录中有一个 `compose.yaml` 文件。通过如下使用 `-f` 标志，您可以从任何地方运行类似 [docker compose pull](/reference/cli/docker/compose/pull.md) 的命令来获取 `db` 服务的 Postgres 镜像：`docker compose -f ~/sandbox/rails/compose.yaml pull db`

   完整示例如下：

   ```console
   $ docker compose -f ~/sandbox/rails/compose.yaml pull db
   Pulling db (postgres:latest)...
   latest: Pulling from library/postgres
   ef0380f84d05: Pull complete
   50cf91dc1db8: Pull complete
   d3add4cd115c: Pull complete
   467830d8a616: Pull complete
   089b9db7dc57: Pull complete
   6fba0a36935c: Pull complete
   81ef0e73c953: Pull complete
   338a6c4894dc: Pull complete
   15853f32f67c: Pull complete
   044c83d92898: Pull complete
   17301519f133: Pull complete
   dcca70822752: Pull complete
   cecf11b8ccf3: Pull complete
   Digest: sha256:1364924c753d5ff7e2260cd34dc4ba05ebd40ee8193391220be0f9901d4e1651
   Status: Downloaded newer image for postgres:latest
   ```

## 示例

多个文件的一个常见用例是针对类生产环境（可能是生产、分阶段发布或 CI）更改开发版的 Compose 应用。为了支持这些差异，您可以将 Compose 配置拆分为几个不同的文件：

首先从一个定义了服务规范配置的基础文件开始。

`compose.yaml`

```yaml
services:
  web:
    image: example/my_web_app:latest
    depends_on:
      - db
      - cache

  db:
    image: postgres:latest

  cache:
    image: redis:latest
```

在此示例中，开发配置向宿主机暴露了一些端口，将我们的代码挂载为一个卷，并构建 Web 镜像。

`compose.override.yaml`

```yaml
services:
  web:
    build: .
    volumes:
      - '.:/code'
    ports:
      - 8883:80
    environment:
      DEBUG: 'true'

  db:
    command: '-d'
    ports:
     - 5432:5432

  cache:
    ports:
      - 6379:6379
```

当您运行 `docker compose up` 时，它会自动读取这些覆盖项。

要在生产环境中使用此 Compose 应用，可以创建另一个覆盖文件，该文件可能存储在不同的 Git 仓库中或由不同的团队管理。

`compose.prod.yaml`

```yaml
services:
  web:
    ports:
      - 80:80
    environment:
      PRODUCTION: 'true'

  cache:
    environment:
      TTL: '500'
```

要使用此生产环境 Compose 文件进行部署，您可以运行：

```console
$ docker compose -f compose.yaml -f compose.prod.yaml up -d
```

这将使用 `compose.yaml` 和 `compose.prod.yaml` 中的配置来部署所有三个服务，而不会使用 `compose.override.yaml` 中的开发配置。

有关更多信息，请参阅 [在生产环境中使用 Compose](../production.md)。 

## 局限性

Docker Compose 支持应用程序模型中包含的许多资源的相对路径：服务镜像的构建上下文、定义环境变量文件的位置、绑定挂载卷中使用的本地目录路径。有了这样的约束，单体仓库（monorepo）中的代码组织可能会变得困难，因为自然的选择是为每个团队或组件设置专门的文件夹，但这样一来，Compose 文件的相对路径就会变得牛头不对马嘴。 

## 参考信息

- [合并规则](/reference/compose-file/merge.md)
