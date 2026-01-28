---
description: 了解如何在 Docker Desktop 上部署到 Kubernetes
keywords: deploy, kubernetes, kubectl, orchestration, Docker Desktop
title: 使用 Docker Desktop 在 Kubernetes 上部署
linkTitle: 在 Kubernetes 上部署
aliases:
- /docker-for-windows/kubernetes/
- /docker-for-mac/kubernetes/
- /desktop/kubernetes/
weight: 60
---

Docker Desktop 包含独立的 Kubernetes 服务器和客户端，以及 Docker CLI 集成，可直接在您的机器上进行本地 Kubernetes 开发和测试。

Kubernetes 服务器作为单节点或多节点集群运行，运行在 Docker 容器中。这种轻量级设置帮助您探索 Kubernetes 功能、测试工作负载，并与其他 Docker 功能并行使用容器编排。

Docker Desktop 上的 Kubernetes 与其他工作负载并行运行，包括 Swarm 服务和独立容器。

![k8s 设置](../images/k8s-settings.png)

## 在 Docker Desktop 中启用 Kubernetes 会发生什么？

以下操作会在 Docker Desktop 后端和虚拟机中触发：

- 生成证书和集群配置
- 下载并安装 Kubernetes 内部组件
- 集群启动
- 安装网络和存储的附加控制器

在 Docker Desktop 中开启或关闭 Kubernetes 服务器不会影响您的其他工作负载。

## 安装并开启 Kubernetes

