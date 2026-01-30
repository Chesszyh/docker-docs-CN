---
description: 了解如何在 Docker Engine 中使用 Graylog 扩展格式 (GELF) 日志驱动程序
keywords: graylog, gelf, logging, driver, 日志, 驱动程序
title: Graylog 扩展格式 (GELF) 日志驱动程序
---

`gelf` 日志驱动程序是一种便捷的格式，可被 [Graylog](https://www.graylog.org/)、[Logstash](https://www.elastic.co/products/logstash) 和 [Fluentd](https://www.fluentd.org/) 等多种工具理解。许多工具都使用这种格式。

在 GELF 中，每条日志消息都是一个包含以下字段的字典：

- 版本 (Version)
- 主机 (Host，即最初发送消息的机器)
- 时间戳 (Timestamp)
- 消息的短版本和长版本
- 您自己配置的任何自定义字段

## 用法

要将 `gelf` 驱动程序设置为默认日志驱动程序，请在 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json` 中的 `daemon.json` 文件中，将 `log-driver` 和 `log-opt` 键设置为适当的值。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例设置日志驱动程序为 `gelf` 并设置 `gelf-address` 选项。

```json
{
  "log-driver": "gelf",
  "log-opts": {
    "gelf-address": "udp://1.2.3.4:12201"
  }
}
```

重启 Docker 使更改生效。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。因此，布尔值和数值 (如 `gelf-tcp-max-reconnect` 的值) 必须用引号 (`"`) 括起来。

在运行 `docker container create` 或 `docker run` 时，可以通过设置 `--log-driver` 标志为特定容器设置日志驱动程序：

```console
$ docker run \
      --log-driver gelf --log-opt gelf-address=udp://1.2.3.4:12201 \
      alpine echo hello world
```

### GELF 选项

`gelf` 日志驱动程序支持以下选项：

| 选项                       | 是否必填 | 描述                                                                                                                                                                                                                                                                         | 示例值                                             |
| :------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `gelf-address`             | 必填     | GELF 服务器的地址。`tcp` 和 `udp` 是仅有的受支持 URI 标识符，且必须指定端口。                                                                                                                                                                 | `--log-opt gelf-address=udp://192.168.0.42:12201`  |
| `gelf-compression-type`    | 可选     | `仅限 UDP` GELF 驱动程序压缩每条日志消息所使用的压缩类型。允许的值有 `gzip`、`zlib` 和 `none`。默认为 `gzip`。请注意，启用压缩会导致过多的 CPU 占用，因此强烈建议将其设置为 `none`。            | `--log-opt gelf-compression-type=gzip`             |
| `gelf-compression-level`   | 可选     | `仅限 UDP` 当 `gelf-compression-type` 为 `gzip` 或 `zlib` 时的压缩级别。取值范围为 `-1` 到 `9` (最高压缩)。默认值为 1 (最高速度)。更高的级别提供更高的压缩率但速度更慢。`-1` 或 `0` 禁用压缩。 | `--log-opt gelf-compression-level=2`               |
| `gelf-tcp-max-reconnect`   | 可选     | `仅限 TCP` 连接断开时的最大重连尝试次数。正整数。默认值为 3。                                                                                                                                                            | `--log-opt gelf-tcp-max-reconnect=3`               |
| `gelf-tcp-reconnect-delay` | 可选     | `仅限 TCP` 重连尝试之间的等待秒数。正整数。默认值为 1。                                                                                                                                                                     | `--log-opt gelf-tcp-reconnect-delay=1`             |
| `tag`                      | 可选     | 附加到 `gelf` 消息中 `APP-NAME` 的字符串。默认情况下，Docker 使用容器 ID 的前 12 个字符来标记日志消息。参考 [日志标签选项文档](log_tags.md) 来自定义日志标签格式。                             | `--log-opt tag=mailer`                             |
| `labels`                   | 可选     | 在启动 Docker 守护进程时应用。该守护进程接受的以逗号分隔的日志相关标签列表。在 `extra` 字段中添加额外的键，前缀为下划线 (`_`)。用于高级 [日志标签选项](log_tags.md)。                                        | `--log-opt labels=production_status,geo`           |
| `labels-regex`             | 可选     | 分别与 `labels` 类似且兼容。一个用于匹配日志相关标签的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                    | `--log-opt labels-regex=^(production_status\|geo)` |
| `env`                      | 可选     | 在启动 Docker 守护进程时应用。该守护进程接受的以逗号分隔的日志相关环境变量列表。在 `extra` 字段中添加额外的键，前缀为下划线 (`_`)。用于高级 [日志标签选项](log_tags.md)。                         | `--log-opt env=os,customer`                        |
| `env-regex`                | 可选     | 分别与 `env` 类似且兼容。一个用于匹配日志相关环境变量的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                        | `--log-opt env-regex=^(os\|customer)`              |

> [!NOTE]
>
> `gelf` 驱动程序不支持 TCP 连接的 TLS。发送到受 TLS 保护的端点的消息可能会静默失败。

### 示例

此示例配置容器使用运行在 `192.168.0.42` 端口 `12201` 上的 GELF 服务器。

```console
$ docker run -dit \
    --log-driver=gelf \
    --log-opt gelf-address=udp://192.168.0.42:12201 \
    alpine sh
```
