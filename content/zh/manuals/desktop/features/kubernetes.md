--- 
description: 了解如何在 Docker Desktop 上部署 Kubernetes
keywords: 部署, kubernetes, kubectl, 编排, Docker Desktop
title: 在 Docker Desktop 上部署 Kubernetes
linkTitle: 部署到 Kubernetes
alias:
- /docker-for-windows/kubernetes/
- /docker-for-mac/kubernetes/
- /desktop/kubernetes/
weight: 60
---

Docker Desktop 包含一个独立的 Kubernetes 服务器和客户端，以及 Docker CLI 集成，让您可以直接在机器上进行本地 Kubernetes 开发和测试。

Kubernetes 服务器作为一个单节点或多节点集群运行在 Docker 容器内。这种轻量级设置有助于您在探索 Kubernetes 特性、测试工作负载以及进行容器编排的同时，并行使用其他 Docker 功能。

Docker Desktop 上的 Kubernetes 与其他工作负载（包括 Swarm 服务和独立容器）并行运行。

![k8s 设置](../images/k8s-settings.png)

## 当我在 Docker Desktop 中启用 Kubernetes 时会发生什么？

Docker Desktop 后端和虚拟机中会触发以下操作：

- 生成证书和集群配置
- 下载并安装 Kubernetes 内部组件
- 集群启动
- 安装用于网络和存储的额外控制器

在 Docker Desktop 中开启或关闭 Kubernetes 服务器不会影响您的其他工作负载。

## 安装并开启 Kubernetes

1. 打开 Docker Desktop 控制面板并导航到 **Settings**（设置）。
2. 选择 **Kubernetes** 选项卡。
3. 开启 **Enable Kubernetes**。
4. 选择您的 [集群配置方式](#集群配置方式)。
5. 选择 **Apply**（应用）以保存设置。

这将设置运行 Kubernetes 服务器容器所需的镜像，并在您的系统上安装 `kubectl` 命令行工具，位置为 `/usr/local/bin/kubectl` (Mac) 或 `C:\Program Files\Docker\Docker\resources\bin\kubectl.exe` (Windows)。

   > [!NOTE] 
   > 
   > 适用于 Linux 的 Docker Desktop 默认不包含 `kubectl`。您可以按照 [Kubernetes 安装指南](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) 单独安装它。请确保 `kubectl` 二进制文件安装在 `/usr/local/bin/kubectl`。

当 Kubernetes 启用时，其状态会显示在 Docker Desktop 控制面板页脚和 Docker 菜单中。

您可以通过以下命令检查当前的 Kubernetes 版本：

```console
$ kubectl version
```

### 集群配置方式

Docker Desktop Kubernetes 可以通过 `kubeadm` 或 `kind` 配置程序（provisioners）进行配置。

`kubeadm` 是较旧的配置程序。它支持单节点集群，您无法选择 Kubernetes 版本，其配置速度比 `kind` 慢，且不受 [增强型容器隔离 (ECI)](/manuals/security/for-admins/hardened-desktop/enhanced-container-isolation/index.md) 支持，这意味着如果启用了 ECI，集群可以工作但不受 ECI 保护。

`kind` 是较新的配置程序，如果您已登录并使用 Docker Desktop 4.38 或更高版本，则可以使用它。它支持多节点集群（用于更真实的 Kubernetes 设置），您可以选择 Kubernetes 版本，配置速度比 `kubeadm` 快，且受 ECI 支持（即启用 ECI 时，Kubernetes 集群在非特权 Docker 容器中运行，从而使其更安全）。但请注意，`kind` 要求 Docker Desktop 配置为使用 [containerd 镜像库](containerd.md)（Docker Desktop 4.34 及更高版本的默认镜像库）。

下表总结了这一对比：

| 功能 | `kubeadm` | `kind` |
| :------ | :-----: | :--: |
| 可用性 | Docker Desktop 4.0+ | Docker Desktop 4.38+ (需要登录) |
| 多节点集群支持 | 否 | 是 |
| Kubernetes 版本选择 | 否 | 是 |
| 配置速度 | 约 1 分钟 | 约 30 秒 |
| 受 ECI 支持 | 否 | 是 |
| 兼容 containerd 镜像库 | 是 | 是 |
| 兼容 Docker 镜像库 | 是 | 否 |

## 使用 kubectl 命令

Kubernetes 集成会自动在 Mac 的 `/usr/local/bin/kubectl` 和 Windows 的 `C:\Program Files\Docker\Docker\Resources\bin\kubectl.exe` 安装 Kubernetes CLI 命令。此位置可能不在您的 shell `PATH` 变量中，因此您可能需要输入命令的全路径或将其添加到 `PATH` 中。

如果您已经安装了 `kubectl` 且它指向其他环境（如 `minikube` 或 Google Kubernetes Engine 集群），请确保更改上下文，使 `kubectl` 指向 `docker-desktop`：

```console
$ kubectl config get-contexts
$ kubectl config use-context docker-desktop
```

> [!TIP] 
> 
> 如果 `kubectl` config get-contexts 命令返回空结果，请尝试：
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

## 升级您的集群

Kubernetes 集群不会随 Docker Desktop 的更新而自动升级。要升级集群，您必须在设置中手动选择 **Reset Kubernetes Cluster**（重置 Kubernetes 集群）。

## 额外设置

### 查看系统容器

默认情况下，Kubernetes 系统容器是隐藏的。要检查这些容器，请启用 **Show system containers (advanced)**（显示系统容器（高级））。

您现在可以使用 `docker ps` 或在 Docker Desktop 控制面板中查看运行中的 Kubernetes 容器。

### 为 Kubernetes 控制平面镜像配置自定义镜像库

Docker Desktop 使用容器运行 Kubernetes 控制平面。默认情况下，Docker Desktop 从 Docker Hub 拉取相关的容器镜像。拉取的镜像取决于 [集群配置方式](#集群配置方式)。

例如，在 `kind` 模式下需要以下镜像：

```console
docker.io/kindest/node:<tag>
docker.io/envoyproxy/envoy:<tag>
docker.io/docker/desktop-cloud-provider-kind:<tag>
docker.io/docker/desktop-containerd-registry-mirror:<tag>
```

在 `kubeadm` 模式下需要以下镜像：

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

镜像标签由 Docker Desktop 根据多种因素（包括正在使用的 Kubernetes 版本）自动选择。每个镜像的标签各不相同。

为了适应不允许访问 Docker Hub 的场景，管理员可以按照以下方式使用 [KubernetesImagesRepository](../../security/for-admins/hardened-desktop/settings-management/configure-json-file.md#kubernetes) 设置，配置 Docker Desktop 从不同的镜像库（例如镜像站）拉取上述列出的镜像。

镜像名称可以分解为 `[registry[:port]/][namespace/]repository[:tag]` 组件。`KubernetesImagesRepository` 设置允许用户覆盖镜像名称中的 `[registry[:port]/][namespace]` 部分。

例如，如果 Docker Desktop Kubernetes 配置为 `kind` 模式，且 `KubernetesImagesRepository` 设置为 `my-registry:5000/kind-images` ，那么 Docker Desktop 将从以下位置拉取镜像：

```console
my-registry:5000/kind-images/node:<tag>
my-registry:5000/kind-images/envoy:<tag>
my-registry:5000/kind-images/desktop-cloud-provider-kind:<tag>
my-registry:5000/kind-images/desktop-containerd-registry-mirror:<tag>
```

这些镜像应该从 Docker Hub 中的相应镜像克隆/镜像得到。标签也必须与 Docker Desktop 的预期相匹配。

推荐的设置方法如下：

1) 启动 Docker Desktop。

2) 在 Settings > Kubernetes 中，启用 *Show system containers* 设置。

3) 在 Settings > Kubernetes 中，使用所需的集群配置方式（`kubeadm` 或 `kind`）启动 Kubernetes。

