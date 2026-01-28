---
description: >
  Learn how to read container logs locally when using a third party logging
  solution.
keywords: >
  docker, logging, driver, dual logging, dual logging, cache, ring-buffer,
  configuration
title: 在远程日志驱动程序中使用 docker logs
aliases:
  - /config/containers/logging/dual-logging/
---

## 概述

无论配置了哪种日志驱动程序或插件，你都可以使用 `docker logs` 命令读取容器日志。Docker Engine 使用 [`local`](drivers/local.md) 日志驱动程序作为缓存，用于读取容器的最新日志。这称为双重日志（dual logging）。默认情况下，缓存启用了日志文件轮转，每个容器限制为最多 5 个文件，每个文件最大 20 MB（压缩前）。

请参阅[配置选项](#configuration-options)部分自定义这些默认值，或参阅[禁用双重日志](#disable-the-dual-logging-cache)部分禁用此功能。

## 前提条件

如果配置的日志驱动程序不支持读取日志，Docker Engine 会自动启用双重日志。

以下示例显示了在有和没有双重日志功能时运行 `docker logs` 命令的结果：

### 没有双重日志功能

当容器配置了远程日志驱动程序（如 `splunk`）且禁用了双重日志时，尝试在本地读取容器日志会显示错误：

- 步骤 1：配置 Docker 守护进程

  ```console
  $ cat /etc/docker/daemon.json
  {
    "log-driver": "splunk",
    "log-opts": {
      "cache-disabled": "true",
      ... (options for "splunk" logging driver)
    }
  }
  ```

- 步骤 2：启动容器

  ```console
  $ docker run -d busybox --name testlog top
  ```

- 步骤 3：读取容器日志

  ```console
  $ docker logs 7d6ac83a89a0
  Error response from daemon: configured logging driver does not support reading
  ```

### 有双重日志功能

启用双重日志缓存后，即使日志驱动程序不支持读取日志，也可以使用 `docker logs` 命令读取日志。以下示例显示了一个守护进程配置，使用 `splunk` 远程日志驱动程序作为默认值，并启用了双重日志缓存：

- 步骤 1：配置 Docker 守护进程

  ```console
  $ cat /etc/docker/daemon.json
  {
    "log-driver": "splunk",
    "log-opts": {
      ... (options for "splunk" logging driver)
    }
  }
  ```

- 步骤 2：启动容器

  ```console
  $ docker run -d busybox --name testlog top
  ```

- 步骤 3：读取容器日志

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
> 对于支持读取日志的日志驱动程序，如 `local`、`json-file` 和 `journald` 驱动程序，在双重日志功能可用之前和之后的功能没有区别。对于这些驱动程序，在两种场景下都可以使用 `docker logs` 读取日志。

### 配置选项

双重日志缓存接受与 [`local` 日志驱动程序](drivers/local.md)相同的配置选项，但带有 `cache-` 前缀。这些选项可以按容器指定，新容器的默认值可以使用[守护进程配置文件](/reference/cli/dockerd/#daemon-configuration-file)设置。

默认情况下，缓存启用了日志文件轮转，每个容器限制为最多 5 个文件，每个文件最大 20MB（压缩前）。使用下面描述的配置选项自定义这些默认值。

| 选项             | 默认值    | 描述                                                                                                                                              |
| :--------------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cache-disabled` | `"false"` | 禁用本地缓存。以字符串形式传递的布尔值（`true`、`1`、`0` 或 `false`）。                                                                           |
| `cache-max-size` | `"20m"`   | 缓存轮转前的最大大小。一个正整数加上表示计量单位的修饰符（`k`、`m` 或 `g`）。                                                                      |
| `cache-max-file` | `"5"`     | 可以存在的最大缓存文件数。如果轮转日志创建了过多文件，则删除最旧的文件。一个正整数。                                                              |
| `cache-compress` | `"true"`  | 启用或禁用轮转日志文件的压缩。以字符串形式传递的布尔值（`true`、`1`、`0` 或 `false`）。                                                           |

## 禁用双重日志缓存

使用 `cache-disabled` 选项禁用双重日志缓存。在只通过远程日志系统读取日志且不需要通过 `docker logs` 读取日志进行调试的情况下，禁用缓存可以节省存储空间。

可以为单个容器禁用缓存，也可以在使用[守护进程配置文件](/reference/cli/dockerd/#daemon-configuration-file)时为新容器设置默认禁用缓存。

以下示例使用守护进程配置文件将 [`splunk`](drivers/splunk.md) 日志驱动程序设置为默认值，并禁用缓存：

```console
$ cat /etc/docker/daemon.json
{
  "log-driver": "splunk",
  "log-opts": {
    "cache-disabled": "true",
    ... (options for "splunk" logging driver)
  }
}
```

> [!NOTE]
>
> 对于支持读取日志的日志驱动程序，如 `local`、`json-file` 和 `journald` 驱动程序，不使用双重日志，禁用该选项没有效果。

## 限制

- 如果使用发送远程日志的日志驱动程序或插件的容器出现网络问题，则不会向本地缓存写入。
- 如果由于任何原因（文件系统已满、写入权限被移除）导致写入 `logdriver` 失败，则缓存写入失败并记录在守护进程日志中。不会重试向缓存写入日志条目。
- 在默认配置中，由于使用环形缓冲区来防止在文件写入缓慢的情况下阻塞容器的 stdio，可能会从缓存中丢失一些日志。管理员必须在守护进程关闭时修复这些问题。
