---
title: 在 Docker Engine 中使用 containerd 镜像存储
linkTitle: containerd 镜像存储
weight: 50
keywords: containerd, snapshotters, image store, docker engine, 快照器, 镜像存储
description: 了解如何在 Docker Engine 上启用 containerd 镜像存储
aliases:
  - /storage/containerd/
---

{{< summary-bar feature_name="containerd" >}}

containerd 是行业标准的容器运行时，它使用快照器 (snapshotters) 而不是传统的存储驱动程序来存储镜像和容器数据。虽然 `overlay2` 驱动程序仍然是 Docker Engine 的默认驱动程序，但您可以选择使用 containerd 快照器作为实验性功能。

要了解有关 containerd 镜像存储及其优势的更多信息，请参阅 [Docker Desktop 上的 containerd 镜像存储](/manuals/desktop/features/containerd.md)。

## 在 Docker Engine 上启用 containerd 镜像存储

切换到 containerd 快照器会导致您暂时丢失使用传统存储驱动程序创建的镜像和容器。这些资源仍然存在于您的文件系统中，您可以通过关闭 containerd 快照器功能来找回它们。

以下步骤说明了如何启用 containerd 快照器功能。

1. 将以下配置添加到您的 `/etc/docker/daemon.json` 配置文件中：

   ```json
   {
     "features": {
       "containerd-snapshotter": true
     }
   }
   ```

2. 保存文件。
3. 重启守护进程以使更改生效。

   ```console
   $ sudo systemctl restart docker
   ```

重启守护进程后，运行 `docker info` 会显示您正在使用 containerd 快照器存储驱动程序。

```console
$ docker info -f '{{ .DriverStatus }}'
[[driver-type io.containerd.snapshotter.v1]]
```

Docker Engine 默认使用 `overlayfs` containerd 快照器。
