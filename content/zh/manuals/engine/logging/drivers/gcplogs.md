---
description: Learn how to use the Google Cloud Logging driver with Docker Engine
keywords: gcplogs, google, docker, logging, driver
title: Google Cloud Logging 日志驱动程序
aliases:
  - /engine/admin/logging/gcplogs/
  - /config/containers/logging/gcplogs/
---

Google Cloud Logging 驱动程序将容器日志发送到 [Google Cloud Logging](https://cloud.google.com/logging/docs/) Logging。

## 用法

要将 `gcplogs` 驱动程序用作默认日志驱动程序，请在 `daemon.json` 文件中将 `log-driver` 和 `log-opt` 键设置为适当的值，该文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动程序设置为 `gcplogs` 并设置 `gcp-meta-name` 选项。

```json
{
  "log-driver": "gcplogs",
  "log-opts": {
    "gcp-meta-name": "example-instance-12345"
  }
}
```

重启 Docker 以使更改生效。

你可以使用 `docker run` 的 `--log-driver` 选项为特定容器设置日志驱动程序：

```console
$ docker run --log-driver=gcplogs ...
```

如果 Docker 检测到它正在 Google Cloud 项目中运行，它会从[实例元数据服务](https://cloud.google.com/compute/docs/metadata)发现配置。否则，用户必须使用 `--gcp-project` 日志选项指定要记录到哪个项目，Docker 会尝试从 [Google 应用程序默认凭证](https://developers.google.com/identity/protocols/application-default-credentials)获取凭证。`--gcp-project` 标志优先于从元数据服务器发现的信息，因此在 Google Cloud 项目中运行的 Docker 守护进程可以被覆盖以记录到不同的项目，使用 `--gcp-project`。

Docker 从 Google Cloud 元数据服务器获取区域、实例名称和实例 ID 的值。如果元数据服务器不可用，可以通过选项提供这些值。它们不会覆盖元数据服务器的值。

## gcplogs 选项

你可以使用 `--log-opt NAME=VALUE` 标志指定以下额外的 Google Cloud Logging 驱动程序选项：

| 选项            | 必需     | 描述                                                                                                                                                         |
| :-------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gcp-project`   | 可选     | 要记录到哪个 Google Cloud 项目。默认从 Google Cloud 元数据服务器发现此值。                                                                                    |
| `gcp-log-cmd`   | 可选     | 是否记录容器启动时使用的命令。默认为 false。                                                                                                                 |
| `labels`        | 可选     | 以逗号分隔的标签键列表，如果为容器指定了这些标签，则应包含在消息中。                                                                                         |
| `labels-regex`  | 可选     | 与 `labels` 类似并兼容。用于匹配与日志相关的标签的正则表达式。用于高级[日志标签选项](log_tags.md)。                                                           |
| `env`           | 可选     | 以逗号分隔的环境变量键列表，如果为容器指定了这些变量，则应包含在消息中。                                                                                     |
| `env-regex`     | 可选     | 与 `env` 类似并兼容。用于匹配与日志相关的环境变量的正则表达式。用于高级[日志标签选项](log_tags.md)。                                                          |
| `gcp-meta-zone` | 可选     | 实例的区域名称。                                                                                                                                             |
| `gcp-meta-name` | 可选     | 实例名称。                                                                                                                                                   |
| `gcp-meta-id`   | 可选     | 实例 ID。                                                                                                                                                    |

如果 `label` 和 `env` 键之间存在冲突，则 `env` 的值优先。这两个选项都会向日志消息的属性添加额外字段。

以下是记录到默认日志目的地（通过查询 Google Cloud 元数据服务器发现）所需的日志选项示例。

```console
$ docker run \
    --log-driver=gcplogs \
    --log-opt labels=location \
    --log-opt env=TEST \
    --log-opt gcp-log-cmd=true \
    --env "TEST=false" \
    --label location=west \
    your/application
```

此配置还指示驱动程序在负载中包含标签 `location`、环境变量 `ENV` 以及用于启动容器的命令。

以下示例显示了在 Google Cloud 外部运行时的日志选项。必须为守护进程设置 `GOOGLE_APPLICATION_CREDENTIALS` 环境变量，例如通过 systemd：

```ini
[Service]
Environment="GOOGLE_APPLICATION_CREDENTIALS=uQWVCPkMTI34bpssr1HI"
```

```console
$ docker run \
    --log-driver=gcplogs \
    --log-opt gcp-project=test-project \
    --log-opt gcp-meta-zone=west1 \
    --log-opt gcp-meta-name=`hostname` \
    your/application
```
