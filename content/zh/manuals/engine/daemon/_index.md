---
description: 配置 Docker 守护进程
keywords: docker, daemon, configuration, 守护进程, 配置
title: Docker 守护进程配置概览
linkTitle: 守护进程
weight: 60
alias:
  - /articles/chef/
  - /articles/configuring/
  - /articles/dsc/
  - /articles/puppet/
  - /config/thirdparty/
  - /config/thirdparty/ansible/
  - /config/thirdparty/chef/
  - /config/thirdparty/dsc/
  - /config/thirdparty/puppet/
  - /engine/admin/
  - /engine/admin/ansible/
  - /engine/admin/chef/
  - /engine/admin/configuring/
  - /engine/admin/dsc/
  - /engine/admin/puppet/
  - /engine/articles/chef/
  - /engine/articles/configuring/
  - /engine/articles/dsc/
  - /engine/articles/puppet/
  - /engine/userguide/
  - /config/daemon/
---

本页介绍如何自定义 Docker 守护进程 `dockerd`。

> [!NOTE]
> 
> 本页适用于手动安装 Docker Engine 的用户。如果您使用的是 Docker Desktop，请参考 [设置页面](/manuals/desktop/settings-and-maintenance/settings.md#docker-engine)。

## 配置 Docker 守护进程

配置 Docker 守护进程有两种方式：

- 使用 JSON 配置文件。这是首选方案，因为它将所有配置集中在一个地方。
- 在启动 `dockerd` 时使用标志 (flags)。

您可以同时使用这两个选项，只要不在标志和 JSON 文件中指定相同的选项即可。如果发生这种情况，Docker 守护进程将无法启动并打印错误消息。

### 配置文件

下表显示了 Docker 守护进程默认期望找到配置文件的位置，具体取决于您的系统以及运行守护进程的方式。

| 操作系统和配置       | 文件位置                                   |
| -------------------- | ------------------------------------------ |
| Linux, 常规设置      | `/etc/docker/daemon.json`                  |
| Linux, 无根模式      | `~/.config/docker/daemon.json`             |
| Windows              | `C:\ProgramData\docker\config\daemon.json` |

对于无根模式，守护进程尊重 `XDG_CONFIG_HOME` 变量。如果设置了该变量，预期的文件位置为 `$XDG_CONFIG_HOME/docker/daemon.json`。

您还可以在启动时使用 `dockerd --config-file` 标志显式指定配置文件的位置。

在 [dockerd 参考文档](/reference/cli/dockerd.md#daemon-configuration-file) 中了解可用的配置选项。

### 使用标志进行配置

您也可以手动启动 Docker 守护进程并使用标志对其进行配置。这对于故障排查非常有用。

以下是一个手动启动 Docker 守护进程的示例，使用了与之前 JSON 配置中相同的配置：

```console
$ dockerd --debug \
  --tls=true \
  --tlscert=/var/docker/server.pem \
  --tlskey=/var/docker/serverkey.pem \
  --host tcp://192.168.59.3:2376
```

在 [dockerd 参考文档](/reference/cli/dockerd.md) 中了解可用的配置选项，或者运行以下命令：

```console
$ dockerd --help
```

## 守护进程数据目录

Docker 守护进程将所有数据持久化在单个目录中。这会跟踪与 Docker 相关的所有内容，包括容器、镜像、卷、服务定义和机密。

默认情况下，该目录为：

- Linux：`/var/lib/docker`
- Windows：`C:\ProgramData\docker`

您可以使用 `data-root` 配置选项配置 Docker 守护进程使用不同的目录。例如：

```json
{
  "data-root": "/mnt/docker-data"
}
```

由于 Docker 守护进程的状态保存在此目录中，请确保为每个守护进程使用专用目录。如果两个守护进程共享同一个目录 (例如 NFS 共享)，您将遇到难以排查的错误。

## 后续步骤

Docker 文档中讨论了许多特定的配置选项。您可以接着阅读以下内容：

- [自动启动容器](/manuals/engine/containers/start-containers-automatically.md)
- [限制容器资源](/manuals/engine/containers/resource_constraints.md)
- [配置存储驱动程序](/manuals/engine/storage/drivers/select-storage-driver.md)
- [容器安全](/manuals/engine/security/_index.md)
- [配置 Docker 守护进程使用代理](./proxy.md)
