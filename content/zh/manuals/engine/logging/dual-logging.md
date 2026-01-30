---
description: 了解在使用第三方日志解决方案时如何在本地读取容器日志。
keywords: docker, logging, driver, dual logging, cache, ring-buffer, configuration, 双重日志, 缓存, 配置
title: 将 docker logs 与远程日志驱动程序配合使用
aliases:
  - /config/containers/logging/dual-logging/
---

## 概览

无论配置了哪种日志驱动程序或插件，您都可以使用 `docker logs` 命令来读取容器日志。Docker Engine 使用 [`local`](drivers/local.md) 日志驱动程序充当缓存，用于读取容器的最新日志。这被称为双重日志 (dual logging)。默认情况下，该缓存启用了日志文件轮转，并且每个容器限制为最多 5 个文件，每个文件 20 MB (压缩前)。

参考 [配置选项](#configuration-options) 章节来自定义这些默认值，或者参考 [禁用双重日志](#disable-the-dual-logging-cache) 章节来禁用此功能。

## 前提条件

如果配置的日志驱动程序不支持读取日志，Docker Engine 会自动启用双重日志。

以下示例展示了在双重日志可用和不可用的情况下运行 `docker logs` 命令的结果：

### 无双重日志功能

当容器配置了远程日志驱动程序 (如 `splunk`) 且禁用了双重日志时，尝试在本地读取容器日志将显示错误：

- 第 1 步：配置 Docker 守护进程

  ```console
  $ cat /etc/docker/daemon.json
  {
    "log-driver": "splunk",
    "log-opts": {
      "cache-disabled": "true",
      ... ("splunk" 日志驱动程序的选项)
    }
  }
  ```

- 第 2 步：启动容器

  ```console
  $ docker run -d busybox --name testlog top
  ```

- 第 3 步：读取容器日志

  ```console
  $ docker logs 7d6ac83a89a0
  Error response from daemon: configured logging driver does not support reading
  ```

### 具有双重日志功能

启用双重日志缓存后，即使日志驱动程序不支持读取日志，也可以使用 `docker logs` 命令读取日志。以下示例显示了一个守护进程配置，该配置默认使用 `splunk` 远程日志驱动程序，并启用了双重日志缓存：

- 第 1 步：配置 Docker 守护进程

  ```console
  $ cat /etc/docker/daemon.json
  {
    "log-driver": "splunk",
    "log-opts": {
      ... ("splunk" 日志驱动程序的选项)
    }
  }
  ```

- 第 2 步：启动容器

  ```console
  $ docker run -d busybox --name testlog top
  ```

- 第 3 步：读取容器日志

  ```console
  $ docker logs 7d6ac83a89a0
  2019-02-04T19:48:15.423Z [INFO]  core: marked as sealed
  2019-02-04T19:48:15.423Z [INFO]  core: pre-seal teardown starting
  2019-02-04T19:48:15.423Z [INFO]  core: stopping cluster listeners
  2019-02-04T19:48:15.423Z [INFO]  core: shutting down forwarding rpc listeners
  2019-02-04T19:48:15.423Z [INFO]  core: forwarding rpc listeners stopped
  2019-02-04T19:48:15.599Z [INFO]  core: rpc listeners successfully shut down
  2019-02-04T19:48:15.599Z [INFO]  core: cluster listeners successfully shut down
  ```

> [!NOTE]
>
> 对于支持读取日志的日志驱动程序 (如 `local`、`json-file` 和 `journald` 驱动程序)，在双重日志功能可用之前或之后，功能上没有区别。在两种情况下，都可以使用 `docker logs` 读取这些驱动程序的日志。

### 配置选项

双重日志缓存接受与 [`local` 日志驱动程序](drivers/local.md) 相同的配置选项，但带有 `cache-` 前缀。这些选项可以针对每个容器进行指定，新容器的默认值可以使用 [守护进程配置文件](/reference/cli/dockerd/#daemon-configuration-file) 进行设置。

默认情况下，该缓存启用了日志文件轮转，并且每个容器限制为最多 5 个文件，每个文件 20MB (压缩前)。使用下面描述的配置选项来自定义这些默认值。

| 选项             | 默认值    | 描述                                                                                                                                       |
| :--------------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cache-disabled` | `"false"` | 禁用本地缓存。布尔值，以字符串形式传递 (`true`, `1`, `0`, 或 `false`)。                                                           |
| `cache-max-size` | `"20m"`   | 轮转前的缓存最大大小。正整数加上表示计量单位的修饰符 (`k`, `m`, 或 `g`)。       |
| `cache-max-file` | `"5"`     | 允许存在的最大缓存文件数。如果轮转日志导致文件超标，则删除最旧的文件。正整数。 |
| `cache-compress` | `"true"`  | 启用或禁用对轮转后的日志文件的压缩。布尔值，以字符串形式传递 (`true`, `1`, `0`, 或 `false`)。                              |

## 禁用双重日志缓存

使用 `cache-disabled` 选项来禁用双重日志缓存。在日志仅通过远程日志系统读取，且不需要通过 `docker logs` 进行调试的情况下，禁用缓存有助于节省存储空间。

缓存可以针对单个容器禁用，也可以在 [守护进程配置文件](/reference/cli/dockerd/#daemon-configuration-file) 中针对新容器默认禁用。

以下示例使用守护进程配置文件，默认使用 [`splunk`](drivers/splunk.md) 日志驱动程序并禁用了缓存：

```console
$ cat /etc/docker/daemon.json
{
  "log-driver": "splunk",
  "log-opts": {
    "cache-disabled": "true",
    ... ("splunk" 日志驱动程序的选项)
  }
}
```

> [!NOTE]
>
> 对于支持读取日志的日志驱动程序 (如 `local`、`json-file` 和 `journald` 驱动程序)，不会使用双重日志，禁用该选项无效。

## 限制

- 如果使用远程发送日志的日志驱动程序或插件的容器出现网络问题，则不会向本地缓存执行 `write` 操作。
- 如果由于任何原因 (文件系统满、写权限被移除) 导致向 `logdriver` 的写入失败，则缓存写入也会失败，并记录在守护进程日志中。不会重试向缓存的日志条目写入。
- 在默认配置中，某些日志可能会从缓存中丢失，因为使用了环形缓冲区 (ring buffer) 以防止在文件写入缓慢的情况下阻塞容器的标准输入输出 (stdio)。管理员必须在守护进程关闭时修复这些问题。
