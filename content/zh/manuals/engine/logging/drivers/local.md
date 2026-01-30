---
description: 了解如何在 Docker Engine 中使用 local 日志驱动程序
keywords: local, docker, logging, driver, file, 日志, 驱动程序
title: 本地文件日志驱动程序
---

`local` 日志驱动程序捕获容器的 stdout/stderr 输出，并将其写入专为性能和磁盘利用率优化的内部存储中。

默认情况下，`local` 驱动程序为每个容器保留 100MB 的日志消息，并使用自动压缩来减小磁盘占用。100MB 的默认值是基于每个文件 20MB 的默认大小以及 5 个此类文件的默认数量 (以进行日志轮转)。

> [!WARNING]
> 
> `local` 日志驱动程序使用基于文件的存储。这些文件被设计为仅供 Docker 守护进程访问。使用外部工具与这些文件交互可能会干扰 Docker 的日志系统并导致意外行为，应予以避免。

## 用法

要将 `local` 驱动程序设置为默认日志驱动程序，请在 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json` 中的 `daemon.json` 文件中，将 `log-driver` 和 `log-opt` 键设置为适当的值。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动程序设置为 `local`，并设置 `max-size` 选项。

```json
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "10m"
  }
}
```

重启 Docker 使更改对新创建的容器生效。现有容器不会自动使用新的日志配置。

您可以通过向 `docker container create` 或 `docker run` 传递 `--log-driver` 标志来为特定容器设置日志驱动程序：

```console
$ docker run \
      --log-driver local --log-opt max-size=10m \
      alpine echo hello world
```

注意，`local` 是 bash 的保留关键字，因此在脚本中可能需要对其加引号。

### 选项

`local` 日志驱动程序支持以下日志选项：

| 选项       | 描述                                                                                                                                                   | 示例值                     |
| :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------- |
| `max-size` | 日志轮转前的最大大小。正整数加上表示计量单位的修饰符 (`k`, `m` 或 `g`)。默认为 20m。      | `--log-opt max-size=10m`   |
| `max-file` | 允许存在的最大日志文件数。如果轮转日志导致文件超标，则删除最旧的文件。正整数。默认为 5。 | `--log-opt max-file=3`     |
| `compress` | 切换对轮转后日志文件的压缩。默认启用。                                                                                                  | `--log-opt compress=false` |

### 示例

此示例启动一个 Alpine 容器，该容器最多可以拥有 3 个日志文件，每个文件的大小不超过 10 MB。

```console
$ docker run -it --log-driver local --log-opt max-size=10m --log-opt max-file=3 alpine ash
```

