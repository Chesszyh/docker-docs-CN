---
description: 了解如何在 Docker Engine 中使用 json-file 日志驱动程序
keywords: json-file, docker, logging, driver, 日志, 驱动程序
title: JSON 文件日志驱动程序
---

默认情况下，Docker 会捕获所有容器的标准输出 (和标准错误)，并将它们以 JSON 格式写入文件。JSON 格式会为每一行注释其来源 (`stdout` 或 `stderr`) 及其时间戳。每个日志文件仅包含关于一个容器的信息。

```json
{
  "log": "Log line is here\n",
  "stream": "stdout",
  "time": "2019-01-01T11:11:11.111111111Z"
}
```

> [!WARNING]
> 
> `json-file` 日志驱动程序使用基于文件的存储。这些文件被设计为仅供 Docker 守护进程访问。使用外部工具与这些文件交互可能会干扰 Docker 的日志系统并导致意外行为，应予以避免。

## 用法

要将 `json-file` 驱动程序设置为默认日志驱动程序，请在 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\` 中的 `daemon.json` 文件中，将 `log-driver` 和 `log-opts` 键设置为适当的值。如果该文件不存在，请先创建它。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动程序设置为 `json-file`，并设置 `max-size` 和 `max-file` 选项以启用自动日志轮转。

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

> [!NOTE]
> 
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。因此，布尔值和数值 (如上例中的 `max-file` 值) 必须用引号 (`"`) 括起来。

重启 Docker 使更改对新创建的容器生效。现有容器不会自动使用新的日志配置。

您可以通过向 `docker container create` 或 `docker run` 传递 `--log-driver` 标志来为特定容器设置日志驱动程序：

```console
$ docker run \
      --log-driver json-file --log-opt max-size=10m \
      alpine echo hello world
```

### 选项

`json-file` 日志驱动程序支持以下日志选项：

| 选项           | 描述                                                                                                                                                                                                   | 示例值                                             |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------- |
| `max-size`     | 日志轮转前的最大大小。正整数加上表示计量单位的修饰符 (`k`, `m` 或 `g`)。默认为 -1 (无限制)。                                          | `--log-opt max-size=10m`                           |
| `max-file`     | 允许存在的最大日志文件数。如果轮转日志导致文件超标，则删除最旧的文件。**仅在同时设置了 `max-size` 时有效。** 正整数。默认为 1。 | `--log-opt max-file=3`                             |
| `labels`       | 在启动 Docker 守护进程时应用。该守护进程接受的以逗号分隔的日志相关标签列表。用于高级 [日志标签选项](log_tags.md)。                                              | `--log-opt labels=production_status,geo`           |
| `labels-regex` | 分别与 `labels` 类似且兼容。一个用于匹配日志相关标签的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                              | `--log-opt labels-regex=^(production_status|geo)` | 
| `env`          | 在启动 Docker 守护进程时应用。该守护进程接受的以逗号分隔的日志相关环境变量列表。用于高级 [日志标签选项](log_tags.md)。                               | `--log-opt env=os,customer`                        |
| `env-regex`    | 分别与 `env` 类似且兼容。一个用于匹配日志相关环境变量的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                  | `--log-opt env-regex=^(os|customer)`              |
| `compress`     | 切换对轮转后日志的压缩。默认值为 `disabled` (禁用)。                                                                                                                                                  | `--log-opt compress=true`                          |

### 示例

此示例启动一个 Alpine 容器，该容器最多可以拥有 3 个日志文件，每个文件的大小不超过 10 MB。

```console
$ docker run -it --log-opt max-size=10m --log-opt max-file=3 alpine ash
```

