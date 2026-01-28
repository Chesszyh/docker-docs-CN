---
description: Overview of persisting data in containers
title: 存储
weight: 20
keywords: storage, persistence, data persistence, volumes, mounts, bind mounts, tmpfs
aliases:
  - /engine/admin/volumes/
  - /storage/
---

默认情况下，在容器内创建的所有文件都存储在容器的可写层（writable container layer）上，该层位于只读、不可变的镜像层之上。

写入容器层的数据在容器被销毁时不会持久化。这意味着如果其他进程需要这些数据，将很难从容器中获取。

可写层是每个容器独有的。你无法轻松地将数据从可写层提取到主机或另一个容器。

## 存储挂载选项

Docker 支持以下类型的存储挂载，用于在容器可写层之外存储数据：

- [卷挂载](#volume-mounts)
- [绑定挂载](#bind-mounts)
- [tmpfs 挂载](#tmpfs-mounts)
- [命名管道](#named-pipes)

无论你选择使用哪种类型的挂载，从容器内部看，数据的呈现方式都是相同的。它以目录或单个文件的形式暴露在容器的文件系统中。

### 卷挂载

卷（Volume）是由 Docker 守护进程管理的持久存储机制。即使使用它们的容器被移除，卷中的数据也会保留。卷数据存储在主机的文件系统上，但要与卷中的数据交互，你必须将卷挂载到容器中。不支持直接访问或与卷数据交互，这是未定义的行为，可能导致卷或其数据以意外方式损坏。

卷非常适合性能关键型数据处理和长期存储需求。由于存储位置在守护进程主机上管理，卷提供了与直接访问主机文件系统相同的原始文件性能。

### 绑定挂载

绑定挂载（Bind mount）在主机系统路径和容器之间创建直接链接，允许访问存储在主机任何位置的文件或目录。由于它们不受 Docker 隔离，主机上的非 Docker 进程和容器进程都可以同时修改挂载的文件。

当你需要能够从容器和主机两端访问文件时，请使用绑定挂载。

### tmpfs 挂载

tmpfs 挂载将文件直接存储在主机的内存中，确保数据不会写入磁盘。这种存储是临时的：当容器停止或重启时，或当主机重启时，数据就会丢失。tmpfs 挂载既不会在 Docker 主机上持久化数据，也不会在容器的文件系统中持久化数据。

这些挂载适用于需要临时内存存储的场景，例如缓存中间数据、处理凭据等敏感信息或减少磁盘 I/O。仅当数据不需要在当前容器会话之外持久化时，才使用 tmpfs 挂载。

### 命名管道

[命名管道](https://docs.microsoft.com/en-us/windows/desktop/ipc/named-pipes)可用于 Docker 主机和容器之间的通信。常见的用例是在容器内运行第三方工具，并使用命名管道连接到 Docker Engine API。

## 后续步骤

- 了解更多关于[卷](./volumes.md)的信息。
- 了解更多关于[绑定挂载](./bind-mounts.md)的信息。
- 了解更多关于[tmpfs 挂载](./tmpfs.md)的信息。
- 了解更多关于[存储驱动程序](/engine/storage/drivers/)的信息，它们与绑定挂载或卷无关，但允许你在容器的可写层中存储数据。
