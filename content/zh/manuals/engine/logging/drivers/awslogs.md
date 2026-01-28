---
description: Learn how to use the Amazon CloudWatch Logs logging driver with Docker Engine
keywords: AWS, Amazon, CloudWatch, logging, driver
title: Amazon CloudWatch Logs 日志驱动程序
aliases:
  - /engine/reference/logging/awslogs/
  - /engine/admin/logging/awslogs/
  - /config/containers/logging/awslogs/
---

`awslogs` 日志驱动程序将容器日志发送到 [Amazon CloudWatch Logs](https://aws.amazon.com/cloudwatch/details/#log-monitoring)。可以通过 [AWS 管理控制台](https://console.aws.amazon.com/cloudwatch/home#logs:)或 [AWS SDK 和命令行工具](https://docs.aws.amazon.com/cli/latest/reference/logs/index.html)检索日志条目。

## 用法

要将 `awslogs` 驱动程序用作默认日志驱动程序，请在 `daemon.json` 文件中将 `log-driver` 和 `log-opt` 键设置为适当的值，该文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。以下示例将日志驱动程序设置为 `awslogs` 并设置 `awslogs-region` 选项。

```json
{
  "log-driver": "awslogs",
  "log-opts": {
    "awslogs-region": "us-east-1"
  }
}
```

重启 Docker 以使更改生效。

你可以使用 `docker run` 的 `--log-driver` 选项为特定容器设置日志驱动程序：

```console
$ docker run --log-driver=awslogs ...
```

如果你使用 Docker Compose，请使用以下声明示例设置 `awslogs`：

```yaml
myservice:
  logging:
    driver: awslogs
    options:
      awslogs-region: us-east-1
```

## Amazon CloudWatch Logs 选项

你可以在 `daemon.json` 中添加日志选项来设置 Docker 范围的默认值，或在启动容器时使用 `--log-opt NAME=VALUE` 标志指定 Amazon CloudWatch Logs 日志驱动程序选项。

### awslogs-region

`awslogs` 日志驱动程序将你的 Docker 日志发送到特定区域。使用 `awslogs-region` 日志选项或 `AWS_REGION` 环境变量来设置区域。默认情况下，如果你的 Docker 守护进程在 EC2 实例上运行且未设置区域，驱动程序将使用实例的区域。

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 ...
```

### awslogs-endpoint

默认情况下，Docker 使用 `awslogs-region` 日志选项或检测到的区域来构造远程 CloudWatch Logs API 端点。使用 `awslogs-endpoint` 日志选项可以用提供的端点覆盖默认端点。

> [!NOTE]
>
> `awslogs-region` 日志选项或检测到的区域控制用于签名的区域。如果你使用 `awslogs-endpoint` 指定的端点使用不同的区域，可能会遇到签名错误。

### awslogs-group

你必须为 `awslogs` 日志驱动程序指定一个[日志组](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)。你可以使用 `awslogs-group` 日志选项指定日志组：

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 --log-opt awslogs-group=myLogGroup ...
```

### awslogs-stream

要配置应使用哪个[日志流](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)，你可以指定 `awslogs-stream` 日志选项。如果未指定，则使用容器 ID 作为日志流。

> [!NOTE]
>
> 给定日志组中的日志流一次只能由一个容器使用。同时为多个容器使用同一个日志流可能会导致日志性能下降。

### awslogs-create-group

如果日志组不存在，日志驱动程序默认返回错误。但是，你可以将 `awslogs-create-group` 设置为 `true` 以根据需要自动创建日志组。`awslogs-create-group` 选项默认为 `false`。

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
> 在尝试使用 `awslogs-create-group` 之前，你的 AWS IAM 策略必须包含 `logs:CreateLogGroup` 权限。

### awslogs-create-stream

默认情况下，日志驱动程序会创建用于容器日志持久化的 AWS CloudWatch Logs 流。

将 `awslogs-create-stream` 设置为 `false` 以禁用日志流创建。禁用后，Docker 守护进程假定日志流已经存在。这在日志流创建由另一个进程处理以避免冗余的 AWS CloudWatch Logs API 调用时很有用。

如果 `awslogs-create-stream` 设置为 `false` 且日志流不存在，则在容器运行时日志持久化到 CloudWatch 会失败，导致守护进程日志中出现 `Failed to put log events` 错误消息。

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

`awslogs-datetime-format` 选项以 [Python `strftime` 格式](https://strftime.org)定义多行起始模式。日志消息由匹配该模式的行和其后不匹配该模式的任何行组成。因此，匹配的行是日志消息之间的分隔符。

此格式的一个用例是解析诸如堆栈转储之类的输出，否则可能会被记录为多个条目。正确的模式允许将其捕获为单个条目。

如果同时配置了 `awslogs-datetime-format` 和 `awslogs-multiline-pattern`，此选项始终优先。

> [!NOTE]
>
> 多行日志记录对所有日志消息执行正则表达式解析和匹配，这可能会对日志性能产生负面影响。

考虑以下日志流，其中新的日志消息以时间戳开头：

```console
[May 01, 2017 19:00:01] A message was logged
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words
[May 01, 2017 19:01:32] Another message was logged
```

该格式可以表示为 `strftime` 表达式 `[%b %d, %Y %H:%M:%S]`，`awslogs-datetime-format` 值可以设置为该表达式：

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-datetime-format='\[%b %d, %Y %H:%M:%S\]' \
    ...
```

这会将日志解析为以下 CloudWatch 日志事件：

```console
# First event
[May 01, 2017 19:00:01] A message was logged

# Second event
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words

# Third event
[May 01, 2017 19:01:32] Another message was logged
```

支持以下 `strftime` 代码：

| 代码 | 含义                                                             | 示例     |
| :--- | :--------------------------------------------------------------- | :------- |
| `%a` | 星期的缩写名称。                                                 | Mon      |
| `%A` | 星期的完整名称。                                                 | Monday   |
| `%w` | 以十进制数表示的星期几，其中 0 是星期日，6 是星期六。            | 0        |
| `%d` | 以零填充的十进制数表示的月份中的日期。                           | 08       |
| `%b` | 月份的缩写名称。                                                 | Feb      |
| `%B` | 月份的完整名称。                                                 | February |
| `%m` | 以零填充的十进制数表示的月份。                                   | 02       |
| `%Y` | 带世纪的年份，以十进制数表示。                                   | 2008     |
| `%y` | 不带世纪的年份，以零填充的十进制数表示。                         | 08       |
| `%H` | 小时（24 小时制），以零填充的十进制数表示。                      | 19       |
| `%I` | 小时（12 小时制），以零填充的十进制数表示。                      | 07       |
| `%p` | AM 或 PM。                                                       | AM       |
| `%M` | 分钟，以零填充的十进制数表示。                                   | 57       |
| `%S` | 秒，以零填充的十进制数表示。                                     | 04       |
| `%L` | 毫秒，以零填充的十进制数表示。                                   | .123     |
| `%f` | 微秒，以零填充的十进制数表示。                                   | 000345   |
| `%z` | 以 +HHMM 或 -HHMM 形式表示的 UTC 偏移量。                        | +1300    |
| `%Z` | 时区名称。                                                       | PST      |
| `%j` | 一年中的第几天，以零填充的十进制数表示。                         | 363      |

### awslogs-multiline-pattern

`awslogs-multiline-pattern` 选项使用正则表达式定义多行起始模式。日志消息由匹配该模式的行和其后不匹配该模式的任何行组成。因此，匹配的行是日志消息之间的分隔符。

如果同时配置了 `awslogs-datetime-format`，则此选项被忽略。

> [!NOTE]
>
> 多行日志记录对所有日志消息执行正则表达式解析和匹配。这可能会对日志性能产生负面影响。

考虑以下日志流，其中每条日志消息应以模式 `INFO` 开头：

```console
INFO A message was logged
INFO Another multi-line message was logged
     Some random message
INFO Another message was logged
```

你可以使用正则表达式 `^INFO`：

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-multiline-pattern='^INFO' \
    ...
```

这会将日志解析为以下 CloudWatch 日志事件：

```console
# First event
INFO A message was logged

# Second event
INFO Another multi-line message was logged
     Some random message

# Third event
INFO Another message was logged
```

### tag

指定 `tag` 作为 `awslogs-stream` 选项的替代方案。`tag` 解释 Go 模板标记，如 `{{.ID}}`、`{{.FullID}}` 或 `{{.Name}}` `docker.{{.ID}}`。有关支持的模板替换的详细信息，请参阅 [tag 选项文档](log_tags.md)。

当同时指定 `awslogs-stream` 和 `tag` 时，`awslogs-stream` 提供的值会覆盖 `tag` 指定的模板。

如果未指定，则使用容器 ID 作为日志流。

> [!NOTE]
>
> CloudWatch 日志 API 不支持日志名称中的 `:`。当使用 `{{ .ImageName }}` 作为标签时，这可能会导致一些问题，因为 Docker 镜像的格式为 `IMAGE:TAG`，如 `alpine:latest`。可以使用模板标记来获取正确的格式。要获取镜像名称和容器 ID 的前 12 个字符，你可以使用：
>
> ```bash
> --log-opt tag='{{ with split .ImageName ":" }}{{join . "_"}}{{end}}-{{.ID}}'
> ```
>
> 输出类似于：`alpine_latest-bf0072049c76`

### awslogs-force-flush-interval-seconds

`awslogs` 驱动程序定期将日志刷新到 CloudWatch。

`awslogs-force-flush-interval-seconds` 选项更改日志刷新间隔秒数。

默认值为 5 秒。

### awslogs-max-buffered-events

`awslogs` 驱动程序缓冲日志。

`awslogs-max-buffered-events` 选项更改日志缓冲区大小。

默认值为 4K。

## 凭证

你必须向 Docker 守护进程提供 AWS 凭证才能使用 `awslogs` 日志驱动程序。你可以使用 `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 和 `AWS_SESSION_TOKEN` 环境变量、默认的 AWS 共享凭证文件（root 用户的 `~/.aws/credentials`）提供这些凭证，或者如果你在 Amazon EC2 实例上运行 Docker 守护进程，则可以使用 Amazon EC2 实例配置文件。

凭证必须应用允许 `logs:CreateLogStream` 和 `logs:PutLogEvents` 操作的策略，如以下示例所示。

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
