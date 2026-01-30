---
description: 了解如何为 Docker 守护进程配置日志驱动程序
keywords: docker, logging, driver, 日志, 驱动程序, 配置
title: 配置日志驱动程序
---

Docker 包含多种日志机制，帮助您从运行中的容器和服务获取信息。这些机制被称为日志驱动程序 (logging drivers)。每个 Docker 守护进程都有一个默认的日志驱动程序，除非您将容器配置为使用不同的日志驱动程序 (简称日志驱动)，否则每个容器都会使用该默认驱动。

默认情况下，Docker 使用 [`json-file` 日志驱动程序](drivers/json-file.md)，它在内部将容器日志缓存为 JSON 格式。除了使用 Docker 自带的日志驱动程序外，您还可以实现并使用 [日志驱动程序插件](plugins.md)。

> [!TIP]
>
> 使用 `local` 日志驱动程序可以防止磁盘耗尽。默认情况下，日志不会进行轮转 (log-rotation)。因此，默认 [`json-file` 日志驱动程序](drivers/json-file.md) 存储的日志文件可能会导致产生大量输出的容器占用大量磁盘空间，从而导致磁盘空间耗尽。
>
> Docker 保持 `json-file` 日志驱动程序 (不带日志轮转) 作为默认值，是为了与旧版本的 Docker 保持向后兼容，以及适用于将 Docker 作为 Kubernetes 运行时的情况。
>
> 对于其他情况，建议使用 `local` 日志驱动程序，因为它默认执行日志轮转，并使用更高效的文件格式。参考下文的 [配置默认日志驱动程序](#configure-the-default-logging-driver) 章节，了解如何将 `local` 日志驱动程序配置为默认值，并查阅 [本地文件日志驱动程序](drivers/local.md) 页面以获取有关 `local` 日志驱动程序的更多详情。

## 配置默认日志驱动程序

要将 Docker 守护进程配置为默认使用特定的日志驱动程序，请在 `daemon.json` 配置文件中将 `log-driver` 的值设置为日志驱动程序的名称。详情请参阅 [`dockerd` 参考手册](/reference/cli/dockerd/#daemon-configuration-file) 中的“守护进程配置文件”部分。

默认的日志驱动程序是 `json-file`。以下示例将默认日志驱动程序设置为 [`local` 日志驱动程序](drivers/local.md)：

```json
{
  "log-driver": "local"
}
```

如果日志驱动程序有可配置的选项，您可以在 `daemon.json` 文件中以 JSON 对象的形式设置它们，键名为 `log-opts`。以下示例在 `json-file` 日志驱动程序上设置了四个可配置选项：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3",
    "labels": "production_status",
    "env": "os,customer"
  }
}
```

重启 Docker 使更改对新创建的容器生效。现有容器不会自动使用新的日志配置。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。因此，布尔值和数值 (如上例中的 `max-file` 值) 必须用引号 (`"`) 括起来。

如果您不指定日志驱动程序，默认值为 `json-file`。要查找 Docker 守护进程当前的默认日志驱动程序，运行 `docker info` 并搜索 `Logging Driver`。您可以在 Linux、macOS 或 Windows 的 PowerShell 中使用以下命令：

```console
$ docker info --format '{{.LoggingDriver}}'

json-file
```

