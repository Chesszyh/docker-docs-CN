---
description: 了解如何在 Docker Engine 中使用 Journald 日志驱动程序
keywords: journald, systemd-journald, docker, logging, driver, 日志, 驱动程序
title: Journald 日志驱动程序
---

`journald` 日志驱动程序将容器日志发送到 [`systemd` journal](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html)。可以使用 `journalctl` 命令、`journal` API 或 `docker logs` 命令检索日志条目。

除了日志消息本身的文本之外，`journald` 日志驱动程序还在 journal 中为每条消息存储以下元数据：

| 字段                                 | 描述                                                                                                                                           |
| :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CONTAINER_ID`                       | 截断为 12 个字符的容器 ID。                                                                                                          |
| `CONTAINER_ID_FULL`                  | 完整的 64 位容器 ID。                                                                                                                   |
| `CONTAINER_NAME`                     | 容器启动时的名称。如果您使用 `docker rename` 对容器进行重命名，新名称不会反映在 journal 条目中。 |
| `CONTAINER_TAG`, `SYSLOG_IDENTIFIER` | 容器标签 ([日志标签选项文档](log_tags.md))。                                                                                      |
| `CONTAINER_PARTIAL_MESSAGE`          | 用于标记日志完整性的字段。改善了长日志行的记录。                                                                                  |
| `IMAGE_NAME`                         | 容器镜像的名称。                                                                                                                      |

## 用法

要将 `journald` 驱动程序设置为默认日志驱动程序，请在 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json` 中的 `daemon.json` 文件中，将 `log-driver` 和 `log-opts` 键设置为适当的值。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动程序设置为 `journald`：

```json
{
  "log-driver": "journald"
}
```

重启 Docker 使更改生效。

要为特定容器配置日志驱动程序，请在 `docker run` 命令中使用 `--log-driver` 标志。

```console
$ docker run --log-driver=journald ...
```

## 选项

使用 `--log-opt NAME=VALUE` 标志指定额外的 `journald` 日志驱动程序选项。

| 选项           | 是否必填 | 描述                                                                                                                                                                   |
| :------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tag`          | 可选     | 指定模板以设置 journald 日志中的 `CONTAINER_TAG` 和 `SYSLOG_IDENTIFIER` 值。参考 [日志标签选项文档](log_tags.md) 来自定义日志标签格式。 |
| `labels`       | 可选     | 以逗号分隔的标签键列表，如果为容器指定了这些标签，则应将其包含在消息中。                                                 |
| `labels-regex` | 可选     | 分别与 `labels` 类似且兼容。一个用于匹配日志相关标签的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                |
| `env`          | 可选     | 以逗号分隔的环境变量键列表，如果为容器指定了这些变量，则应将其包含在消息中。                               | |
| `env-regex`    | 可选     | 分别与 `env` 类似且兼容。一个用于匹配日志相关环境变量的正则表达式。用于高级 [日志标签选项](log_tags.md)。                    |

如果 `label` 和 `env` 选项发生冲突，则以 `env` 的值为准。每个选项都会向日志消息的属性中添加额外字段。

以下是记录到 journald 所需日志选项的示例。

```console
$ docker run \
    --log-driver=journald \
    --log-opt labels=location \
    --log-opt env=TEST \
    --env "TEST=false" \
    --label location=west \
    your/application
```

此配置还指示驱动程序在负载中包含标签 `location` 和环境变量 `TEST`。如果省略了 `--env "TEST=false"` 或 `--label location=west` 参数，则 journald 日志中将不会设置相应的键。

## 关于容器名称的说明

`CONTAINER_NAME` 字段中记录的值是启动时设置的容器名称。如果您使用 `docker rename` 对容器进行重命名，新名称不会反映在 journal 条目中。Journal 条目将继续使用原始名称。

## 使用 `journalctl` 检索日志消息

使用 `journalctl` 命令检索日志消息。您可以应用过滤表达式来限制检索到的消息仅为与特定容器关联的消息：

```console
$ sudo journalctl CONTAINER_NAME=webserver
```

您可以使用其他过滤器来进一步限制检索到的消息。`-b` 标志仅检索自上次系统启动以来生成的消息：

```console
$ sudo journalctl -b CONTAINER_NAME=webserver
```

`-o` 标志指定检索到的日志消息的格式。使用 `-o json` 以 JSON 格式返回日志消息。

```console
$ sudo journalctl -o json CONTAINER_NAME=webserver
```

### 查看启用了 TTY 的容器日志

如果容器启用了 TTY，您在检索日志消息时可能会在输出中看到 `[10B blob data]`。原因是 `\r` 被附加到了行尾，除非设置了 `--all`，否则 `journalctl` 不会自动剥离它：

```console
$ sudo journalctl -b CONTAINER_NAME=webserver --all
```

## 使用 `journal` API 检索日志消息

此示例使用 `systemd` Python 模块来检索容器日志：

```python
import systemd.journal

reader = systemd.journal.Reader()
reader.add_match('CONTAINER_NAME=web')

for msg in reader:
    print '{CONTAINER_ID_FULL}: {MESSAGE}'.format(**msg)
```
