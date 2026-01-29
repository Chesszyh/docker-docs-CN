---
description: 了解如何使用 depends_on 和运行状况检查在 Docker Compose 中管理服务的启动和关闭顺序。
keywords: docker compose 启动顺序, compose 关闭顺序, depends_on, 服务运行状况检查, 控制服务依赖关系
title: 在 Compose 中控制启动和关闭顺序
linkTitle: 控制启动顺序
weight: 30
---

您可以使用 [`depends_on`](/reference/compose-file/services.md#depends_on) 属性来控制服务的启动和关闭顺序。Compose 始终按照依赖顺序启动和停止容器，依赖关系由 `depends_on`、`links`、`volumes_from` 以及 `network_mode: "service:..."` 确定。

例如，如果您的应用程序需要访问数据库，并且两个服务都通过 `docker compose up` 启动，那么很有可能会失败，因为应用程序服务可能会在数据库服务之前启动，从而找不到能够处理其 SQL 语句的数据库。 

## 控制启动

在启动时，Compose 不会等待容器“就绪”，而只等待它开始运行。这可能会导致问题，例如，如果您有一个关系数据库系统，它在能够处理传入连接之前需要先启动自己的服务。

检测服务就绪状态的解决方案是使用 `condition` 属性，并配合以下选项之一：

- `service_started`
- `service_healthy`：这指定在启动依赖服务之前，预期被依赖项必须是“健康”的（通过 `healthcheck` 定义）。
- `service_completed_successfully`：这指定在启动依赖服务之前，预期被依赖项必须运行直到成功完成。

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

Compose 按照依赖顺序创建服务。`db` 和 `redis` 会在 `web` 之前被创建。 

Compose 会等待标记为 `service_healthy` 的依赖项通过运行状况检查。在创建 `web` 之前，预期 `db` 必须是“健康”的（如 `healthcheck` 所指示）。

`restart: true` 确保如果 `db` 因显式的 Compose 操作（例如 `docker compose restart`）而被更新或重启，`web` 服务也会自动重启，从而确保它能正确地重新建立连接或依赖关系。

`db` 服务的运行状况检查使用 `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}` 命令来检查 PostgreSQL 数据库是否就绪。该服务每 10 秒重试一次，最多重试 5 次。

Compose 也会按照依赖顺序移除服务。`web` 会在 `db` 和 `redis` 之前被移除。

## 参考信息 

- [`depends_on`](/reference/compose-file/services.md#depends_on)
- [`healthcheck`](/reference/compose-file/services.md#healthcheck)