> [!NOTE]
>
> 更改守护进程配置中的默认日志驱动程序或日志驱动程序选项仅影响配置更改后创建的容器。现有容器保留其创建时使用的日志驱动程序选项。要更新容器的日志驱动程序，必须使用所需的选项重新创建容器。参考下文的 [为容器配置日志驱动程序](#configure-the-logging-driver-for-a-container) 章节，了解如何查找容器的日志驱动程序配置。

## 为容器配置日志驱动程序

启动容器时，您可以使用 `--log-driver` 标志将其配置为使用与 Docker 守护进程默认不同的日志驱动程序。如果该日志驱动程序有可配置选项，您可以使用一个或多个 `--log-opt <NAME>=<VALUE>` 标志实例来设置它们。即使容器使用默认日志驱动程序，它也可以使用不同的可配置选项。

以下示例启动一个带有 `none` 日志驱动程序的 Alpine 容器。

```console
$ docker run -it --log-driver none alpine ash
```

要查找运行中容器的当前日志驱动程序，如果守护进程正在使用 `json-file` 日志驱动程序，请运行以下 `docker inspect` 命令，将 `<CONTAINER>` 替换为容器名称或 ID：

```console
$ docker inspect -f '{{.HostConfig.LogConfig.Type}}' <CONTAINER>

json-file
```

## 配置从容器到日志驱动程序的消息传递模式

Docker 提供了两种将消息从容器传递到日志驱动程序的模式：

- (默认) 从容器到驱动程序的直接、阻塞式 (blocking) 传递
- 非阻塞式 (non-blocking) 传递，将日志消息存储在每个容器的中间缓冲区中，供驱动程序消费

`non-blocking` 消息传递模式可防止应用程序因日志写入背压而阻塞。当 STDERR 或 STDOUT 流阻塞时，应用程序可能会以意外方式失败。

> [!WARNING]
>
> 当缓冲区满时，新消息将不会入队。丢弃消息通常优于阻塞应用程序的日志写入过程。

`mode` 日志选项控制是使用 `blocking` (默认) 还是 `non-blocking` 消息传递。

当 `mode` 设置为 `non-blocking` 时，`max-buffer-size` 控制用于中间消息存储的缓冲区大小。默认值为 `1m`，即 1 MB (100 万字节)。有关允许的格式字符串，请参阅 [`go-units` 包中的 `FromHumanSize()` 函数](https://pkg.go.dev/github.com/docker/go-units#FromHumanSize)，例如 `1KiB` 表示 1024 字节，`2g` 表示 20 亿字节。

以下示例启动一个 Alpine 容器，日志输出为非阻塞模式，并带有 4 MB 缓冲区：

```console
$ docker run -it --log-opt mode=non-blocking --log-opt max-buffer-size=4m alpine ping 127.0.0.1
```

### 在日志驱动程序中使用环境变量或标签

某些日志驱动程序会将容器的 `--env|-e` 或 `--label` 标志的值添加到容器日志中。此示例启动一个使用 Docker 守护进程默认日志驱动程序 (在下例中为 `json-file`) 的容器，但设置了环境变量 `os=ubuntu`。

```console
$ docker run -dit --label production_status=testing -e os=ubuntu alpine sh
```

如果日志驱动程序支持，这会向日志输出中添加额外字段。以下输出由 `json-file` 日志驱动程序生成：

```json
"attrs":{"production_status":"testing","os":"ubuntu"}
```

## 受支持的日志驱动程序

支持以下日志驱动程序。如果适用，请查看各驱动程序文档链接以了解其可配置选项。如果您使用的是 [日志驱动程序插件](plugins.md)，可能会看到更多选项。

| 驱动程序                              | 描述                                                                                                 |
| :------------------------------------ | :---------------------------------------------------------------------------------------------------------- |
| `none`                                | 容器没有日志可用，且 `docker logs` 不返回任何输出。                       |
| [`local`](drivers/local.md)           | 日志存储在专为最小开销而设计的自定义格式中。                                           |
| [`json-file`](drivers/json-file.md)   | 日志格式化为 JSON。Docker 的默认日志驱动程序。                                      |
| [`syslog`](drivers/syslog.md)         | 将日志消息写入 `syslog` 设施。宿主机上必须运行有 `syslog` 守护进程。  |
| [`journald`](drivers/journald.md)     | 将日志消息写入 `journald`。宿主机上必须运行有 `journald` 守护进程。               |
| [`gelf`](drivers/gelf.md)             | 将日志消息写入 Graylog 扩展日志格式 (GELF) 端点，如 Graylog 或 Logstash。           |
| [`fluentd`](drivers/fluentd.md)       | 将日志消息写入 `fluentd` (forward 输入)。宿主机上必须运行有 `fluentd` 守护进程。 |
| [`awslogs`](drivers/awslogs.md)       | 将日志消息写入 Amazon CloudWatch Logs。                                                              |
| [`splunk`](drivers/splunk.md)         | 使用 HTTP 事件收集器将日志消息写入 `splunk`。                                             |
| [`etwlogs`](drivers/etwlogs.md)       | 将日志消息作为 Windows 事件追踪 (ETW) 事件写入。仅适用于 Windows 平台。         |
| [`gcplogs`](drivers/gcplogs.md)       | 将日志消息写入 Google Cloud Platform (GCP) Logging。                                                 |

## 日志驱动程序的限制

- 读取日志信息需要解压轮转后的日志文件，这会导致磁盘使用量暂时增加 (直到读取完轮转文件中的日志条目)，并在解压时增加 CPU 使用率。
- Docker 数据目录所在的宿主机存储容量决定了日志文件信息的最大容量。
