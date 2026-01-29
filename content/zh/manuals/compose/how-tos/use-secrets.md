---
title: 在 Docker Compose 中安全地管理机密 (Secrets)
linkTitle: Compose 中的机密
weight: 60
description: 了解如何在 Docker Compose 中安全地管理运行阶段和构建阶段的机密。
keywords: 机密, compose, 安全, 环境变量, docker 机密, 安全 Docker 构建, 容器中的敏感数据
tags: [机密]
aliases:
- /compose/use-secrets/
---

机密（secret）是指任何不应通过网络传输或以未加密方式存储在 Dockerfile 或应用程序源代码中的数据，例如密码、证书或 API 密钥。

{{% include "compose/secrets.md" %}}

环境变量通常对所有进程都可用，且难以跟踪访问情况。在调试错误时，它们也可能在您不知情的情况下被打印到日志中。使用机密功能可以降低这些风险。

## 使用机密

机密在容器内部被挂载为 `/run/secrets/<secret_name>` 路径下的文件。

将机密引入容器是一个两步过程。首先，使用 [Compose 文件中的顶级 secrets 元素](/reference/compose-file/secrets.md) 定义机密。接下来，更新您的服务定义，使用 [secrets 属性](/reference/compose-file/services.md#secrets) 引用它们所需的机密。Compose 按服务授予对机密的访问权限。

与其他方法不同，这允许通过标准文件系统权限在服务容器内进行细粒度的访问控制。

## 示例

### 单个服务的机密注入

在以下示例中，`frontend` 服务被授予了对 `my_secret` 机密的访问权限。在容器中，`/run/secrets/my_secret` 的内容被设置为文件 `./my_secret.txt` 的内容。

```yaml
services:
  myapp:
    image: myapp:latest
    secrets:
      - my_secret
secrets:
  my_secret:
    file: ./my_secret.txt
```

### 多个服务的机密共享和密码管理

```yaml
services:
   db:
     image: mysql:latest
     volumes:
       - db_data:/var/lib/mysql
     environment:
       MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_root_password
       - db_password

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_password


secrets:
   db_password:
     file: db_password.txt
   db_root_password:
     file: db_root_password.txt

volumes:
    db_data:
```
在上面的高级示例中：

- 每个服务下的 `secrets` 属性定义了您想要注入到该特定容器中的机密。
- 顶级 `secrets` 部分定义了变量 `db_password` 和 `db_root_password` ，并指定了提供其值的文件。
- 每个容器部署时，Docker 会在 `/run/secrets/<secret_name>` 下创建一个包含其特定值的临时文件系统挂载。

> [!NOTE]
>
> 这里演示的 `_FILE` 环境变量是某些镜像使用的一种约定，包括 [mysql](https://hub.docker.com/_/mysql) 和 [postgres](https://hub.docker.com/_/postgres) 等 Docker 官方镜像。

### 构建机密

在以下示例中，`npm_token` 机密在构建时可用。其值取自 `NPM_TOKEN` 环境变量。

```yaml
services:
  myapp:
    build:
      secrets:
        - npm_token
      context: .

secrets:
  npm_token:
    environment: NPM_TOKEN
```

## 资源

- [顶级 `secrets` 元素](/reference/compose-file/secrets.md)
- [服务级 `secrets` 属性](/reference/compose-file/services.md#secrets)
- [构建机密](https://docs.docker.com/build/building/secrets/)
