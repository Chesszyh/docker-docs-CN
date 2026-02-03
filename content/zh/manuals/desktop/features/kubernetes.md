---
description: 了解如何在 Docker Desktop 上部署到 Kubernetes
keywords: 部署, deploy, kubernetes, kubectl, 编排, orchestration, Docker Desktop
title: 在 Docker Desktop 上使用 Kubernetes
linkTitle: 在 Kubernetes 上部署
alias:
- /docker-for-windows/kubernetes/
- /docker-for-mac/kubernetes/
- /desktop/kubernetes/
weight: 60
---

Docker Desktop 包含一个独立的 Kubernetes 服务器和客户端，以及 Docker CLI 集成，从而实现在您的机器上直接进行本地 Kubernetes 开发和测试。

Kubernetes 服务器作为一个单节点或多节点集群运行在 Docker 容器中。这种轻量级的设置可帮助您探索 Kubernetes 功能、测试工作负载，并在使用其他 Docker 功能的同时进行容器编排工作。

Docker Desktop 上的 Kubernetes 与其他工作负载（包括 Swarm 服务和独立容器）并行运行。

![k8s 设置](../images/k8s-settings.png)

## 当我在 Docker Desktop 中启用 Kubernetes 时会发生什么？

以下操作将在 Docker Desktop 后端和虚拟机中触发：

- 生成证书和集群配置
- 下载并安装 Kubernetes 内部组件
- 启动集群
- 为网络和存储安装额外的控制器

在 Docker Desktop 中开启或关闭 Kubernetes 服务器不会影响您的其他工作负载。

## 安装并开启 Kubernetes

1. 打开 Docker Desktop 控制面板并导航到 **Settings（设置）**。
2. 选择 **Kubernetes** 选项卡。
3. 开启 **Enable Kubernetes（启用 Kubernetes）**。
4. 选择您的[集群预配方法](#集群预配方法)。
5. 选择 **Apply（应用）** 保存设置。

这将设置作为容器运行 Kubernetes 服务器所需的镜像，并在您的系统中安装 `kubectl` 命令行工具，路径为 `/usr/local/bin/kubectl` (Mac) 或 `C:\Program Files\Docker\Docker\resources\bin\kubectl.exe` (Windows)。

   > [!NOTE]
   > 
   > Linux 版 Docker Desktop 默认不包含 `kubectl`。您可以按照 [Kubernetes 安装指南](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) 单独安装它。请确保 `kubectl` 二进制文件安装在 `/usr/local/bin/kubectl`。

启用 Kubernetes 后，其状态会显示在 Docker Desktop 控制面板的页脚和 Docker 菜单中。

您可以通过以下命令检查 Kubernetes 的版本：

```console
$ kubectl version
```

### 集群预配方法

Docker Desktop Kubernetes 可以使用 `kubeadm` 或 `kind` 预配程序进行预配。

`kubeadm` 是较旧的预配程序。它支持单节点集群，您无法选择 Kubernetes 版本，预配速度比 `kind` 慢，且不受 [增强型容器隔离](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/index.md) (ECI) 的支持。这意味着如果启用了 ECI，集群虽然可以工作，但不受 ECI 保护。

`kind` 是较新的预配程序，如果您已登录并使用 Docker Desktop 4.38 或更高版本，则可以使用它。它支持多节点集群（以实现更真实的 Kubernetes 设置），您可以选择 Kubernetes 版本，预配速度比 `kubeadm` 快，并且受 ECI 支持（即在启用 ECI 时，Kubernetes 集群在无特权的 Docker 容器中运行，从而使其更安全）。但请注意，`kind` 要求将 Docker Desktop 配置为使用 [containerd 镜像存储](containerd.md)（Docker Desktop 4.34 及更高版本的默认镜像存储）。

下表总结了这一对比：

| 特性 | `kubeadm` | `kind` |
| :------ | :-----: | :--: |
| 可用性 | Docker Desktop 4.0+ | Docker Desktop 4.38+ (需登录) |
| 多节点集群支持 | 否 | 是 |
| Kubernetes 版本选择器 | 否 | 是 |
| 预配速度 | 约 1 分钟 | 约 30 秒 |
| 受 ECI 支持 | 否 | 是 |
| 兼容 containerd 镜像存储 | 是 | 是 |
| 兼容 Docker 镜像存储 | 是 | 否 |

## 使用 kubectl 命令

Kubernetes 集成会自动在 Mac 的 `/usr/local/bin/kubectl` 和 Windows 的 `C:\Program Files\Docker\Docker\Resources\bin\kubectl.exe` 安装 Kubernetes CLI 命令。由于此路径可能不在您 shell 的 `PATH` 变量中，您可能需要输入命令的全路径或将其添加到 `PATH` 中。

如果您已经安装了 `kubectl` 并且它指向了其他环境（如 `minikube` 或 Google Kubernetes Engine 集群），请确保切换上下文，使 `kubectl` 指向 `docker-desktop`：

```console
$ kubectl config get-contexts
$ kubectl config use-context docker-desktop
```

> [!TIP]
> 
> 如果 `kubectl config get-contexts` 命令返回空结果，请尝试：
> 
> - 在命令提示符或 PowerShell 中运行该命令。
> - 设置 `KUBECONFIG` 环境变量指向您的 `.kube/config` 文件。

### 验证安装

要确认 Kubernetes 正在运行，请列出可用节点：

```console
$ kubectl get nodes
NAME                 STATUS    ROLES            AGE       VERSION
docker-desktop       Ready     control-plane    3h        v1.29.1
```

如果您使用 Homebrew 或其他方法安装了 `kubectl` 并遇到了冲突，请移除 `/usr/local/bin/kubectl`。

有关 `kubectl` 的更多信息，请参阅 [`kubectl` 文档](https://kubernetes.io/docs/reference/kubectl/overview/)。

## 升级集群

Kubernetes 集群不会随 Docker Desktop 的更新而自动升级。要升级集群，您必须在设置中手动选择 **Reset Kubernetes Cluster（重置 Kubernetes 集群）**。

## 额外设置

### 查看系统容器

默认情况下，Kubernetes 系统容器是隐藏的。要检查这些容器，请启用 **Show system containers (advanced)（显示系统容器（高级））**。

现在，您可以使用 `docker ps` 或在 Docker Desktop 控制面板中查看正在运行的 Kubernetes 容器。

### 为 Kubernetes 控制平面镜像配置自定义镜像注册表

Docker Desktop 使用容器来运行 Kubernetes 控制平面。默认情况下，Docker Desktop 从 Docker Hub 拉取相关的容器镜像。拉取的镜像取决于[集群预配模式](#集群预配方法)。

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

镜像标签（tag）由 Docker Desktop 根据包括所使用的 Kubernetes 版本在内的多个因素自动选择。每个镜像的标签各不相同。

为了适应不允许访问 Docker Hub 的场景，管理员可以使用如下的 [KubernetesImagesRepository](../../security/for-admins/hardened-desktop/settings-management/configure-json-file.md#kubernetes) 设置，配置 Docker Desktop 从不同的注册表（例如镜像镜像站）拉取上述列出的镜像。

一个镜像名称可以分解为 `[registry[:port]/][namespace/]repository[:tag]` 组件。`KubernetesImagesRepository` 设置允许用户覆盖镜像名称中的 `[registry[:port]/][namespace]` 部分。

例如，如果 Docker Desktop Kubernetes 配置为 `kind` 模式，且 `KubernetesImagesRepository` 设置为 `my-registry:5000/kind-images`，那么 Docker Desktop 将从以下位置拉取镜像：

```console
my-registry:5000/kind-images/node:<tag>
my-registry:5000/kind-images/envoy:<tag>
my-registry:5000/kind-images/desktop-cloud-provider-kind:<tag>
my-registry:5000/kind-images/desktop-containerd-registry-mirror:<tag>
```

这些镜像应从其在 Docker Hub 中对应的镜像克隆/镜像而来。标签也必须与 Docker Desktop 预期的匹配。

设置此项的推荐方法如下：

1) 启动 Docker Desktop。

2) 在 Settings（设置） > Kubernetes 中，启用 *Show system containers* 设置。

3) 在 Settings（设置） > Kubernetes 中，使用所需的集群预配方法启动 Kubernetes：`kubeadm` 或 `kind`。

4) 等待 Kubernetes 启动。

