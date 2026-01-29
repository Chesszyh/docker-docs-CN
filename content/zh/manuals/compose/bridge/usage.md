---
title: 使用默认的 Compose Bridge 转换
linkTitle: 使用
weight: 10
description: 了解如何使用默认的 Compose Bridge 转换将 Compose 文件转换为 Kubernetes 清单
keywords: docker compose bridge, compose kubernetes transform, kubernetes from compose, compose bridge convert, compose.yaml to kubernetes
---

{{< summary-bar feature_name="Compose bridge" >}}

Compose Bridge 为您的 Compose 配置文件提供开箱即用的转换。基于任意 `compose.yaml` 文件，Compose Bridge 会生成：

- 一个 [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)，使您的所有资源都处于隔离状态，不会与其他部署的资源发生冲突。
- 一个 [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)，包含 Compose 应用程序中每一个 [config](/reference/compose-file/configs.md) 资源的条目。
- 针对应用程序服务的 [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)。这确保了在 Kubernetes 集群中维持指定数量的应用程序实例。
- 针对您的服务所暴露端口的 [Services](https://kubernetes.io/docs/concepts/services-networking/service/)，用于服务间通信。
- 针对您的服务所发布端口的 [Services](https://kubernetes.io/docs/concepts/services-networking/service/)，类型为 `LoadBalancer`，以便 Docker Desktop 也能在宿主机上暴露同样的端口。
- [Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)，用以复制 `compose.yaml` 文件中定义的网络拓扑。 
- 针对您的卷的 [PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)，使用 `hostpath` 存储类，以便由 Docker Desktop 管理卷的创建。
- 编码了您的 secret 的 [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)。这是专为测试环境中的本地使用而设计的。

它还提供了一个专用于 Docker Desktop 的 Kustomize 叠加层（overlay），包含：
 - 为需要在宿主机上暴露端口的服务提供 `Loadbalancer`。
 - 一个 `PersistentVolumeClaim`，使用 Docker Desktop 存储供应程序 `desktop-storage-provisioner` 更有效地处理卷供应。
 - 一个 Kustomize 文件，将所有资源链接在一起。

## 使用默认的 Compose Bridge 转换

要使用默认转换，请运行以下命令：

```console
$ docker compose bridge convert
```

Compose 会在当前目录中查找 `compose.yaml` 文件并进行转换。

成功后，Compose Bridge 会生成 Kubernetes 清单，并记录类似于以下内容的输出：

```console
$ docker compose bridge convert -f compose.yaml 
Kubernetes resource api-deployment.yaml created
Kubernetes resource db-deployment.yaml created
Kubernetes resource web-deployment.yaml created
Kubernetes resource api-expose.yaml created
Kubernetes resource db-expose.yaml created
Kubernetes resource web-expose.yaml created
Kubernetes resource 0-avatars-namespace.yaml created
Kubernetes resource default-network-policy.yaml created
Kubernetes resource private-network-policy.yaml created
Kubernetes resource public-network-policy.yaml created
Kubernetes resource db-db_data-persistentVolumeClaim.yaml created
Kubernetes resource api-service.yaml created
Kubernetes resource web-service.yaml created
Kubernetes resource kustomization.yaml created
Kubernetes resource db-db_data-persistentVolumeClaim.yaml created
Kubernetes resource api-service.yaml created
Kubernetes resource web-service.yaml created
Kubernetes resource kustomization.yaml created
```

这些文件随后存储在您项目的 `/out` 文件夹中。 

随后可以使用标准的部署命令 `kubectl apply -k out/overlays/desktop/` 来在 Kubernetes 上运行该应用程序。

> [!IMPORTANT]
>
> 在部署 Compose Bridge 转换结果之前，请确保已在 Docker Desktop 中启用了 Kubernetes。

如果您想转换位于另一个目录中的 `compose.yaml` 文件，可以运行：

```console
$ docker compose bridge convert -f <path-to-file>/compose.yaml 
```

要查看所有可用标志，请运行：

```console
$ docker compose bridge convert --help
```

> [!TIP]
>
> 您可以从 Compose 文件查看器转换您的 Compose 项目并将其部署到 Kubernetes 集群。
> 
> 请确保您已登录 Docker 账户，在 **Containers**（容器）视图中导航到您的容器，在右上角选择 **View configurations**（查看配置），然后选择 **Convert and Deploy to Kubernetes**（转换并部署到 Kubernetes）。 

## 下一步

- [探索如何自定义 Compose Bridge](customize.md)
