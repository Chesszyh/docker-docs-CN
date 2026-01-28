---
title: 在 Compose 中使用生命周期钩子
linkTitle: 使用生命周期钩子
weight: 20
description: 了解如何使用 Docker Compose 生命周期钩子（如 post_start 和 pre_stop）来自定义容器行为。
keywords: docker compose lifecycle hooks, post_start, pre_stop, docker compose entrypoint, docker container stop hooks, compose hook commands
---

{{< summary-bar feature_name="Compose lifecycle hooks" >}}

## 服务生命周期钩子

当 Docker Compose 运行容器时，它使用两个元素，即 [ENTRYPOINT 和 COMMAND](/manuals/engine/containers/run.md#default-command-and-options)，来管理容器启动和停止时发生的操作。

然而，有时使用生命周期钩子来单独处理这些任务会更容易 - 这些命令在容器启动后立即运行或在容器停止前运行。

生命周期钩子特别有用，因为它们可以拥有特殊权限（例如以 root 用户身份运行），即使容器本身出于安全考虑以较低权限运行。这意味着某些需要更高权限的任务可以在不影响容器整体安全性的情况下完成。

### Post-start 钩子

Post-start 钩子是在容器启动后运行的命令，但它们确切执行的时间没有保证。在容器 `entrypoint` 执行期间，钩子执行时间不能确保。

在提供的示例中：

- 该钩子用于将卷的所有权更改为非 root 用户（因为卷默认以 root 所有权创建）。
- 容器启动后，`chown` 命令将 `/data` 目录的所有权更改为用户 `1001`。

```yaml
services:
  app:
    image: backend
    user: 1001
    volumes:
      - data:/data
    post_start:
      - command: chown -R /data 1001:1001
        user: root

volumes:
  data: {} # Docker 卷以 root 所有权创建
```

### Pre-stop 钩子

Pre-stop 钩子是在容器被特定命令停止之前运行的命令（例如 `docker compose down` 或使用 `Ctrl+C` 手动停止）。如果容器自行停止或被突然终止，这些钩子将不会运行。

在以下示例中，在容器停止之前，会运行 `./data_flush.sh` 脚本来执行任何必要的清理操作。

```yaml
services:
  app:
    image: backend
    pre_stop:
      - command: ./data_flush.sh
```

## 参考信息

- [`post_start`](/reference/compose-file/services.md#post_start)
- [`pre_stop`](/reference/compose-file/services.md#pre_stop)