1. 打开 Docker Desktop Dashboard 并导航到 **Settings**。
2. 选择 **Kubernetes** 选项卡。
3. 开启 **Enable Kubernetes**。
4. 选择您的[集群配置方法](#cluster-provisioning-method)。
5. 选择 **Apply** 保存设置。

这会设置运行 Kubernetes 服务器作为容器所需的镜像，并在您的系统上安装 `kubectl` 命令行工具，位于 `/usr/local/bin/kubectl`（Mac）或 `C:\Program Files\Docker\Docker\resources\bin\kubectl.exe`（Windows）。

   > [!NOTE]
   >
   > Linux 版 Docker Desktop 默认不包含 `kubectl`。您可以按照 [Kubernetes 安装指南](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)单独安装它。确保 `kubectl` 二进制文件安装在 `/usr/local/bin/kubectl`。

当 Kubernetes 启用时，其状态会显示在 Docker Desktop Dashboard 页脚和 Docker 菜单中。

您可以使用以下命令检查正在使用的 Kubernetes 版本：

```console
$ kubectl version
```

### 集群配置方法

Docker Desktop Kubernetes 可以使用 `kubeadm` 或 `kind` 配置器进行配置。

`kubeadm` 是较旧的配置器。它支持单节点集群，您无法选择 Kubernetes 版本，配置速度比 `kind` 慢，并且不受[增强容器隔离](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/index.md)（Enhanced Container Isolation，ECI）支持，这意味着如果启用了 ECI，集群可以工作但不受 ECI 保护。

`kind` 是较新的配置器，如果您已登录并使用 Docker Desktop 4.38 或更高版本，则可以使用它。它支持多节点集群（用于更真实的 Kubernetes 设置），您可以选择 Kubernetes 版本，配置速度比 `kubeadm` 快，并且受 ECI 支持（即，当启用 ECI 时，Kubernetes 集群在非特权 Docker 容器中运行，因此更加安全）。但请注意，`kind` 要求 Docker Desktop 配置为使用 [containerd 镜像存储](containerd.md)（Docker Desktop 4.34 及更高版本中的默认镜像存储）。

下表总结了此比较。

| 功能 | `kubeadm` | `kind` |
| :------ | :-----: | :--: |
| 可用性 | Docker Desktop 4.0+ | Docker Desktop 4.38+（需要登录） |
| 多节点集群支持 | 否 | 是 |
| Kubernetes 版本选择器 | 否 | 是 |
| 配置速度 | ~1 分钟 | ~30 秒 |
| ECI 支持 | 否 | 是 |
| 与 containerd 镜像存储配合使用 | 是 | 是 |
| 与 Docker 镜像存储配合使用 | 是 | 否 |

## 使用 kubectl 命令

Kubernetes 集成会自动在 Mac 上的 `/usr/local/bin/kubectl` 和 Windows 上的 `C:\Program Files\Docker\Docker\Resources\bin\kubectl.exe` 安装 Kubernetes CLI 命令。此位置可能不在您的 shell 的 `PATH` 变量中，因此您可能需要输入命令的完整路径或将其添加到 `PATH`。

如果您已经安装了 `kubectl` 并且它指向其他环境，例如 `minikube` 或 Google Kubernetes Engine 集群，请确保更改上下文，使 `kubectl` 指向 `docker-desktop`：

```console
$ kubectl config get-contexts
$ kubectl config use-context docker-desktop
```

> [!TIP]
>
> 如果 `kubectl` config get-contexts 命令返回空结果，请尝试：
>
> - 在命令提示符或 PowerShell 中运行该命令。
> - 将 `KUBECONFIG` 环境变量设置为指向您的 `.kube/config` 文件。

### 验证安装

要确认 Kubernetes 正在运行，请列出可用节点：

```console
$ kubectl get nodes
NAME                 STATUS    ROLES            AGE       VERSION
docker-desktop       Ready     control-plane    3h        v1.29.1
```

如果您使用 Homebrew 或其他方法安装了 `kubectl`，并遇到冲突，请删除 `/usr/local/bin/kubectl`。

有关 `kubectl` 的更多信息，请参阅 [`kubectl` 文档](https://kubernetes.io/docs/reference/kubectl/overview/)。

## 升级您的集群

Kubernetes 集群不会随 Docker Desktop 更新自动升级。要升级集群，您必须在设置中手动选择 **Reset Kubernetes Cluster**。

## 其他设置

### 查看系统容器

默认情况下，Kubernetes 系统容器是隐藏的。要检查这些容器，请启用 **Show system containers (advanced)**。

现在您可以使用 `docker ps` 或在 Docker Desktop Dashboard 中查看正在运行的 Kubernetes 容器。

### 为 Kubernetes 控制平面镜像配置自定义镜像仓库

Docker Desktop 使用容器运行 Kubernetes 控制平面。默认情况下，Docker Desktop 从 Docker Hub 拉取相关的容器镜像。拉取的镜像取决于[集群配置模式](#cluster-provisioning-method)。

例如，在 `kind` 模式下，它需要以下镜像：

```console
docker.io/kindest/node:<tag>
docker.io/envoyproxy/envoy:<tag>
docker.io/docker/desktop-cloud-provider-kind:<tag>
docker.io/docker/desktop-containerd-registry-mirror:<tag>
```

在 `kubeadm` 模式下，它需要以下镜像：

```console
docker.io/registry.k8s.io/kube-controller-manager:<tag>
docker.io/registry.k8s.io/kube-apiserver:<tag>
docker.io/registry.k8s.io/kube-scheduler:<tag>
docker.io/registry.k8s.io/kube-proxy
docker.io/registry.k8s.io/etcd:<tag>
docker.io/registry.k8s.io/pause:<tag>
docker.io/registry.k8s.io/coredns/coredns:<tag>
docker.io/docker/desktop-storage-provisioner:<tag>
docker.io/docker/desktop-vpnkit-controller:<tag>
docker.io/docker/desktop-kubernetes:<tag>
```

镜像标签由 Docker Desktop 根据多种因素自动选择，包括正在使用的 Kubernetes 版本。每个镜像的标签各不相同。

为了适应不允许访问 Docker Hub 的场景，管理员可以使用 [KubernetesImagesRepository](../../security/for-admins/hardened-desktop/settings-management/configure-json-file.md#kubernetes) 设置将 Docker Desktop 配置为从不同的仓库（例如镜像仓库）拉取上述列出的镜像。

镜像名称可以分解为 `[registry[:port]/][namespace/]repository[:tag]` 组件。`KubernetesImagesRepository` 设置允许用户覆盖镜像名称的 `[registry[:port]/][namespace]` 部分。

例如，如果 Docker Desktop Kubernetes 配置为 `kind` 模式，并且 `KubernetesImagesRepository` 设置为 `my-registry:5000/kind-images`，那么 Docker Desktop 将从以下位置拉取镜像：

```console
my-registry:5000/kind-images/node:<tag>
my-registry:5000/kind-images/envoy:<tag>
my-registry:5000/kind-images/desktop-cloud-provider-kind:<tag>
my-registry:5000/kind-images/desktop-containerd-registry-mirror:<tag>
```

这些镜像应该从 Docker Hub 中各自的镜像克隆/镜像。标签也必须与 Docker Desktop 期望的匹配。

建议的设置方法如下：

1) 启动 Docker Desktop。

2) 在 Settings > Kubernetes 中，启用 *Show system containers* 设置。

3) 在 Settings > Kubernetes 中，使用所需的集群配置方法启动 Kubernetes：`kubeadm` 或 `kind`。

4) 等待 Kubernetes 启动。