4) 等待 Kubernetes 启动。

5) 使用 `docker ps` 查看 Docker Desktop 用于 Kubernetes 控制平面的容器镜像。

6) 将这些镜像（带有匹配的标签）克隆或镜像到您的自定义镜像库。

7) 停止 Kubernetes 集群。

8) 配置 `KubernetesImagesRepository` 设置指向您的自定义镜像库。

9) 重启 Docker Desktop。

10) 使用 `docker ps` 命令验证 Kubernetes 集群是否正在使用自定义镜像库中的镜像。

> [!NOTE] 
> 
> `KubernetesImagesRepository` 设置仅适用于 Docker Desktop 用于建立 Kubernetes 集群的控制平面镜像。它对其他 Kubernetes Pod 没有影响。

> [!NOTE] 
> 
> 当使用 `KubernetesImagesRepository` 且启用了 [增强型容器隔离 (ECI)](../../security/for-admins/hardened-desktop/enhanced-container-isolation/_index.md) 时，请将以下镜像添加到 [ECI Docker 套接字挂载镜像列表](../../security/for-admins/hardened-desktop/settings-management/configure-json-file.md#enhanced-container-isolation)中：
> 
> * [imagesRepository]/desktop-cloud-provider-kind:*
> * [imagesRepository]/desktop-containerd-registry-mirror:*
> 
> 这些容器挂载了 Docker 套接字，因此您必须将这些镜像添加到 ECI 镜像列表中。否则，ECI 将阻止挂载，Kubernetes 将无法启动。

## 故障排除

- 如果 Kubernetes 启动失败，请确保 Docker Desktop 运行且分配了足够的资源。检查 **Settings** > **Resources**。
- 如果 `kubectl` 命令返回错误，请确认上下文已设置为 `docker-desktop`
   ```console
   $ kubectl config use-context docker-desktop
   ```
   如果您启用了该设置，可以尝试检查 [Kubernetes 系统容器](#查看系统容器) 的日志。
- 如果您在更新后遇到集群问题，请重置您的 Kubernetes 集群。重置 Kubernetes 集群通过实质上将集群恢复到干净状态并清除可能导致问题的错误配置、损坏数据或卡住的资源，从而帮助解决问题。如果问题仍然存在，您可能需要清除并彻底删除数据，然后重启 Docker Desktop。

## 关闭并卸载 Kubernetes

在 Docker Desktop 中关闭 Kubernetes 的步骤：

1. 从 Docker Desktop 控制面板中，选择 **Settings**（设置）图标。
2. 选择 **Kubernetes** 选项卡。
3. 取消勾选 **Enable Kubernetes** 复选框。
4. 选择 **Apply**（应用）以保存设置。这将停止并移除 Kubernetes 容器，同时也会移除 `/usr/local/bin/kubectl` 命令。
