---
title: 限制
description: 增强容器隔离的限制
keywords: enhanced container isolation, security, sysbox, known issues, Docker Desktop
toc_max: 2
weight: 50
---

### ECI 对 WSL 的支持

> [!NOTE]
>
> Docker Desktop 需要 WSL 2 版本 2.1.5 或更高版本。要获取主机上的当前 WSL 版本，请键入 `wsl --version`。如果命令失败或返回的版本号早于 2.1.5，请在 Windows 命令或 PowerShell 终端中键入 `wsl --update` 将 WSL 更新到最新版本。

在 WSL 上的 ECI 不如在 Hyper-V 上安全，因为：

- 虽然 WSL 上的 ECI 仍然强化容器，使恶意工作负载不能轻易突破 Docker Desktop 的 Linux 虚拟机，但 WSL 上的 ECI 无法阻止 Docker Desktop 用户突破 Docker Desktop Linux 虚拟机。这些用户可以使用 `wsl -d docker-desktop` 命令轻易访问该虚拟机（以 root 身份），并使用该访问权限修改虚拟机内的 Docker Engine 设置。这使 Docker Desktop 用户可以控制 Docker Desktop 虚拟机，并允许他们绑过管理员通过[设置管理](../settings-management/_index.md)功能设置的 Docker Desktop 配置。相比之下，Hyper-V 上的 ECI 不允许 Docker Desktop 用户突破 Docker Desktop Linux 虚拟机。

- 使用 WSL 2，同一 Windows 主机上的所有 WSL 2 发行版共享 Linux 内核的同一实例。因此，Docker Desktop 无法确保 Docker Desktop Linux 虚拟机中内核的完整性，因为另一个 WSL 2 发行版可能会修改共享的内核设置。相比之下，使用 Hyper-V 时，Docker Desktop Linux 虚拟机具有专用内核，完全由 Docker Desktop 控制。

下表总结了这一点。

| 安全功能                                   | WSL 上的 ECI   | Hyper-V 上的 ECI   | 备注               |
| -------------------------------------------------- | ------------ | ---------------- | --------------------- |
| 强安全容器                         | 是          | 是              | 使恶意容器工作负载更难突破 Docker Desktop Linux 虚拟机和主机。 |
| Docker Desktop Linux 虚拟机受保护免受用户访问 | 否           | 是              | 在 WSL 上，用户可以直接访问 Docker Engine 或绑过 Docker Desktop 安全设置。 |
| Docker Desktop Linux 虚拟机具有专用内核     | 否           | 是              | 在 WSL 上，Docker Desktop 无法保证内核级配置的完整性。 |

通常，将 ECI 与 Hyper-V 一起使用比与 WSL 2 一起使用更安全。但 WSL 2 在主机机器上的性能和资源利用方面具有优势，它是用户在 Windows 主机上运行其喜爱的 Linux 发行版并从中访问 Docker 的绝佳方式。

### 使用"docker"驱动程序的 Docker 构建的 ECI 保护

在 Docker Desktop 4.30 之前，使用 buildx `docker` 驱动程序（默认）的 `docker build` 命令不受 ECI 保护，换句话说，构建在 Docker Desktop 虚拟机内以 root 身份运行。

从 Docker Desktop 4.30 开始，使用 buildx `docker` 驱动程序的 `docker build` 命令受 ECI 保护，除非 Docker Desktop 配置为使用 WSL 2（在 Windows 主机上）。

请注意，使用 `docker-container` 驱动程序的 `docker build` 命令始终受 ECI 保护。

### Docker Build 和 Buildx 有一些限制

启用 ECI 后，Docker build `--network=host` 和 Docker Buildx entitlements（`network.host`、`security.insecure`）不允许使用。需要这些的构建将无法正常工作。

### Kubernetes pods 尚未受保护

使用 Docker Desktop 集成的 Kubernetes 时，pods 尚未受 ECI 保护。因此，恶意或特权 pod 可能会危害 Docker Desktop Linux 虚拟机并绑过安全控制。

作为替代方案，您可以将 [K8s.io KinD](https://kind.sigs.k8s.io/) 工具与 ECI 一起使用。在这种情况下，每个 Kubernetes 节点在受 ECI 保护的容器内运行，从而更强地将 Kubernetes 集群与底层 Docker Desktop Linux 虚拟机（以及其中的 Docker Engine）隔离。无需特殊安排，只需启用 ECI 并像往常一样运行 KinD 工具即可。

### 扩展容器尚未受保护

扩展容器也尚未受 ECI 保护。确保您的扩展容器来自受信任的实体以避免问题。

### Docker Debug 容器尚未受保护

[Docker Debug](https://docs.docker.com/reference/cli/docker/debug/) 容器尚未受 ECI 保护。

### 不支持原生 Windows 容器

ECI 仅在 Docker Desktop 处于 Linux 容器模式（默认的、最常见的模式）时工作。当 Docker Desktop 配置为原生 Windows 容器模式时不支持（即，在 Windows 主机上，当 Docker Desktop 从其默认的 Linux 模式切换到原生 Windows 模式时不支持）。

### 生产环境中的使用

通常，用户在启用 ECI 的 Docker Desktop 中运行容器（使用 Sysbox 运行时）与在生产环境中通过标准 OCI `runc` 运行时运行相同容器时不应体验到差异。

但是，在某些情况下，通常是在容器中运行高级或特权工作负载时，用户可能会体验到一些差异。特别是，容器可能可以使用 ECI 运行但不能使用 `runc` 运行，反之亦然。
