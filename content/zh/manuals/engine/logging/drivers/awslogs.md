---
description: 了解如何在 Docker Engine 中使用 Amazon CloudWatch Logs 日志驱动程序
keywords: AWS, Amazon, CloudWatch, logging, driver, 日志, 驱动程序
title: Amazon CloudWatch Logs 日志驱动程序
alias:
  - /engine/reference/logging/awslogs/
  - /engine/admin/logging/awslogs/
  - /config/containers/logging/awslogs/
---

`awslogs` 日志驱动程序将容器日志发送到 [Amazon CloudWatch Logs](https://aws.amazon.com/cloudwatch/details/#log-monitoring)。日志条目可以通过 [AWS 管理控制台](https://console.aws.amazon.com/cloudwatch/home#logs:) 或 [AWS SDK 和命令行工具](https://docs.aws.amazon.com/cli/latest/reference/logs/index.html) 进行检索。

## 用法

要将 `awslogs` 驱动程序设置为默认日志驱动程序，请在 Linux 主机上的 `/etc/docker/` 目录或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json` 目录下的 `daemon.json` 文件中，将 `log-driver` 和 `log-opt` 键设置为适当的值。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。以下示例设置日志驱动程序为 `awslogs` 并设置 `awslogs-region` 选项。

```json
{
  "log-driver": "awslogs",
  "log-opts": {
    "awslogs-region": "us-east-1"
  }
}
```

重启 Docker 使更改生效。

您可以通过在 `docker run` 中使用 `--log-driver` 选项为特定容器设置日志驱动程序：

```console
$ docker run --log-driver=awslogs ...
```

如果您使用的是 Docker Compose，请参考以下示例声明设置 `awslogs`：

```yaml
myservice:
  logging:
    driver: awslogs
    options:
      awslogs-region: us-east-1
```

## Amazon CloudWatch Logs 选项

您可以将日志选项添加到 `daemon.json` 以设置 Docker 范围的默认值，或者在启动容器时使用 `--log-opt NAME=VALUE` 标志来指定 Amazon CloudWatch Logs 日志驱动程序选项。

### awslogs-region

`awslogs` 日志驱动程序将您的 Docker 日志发送到特定区域。使用 `awslogs-region` 日志选项或 `AWS_REGION` 环境变量来设置区域。默认情况下，如果您的 Docker 守护进程运行在 EC2 实例上且未设置区域，驱动程序将使用该实例所在的区域。

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 ...
```

### awslogs-endpoint

默认情况下，Docker 使用 `awslogs-region` 日志选项或检测到的区域来构建远程 CloudWatch Logs API 端点。使用 `awslogs-endpoint` 日志选项可以用提供的端点覆盖默认端点。

> [!NOTE]
> 
> `awslogs-region` 日志选项或检测到的区域控制用于签名的区域。如果您使用 `awslogs-endpoint` 指定的端点位于不同的区域，可能会遇到签名错误。

### awslogs-group

您必须为 `awslogs` 日志驱动程序指定一个 [日志组 (log group)](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)。您可以使用 `awslogs-group` 日志选项指定日志组：

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 --log-opt awslogs-group=myLogGroup ...
```

### awslogs-stream

要配置应使用哪个 [日志流 (log stream)](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)，您可以指定 `awslogs-stream` 日志选项。如果未指定，将使用容器 ID 作为日志流。

> [!NOTE]
> 
> 给定日志组内的日志流一次只能由一个容器使用。同时为多个容器使用同一个日志流可能会导致日志性能下降。

### awslogs-create-group

如果日志组不存在，日志驱动程序默认返回错误。但是，您可以将 `awslogs-create-group` 设置为 `true` 以根据需要自动创建日志组。`awslogs-create-group` 选项默认为 `false`。

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-create-group=true \
    ...
```

> [!NOTE]
> 
> 在尝试使用 `awslogs-create-group` 之前，您的 AWS IAM 策略必须包含 `logs:CreateLogGroup` 权限。

### awslogs-create-stream

默认情况下，日志驱动程序会创建用于容器日志持久化的 AWS CloudWatch Logs 流。

将 `awslogs-create-stream` 设置为 `false` 以禁用日志流创建。禁用后，Docker 守护进程会假设日志流已经存在。这种做法在日志流创建由另一个进程处理时非常有用，可以避免冗余的 AWS CloudWatch Logs API 调用。

如果 `awslogs-create-stream` 设置为 `false` 且日志流不存在，容器运行时向 CloudWatch 的日志持久化将失败，导致守护进程日志中出现 `Failed to put log events` 错误消息。

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-stream=myLogStream \
    --log-opt awslogs-create-stream=false \
    ...
```

### awslogs-datetime-format

`awslogs-datetime-format` 选项以 [Python `strftime` 格式](https://strftime.org) 定义了多行日志的起始模式。一条日志消息由匹配该模式的一行以及任何不匹配该模式的后续行组成。因此，匹配行是日志消息之间的分隔符。

使用此格式的一个示例用例是解析堆栈转储 (stack dump) 等输出，否则这些输出可能会被记录在多个条目中。正确的模式允许将其捕获在单个条目中。

如果同时配置了 `awslogs-datetime-format` 和 `awslogs-multiline-pattern`，则此选项始终具有优先级。

> [!NOTE]
> 
> 多行日志会对所有日志消息执行正则表达式解析和匹配，这可能会对日志性能产生负面影响。

考虑以下日志流，其中新的日志消息以时间戳开头：

```console
[May 01, 2017 19:00:01] A message was logged
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words
[May 01, 2017 19:01:32] Another message was logged
```

该格式可以表示为 `strftime` 表达式 `[%b %d, %Y %H:%M:%S]`，并且可以将 `awslogs-datetime-format` 的值设置为该表达式：

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-datetime-format='[%b %d, %Y %H:%M:%S]' \
    ...
```

这将把日志解析为以下 CloudWatch 日志事件：

```console
# 第一个事件
[May 01, 2017 19:00:01] A message was logged

# 第二个事件
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words

# 第三个事件
[May 01, 2017 19:01:32] Another message was logged
```

支持以下 `strftime` 代码：

| 代码 | 含义                                                             | 示例     |
| :--- |
| `%a` | 星期几的缩写。                                                   | Mon      |
| `%A` | 星期几的全称。                                                   | Monday   |
| `%w` | 星期几作为十进制数，0 为星期日，6 为星期六。                     | 0        |
| `%d` | 一个月中的第几天，作为补零的十进制数。                           | 08       |
| `%b` | 月份的缩写。                                                     | Feb      |
| `%B` | 月份的全称。                                                     | February |
| `%m` | 月份作为补零的十进制数。                                         | 02       |
| `%Y` | 带有世纪的年份，作为十进制数。                                   | 2008     |
| `%y` | 不带世纪的年份，作为补零的十进制数。                             | 08       |
| `%H` | 小时 (24 小时制)，作为补零的十进制数。                           | 19       |
| `%I` | 小时 (12 小时制)，作为补零的十进制数。                           | 07       |
| `%p` | AM 或 PM。                                                       | AM       |
| `%M` | 分钟作为补零的十进制数。                                         | 57       |
| `%S` | 秒作为补零的十进制数。                                           | 04       |
| `%L` | 毫秒作为补零的十进制数。                                         | .123     |
| `%f` | 微秒作为补零的十进制数。                                         | 000345   |
| `%z` | 格式为 +HHMM 或 -HHMM 的 UTC 偏移量。                            | +1300    |
| `%Z` | 时区名称。                                                       | PST      |
| `%j` | 一年中的第几天，作为补零的十进制数。                             | 363      |

### awslogs-multiline-pattern

`awslogs-multiline-pattern` 选项使用正则表达式定义了多行日志的起始模式。一条日志消息由匹配该模式的一行以及任何不匹配该模式的后续行组成。因此，匹配行是日志消息之间的分隔符。

如果同时配置了 `awslogs-datetime-format`，则忽略此选项。

> [!NOTE]
> 
> 多行日志会对所有日志消息执行正则表达式解析和匹配。这可能会对日志性能产生负面影响。

考虑以下日志流，其中每条日志消息都应以模式 `INFO` 开头：

```console
INFO A message was logged
INFO Another multi-line message was logged
     Some random message
INFO Another message was logged
```

您可以使用正则表达式 `^INFO`：

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-multiline-pattern='^INFO' \
    ...
```

这将把日志解析为以下 CloudWatch 日志事件：

```console
# 第一个事件
INFO A message was logged

# 第二个事件
INFO Another multi-line message was logged
     Some random message

# 第三个事件
INFO Another message was logged
```

### tag

指定 `tag` 作为 `awslogs-stream` 选项的备选方案。`tag` 解析 Go 模板标记，例如 `{{.ID}}`、`{{.FullID}}` 或 `{{.Name}}`。详情请参阅 [tag 选项文档](log_tags.md) 以获取有关受支持模板替换的细节。

当同时指定 `awslogs-stream` 和 `tag` 时，为 `awslogs-stream` 提供的值将覆盖使用 `tag` 指定的模板。

如果未指定，将使用容器 ID 作为日志流。

> [!NOTE]
> 
> CloudWatch log API 不支持日志名称中包含 `:`。这在将 `{{ .ImageName }}` 用作标签时可能会导致一些问题，因为 Docker 镜像格式为 `IMAGE:TAG`，例如 `alpine:latest`。可以使用模板标记来获得正确的格式。要获取镜像名称和容器 ID 的前 12 个字符，您可以使用：
> 
> ```bash
> --log-opt tag='{{ with split .ImageName ":" }}{{join . "_"}}{{end}}-{{.ID}}'
> ```
> 
> 输出类似于：`alpine_latest-bf0072049c76`

### awslogs-force-flush-interval-seconds

`awslogs` 驱动程序定期将日志刷新到 CloudWatch。

`awslogs-force-flush-interval-seconds` 选项更改日志刷新间隔的秒数。

默认值为 5 秒。

### awslogs-max-buffered-events

`awslogs` 驱动程序会对日志进行缓冲。

`awslogs-max-buffered-events` 选项更改日志缓冲区的大小。

默认值为 4K。

## 凭据 (Credentials)

您必须向 Docker 守护进程提供 AWS 凭据才能使用 `awslogs` 日志驱动程序。您可以通过 `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 和 `AWS_SESSION_TOKEN` 环境变量、默认的 AWS 共享凭据文件 (root 用户的 `~/.aws/credentials`) 来提供这些凭据，或者如果您是在 Amazon EC2 实例上运行 Docker 守护进程，则可以使用 Amazon EC2 实例配置文件。

凭据必须应用了允许 `logs:CreateLogStream` 和 `logs:PutLogEvents` 操作的策略，如下例所示。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```