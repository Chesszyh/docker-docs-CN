---
title: Kubernetes 驱动 (Kubernetes driver)
description: |
  Kubernetes 驱动允许您在 Kubernetes 集群中运行 BuildKit。
  您可以使用 Buildx 连接集群并在其中运行构建任务。
keywords: build, buildx, driver, builder, kubernetes, 驱动, 构建器
aliases:
  - /build/buildx/drivers/kubernetes/
  - /build/building/drivers/kubernetes/
  - /build/drivers/kubernetes/
---

Kubernetes 驱动允许您将本地开发环境或 CI 环境连接到 Kubernetes 集群中的构建器，从而能够访问更强大的计算资源，并可选地支持多种原生架构。

## 语法

运行以下命令来创建一个名为 `kube` 且使用 Kubernetes 驱动的新构建器：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=[键=值,...]
```

下表描述了可以传递给 `--driver-opt` 的可用驱动特定选项：

| 参数 | 类型 | 默认值 | 说明 |
| ---------------------------- | ------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `image` | 字符串 | | 设置用于运行 BuildKit 的镜像。 |
| `namespace` | 字符串 | 当前 Kubernetes 上下文中的命名空间 | 设置 Kubernetes 命名空间。 |
| `default-load` | 布尔值 | `false` | 自动将镜像加载到 Docker Engine 镜像库中。 |
| `replicas` | 整数 | 1 | 设置要创建的 Pod 副本数。参见 [扩展 BuildKit][1]。 |
| `requests.cpu` | CPU 单位 | | 设置 CPU 请求值，单位为 Kubernetes CPU 单位。例如 `requests.cpu=100m` 或 `requests.cpu=2`。 |
| `requests.memory` | 内存大小 | | 设置内存请求值，以字节为单位或带有有效后缀。例如 `requests.memory=500Mi` 或 `requests.memory=4G`。 |
| `requests.ephemeral-storage` | 存储大小 | | 设置临时存储 (ephemeral-storage) 请求值，以字节为单位或带有有效后缀。例如 `requests.ephemeral-storage=2Gi`。 |
| `limits.cpu` | CPU 单位 | | 设置 CPU 限制值，单位为 Kubernetes CPU 单位。例如 `requests.cpu=100m` 或 `requests.cpu=2`。 |
| `limits.memory` | 内存大小 | | 设置内存限制值，以字节为单位或带有有效后缀。例如 `requests.memory=500Mi` 或 `requests.memory=4G`。 |
| `limits.ephemeral-storage` | 存储大小 | | 设置临时存储限制值，以字节为单位或带有有效后缀。例如 `requests.ephemeral-storage=100M`。 |
| `nodeselector` | CSV 字符串 | | 设置 pod 的 `nodeSelector` 标签。参见 [节点分配][2]。 |
| `annotations` | CSV 字符串 | | 在 deployment 和 pod 上设置额外的注解 (annotations)。 |
| `labels` | CSV 字符串 | | 在 deployment 和 pod 上设置额外的标签 (labels)。 |
| `tolerations` | CSV 字符串 | | 配置 pod 的污点容忍度 (taint toleration)。参见 [节点分配][2]。 |
| `serviceaccount` | 字符串 | | 设置 pod 的 `serviceAccountName`。 |
| `schedulername` | 字符串 | | 设置负责调度该 pod 的调度器名称。 |
| `timeout` | 时间 | `120s` | 设置超时限制，决定 Buildx 在构建前等待 pod 预配完成的时长。 |
| `rootless` | 布尔值 | `false` | 以非 root 用户运行容器。参见 [rootless 模式][3]。 |
| `loadbalance` | 字符串 | `sticky` | 负载均衡策略（`sticky` 或 `random`）。如果设为 `sticky`，则使用上下文路径的哈希值选择 pod。 |
| `qemu.install` | 布尔值 | `false` | 安装 QEMU 模拟以支持多平台。参见 [QEMU][4]。 |
| `qemu.image` | 字符串 | `tonistiigi/binfmt:latest` | 设置 QEMU 模拟镜像。参见 [QEMU][4]。 |

[1]: #扩展-buildkit
[2]: #节点分配
[3]: #rootless-模式
[4]: #qemu

## 扩展 BuildKit

Kubernetes 驱动的主要优势之一是您可以根据构建负载增减构建器副本的数量。可以通过以下驱动选项配置扩展：

- `replicas=N`

  这将 BuildKit pod 的数量扩展到所需的大小。默认情况下，它仅创建一个 pod。增加副本数量可以让您利用集群中的多个节点。

- `requests.cpu`, `requests.memory`, `requests.ephemeral-storage`, `limits.cpu`, `limits.memory`, `limits.ephemeral-storage`

  这些选项允许根据官方 Kubernetes 文档 [此处](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) 请求并限制每个 BuildKit pod 可用的资源。

例如，创建 4 个 BuildKit pod 副本：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,replicas=4
```

