---
title: Kubernetes 驱动
description: |
  Kubernetes 驱动允许您在 Kubernetes 集群中运行 BuildKit。
  您可以使用 Buildx 连接到集群并在其中运行构建。
keywords: build, buildx, driver, builder, kubernetes
aliases:
  - /build/buildx/drivers/kubernetes/
  - /build/building/drivers/kubernetes/
  - /build/drivers/kubernetes/
---

Kubernetes 驱动允许您将本地开发或 CI 环境连接到 Kubernetes 集群中的构建器，以访问更强大的计算资源，并可选择支持多种原生架构。

## 概要

运行以下命令来创建一个名为 `kube` 的新构建器，该构建器使用 Kubernetes 驱动：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=[key=value,...]
```

下表描述了可以传递给 `--driver-opt` 的特定于驱动的可用选项：

| 参数                         | 类型         | 默认值                                  | 描述                                                                                                                                 |
| ---------------------------- | ------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `image`                      | String       |                                         | 设置用于运行 BuildKit 的镜像。                                                                                                       |
| `namespace`                  | String       | 当前 Kubernetes context 中的命名空间    | 设置 Kubernetes 命名空间。                                                                                                           |
| `default-load`               | Boolean      | `false`                                 | 自动将镜像加载到 Docker Engine 镜像存储。                                                                                            |
| `replicas`                   | Integer      | 1                                       | 设置要创建的 Pod 副本数。参见[扩展 BuildKit][1]                                                                                      |
| `requests.cpu`               | CPU 单位     |                                         | 设置请求的 CPU 值，以 Kubernetes CPU 单位指定。例如 `requests.cpu=100m` 或 `requests.cpu=2`                                          |
| `requests.memory`            | 内存大小     |                                         | 设置请求的内存值，以字节或有效后缀指定。例如 `requests.memory=500Mi` 或 `requests.memory=4G`                                         |
| `requests.ephemeral-storage` | 存储大小     |                                         | 设置请求的临时存储值，以字节或有效后缀指定。例如 `requests.ephemeral-storage=2Gi`                                                    |
| `limits.cpu`                 | CPU 单位     |                                         | 设置限制的 CPU 值，以 Kubernetes CPU 单位指定。例如 `requests.cpu=100m` 或 `requests.cpu=2`                                          |
| `limits.memory`              | 内存大小     |                                         | 设置限制的内存值，以字节或有效后缀指定。例如 `requests.memory=500Mi` 或 `requests.memory=4G`                                         |
| `limits.ephemeral-storage`   | 存储大小     |                                         | 设置限制的临时存储值，以字节或有效后缀指定。例如 `requests.ephemeral-storage=100M`                                                   |
| `nodeselector`               | CSV 字符串   |                                         | 设置 pod 的 `nodeSelector` 标签。参见[节点分配][2]。                                                                                 |
| `annotations`                | CSV 字符串   |                                         | 在 deployment 和 pod 上设置额外的注解。                                                                                              |
| `labels`                     | CSV 字符串   |                                         | 在 deployment 和 pod 上设置额外的标签。                                                                                              |
| `tolerations`                | CSV 字符串   |                                         | 配置 pod 的污点容忍。参见[节点分配][2]。                                                                                             |
| `serviceaccount`             | String       |                                         | 设置 pod 的 `serviceAccountName`。                                                                                                   |
| `schedulername`              | String       |                                         | 设置负责调度 pod 的调度器。                                                                                                          |
| `timeout`                    | Time         | `120s`                                  | 设置超时限制，决定 Buildx 在构建前等待 pod 配置完成的时间。                                                                          |
| `rootless`                   | Boolean      | `false`                                 | 以非 root 用户身份运行容器。参见[无根模式][3]。                                                                                      |
| `loadbalance`                | String       | `sticky`                                | 负载均衡策略（`sticky` 或 `random`）。如果设置为 `sticky`，则使用 context 路径的哈希值选择 pod。                                     |
| `qemu.install`               | Boolean      | `false`                                 | 安装 QEMU 模拟以支持多平台。参见 [QEMU][4]。                                                                                         |
| `qemu.image`                 | String       | `tonistiigi/binfmt:latest`              | 设置 QEMU 模拟镜像。参见 [QEMU][4]。                                                                                                 |

[1]: #扩展-buildkit
[2]: #节点分配
[3]: #无根模式
[4]: #qemu

## 扩展 BuildKit

Kubernetes 驱动的主要优势之一是您可以扩展构建器副本的数量，以应对增加的构建负载。可以使用以下驱动选项配置扩展：

- `replicas=N`

  这会将 BuildKit pod 的数量扩展到所需的规模。默认情况下，它只创建一个 pod。增加副本数量可以让您利用集群中的多个节点。

- `requests.cpu`、`requests.memory`、`requests.ephemeral-storage`、`limits.cpu`、`limits.memory`、`limits.ephemeral-storage`

  这些选项允许根据官方 Kubernetes 文档[此处](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)的说明，请求和限制每个 BuildKit pod 可用的资源。

例如，创建 4 个副本的 BuildKit pod：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,replicas=4
```

