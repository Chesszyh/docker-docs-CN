---
title: Mac 版 Docker Desktop 的虚拟机管理器 (VMM)
linkTitle: 虚拟机管理器 (VMM)
keywords: 虚拟化软件, 资源分配, mac, docker desktop, vm 监控, vm 性能, apple silicon, vmm
description: 了解 Mac 版 Docker Desktop 的虚拟机管理器 (VMM) 选项，包括专为 Apple Silicon 优化的新型 Docker VMM，提供更强的性能和效率。
weight: 110
aliases:
- /desktop/vmm/
---

Docker Desktop 支持多种虚拟机管理器 (VMM) 来驱动运行容器的 Linux 虚拟机。您可以根据您的系统架构（Intel 或 Apple Silicon）、性能需求和功能要求选择最合适的选项。本页提供了可用选项的概览。

要更改 VMM，请前往 **Settings（设置）** > **General（常规）** > **Virtual Machine Manager**。

## Docker VMM

{{< summary-bar feature_name="VMM" >}}

Docker VMM 是一款新型的、针对容器优化的 Hypervisor。通过对 Linux 内核和 Hypervisor 层的双重优化，Docker VMM 在常见的开发任务中实现了显著的性能提升。

Docker VMM 提供的一些关键性能增强包括：
 - **更快的 I/O 操作**：在冷缓存（Cold cache）情况下，使用 `find` 命令遍历大型共享文件系统的速度比使用 Apple Virtualization 框架快 2 倍。
 - **改进的缓存机制**：在热缓存（Warm cache）情况下，性能提升可达 25 倍，甚至超过了 Mac 原生操作的速度。

这些改进直接惠及那些在容器化开发过程中依赖频繁文件访问和整体系统响应速度的开发人员。Docker VMM 标志着速度上的重大飞跃，实现了更顺畅的工作流和更快的迭代周期。

> [!NOTE]
>
> Docker VMM 要求为 Docker Linux VM 分配至少 4GB 的内存。在启用 Docker VMM 之前，您需要增加分配的内存，这可以在 **Settings（设置）** 中的 **Resources（资源）** 选项卡下完成。

### 已知问题

由于 Docker VMM 仍处于 Beta 阶段，目前存在一些已知限制：

- Docker VMM 目前不支持 Rosetta，因此模拟 amd64 架构的速度较慢。Docker 正在探索潜在的解决方案。
- 某些数据库（如 MongoDB 和 Cassandra）在使用 Docker VMM 的 virtiofs 时可能会运行失败。该问题预计将在未来的版本中得到解决。

## Apple Virtualization 框架 (Apple Virtualization framework)

Apple Virtualization 框架是 Mac 上管理虚拟机的一个稳定且成熟的选项。多年来，它一直是许多 Mac 用户的可靠选择。该框架最适合那些偏好成熟方案、且需要稳定性能和广泛兼容性的开发人员。

## 针对 Apple Silicon 的 QEMU (旧版)

> [!NOTE]
>
> QEMU 将于 2025 年 7 月 14 日被弃用。有关更多信息，请参阅[博客公告](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)。

QEMU 是适用于 Apple Silicon Mac 的旧版虚拟化选项，主要用于支持较旧的用例。

Docker 建议迁移到较新的替代方案，如 Docker VMM 或 Apple Virtualization 框架，因为它们提供卓越的性能和持续的支持。特别是 Docker VMM，它提供了大幅的速度提升和更高效的开发环境，是 Apple Silicon 用户非常具有吸引力的选择。

请注意，这与在[多平台构建](/manuals/build/building/multi-platform.md#qemu)中使用 QEMU 模拟非原生架构无关。

## 针对 Intel Mac 的 HyperKit (旧版)

> [!NOTE]
>
> HyperKit 将在未来的版本中被弃用。

HyperKit 是另一个旧版虚拟化选项，专门针对 Intel 架构的 Mac。与 QEMU 类似，它目前仍然可用，但已被视为弃用。Docker 建议切换到现代化的替代方案，以获得更好的性能并确保您的配置具有前瞻性。