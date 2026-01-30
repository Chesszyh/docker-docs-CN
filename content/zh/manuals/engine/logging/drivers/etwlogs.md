---
description: 了解如何在 Docker Engine 中使用 Windows 事件追踪 (ETW) 日志驱动程序
keywords: ETW, docker, logging, driver, 日志, 驱动程序
title: ETW 日志驱动程序
aliases:
  - /engine/admin/logging/etwlogs/
  - /config/containers/logging/etwlogs/
---

Windows 事件追踪 (Event Tracing for Windows, ETW) 日志驱动程序将容器日志作为 ETW 事件转发。ETW 代表 Windows 中的事件追踪，是 Windows 中用于追踪应用程序的通用框架。每个 ETW 事件都包含一条包含日志及其上下文信息的消息。客户端随后可以创建一个 ETW 监听器来监听这些事件。

此日志驱动程序向 Windows 注册的 ETW 提供程序 (provider) 的 GUID 标识符为：`{a3693192-9ed6-46d2-a981-f8226c8363bd}`。客户端创建一个 ETW 监听器并注册以监听来自该日志驱动程序提供程序的事件。提供程序和监听器的创建顺序无关紧要。客户端可以在提供程序向系统注册之前创建其 ETW 监听器并开始监听来自该提供程序的事件。

## 用法

以下是一个使用大多数 Windows 安装中都包含的 `logman` 实用程序来监听这些事件的示例：

1. `logman start -ets DockerContainerLogs -p {a3693192-9ed6-46d2-a981-f8226c8363bd} 0 0 -o trace.etl`
2. 通过向 `docker run` 命令添加 `--log-driver=etwlogs`，使用 `etwlogs` 驱动程序运行您的容器并生成日志消息。
3. `logman stop -ets DockerContainerLogs`
4. 这会生成一个包含事件的 `etl` 文件。将此文件转换为人类可读形式的一种方法是运行：`tracerpt -y trace.etl`。

每个 ETW 事件都包含一个以下格式的结构化消息字符串：

```text
container_name: %s, image_name: %s, container_id: %s, image_id: %s, source: [stdout | stderr], log: %s
```

消息中各项的详情如下：

| 字段             | 描述                                           |
| ---------------- | ---------------------------------------------- |
| `container_name` | 容器启动时的名称。                             |
| `image_name`     | 容器镜像的名称。                               |
| `container_id`   | 完整的 64 位容器 ID。                          |
| `image_id`       | 容器镜像的完整 ID。                            |
| `source`         | `stdout` 或 `stderr`。                         |
| `log`            | 容器日志消息。                                 |

以下是一个示例事件消息 (为了可读性，输出经过了格式化)：

```yaml
container_name: backstabbing_spence,
image_name: windowsservercore,
container_id: f14bb55aa862d7596b03a33251c1be7dbbec8056bbdead1da8ec5ecebbe29731,
image_id: sha256:2f9e19bd998d3565b4f345ac9aaf6e3fc555406239a4fb1b1ba879673713824b,
source: stdout,
log: Hello world!
```

客户端可以解析此消息字符串以获取日志消息及其上下文信息。时间戳在 ETW 事件中也是可用的。

> [!NOTE]
>
> 此 ETW 提供程序仅发布消息字符串，而不是特殊结构的 ETW 事件。因此，您不需要向系统注册清单 (manifest) 文件即可读取和解释其 ETW 事件。
