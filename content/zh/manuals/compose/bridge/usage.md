---
title: 使用默认的 Compose Bridge 转换
linkTitle: 用法
weight: 10
description: 了解如何使用默认的 Compose Bridge 转换将 Compose 文件转换为 Kubernetes 清单
keywords: docker compose bridge, compose kubernetes transform, kubernetes from compose, compose bridge convert, compose.yaml to kubernetes, 转换, 清单
---

{{< summary-bar feature_name="Compose bridge" >}}

Compose Bridge 为您的 Compose 配置文件提供了一个开箱即用的转换。基于任意的 `compose.yaml` 文件，Compose Bridge 会生成：

- 一个 [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)，以便您的所有资源都被隔离，并且不会与其他部署的资源冲突。
- 一个 [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)，其中包含您 Compose 应用程序中每个 [config](/reference/compose-file/configs.md) 资源的条目。
- 应用程序服务的 [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)。这可确保在 Kubernetes 集群中维护指定数量的应用程序实��。
- 用于您的服务公开的端口的 [Services](https://kubernetes.io/docs/concepts/services-networking/service/)，用于服务到服务的通信。
- 用于您的服务发布的端口的 [Services](https://kubernetes.io/docs/concepts/services-networking/service/)，类型为 `LoadBalancer`，以便 Docker Desktop 也会在主机上公开相同的端口。
- [Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) 以复制您 `compose.yaml` 文件中定义的网络拓扑。
- 您的卷的 [PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)，使用 `hostpath` 存储类，以便 Docker Desktop 管理卷创建。
- 包含您的密钥编码的 [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)。这专为在测试环境中本地使用而设计。

它还提供了一个专用于 Docker Desktop 的 Kustomize 覆盖，其中包含：
 - 用于需要���主机上公开端口的服务的 `Loadbalancer`。
 - 一个 `PersistentVolumeClaim`，用于使用 Docker Desktop 存储提供程序 `desktop-storage-provisioner` 更有效地处理卷配置。
 - 一个 Kustomize 文件，用于将所有资源链接在一起。

## 使用默认的 Compose Bridge 转换

要使用默认转换，请运行以下命令：

```console
$ docker compose bridge convert
```

Compose 会在当前目录中查找 `compose.yaml` 文件，然后将其转换。

成功后，Compose Bridge 会生成 Kubernetes 清单并记录类似于以下内容的输出：

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

然后，这些文件将存储在您项目的 `/out` 文件夹中。

然后，可以使用标准的部署命令 `kubectl apply -k out/overlays/desktop/` 将 Kubernetes 清单用于在 Kubernetes 上运行应用程序。

> [!IMPORTANT]
>
> 在部署 Compose Bridge 转换之前，请确保您已在 Docker Desktop 中启用了 Kubernetes。

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
> 您可以从 Compose 文件查看器将您的 Compose 项目转换并部署到 Kubernetes 集群。
> 
> 确保您已登录到您的 Docker 帐户，在 **Containers** 视图中导航到您的容器，然后在右上角选择 **View configurations**，然后选择 **Convert and Deploy to Kubernetes**。

## 下一步是什么？

- [探索如何自定义 Compose Bridge](customize.md)
