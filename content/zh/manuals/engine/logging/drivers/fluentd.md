---
description: 了解如何使用 fluentd 日志驱动程序
keywords: Fluentd, docker, logging, driver, 日志, 驱动程序
title: Fluentd 日志驱动程序
aliases:
  - /engine/reference/logging/fluentd/
  - /reference/logging/fluentd/
  - /engine/admin/logging/fluentd/
  - /config/containers/logging/fluentd/
---

`fluentd` 日志驱动程序将容器日志作为结构化日志数据发送到 [Fluentd](https://www.fluentd.org) 收集器。然后，用户可以使用 Fluentd 的 [各种输出插件](https://www.fluentd.org/plugins) 将这些日志写入不同的目的地。

除了日志消息本身外，`fluentd` 日志驱动程序还在结构化日志消息中发送以下元数据：

| 字段             | 描述                                                                                                                                           |
| :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `container_id`   | 完整的 64 位容器 ID。                                                                                                                   |
| `container_name` | 容器启动时的名称。如果您使用 `docker rename` 对容器进行重命名，新名称不会反映在日志条目中。 |
| `source`         | `stdout` 或 `stderr`                                                                                                                                  |
| `log`            | 容器日志内容                                                                                                                                     |

## 用法

可以通过多次指定 `--log-opt` 来支持一些选项：

- `fluentd-address`: 指定连接 Fluentd 守护进程的套接字地址，例如 `fluentdhost:24224` 或 `unix:///path/to/fluentd.sock`。
- `tag`: 指定 Fluentd 消息的标签。支持部分 Go 模板标记，例如 `{{.ID}}`、`{{.FullID}}` 或 `{{.Name}}`。

要将 `fluentd` 驱动程序设置为默认日志驱动程序，请在 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json` 中的 `daemon.json` 文件中，将 `log-driver` 和 `log-opt` 键设置为适当的值。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例设置日志驱动程序为 `fluentd` 并设置 `fluentd-address` 选项。

```json
{
  "log-driver": "fluentd",
  "log-opts": {
    "fluentd-address": "fluentdhost:24224"
  }
}
```

重启 Docker 使更改生效。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。因此，布尔值和数值 (如 `fluentd-async` 或 `fluentd-max-retries` 的值) 必须用引号 (`"`) 括起来。

要为特定容器设置日志驱动程序，请向 `docker run` 传递 `--log-driver` 选项：

```console
$ docker run --log-driver=fluentd ...
```

在使用此日志驱动程序之前，请启动 Fluentd 守护进程。日志驱动程序默认通过 `localhost:24224` 连接到该守护进程。使用 `fluentd-address` 选项可以连接到不同的地址。

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
```

如果容器无法连接到 Fluentd 守护进程，容器将立即停止，除非使用了 `fluentd-async` 选项。

## 选项

用户可以使用 `--log-opt NAME=VALUE` 标志来指定额外的 Fluentd 日志驱动程序选项。

### fluentd-address

默认情况下，日志驱动程序连接到 `localhost:24224`。提供 `fluentd-address` 选项可以连接到不同的地址。支持 `tcp` (默认) 和 `unix` 套接字。

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=tcp://fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=unix:///path/to/fluentd.sock
```

上面前两个指定的是相同的地址，因为 `tcp` 是默认值。

### tag

默认情况下，Docker 使用容器 ID 的前 12 个字符来标记日志消息。参考 [日志标签选项文档](log_tags.md) 来自定义日志标签格式。

### labels, labels-regex, env, 和 env-regex

`labels` 和 `env` 选项各接受一个以逗号分隔的键列表。如果 `label` 和 `env` 键之间发生冲突，则以 `env` 的值为准。这两个选项都会向日志消息的额外属性中添加额外字段。

`env-regex` 和 `labels-regex` 选项分别与 `env` 和 `labels` 类似且兼容。它们的值是正则表达式，用于匹配与日志相关的环境变量和标签。它用于高级 [日志标签选项](log_tags.md)。

### fluentd-async

Docker 在后台连接到 Fluentd。在连接建立之前，消息会被缓冲。默认为 `false`。

### fluentd-async-reconnect-interval

当启用 `fluentd-async` 时，`fluentd-async-reconnect-interval` 选项定义了重新建立与 `fluentd-address` 连接的间隔时间 (以毫秒为单位)。如果该地址解析为多个 IP 地址 (例如 Consul 服务地址)，此选项非常有用。

### fluentd-buffer-limit

设置内存中缓冲的事件数量。记录在内存中存储的数量上限。如果缓冲区已满，记录日志的调用将失败。默认值为 1048576。
(https://github.com/fluent/fluent-logger-golang/tree/master#bufferlimit)

### fluentd-retry-wait

重试之间的等待时间。默认为 1 秒。

### fluentd-max-retries

最大重试次数。默认为 `4294967295` (2\*\*32 - 1)。

### fluentd-sub-second-precision

生成纳秒级分辨率的事件日志。默认为 `false`。

## 使用 Docker 管理 Fluentd 守护进程

关于 Fluentd 本身，请参阅 [项目网页](https://www.fluentd.org) 及其 [文档](https://docs.fluentd.org)。

要使用此日志驱动程序，请在主机上启动 `fluentd` 守护进程。我们建议您使用 [Fluentd Docker 镜像](https://hub.docker.com/r/fluent/fluentd/)。如果您想在每台主机上聚合多个容器日志，稍后再将日志传输到另一个 Fluentd 节点以创建聚合存储，该镜像特别有用。

### 测试容器日志记录器

1.  编写一个配置文件 (`test.conf`) 来转储输入日志：

    ```text
    <source>
      @type forward
    </source>

    <match *>
      @type stdout
    </match>
    ```

2.  使用此配置文件启动 Fluentd 容器：

    ```console
    $ docker run -it -p 24224:24224 -v /path/to/conf/test.conf:/fluentd/etc/test.conf -e FLUENTD_CONF=test.conf fluent/fluentd:latest
    ```

3.  启动一个或多个使用 `fluentd` 日志驱动程序的容器：

    ```console
    $ docker run --log-driver=fluentd your/application
    ```
