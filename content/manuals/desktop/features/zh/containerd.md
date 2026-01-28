---
title: containerd 镜像存储
weight: 80
description: 如何在 Docker Desktop 中启用 containerd 集成功能
keywords: Docker, containerd, engine, image store, lazy-pull
toc_max: 3
aliases:
- /desktop/containerd/
---

Docker Desktop 正在过渡到使用 containerd 进行镜像和文件系统管理。本页概述了 containerd 镜像存储带来的优势、设置流程以及启用的新功能。

> [!NOTE]
>
> Docker Desktop 为经典镜像存储和 containerd 镜像存储维护独立的镜像库。
> 在两者之间切换时，非活动存储中的镜像和容器仍保留在磁盘上，但在切换回来之前将被隐藏。

## 什么是 `containerd`？

`containerd` 是一个容器运行时（container runtime），为容器生命周期管理提供轻量级、一致的接口。Docker Engine 底层已经使用它来创建、启动和停止容器。

Docker Desktop 对 containerd 的持续集成现已扩展到镜像存储，提供更大的灵活性和现代镜像支持。

## 什么是 `containerd` 镜像存储？

镜像存储是负责推送、拉取和在文件系统上存储镜像的组件。

经典 Docker 镜像存储支持的镜像类型有限。例如，它不支持包含清单列表（manifest lists）的镜像索引（image indices）。当您创建多平台镜像时，镜像索引会解析该镜像的所有平台特定变体。构建带有证明（attestations）的镜像时也需要镜像索引。

containerd 镜像存储扩展了 Docker Engine 可以原生交互的镜像类型范围。虽然这是一个底层架构变更，但它是解锁一系列新用例的先决条件，包括：

- [构建多平台镜像](#build-multi-platform-images)和带有证明的镜像
- 支持使用具有独特特性的 containerd 快照器（snapshotters），
  例如用于在容器启动时延迟拉取镜像的 [stargz][1]，
  或用于点对点镜像分发的 [nydus][2] 和 [dragonfly][3]。
- 能够运行 [Wasm](wasm.md) 容器

[1]: https://github.com/containerd/stargz-snapshotter
[2]: https://github.com/containerd/nydus-snapshotter
[3]: https://github.com/dragonflyoss/image-service

## 启用 containerd 镜像存储

containerd 镜像存储在 Docker Desktop 4.34 及更高版本中默认启用，但仅适用于全新安装或执行恢复出厂设置的情况。如果您从早期版本的 Docker Desktop 升级，或者使用较旧版本的 Docker Desktop，则必须手动切换到 containerd 镜像存储。

要在 Docker Desktop 中手动启用此功能：

1. 导航到 Docker Desktop 中的 **Settings**。
2. 在 **General** 选项卡中，勾选 **Use containerd for pulling and storing images**。
3. 选择 **Apply**。

要禁用 containerd 镜像存储，请取消勾选 **Use containerd for pulling and storing images** 复选框。

## 构建多平台镜像

多平台镜像（multi-platform image）一词指的是适用于多种不同架构的镜像捆绑包。开箱即用时，Docker Desktop 的默认构建器不支持构建多平台镜像。

```console
$ docker build --platform=linux/amd64,linux/arm64 .
[+] Building 0.0s (0/0)
ERROR: Multi-platform build is not supported for the docker driver.
Switch to a different driver, or turn on the containerd image store, and try again.
Learn more at https://docs.docker.com/go/build-multi-platform/
```

启用 containerd 镜像存储后，您可以构建多平台镜像并将其加载到本地镜像存储中：

<script async id="asciicast-ZSUI4Mi2foChLjbevl2dxt5GD" src="https://asciinema.org/a/ZSUI4Mi2foChLjbevl2dxt5GD.js"></script>


