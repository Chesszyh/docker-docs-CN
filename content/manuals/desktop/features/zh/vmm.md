---
title: Mac 版 Docker Desktop 的虚拟机管理器
linkTitle: 虚拟机管理器
keywords: virtualization software, resource allocation, mac, docker desktop, vm monitoring, vm performance, apple silicon
description: 了解 Mac 版 Docker Desktop 的虚拟机管理器（VMM）选项，包括为 Apple Silicon 提供增强性能和效率的新 Docker VMM
weight: 110
aliases:
- /desktop/vmm/
---

Docker Desktop 支持多种虚拟机管理器（Virtual Machine Manager，VMM）来驱动运行容器的 Linux 虚拟机。您可以根据系统架构（Intel 或 Apple Silicon）、性能需求和功能要求选择最合适的选项。本页概述了可用选项。

要更改 VMM，请转到 **Settings** > **General** > **Virtual Machine Manager**。

## Docker VMM

{{< summary-bar feature_name="VMM" >}}

Docker VMM 是一个新的、针对容器优化的 hypervisor。通过优化 Linux 内核和 hypervisor 层，Docker VMM 在常见开发任务中提供显著的性能增强。

Docker VMM 提供的一些关键性能增强包括：
 - 更快的 I/O 操作：使用冷缓存时，使用 `find` 遍历大型共享文件系统的速度比使用 Apple Virtualization 框架快 2 倍。
 - 改进的缓存：使用热缓存时，性能可提高多达 25 倍，甚至超过原生 Mac 操作。

这些改进直接影响依赖频繁文件访问和容器化开发期间整体系统响应能力的开发者。Docker VMM 标志着速度的重大飞跃，实现更流畅的工作流程和更快的迭代周期。

> [!NOTE]
>
> Docker VMM 要求为 Docker Linux 虚拟机分配至少 4GB 内存。需要在启用 Docker VMM 之前增加内存，这可以从 **Settings** 中的 **Resources** 选项卡完成。

### 已知问题

由于 Docker VMM 仍处于 Beta 阶段，存在一些已知限制：

- Docker VMM 目前不支持 Rosetta，因此 amd64 架构的模拟速度较慢。Docker 正在探索潜在的解决方案。
- 某些数据库，如 MongoDB 和 Cassandra，在使用带有 Docker VMM 的 virtiofs 时可能会失败。此问题预计将在未来版本中解决。

## Apple Virtualization 框架

Apple Virtualization 框架是在 Mac 上管理虚拟机的稳定且成熟的选项。多年来，它一直是许多 Mac 用户的可靠选择。此框架最适合偏好具有稳定性能和广泛兼容性的成熟解决方案的开发者。

## QEMU（传统）用于 Apple Silicon

> [!NOTE]
>
> QEMU 将于 2025 年 7 月 14 日弃用。有关更多信息，请参阅[博客公告](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)

QEMU 是 Apple Silicon Mac 的传统虚拟化选项，主要支持较旧的用例。

Docker 建议过渡到较新的替代方案，如 Docker VMM 或 Apple Virtualization 框架，因为它们提供更好的性能和持续支持。特别是 Docker VMM，它提供了显著的速度提升和更高效的开发环境，使其成为使用 Apple Silicon 工作的开发者的理想选择。

请注意，这与在[多平台构建](/manuals/build/building/multi-platform.md#qemu)中使用 QEMU 模拟非原生架构无关。

## HyperKit（传统）用于 Intel Mac

> [!NOTE]
>
> HyperKit 将在未来版本中弃用。

HyperKit 是另一个传统虚拟化选项，专门用于基于 Intel 的 Mac。与 QEMU 一样，它仍然可用但被视为已弃用。Docker 建议切换到现代替代方案以获得更好的性能并确保您的设置面向未来。
