---
description: Learn how to use the fluentd logging driver
keywords: Fluentd, docker, logging, driver
title: Fluentd 日志驱动程序
aliases:
  - /engine/reference/logging/fluentd/
  - /reference/logging/fluentd/
  - /engine/admin/logging/fluentd/
  - /config/containers/logging/fluentd/
---

`fluentd` 日志驱动程序将容器日志作为结构化日志数据发送到 [Fluentd](https://www.fluentd.org) 收集器。然后，用户可以使用 [Fluentd 的各种输出插件](https://www.fluentd.org/plugins)将这些日志写入各种目的地。

除了日志消息本身，`fluentd` 日志驱动程序还在结构化日志消息中发送以下元数据：

| 字段             | 描述                                                                                                                                                  |
| :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `container_id`   | 完整的 64 字符容器 ID。                                                                                                                               |
| `container_name` | 启动时的容器名称。如果你使用 `docker rename` 重命名容器，新名称不会反映在日志条目中。                                                                 |
| `source`         | `stdout` 或 `stderr`                                                                                                                                  |
| `log`            | 容器日志                                                                                                                                              |

## 用法

通过根据需要多次指定 `--log-opt` 来支持某些选项：

- `fluentd-address`：指定连接到 Fluentd 守护进程的套接字地址，例如 `fluentdhost:24224` 或 `unix:///path/to/fluentd.sock`。
- `tag`：为 Fluentd 消息指定标签。支持一些 Go 模板标记，例如 `{{.ID}}`、`{{.FullID}}` 或 `{{.Name}}` `docker.{{.ID}}`。

要将 `fluentd` 驱动程序用作默认日志驱动程序，请在 `daemon.json` 文件中将 `log-driver` 和 `log-opt` 键设置为适当的值，该文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动程序设置为 `fluentd` 并设置 `fluentd-address` 选项。

```json
{
  "log-driver": "fluentd",
  "log-opts": {
    "fluentd-address": "fluentdhost:24224"
  }
}
```

重启 Docker 以使更改生效。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。因此，布尔值和数值（如 `fluentd-async` 或 `fluentd-max-retries` 的值）必须用引号（`"`）括起来。

要为特定容器设置日志驱动程序，请将 `--log-driver` 选项传递给 `docker run`：

```console
$ docker run --log-driver=fluentd ...
```

在使用此日志驱动程序之前，启动一个 Fluentd 守护进程。日志驱动程序默认通过 `localhost:24224` 连接到此守护进程。使用 `fluentd-address` 选项连接到不同的地址。

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
```

如果容器无法连接到 Fluentd 守护进程，容器将立即停止，除非使用了 `fluentd-async` 选项。

## 选项

用户可以使用 `--log-opt NAME=VALUE` 标志指定额外的 Fluentd 日志驱动程序选项。

### fluentd-address

默认情况下，日志驱动程序连接到 `localhost:24224`。提供 `fluentd-address` 选项以连接到不同的地址。支持 `tcp`（默认）和 `unix` 套接字。

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=tcp://fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=unix:///path/to/fluentd.sock
```

上面的两个指定了相同的地址，因为 `tcp` 是默认值。

### tag

默认情况下，Docker 使用容器 ID 的前 12 个字符来标记日志消息。有关自定义日志标签格式，请参阅[日志标签选项文档](log_tags.md)。

### labels、labels-regex、env 和 env-regex

`labels` 和 `env` 选项各自接受以逗号分隔的键列表。如果 `label` 和 `env` 键之间存在冲突，则 `env` 的值优先。这两个选项都会向日志消息的额外属性添加额外字段。

`env-regex` 和 `labels-regex` 选项与 `env` 和 `labels` 类似并兼容。它们的值是用于匹配与日志相关的环境变量和标签的正则表达式。用于高级[日志标签选项](log_tags.md)。

### fluentd-async

Docker 在后台连接到 Fluentd。消息被缓冲直到连接建立。默认为 `false`。

### fluentd-async-reconnect-interval

当启用 `fluentd-async` 时，`fluentd-async-reconnect-interval` 选项定义重新建立与 `fluentd-address` 连接的间隔（以毫秒为单位）。如果地址解析为一个或多个 IP 地址（例如 Consul 服务地址），此选项很有用。

### fluentd-buffer-limit

设置内存中缓冲的事件数。记录将在内存中存储到达此数量。如果缓冲区已满，记录日志的调用将失败。默认值为 1048576。
(https://github.com/fluent/fluent-logger-golang/tree/master#bufferlimit)

### fluentd-retry-wait

重试之间的等待时间。默认为 1 秒。

### fluentd-max-retries

最大重试次数。默认为 `4294967295`（2\*\*32 - 1）。

### fluentd-sub-second-precision

以纳秒分辨率生成事件日志。默认为 `false`。

## 使用 Docker 管理 Fluentd 守护进程

关于 `Fluentd` 本身，请参阅[项目网页](https://www.fluentd.org)和[其文档](https://docs.fluentd.org)。

要使用此日志驱动程序，请在主机上启动 `fluentd` 守护进程。我们建议你使用 [Fluentd docker 镜像](https://hub.docker.com/r/fluent/fluentd/)。如果你想在每个主机上聚合多个容器日志，然后将日志传输到另一个 Fluentd 节点以创建聚合存储，此镜像特别有用。

### 测试容器日志记录器

1.  编写配置文件（`test.conf`）以转储输入日志：

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

3.  使用 `fluentd` 日志驱动程序启动一个或多个容器：

    ```console
    $ docker run --log-driver=fluentd your/application
    ```