5) 使用 `docker ps` 查看 Docker Desktop 用于 Kubernetes 控制平面的容器镜像。

6) 将这些镜像（带有匹配的标签）克隆或镜像到您的自定义仓库。

7) 停止 Kubernetes 集群。

8) 配置 `KubernetesImagesRepository` 设置以指向您的自定义仓库。

9) 重启 Docker Desktop。

10) 使用 `docker ps` 命令验证 Kubernetes 集群正在使用自定义仓库镜像。

> [!NOTE]
>
> `KubernetesImagesRepository` 设置仅适用于 Docker Desktop 用于设置 Kubernetes 集群的控制平面镜像。它对其他 Kubernetes Pod 没有影响。

> [!NOTE]
>
> 当使用 `KubernetesImagesRepository` 并启用了[增强容器隔离（ECI）](../../security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md)时，请将以下镜像添加到 [ECI Docker socket 挂载镜像列表](../../security/for-admins/hardened-desktop/settings-management/configure-json-file.md#enhanced-container-isolation)：
>
> * [imagesRepository]/desktop-cloud-provider-kind:*
> * [imagesRepository]/desktop-containerd-registry-mirror:*
>
> 这些容器会挂载 Docker socket，因此您必须将镜像添加到 ECI 镜像列表。否则，ECI 将阻止挂载，Kubernetes 将无法启动。

## 故障排除

- 如果 Kubernetes 无法启动，请确保 Docker Desktop 运行时分配了足够的资源。检查 **Settings** > **Resources**。
- 如果 `kubectl` 命令返回错误，请确认上下文设置为 `docker-desktop`
   ```console
   $ kubectl config use-context docker-desktop
   ```
   如果您已启用该设置，可以尝试检查 [Kubernetes 系统容器](#viewing-system-containers)的日志。
- 如果更新后遇到集群问题，请重置您的 Kubernetes 集群。重置 Kubernetes 集群可以通过将集群基本恢复到干净状态来帮助解决问题，并清除可能导致问题的错误配置、损坏数据或卡住的资源。如果问题仍然存在，您可能需要清理和清除数据，然后重启 Docker Desktop。

## 关闭和卸载 Kubernetes

要在 Docker Desktop 中关闭 Kubernetes：

1. 从 Docker Desktop Dashboard，选择 **Settings** 图标。
2. 选择 **Kubernetes** 选项卡。
3. 取消选择 **Enable Kubernetes** 复选框。
4. 选择 **Apply** 保存设置。这将停止并删除 Kubernetes 容器，并删除 `/usr/local/bin/kubectl` 命令。