列出 pod，您会得到：

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

此外，当有多个副本时，您可以使用 `loadbalance=(sticky|random)` 选项来控制负载均衡行为。`random` 从节点池中随机选择节点，在副本之间提供均匀的工作负载分布。`sticky`（默认）会尝试每次将多次执行的相同构建连接到相同的节点，确保更好地利用本地缓存。

有关可扩展性的更多信息，请参阅 [`docker buildx create`](/reference/cli/docker/buildx/create.md#driver-opt) 的选项。

## 节点分配

Kubernetes 驱动允许您使用 `nodeSelector` 和 `tolerations` 驱动选项来控制 BuildKit pod 的调度。如果您想完全使用自定义调度器，还可以设置 `schedulername` 选项。

您可以使用 `annotations` 和 `labels` 驱动选项向托管构建器的 deployment 和 pod 应用额外的元数据。

`nodeSelector` 参数的值是一个逗号分隔的键值对字符串，其中键是节点标签，值是标签文本。例如：`"nodeselector=kubernetes.io/arch=arm64"`

`tolerations` 参数是一个分号分隔的污点列表。它接受与 Kubernetes manifest 相同的值。每个 `tolerations` 条目指定一个污点键及其值、操作符或效果。例如：`"tolerations=key=foo,value=bar;key=foo2,operator=exists;key=foo3,effect=NoSchedule"`

这些选项接受 CSV 分隔的字符串作为值。由于 shell 命令的引号规则，您必须用单引号包裹这些值。您甚至可以用单引号包裹整个 `--driver-opt`，例如：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  '--driver-opt="nodeselector=label1=value1,label2=value2","tolerations=key=key1,value=value1"'
```

## 多平台构建

Kubernetes 驱动支持创建[多平台镜像](/manuals/build/building/multi-platform.md)，可以通过 QEMU 或利用节点的原生架构来实现。

### QEMU

与 `docker-container` 驱动一样，Kubernetes 驱动也支持使用 [QEMU](https://www.qemu.org/)（用户模式）来构建非原生平台的镜像。包含 `--platform` 标志并指定您要输出的目标平台。

例如，为 `amd64` 和 `arm64` 构建 Linux 镜像：

```console
$ docker buildx build \
  --builder=kube \
  --platform=linux/amd64,linux/arm64 \
  -t <user>/<image> \
  --push .
```

> [!WARNING]
>
> QEMU 执行非原生平台的完整 CPU 模拟，这比原生构建慢得多。计算密集型任务（如编译和压缩/解压缩）可能会受到很大的性能影响。

使用自定义 BuildKit 镜像或在构建中调用非原生二进制文件可能需要您在创建构建器时使用 `qemu.install` 选项显式启用 QEMU：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,qemu.install=true
```

### 原生

如果您可以访问不同架构的集群节点，Kubernetes 驱动可以利用这些节点进行原生构建。为此，请使用 `docker buildx create` 的 `--append` 标志。

首先，创建一个明确支持单一架构的构建器，例如 `amd64`：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/amd64 \
  --node=builder-amd64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=amd64"
```

这会创建一个名为 `kube` 的 Buildx 构建器，包含一个名为 `builder-amd64` 的构建器节点。使用 `--node` 分配节点名称是可选的。如果不提供，Buildx 会生成一个随机节点名称。

请注意，Buildx 的节点概念与 Kubernetes 的节点概念不同。在这种情况下，Buildx 节点可以将多个相同架构的 Kubernetes 节点连接在一起。

创建 `kube` 构建器后，您现在可以使用 `--append` 引入另一个架构。例如，添加 `arm64`：

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

列出您的构建器会显示 `kube` 构建器的两个节点：

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT                                         STATUS   PLATFORMS
kube            kubernetes
  builder-amd64 kubernetes:///kube?deployment=builder-amd64&kubeconfig= running  linux/amd64*, linux/amd64/v2, linux/amd64/v3, linux/386
  builder-arm64 kubernetes:///kube?deployment=builder-arm64&kubeconfig= running  linux/arm64*
```

现在您可以通过在构建命令中同时指定这些平台来构建多架构 `amd64` 和 `arm64` 镜像：

```console
$ docker buildx build --builder=kube --platform=linux/amd64,linux/arm64 -t <user>/<image> --push .
```

您可以对想要支持的任意数量的架构重复 `buildx create --append` 命令。

## 无根模式

Kubernetes 驱动支持无根模式（rootless mode）。有关无根模式如何工作及其要求的更多信息，请参阅[此处](https://github.com/moby/buildkit/blob/master/docs/rootless.md)。

要在集群中启用它，您可以使用 `rootless=true` 驱动选项：

```console
$ docker buildx create \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,rootless=true
```

这将创建不带 `securityContext.privileged` 的 pod。

需要 Kubernetes 1.19 或更高版本。建议使用 Ubuntu 作为主机内核。

## 示例：在 Kubernetes 中创建 Buildx 构建器

本指南向您展示如何：

- 为 Buildx 资源创建命名空间
- 创建 Kubernetes 构建器
- 列出可用的构建器
- 使用 Kubernetes 构建器构建镜像

前提条件：

- 您有一个现有的 Kubernetes 集群。如果您还没有，可以通过安装 [minikube](https://minikube.sigs.k8s.io/docs/) 来跟随操作。
- 您要连接的集群可以通过 `kubectl` 命令访问，如有必要，请[适当设置](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/#set-the-kubeconfig-environment-variable) `KUBECONFIG` 环境变量。

1. 创建一个 `buildkit` 命名空间。

   创建单独的命名空间有助于将 Buildx 资源与集群中的其他资源分开。

   ```console
   $ kubectl create namespace buildkit
   namespace/buildkit created
   ```

2. 使用 Kubernetes 驱动创建一个新的构建器：

   ```console
   $ docker buildx create \
     --bootstrap \
     --name=kube \
     --driver=kubernetes \
     --driver-opt=namespace=buildkit
   ```

   > [!NOTE]
   >
   > 请记住在驱动选项中指定命名空间。

3. 使用 `docker buildx ls` 列出可用的构建器

   ```console
   $ docker buildx ls
   NAME/NODE                DRIVER/ENDPOINT STATUS  PLATFORMS
   kube                     kubernetes
     kube0-6977cdcb75-k9h9m                 running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
   default *                docker
     default                default         running linux/amd64, linux/386
   ```

4. 使用 `kubectl` 检查由构建驱动创建的正在运行的 pod。

   ```console
   $ kubectl -n buildkit get deployments
   NAME    READY   UP-TO-DATE   AVAILABLE   AGE
   kube0   1/1     1            1           32s

   $ kubectl -n buildkit get pods
   NAME                     READY   STATUS    RESTARTS   AGE
   kube0-6977cdcb75-k9h9m   1/1     Running   0          32s
   ```

   构建驱动会在指定的命名空间（在本例中为 `buildkit`）中的集群上创建必要的资源，同时在本地保留您的驱动配置。

5. 在运行 buildx 命令时包含 `--builder` 标志来使用您的新构建器。例如：

   ```console
   # Replace <registry> with your Docker username
   # and <image> with the name of the image you want to build
   docker buildx build \
     --builder=kube \
     -t <registry>/<image> \
     --push .
   ```

就是这样：您现在已经使用 Buildx 从 Kubernetes pod 构建了一个镜像。

## 延伸阅读

有关 Kubernetes 驱动的更多信息，请参阅 [buildx 参考文档](/reference/cli/docker/buildx/create.md#driver)。
