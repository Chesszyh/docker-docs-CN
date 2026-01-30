---
description: 了解如何在 Docker Engine 中使用 syslog 日志驱动程序
keywords: syslog, docker, logging, driver, 日志, 驱动程序
title: Syslog 日志驱动程序
alias:
  - /engine/reference/logging/syslog/
  - /engine/admin/logging/syslog/
  - /config/containers/logging/syslog/
---

`syslog` 日志驱动程序将日志路由到 `syslog` 服务器。`syslog` 协议使用原始字符串作为日志消息，并支持有限的一组元数据。syslog 消息必须以特定方式格式化才有效。接收方可以从有效的消息中提取以下信息：

- 优先级 (Priority): 日志级别，如 `debug`、`warning`、`error`、`info`。
- 时间戳 (Timestamp): 事件发生的时间。
- 主机名 (Hostname): 事件发生的位置。
- 设施 (Facility): 记录消息的子系统，如 `mail` 或 `kernel`。
- 进程名称和进程 ID (PID): 生成日志的进程的名称和 ID。

该格式在 [RFC 5424](https://tools.ietf.org/html/rfc5424) 中定义，Docker 的 syslog 驱动程序以下述方式实现 [ABNF 参考](https://tools.ietf.org/html/rfc5424#section-6)：

```none
                TIMESTAMP SP HOSTNAME SP APP-NAME SP PROCID SP MSGID
                    +          +             +           |        +
                    |          |             |           |        |
                    |          |             |           |        |
       +------------+          +----+        |           +----+   +---------+
       v                            v        v                v             v
2017-04-01T17:41:05.616647+08:00 a.vm {taskid:aa,version:} 1787791 {taskid:aa,version:}
```

## 用法

要将 `syslog` 驱动程序设置为默认日志驱动程序，请在 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json` 中的 `daemon.json` 文件中，将 `log-driver` 和 `log-opt` 键设置为适当的值。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例设置日志驱动程序为 `syslog` 并设置 `syslog-address` 选项。`syslog-address` 选项支持 UDP 和 TCP；本示例使用 UDP。

```json
{
  "log-driver": "syslog",
  "log-opts": {
    "syslog-address": "udp://1.2.3.4:1111"
  }
}
```

重启 Docker 使更改生效。

> [!NOTE]
> 
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。数值和布尔值 (如 `syslog-tls-skip-verify` 的值) 必须用引号 (`"`) 括起来。

您可以通过向 `docker container create` 或 `docker run` 传递 `--log-driver` 标志来为特定容器设置日志驱动程序：

```console
$ docker run \
      --log-driver syslog --log-opt syslog-address=udp://1.2.3.4:1111 \
      alpine echo hello world
```

## 选项

支持以下日志选项作为 `syslog` 日志驱动程序的选项。它们可以作为默认值在 `daemon.json` 中设置，通过将其作为键值对添加到 `log-opts` JSON 数组中。也可以在启动容器时，通过为每个选项添加 `--log-opt <key>=<value>` 标志来针对特定容器设置。

| 选项                     | 描述                                                                                                                                                                                                                                                                                                      |
| :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `syslog-address`         | 外部 `syslog` 服务器的地址。URI 标识符可以是 `[tcp|udp|tcp+tls]://host:port`、`unix://path` 或 `unixgram://path`。如果传输协议是 `tcp`、`udp` 或 `tcp+tls`，默认端口为 `514`。                                                                                          |
| `syslog-facility`        | 要使用的 `syslog` 设施。可以是任何有效 `syslog` 设施的数字或名称。参考 [syslog 文档](https://tools.ietf.org/html/rfc5424#section-6.2.1)。                                                                                                                                      |
| `syslog-tls-ca-cert`     | 由 CA 签名的信任证书的绝对路径。如果地址协议不是 `tcp+tls`，则忽略此选项。                                                                                                                                                                                                   |
| `syslog-tls-cert`        | TLS 证书文件的绝对路径。如果地址协议不是 `tcp+tls`，则忽略此选项。                                                                                                                                                                                                                  |
| `syslog-tls-key`         | TLS 密钥文件的绝对路径。如果地址协议不是 `tcp+tls`，则忽略此选项。                                                                                                                                                                                                                          |
| `syslog-tls-skip-verify` | 如果设置为 `true`，则在连接 `syslog` 守护进程时跳过 TLS 验证。默认为 `false`。如果地址协议不是 `tcp+tls`，则忽略此选项。                                                                                                                                                      |
| `tag`                    | 附加到 `syslog` 消息中 `APP-NAME` 的字符串。默认情况下，Docker 使用容器 ID 的前 12 个字符来标记日志消息。参考 [日志标签选项文档](log_tags.md) 来自定义日志标签格式。                                                        |
| `syslog-format`          | 要使用的 `syslog` 消息格式。如果未指定，则使用本地 Unix syslog 格式，且不包含指定的主机名。指定 `rfc3164` 使用 RFC-3164 兼容格式，指定 `rfc5424` 使用 RFC-5424 兼容格式，或指定 `rfc5424micro` 使用具有微秒时间戳分辨率的 RFC-5424 兼容格式。 |
| `labels`                 | 在启动 Docker 守护进程时应用。该守护进程接受的以逗号分隔的日志相关标签列表。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                                 |
| `labels-regex`           | 在启动 Docker 守护进程时应用。分别与 `labels` 类似且兼容。一个用于匹配日志相关标签的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                        |
| `env`                    | 在启动 Docker 守护进程时应用。该守护进程接受的以逗号分隔的日志相关环境变量列表。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                  |
| `env-regex`              | 在启动 Docker 守护进程时应用。分别与 `env` 类似且兼容。一个用于匹配日志相关环境变量的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                            |
