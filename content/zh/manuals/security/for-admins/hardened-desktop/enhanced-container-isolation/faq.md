---
title: 增强容器隔离常见问题
linkTitle: 常见问题
description: 增强容器隔离的常见问题
keywords: enhanced container isolation, security, faq, sysbox, Docker Desktop
toc_max: 2
aliases:
 - /desktop/hardened-desktop/enhanced-container-isolation/faq/
weight: 40
---

### 启用 ECI 后，我需要改变使用 Docker 的方式吗？

不需要，您可以继续像往常一样使用 Docker。ECI 在底层工作，创建更安全的容器。

### 所有容器工作负载都能与 ECI 良好配合吗？

绑大多数容器工作负载在启用 ECI 的情况下运行良好，但少数工作负载（目前）不行。对于那些尚不能与增强容器隔离一起工作的少数工作负载，Docker 正在持续改进该功能以将其减少到最低限度。

### 我可以使用 ECI 运行特权容器吗？

是的，您可以在容器中使用 `--privileged` 标志，但与没有 ECI 的特权容器不同，容器只能使用其提升的权限来访问分配给容器的资源。它无法访问 Docker Desktop Linux 虚拟机中的全局内核资源。这使您可以安全地运行特权容器（包括 Docker-in-Docker）。有关更多信息，请参阅[主要功能和优势](features-benefits.md#特权容器也得到保护)。

### 所有特权容器工作负载都能使用 ECI 运行吗？

不能。想要访问 Docker Desktop Linux 虚拟机内全局内核资源的特权容器工作负载将无法工作。例如，您不能使用特权容器加载内核模块。

### 为什么不直接限制 `--privileged` 标志的使用？

特权容器通常用于在容器中运行高级工作负载，例如 Docker-in-Docker 或 Kubernetes-in-Docker，执行内核操作（如加载模块），或访问硬件设备。

ECI 允许运行高级工作负载，但拒绝执行内核操作或访问硬件设备的能力。

### ECI 是否限制容器内的绑定挂载？

是的，它限制将位于 Docker Desktop Linux 虚拟机中的目录绑定挂载到容器中。

它不限制将主机机器文件绑定挂载到容器中，如通过 Docker Desktop 的 **Settings** > **Resources** > **File Sharing** 配置的那样。

### 启用 ECI 时，我可以将主机的 Docker Socket 挂载到容器中吗？

默认情况下，出于安全原因，ECI 会阻止将主机的 Docker socket 绑定挂载到容器中。但是，有些合法的用例需要这样做，例如使用 [Testcontainers](https://testcontainers.com/) 进行本地测试。

为了启用此类用例，可以配置 ECI 以允许将 Docker socket 挂载到容器中，但仅限于您选择的（即受信任的）容器镜像，甚至可以限制容器可以通过 socket 发送到 Docker Engine 的命令。请参阅 [ECI Docker socket 挂载权限](config.md#docker-socket-挂载权限)。

### ECI 是否保护使用 Docker Desktop 启动的所有容器？

尚未完全保护。它保护用户通过 `docker create` 和 `docker run` 启动的所有容器。

对于由 `docker build` 隐式创建的容器以及 Docker Desktop 的集成 Kubernetes，保护程度因 Docker Desktop 版本而异（请参阅以下两个常见问题）。

### ECI 是否保护 `docker build` 隐式使用的容器？

在 Docker Desktop 4.19 之前，ECI 不保护 `docker build` 在构建过程中隐式使用的容器。

从 Docker Desktop 4.19 开始，当使用 [Docker container 驱动程序](/manuals/build/builders/drivers/_index.md)时，ECI 保护 `docker build` 使用的容器。

此外，从 Docker Desktop 4.30 开始，当使用默认的"docker"构建驱动程序时，ECI 也保护 `docker build` 使用的容器，适用于 Docker Desktop 支持的所有平台，除了带有 WSL 2 的 Windows。

### ECI 是否保护 Docker Desktop 中的 Kubernetes？

在 Docker Desktop 4.38 之前，ECI 不保护集成在 Docker Desktop 中的 Kubernetes 集群。

从 Docker Desktop 4.38 开始，当使用新的 **kind** 配置器时（请参阅[在 Kubernetes 上部署](/manuals/desktop/features/kubernetes.md)），ECI 保护集成的 Kubernetes 集群。在这种情况下，多节点 Kubernetes 集群中的每个节点实际上是一个受 ECI 保护的容器。禁用 ECI 时，Kubernetes 集群中的每个节点是一个安全性较低的完全特权容器。

当使用较旧的 **Kubeadm** 单节点集群配置器时，ECI 不保护集成的 Kubernetes 集群。

### ECI 是否保护在启用 ECI 之前启动的容器？

不保护。在启用 ECI 之前创建的容器不受保护。因此，建议您在启用 ECI 之前删除所有容器。

### ECI 是否影响容器的性能？

ECI 对容器性能的影响很小。例外情况是执行大量 `mount` 和 `umount` 系统调用的容器，因为这些调用会被 Sysbox 容器运行时拦截和审查，以确保它们不会被用来突破容器的文件系统。

### 使用 ECI 时，用户是否仍然可以从 CLI 覆盖 `--runtime` 标志？

不能。启用 ECI 后，Sysbox 被设置为 Docker Desktop 用户部署的容器的默认（且唯一）运行时。如果用户尝试覆盖运行时（例如，`docker run --runtime=runc`），此请求将被忽略，容器将通过 Sysbox 运行时创建。

不允许 `runc` 的原因是它允许用户在 Docker Desktop Linux 虚拟机上以"真正的 root"身份运行，从而使他们隐式控制虚拟机，并能够修改 Docker Desktop 的管理配置。

### ECI 与 Docker Engine 的 userns-remap 模式有何不同？

请参阅[工作原理](how-eci-works.md#增强容器隔离与-docker-userns-remap-模式)。

### ECI 与 Rootless Docker 有何不同？

请参阅[工作原理](how-eci-works.md#增强容器隔离与-rootless-docker)
