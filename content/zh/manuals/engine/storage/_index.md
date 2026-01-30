---
description: 容器持久化数据概览
title: 存储
weight: 20
keywords: storage, persistence, data persistence, volumes, mounts, bind mounts, tmpfs, 存储, 持久化, 卷, 挂载, 绑定挂载
aliases:
  - /engine/admin/volumes/
  - /storage/
---

默认情况下，在容器内部创建的所有文件都存储在可写的容器层中，该层位于只读的、不可变的镜像层之上。

写入容器层的数据在容器销毁时不会持久化。这意味着如果另一个进程需要这些数据，可能很难从容器中获取。

可写层对于每个容器都是唯一的。您无法轻松地将数据从可写层提取到主机或其他容器中。

## 存储挂载选项

Docker 支持以下类型的存储挂载，用于在容器的可写层之外存储数据：

- [卷挂载 (Volume mounts)](#volume-mounts)
- [绑定挂载 (Bind mounts)](#bind-mounts)
- [tmpfs 挂载 (tmpfs mounts)](#tmpfs-mounts)
- [命名管道 (Named pipes)](#named-pipes)

无论您选择哪种挂载类型，从容器内部看，数据看起来都是一样的。它在容器文件系统中显示为目录或单个文件。

### 卷挂载 (Volume mounts)

卷 (Volumes) 是由 Docker 守护进程管理的持久化存储机制。即使在使用它们的容器被移除后，它们也会保留数据。卷数据存储在主机的网络文件系统上，但为了与卷中的数据交互，您必须将卷挂载到容器。直接访问或交互卷数据是不受支持的、未定义的行为，可能会导致卷或其数据以意外方式损坏。

卷非常适合对性能要求极高的数据处理和长期存储需求。由于存储位置由守护进程主机管理，卷提供的原始文件性能与直接访问主机文件系统相同。

### 绑定挂载 (Bind mounts)

绑定挂载 (Bind mounts) 在主机系统路径和容器之间创建直接链接，允许访问存储在主机任何位置的文件或目录。由于它们不受 Docker 隔离，主机上的非 Docker 进程和容器进程可以同时修改挂载的文件。

当您需要能够从容器和主机双方访问文件时，请使用绑定挂载。

### tmpfs 挂载 (tmpfs mounts)

tmpfs 挂载直接将文件存储在主机机器的内存中，确保数据不被写入磁盘。这种存储是临时性的：当容器停止或重启，或者主机重启时，数据就会丢失。tmpfs 挂载不会在 Docker 主机或容器文件系统中持久化数据。

这些挂载适用于需要临时、内存存储的场景，例如缓存中间数据、处理凭据等敏感信息，或者减少磁盘 I/O。仅在数据不需要持久化到当前容器会话之外时使用 tmpfs 挂载。

### 命名管道 (Named pipes)

[命名管道](https://docs.microsoft.com/en-us/windows/desktop/ipc/named-pipes) 可用于 Docker 主机与容器之间的通信。常见的用例是在容器内运行第三方工具，并通过命名管道连接到 Docker Engine API。

## 后续步骤

- 详细了解 [卷 (volumes)](./volumes.md)。
- 详细了解 [绑定挂载 (bind mounts)](./bind-mounts.md)。
- 详细了解 [tmpfs 挂载 (tmpfs mounts)](./tmpfs.md)。
- 详细了解 [存储驱动程序 (storage drivers)](/engine/storage/drivers/)，它们与绑定挂载或卷无关，但允许您在容器的可写层中存储数据。