5) 使用 `docker ps` 查看 Docker Desktop 用于 Kubernetes 控制平面的容器镜像。

6) 将这些镜像（带匹配标签）克隆或镜像到您的自定义注册表。

7) 停止 Kubernetes 集群。

8) 将 `KubernetesImagesRepository` 设置配置为指向您的自定义注册表。

9) 重新启动 Docker Desktop。

10) 使用 `docker ps` 命令验证 Kubernetes 集群是否正在使用自定义注册表的镜像。

> [!NOTE]
> 
> `KubernetesImagesRepository` 设置仅适用于 Docker Desktop 用于设置 Kubernetes 集群的控制平面镜像。它对其他 Kubernetes pod 没有影响。

> [!NOTE]
> 
> 在使用 `KubernetesImagesRepository` 且启用了 [增强型容器隔离 (ECI)](../../security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md) 时，请将以下镜像添加到 [ECI Docker 套接字挂载镜像列表](../../security/for-admins/hardened-desktop/settings-management/configure-json-file.md#enhanced-container-isolation)：
> 
> * [imagesRepository]/desktop-cloud-provider-kind:*
> * [imagesRepository]/desktop-containerd-registry-mirror:*
> 
> 这些容器需要挂载 Docker 套接字，因此您必须将这些镜像添加到 ECI 镜像列表中。否则，ECI 将阻止挂载，Kubernetes 将无法启动。

## 故障排查

- 如果 Kubernetes 无法启动，请确保 Docker Desktop 运行在足够的分配资源下。检查 **Settings** > **Resources**。
- 如果 `kubectl` 命令返回错误，请确认上下文已设置为 `docker-desktop`：
   ```console
   $ kubectl config use-context docker-desktop
   ```
   如果您启用了该设置，可以尝试检查 [Kubernetes 系统容器](#查看系统容器) 的日志。
- 如果在更新后遇到集群问题，请重置您的 Kubernetes 集群。重置 Kubernetes 集群通过将集群恢复到干净状态并清除可能导致问题的错误配置、损坏数据或卡住的资源来帮助解决问题。如果问题仍然存在，您可能需要清理并擦除数据，然后重新启动 Docker Desktop。

## 关闭并卸载 Kubernetes

要在 Docker Desktop 中关闭 Kubernetes：

1. 从 Docker Desktop 控制面板中，选择 **Settings（设置）** 图标。
2. 选择 **Kubernetes** 选项卡。
3. 取消勾选 **Enable Kubernetes（启用 Kubernetes）** 复选框。
4. 选择 **Apply（应用）** 保存设置。这将停止并移除 Kubernetes 容器，并移除 `/usr/local/bin/kubectl` 命令。