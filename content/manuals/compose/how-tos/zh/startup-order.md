---
description: 了解如何使用 depends_on 和健康检查在 Docker Compose 中管理服务启动和关闭顺序。
keywords: docker compose startup order, compose shutdown order, depends_on, service healthcheck, control service dependencies
title: 控制 Compose 中的启动和关闭顺序
linkTitle: 控制启动顺序
weight: 30
aliases:
- /compose/startup-order/
---

您可以使用 [depends_on](/reference/compose-file/services.md#depends_on) 属性来控制服务启动和关闭的顺序。Compose 始终按依赖顺序启动和停止容器，其中依赖关系由 `depends_on`、`links`、`volumes_from` 和 `network_mode: "service:..."` 确定。

例如，如果您的应用程序需要访问数据库并且两个服务都使用 `docker compose up` 启动，则有可能失败，因为应用程序服务可能在数据库服务之前启动，而无法找到能够处理其 SQL 语句的数据库。

## 控制启动

在启动时，Compose 不会等待容器"就绪"，只等待它运行。如果例如您有一个关系型数据库系统需要在能够处理传入连接之前启动自己的服务，这可能会导致问题。

检测服务就绪状态的解决方案是使用 `condition` 属性与以下选项之一：

- `service_started`
- `service_healthy`。这指定依赖项预期在启动依赖服务之前是"健康的"，健康状态通过 `healthcheck` 定义。
- `service_completed_successfully`。这指定依赖项预期在启动依赖服务之前成功完成运行。

## 示例

```yaml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      retries: 5
      start_period: 30s
      timeout: 10s
```

Compose 按依赖顺序创建服务。`db` 和 `redis` 在 `web` 之前创建。

Compose 等待标记为 `service_healthy` 的依赖项通过健康检查。`db` 预期在创建 `web` 之前是"健康的"（由 `healthcheck` 指示）。

`restart: true` 确保如果 `db` 由于显式 Compose 操作（例如 `docker compose restart`）而更新或重启，`web` 服务也会自动重启，确保它重新建立连接或依赖关系正确。

`db` 服务的健康检查使用 `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}` 命令来检查 PostgreSQL 数据库是否就绪。该服务每 10 秒重试一次，最多 5 次。

Compose 还按依赖顺序删除服务。`web` 在 `db` 和 `redis` 之前被删除。

## 参考信息

- [`depends_on`](/reference/compose-file/services.md#depends_on)
- [`healthcheck`](/reference/compose-file/services.md#healthcheck)