列出 pod 时，您会看到：

```console
$ kubectl -n buildkit get deployments
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
kube0   4/4     4            4           8s

$ kubectl -n buildkit get pods
NAME                     READY   STATUS    RESTARTS   AGE
kube0-6977cdcb75-48ld2   1/1     Running   0          8s
kube0-6977cdcb75-rkc6b   1/1     Running   0          8s
kube0-6977cdcb75-vb4ks   1/1     Running   0          8s
kube0-6977cdcb75-z4fzs   1/1     Running   0          8s
```

此外，您还可以使用 `loadbalance=(sticky|random)` 选项来控制存在多个副本时的负载均衡行为。`random` 会从节点池中随机选择节点，使工作负载在各副本间均匀分布。`sticky`（默认值）会尝试将多次执行的同一构建连接到同一个节点上，以确保更好地利用本地缓存。

有关扩展性的更多信息，请参阅 [`docker buildx create`](/reference/cli/docker/buildx/create.md#driver-opt) 的选项。

## 节点分配

Kubernetes 驱动允许您使用 `nodeSelector` 和 `tolerations` 驱动选项来控制 BuildKit pod 的调度。如果您想使用完全自定义的调度器，还可以设置 `schedulername` 选项。

您可以使用 `annotations` 和 `labels` 驱动选项，为托管构建器的 deployment 和 pod 添加额外的元数据。

`nodeSelector` 参数的值是一个由逗号分隔的键值对字符串，其中键是节点标签，值是标签文本。例如：`"nodeselector=kubernetes.io/arch=arm64"`。

`tolerations` 参数是一个由分号分隔的污点列表。它接受与 Kubernetes 清单相同的值。每个 `tolerations` 条目指定一个污点键及其值、运算符或影响（effect）。例如：`"tolerations=key=foo,value=bar;key=foo2,operator=exists;key=foo3,effect=NoSchedule"`。

这些选项接受 CSV 格式的字符串作为值。由于 shell 命令的引用规则，您必须将值包裹在单引号中。您甚至可以将整个 `--driver-opt` 参数包裹在单引号中，例如：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  '--driver-opt="nodeselector=label1=value1,label2=value2","tolerations=key=key1,value=value1"'
```

## 多平台构建

Kubernetes 驱动支持创建 [多平台镜像](/manuals/build/building/multi-platform.md)，既可以使用 QEMU，也可以利用节点的原生架构。

### QEMU

与 `docker-container` 驱动类似，Kubernetes 驱动也支持使用 [QEMU](https://www.qemu.org/)（用户模式）为非原生平台构建镜像。在 build 命令中包含 `--platform` 标志并指定您想要输出的平台。

例如，构建一个支持 `amd64` 和 `arm64` 的 Linux 镜像：

```console
$ docker buildx build \
  --builder=kube \
  --platform=linux/amd64,linux/arm64 \
  -t <用户名>/<镜像名> \
  --push .
```

> [!WARNING]
> 
> QEMU 执行对非原生平台的完整 CPU 模拟，这比原生构建要慢得多。编译和压缩/解压等计算密集型任务可能会受到较大的性能影响。

使用自定义 BuildKit 镜像或在构建中调用非原生二进制文件时，可能需要在创建构建器时通过 `qemu.install` 选项显式开启 QEMU：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,qemu.install=true
```

### 原生构建 (Native)

如果您可以访问不同架构的集群节点，Kubernetes 驱动可以利用这些节点进行原生构建。为此，请使用 `docker buildx create` 的 `--append` 标志。

首先，创建一个明确支持单一架构（例如 `amd64`）的构建器：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/amd64 \
  --node=builder-amd64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=amd64"
```

这创建了一个名为 `kube` 的 Buildx 构建器，包含一个名为 `builder-amd64` 的构建器节点。使用 `--node` 分配节点名称是可选的；如果您未提供，Buildx 会生成一个随机名称。

请注意，Buildx 中的“节点 (node)”概念与 Kubernetes 中的“节点”概念不同。在此案例中，一个 Buildx 节点可以将多个具有相同架构的 Kubernetes 节点连接在一起。

创建好 `kube` 构建器后，您现在可以使用 `--append` 引入另一种架构。例如，添加 `arm64`：

```console
$ docker buildx create \
  --append \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/arm64 \
  --node=builder-arm64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=arm64"
```

列出您的构建器，会看到 `kube` 构建器的两个节点：

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT                                         STATUS   PLATFORMS
kube            kubernetes
  builder-amd64 kubernetes:///kube?deployment=builder-amd64&kubeconfig= running  linux/amd64*, linux/amd64/v2, linux/amd64/v3, linux/386
  builder-arm64 kubernetes:///kube?deployment=builder-arm64&kubeconfig= running  linux/arm64*
```

您现在可以同时构建支持 `amd64` 和 `arm64` 的多架构镜像，只需在 build 命令中同时指定这些平台：

```console
$ docker buildx build --builder=kube --platform=linux/amd64,linux/arm64 -t <用户名>/<镜像名> --push .
```

您可以根据需要重复执行 `buildx create --append` 命令，以支持尽可能多的架构。

## Rootless 模式

Kubernetes 驱动支持 rootless 模式。有关 rootless 模式的工作原理及其要求的更多信息，请参阅 [此处](https://github.com/moby/buildkit/blob/master/docs/rootless.md)。

要在您的集群中开启该模式，可以使用 `rootless=true` 驱动选项：

```console
$ docker buildx create \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,rootless=true
```

这将创建不带 `securityContext.privileged` 权限的 pod。

要求使用 Kubernetes 1.19 或更高版本。建议使用 Ubuntu 作为宿主机内核。

## 示例：在 Kubernetes 中创建一个 Buildx 构建器

本指南向您展示如何：

- 为您的 Buildx 资源创建一个命名空间
- 创建一个 Kubernetes 构建器
- 列出可用构建器
- 使用您的 Kubernetes 构建器构建镜像

前提条件：

- 您已有一个现有的 Kubernetes 集群。如果您还没有，可以按照说明安装 [minikube](https://minikube.sigs.k8s.io/docs/)。
- 想要连接的集群可以通过 `kubectl` 命令访问，且必要时已 [正确设置](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/#set-the-kubeconfig-environment-variable) 了 `KUBECONFIG` 环境变量。

1. 创建一个 `buildkit` 命名空间。

   创建一个独立的命名空间有助于将您的 Buildx 资源与集群中的其他资源隔离开来。

   ```console
   $ kubectl create namespace buildkit
   namespace/buildkit created
   ```

2. 使用 Kubernetes 驱动创建一个新构建器：

   ```console
   $ docker buildx create \
     --bootstrap \
     --name=kube \
     --driver=kubernetes \
     --driver-opt=namespace=buildkit
   ```

   > [!NOTE]
   > 
   > 请记得在驱动选项中指定命名空间。

3. 使用 `docker buildx ls` 列出可用构建器。

   ```console
   $ docker buildx ls
   NAME/NODE                DRIVER/ENDPOINT STATUS  PLATFORMS
   kube                     kubernetes
     kube0-6977cdcb75-k9h9m                 running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
   default *                docker
     default                default         running linux/amd64, linux/386
   ```

4. 使用 `kubectl` 检查由该驱动创建的运行中的 pod。

   ```console
   $ kubectl -n buildkit get deployments
   NAME    READY   UP-TO-DATE   AVAILABLE   AGE
   kube0   1/1     1            1           32s

   $ kubectl -n buildkit get pods
   NAME                     READY   STATUS    RESTARTS   AGE
   kube0-6977cdcb75-k9h9m   1/1     Running   0          32s
   ```

   构建驱动会在您集群的指定命名空间（本例中为 `buildkit`）中创建必要的资源，同时将驱动配置保存在本地。

5. 运行 buildx 命令时包含 `--builder` 标志来使用您的新构建器。例如：

   ```console
   # 将 <注册表> 替换为您的 Docker 用户名
   # 将 <镜像名> 替换为您想要构建的镜像名称
   docker buildx build \
     --builder=kube \
     -t <注册表>/<镜像名> \
     --push .
   ```

大功告成：您现在已经使用 Buildx 通过 Kubernetes pod 构建了一个镜像。

## 深入阅读

欲了解更多关于 Kubernetes 驱动的信息，请参阅 [Buildx 参考](/reference/cli/docker/buildx/create.md#driver)。