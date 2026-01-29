---
title: containerd 镜像库
weight: 80
description: 了解如何在 Docker Desktop 中启用 containerd 集成功能
keywords: Docker, containerd, engine, image store, lazy-pull
toc_max: 3
aliases:
- /desktop/containerd/
---

Docker Desktop 正在过渡到使用 containerd 进行镜像和文件系统管理。本页概述了 containerd 镜像库的优势、设置过程以及其带来的新功能。

> [!NOTE]
> 
> Docker Desktop 分别为“经典”镜像库和 containerd 镜像库维护独立的存储。在它们之间切换时，非活动存储中的镜像和容器仍保留在磁盘上，但在您切换回之前会被隐藏。

## 什么是 `containerd`？

`containerd` 是一个容器运行时，为容器生命周期管理提供轻量级、一致的接口。它已经被 Docker Engine 在后台用于创建、启动和停止容器。

Docker Desktop 持续进行的 containerd 集成现在扩展到了镜像库，提供了更大的灵活性和对现代镜像的支持。

## 什么是 `containerd` 镜像库？

镜像库是负责在文件系统上推送、拉取和存储镜像的组件。

经典的 Docker 镜像库在支持的镜像类型方面存在局限。例如，它不支持包含清单列表（manifest lists）的镜像索引（image indices）。例如，当您创建多平台镜像时，镜像索引会解析该镜像的所有特定于平台的变体。在构建带有证明（attestations）的镜像时，也需要镜像索引。

containerd 镜像库扩展了 Docker Engine 可以原生交互的镜像类型范围。虽然这是一项底层架构更改，但它是开启一系列新用例的前提条件，包括：

- [构建多平台镜像](#构建多平台镜像)和带有证明的镜像
- 支持使用具有独特特性的 containerd 快照器（snapshotters），例如用于在容器启动时延迟拉取（lazy-pulling）镜像的 [stargz][1]，或用于点对点镜像分发的 [nydus][2] 和 [dragonfly][3]。
- 能够运行 [Wasm](wasm.md) 容器

[1]: https://github.com/containerd/stargz-snapshotter
[2]: https://github.com/containerd/nydus-snapshotter
[3]: https://github.com/dragonflyoss/image-service

## 启用 containerd 镜像库

containerd 镜像库在 Docker Desktop 4.34 及更高版本中默认启用，但仅适用于全新安装或执行恢复出厂设置的情况。如果您是从较早版本的 Docker Desktop 升级，或者使用的是旧版本，则必须手动切换到 containerd 镜像库。

要在 Docker Desktop 中手动启用此功能的步骤：

1. 导航到 Docker Desktop 中的 **Settings**（设置）。
2. 在 **General**（常规）选项卡中，勾选 **Use containerd for pulling and storing images**。
3. 选择 **Apply**（应用）。

要禁用 containerd 镜像库，请取消勾选 **Use containerd for pulling and storing images** 复选框。

## 构建多平台镜像

“多平台镜像”是指针对多种不同架构的一组镜像。开箱即用状态下，Docker Desktop 的默认构建器不支持构建多平台镜像。

```console
$ docker build --platform=linux/amd64,linux/arm64 .
[+] Building 0.0s (0/0)
ERROR: Multi-platform build is not supported for the docker driver.
Switch to a different driver, or turn on the containerd image store, and try again.
Learn more at https://docs.docker.com/go/build-multi-platform/
```

启用 containerd 镜像库后，您可以构建多平台镜像并将其加载到本地镜像库中：

<script async id="asciicast-ZSUI4Mi2foChLjbevl2dxt5GD" src="https://asciinema.org/a/ZSUI4Mi2foChLjbevl2dxt5GD.js"></script>
