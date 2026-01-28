---
description: Learn about how to format log output with Go templates
keywords: docker, logging, driver, syslog, Fluentd, gelf, journald
title: 自定义日志驱动程序输出
aliases:
  - /engine/reference/logging/log_tags/
  - /engine/admin/logging/log_tags/
  - /config/containers/logging/log_tags/
---

`tag` 日志选项指定如何格式化用于标识容器日志消息的标签。默认情况下，系统使用容器 ID 的前 12 个字符。要覆盖此行为，请指定 `tag` 选项：

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=myhost.local:24224 --log-opt tag="mailer"
```

Docker 支持一些特殊的模板标记，你可以在指定标签值时使用：

| 标记               | 描述                                         |
| ------------------ | -------------------------------------------- |
| `{{.ID}}`          | 容器 ID 的前 12 个字符。                     |
| `{{.FullID}}`      | 完整的容器 ID。                              |
| `{{.Name}}`        | 容器名称。                                   |
| `{{.ImageID}}`     | 容器镜像 ID 的前 12 个字符。                 |
| `{{.ImageFullID}}` | 容器的完整镜像 ID。                          |
| `{{.ImageName}}`   | 容器使用的镜像名称。                         |
| `{{.DaemonName}}`  | Docker 程序的名称（`docker`）。              |

例如，指定 `--log-opt tag="{{.ImageName}}/{{.Name}}/{{.ID}}"` 值会产生如下 `syslog` 日志行：

```none
Aug  7 18:33:19 HOSTNAME hello-world/foobar/5790672ab6a0[9103]: Hello from Docker.
```

在启动时，系统会设置 `container_name` 字段和标签中的 `{{.Name}}`。如果你使用 `docker rename` 重命名容器，新名称不会反映在日志消息中。相反，这些消息继续使用原始容器名称。
