---
title: containerd 镜像存储
weight: 80
description: 如何在 Docker Desktop 中启用 containerd 集成功能
keywords: Docker, containerd, engine, 镜像存储, image store, lazy-pull, 懒加载拉取
toc_max: 3
aliases:
- /desktop/containerd/
---

Docker Desktop 正在过渡到使用 containerd 来进行镜像和文件系统管理。本页概述了 containerd 镜像存储带来的优势、设置过程以及由此启用的新功能。

> [!NOTE]
> 
> Docker Desktop 为经典镜像存储和 containerd 镜像存储分别维护了独立的镜像库。在两者之间切换时，处于非活动状态的存储库中的镜像和容器将保留在磁盘上，但会被隐藏，直到您切换回该模式。

## 什么是 `containerd`？

`containerd` 是一个容器运行时，它为容器生命周期管理提供了一个轻量级且一致的界面。Docker Engine 已经在底层使用它来创建、启动和停止容器。

Docker Desktop 正在进行的 containerd 集成现在已扩展到镜像存储（image store），从而提供了更多的灵活性和对现代镜像的支持。

## 什么是 `containerd` 镜像存储？

镜像存储是负责在文件系统上推送、拉取和存储镜像的组件。

经典（Classic）的 Docker 镜像存储在支持的镜像类型方面存在局限。例如，它不支持镜像索引（image indices），即包含清单列表（manifest lists）的内容。例如，当您创建多平台镜像时，镜像索引会解析该镜像的所有特定于平台的变体。在构建带有证明（attestations）的镜像时，也需要镜像索引。

containerd 镜像存储扩展了 Docker Engine 能够原生交互的镜像类型范围。虽然这是一个底层的架构变化，但它是解锁一系列新用例的前提，包括：

- [构建多平台镜像](#构建多平台镜像)以及带有证明的镜像
- 支持使用具有独特特性的 containerd 快照程序（snapshotters），例如用于在容器启动时实现镜像延迟拉取的 [stargz][1]，或用于点对点镜像分发的 [nydus][2] 和 [dragonfly][3]。
- 运行 [Wasm](wasm.md) 容器的能力

[1]: https://github.com/containerd/stargz-snapshotter
[2]: https://github.com/containerd/nydus-snapshotter
[3]: https://github.com/dragonflyoss/image-service

## 启用 containerd 镜像存储

containerd 镜像存储在 Docker Desktop 4.34 及更高版本中默认启用，但仅适用于全新安装或执行恢复出厂设置的情况。如果您是从旧版本的 Docker Desktop 升级，或者使用的是较早版本的 Docker Desktop，则必须手动切换到 containerd 镜像存储。

要在 Docker Desktop 中手动启用此功能：

1. 导航到 Docker Desktop 中的 **Settings（设置）**。
2. 在 **General（常规）** 选项卡中，勾选 **Use containerd for pulling and storing images（使用 containerd 拉取和存储镜像）**。
3. 选择 **Apply（应用）**。

要禁用 containerd 镜像存储，只需取消勾选 **Use containerd for pulling and storing images** 即可。

## 构建多平台镜像

多平台镜像（multi-platform image）是指针对多种不同架构的一组镜像包。开箱即用的 Docker Desktop 默认构建器不支持构建多平台镜像。

```console
$ docker build --platform=linux/amd64,linux/arm64 .
[+] Building 0.0s (0/0)
ERROR: Multi-platform build is not supported for the docker driver.
Switch to a different driver, or turn on the containerd image store, and try again.
Learn more at https://docs.docker.com/go/build-multi-platform/
```

启用 containerd 镜像存储后，您可以构建多平台镜像并将其加载到本地镜像存储中：

<script async id="asciicast-ZSUI4Mi2foChLjbevl2dxt5GD" src="https://asciinema.org/a/ZSUI4Mi2foChLjbevl2dxt5GD.js"></script>