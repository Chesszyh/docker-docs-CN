---
description: Learn how to use the Graylog Extended Format logging driver with Docker Engine
keywords: graylog, gelf, logging, driver
title: Graylog 扩展格式日志驱动程序
aliases:
  - /engine/reference/logging/gelf/
  - /engine/admin/logging/gelf/
  - /config/containers/logging/gelf/
---

`gelf` 日志驱动程序是一种方便的格式，被许多工具理解，如 [Graylog](https://www.graylog.org/)、[Logstash](https://www.elastic.co/products/logstash) 和 [Fluentd](https://www.fluentd.org)。许多工具使用此格式。

在 GELF 中，每条日志消息都是一个包含以下字段的字典：

- 版本
- 主机（最初发送消息的来源）
- 时间戳
- 消息的短版本和长版本
- 你自己配置的任何自定义字段

## 用法

要将 `gelf` 驱动程序用作默认日志驱动程序，请在 `daemon.json` 文件中将 `log-driver` 和 `log-opt` 键设置为适当的值，该文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动程序设置为 `gelf` 并设置 `gelf-address` 选项。

```json
{
  "log-driver": "gelf",
  "log-opts": {
    "gelf-address": "udp://1.2.3.4:12201"
  }
}
```

重启 Docker 以使更改生效。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。因此，布尔值和数值（如 `gelf-tcp-max-reconnect` 的值）必须用引号（`"`）括起来。

你可以在使用 `docker container create` 或 `docker run` 时通过设置 `--log-driver` 标志为特定容器设置日志驱动程序：

```console
$ docker run \
      --log-driver gelf --log-opt gelf-address=udp://1.2.3.4:12201 \
      alpine echo hello world
```

### GELF 选项

`gelf` 日志驱动程序支持以下选项：

| 选项                       | 必需     | 描述                                                                                                                                                                                                                                                                                | 示例值                                             |
| :------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `gelf-address`             | 必需     | GELF 服务器的地址。`tcp` 和 `udp` 是唯一支持的 URI 指定符，你必须指定端口。                                                                                                                                                                                                          | `--log-opt gelf-address=udp://192.168.0.42:12201`  |
| `gelf-compression-type`    | 可选     | `仅限 UDP` GELF 驱动程序用于压缩每条日志消息的压缩类型。允许的值是 `gzip`、`zlib` 和 `none`。默认为 `gzip`。注意启用压缩会导致 CPU 使用率过高，因此强烈建议将其设置为 `none`。                                                                                                        | `--log-opt gelf-compression-type=gzip`             |
| `gelf-compression-level`   | 可选     | `仅限 UDP` 当 `gelf-compression-type` 为 `gzip` 或 `zlib` 时的压缩级别。范围为 `-1` 到 `9`（最佳压缩）的整数。默认值为 1（最快速度）。更高级别提供更多压缩但速度更慢。`-1` 或 `0` 禁用压缩。                                                                                          | `--log-opt gelf-compression-level=2`               |
| `gelf-tcp-max-reconnect`   | 可选     | `仅限 TCP` 连接断开时的最大重连尝试次数。正整数。默认值为 3。                                                                                                                                                                                                                        | `--log-opt gelf-tcp-max-reconnect=3`               |
| `gelf-tcp-reconnect-delay` | 可选     | `仅限 TCP` 重连尝试之间等待的秒数。正整数。默认值为 1。                                                                                                                                                                                                                              | `--log-opt gelf-tcp-reconnect-delay=1`             |
| `tag`                      | 可选     | 附加到 `gelf` 消息中 `APP-NAME` 的字符串。默认情况下，Docker 使用容器 ID 的前 12 个字符来标记日志消息。有关自定义日志标签格式，请参阅[日志标签选项文档](log_tags.md)。                                                                                                                | `--log-opt tag=mailer`                             |
| `labels`                   | 可选     | 启动 Docker 守护进程时应用。此守护进程接受的与日志相关的标签的逗号分隔列表。在 `extra` 字段上添加额外的键，以下划线（`_`）为前缀。用于高级[日志标签选项](log_tags.md)。                                                                                                               | `--log-opt labels=production_status,geo`           |
| `labels-regex`             | 可选     | 与 `labels` 类似并兼容。用于匹配与日志相关的标签的正则表达式。用于高级[日志标签选项](log_tags.md)。                                                                                                                                                                                  | `--log-opt labels-regex=^(production_status\|geo)` |
| `env`                      | 可选     | 启动 Docker 守护进程时应用。此守护进程接受的与日志相关的环境变量的逗号分隔列表。在 `extra` 字段上添加额外的键，以下划线（`_`）为前缀。用于高级[日志标签选项](log_tags.md)。                                                                                                           | `--log-opt env=os,customer`                        |
| `env-regex`                | 可选     | 与 `env` 类似并兼容。用于匹配与日志相关的环境变量的正则表达式。用于高级[日志标签选项](log_tags.md)。                                                                                                                                                                                 | `--log-opt env-regex=^(os\|customer)`              |

> [!NOTE]
>
> `gelf` 驱动程序不支持 TCP 连接的 TLS。发送到受 TLS 保护的输入的消息可能会静默失败。

### 示例

此示例配置容器使用运行在 `192.168.0.42` 端口 `12201` 上的 GELF 服务器。

```console
$ docker run -dit \
    --log-driver=gelf \
    --log-opt gelf-address=udp://192.168.0.42:12201 \
    alpine sh
```
