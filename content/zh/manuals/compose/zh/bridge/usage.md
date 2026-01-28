---
title: 使用默认的 Compose Bridge 转换
linkTitle: 使用
weight: 10
description: 了解如何使用默认的 Compose Bridge 转换将 Compose 文件转换为 Kubernetes 清单
keywords: docker compose bridge, compose kubernetes transform, kubernetes from compose, compose bridge convert, compose.yaml to kubernetes
---

{{< summary-bar feature_name="Compose bridge" >}}

Compose Bridge 为您的 Compose 配置文件提供开箱即用的转换。基于任意 `compose.yaml` 文件，Compose Bridge 生成：

- 一个 [Namespace（命名空间）](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)，以便您的所有资源都被隔离，不会与其他部署的资源冲突。
- 一个 [ConfigMap（配置映射）](https://kubernetes.io/docs/concepts/configuration/configmap/)，其中包含 Compose 应用程序中每个 [config](/reference/compose-file/configs.md) 资源的条目。
- [Deployments（部署）](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)用于应用程序服务。这确保在 Kubernetes 集群中维护指定数量的应用程序实例。
- [Services（服务）](https://kubernetes.io/docs/concepts/services-networking/service/)用于您的服务暴露的端口，用于服务间通信。
- [Services（服务）](https://kubernetes.io/docs/concepts/services-networking/service/)用于您的服务发布的端口，类型为 `LoadBalancer`，以便 Docker Desktop 也在主机上暴露相同的端口。
- [Network policies（网络策略）](https://kubernetes.io/docs/concepts/services-networking/network-policies/)用于复制 `compose.yaml` 文件中定义的网络拓扑。
- [PersistentVolumeClaims（持久卷声明）](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)用于您的卷，使用 `hostpath` 存储类，以便 Docker Desktop 管理卷的创建。
- [Secrets（密钥）](https://kubernetes.io/docs/concepts/configuration/secret/)包含您编码后的密钥。这是为在测试环境中本地使用而设计的。

它还提供专门用于 Docker Desktop 的 Kustomize 覆盖层，包含：
 - 用于需要在主机上暴露端口的服务的 `Loadbalancer`。
 - 使用 Docker Desktop 存储供应器 `desktop-storage-provisioner` 的 `PersistentVolumeClaim`，以更有效地处理卷供应。
 - 一个 Kustomize 文件，将所有资源链接在一起。

## 使用默认的 Compose Bridge 转换

要使用默认转换，运行以下命令：

```console
$ docker compose bridge convert
```

Compose 在当前目录中查找 `compose.yaml` 文件，然后进行转换。

成功后，Compose Bridge 会生成 Kubernetes 清单并输出类似以下的日志：

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

然后可以使用标准部署命令 `kubectl apply -k out/overlays/desktop/` 在 Kubernetes 上运行这些 Kubernetes 清单。

> [!IMPORTANT]
>
> 在部署 Compose Bridge 转换之前，请确保已在 Docker Desktop 中启用 Kubernetes。

如果您想转换位于另一个目录中的 `compose.yaml` 文件，可以运行：

```console
$ docker compose bridge convert -f <path-to-file>/compose.yaml
```

要查看所有可用标志，运行：

```console
$ docker compose bridge convert --help
```

> [!TIP]
>
> 您可以从 Compose 文件查看器将 Compose 项目转换并部署到 Kubernetes 集群。
>
> 确保您已登录 Docker 账户，在**容器**视图中导航到您的容器，然后在右上角选择**查看配置**，接着选择**转换并部署到 Kubernetes**。

## 下一步是什么？

- [探索如何自定义 Compose Bridge](customize.md)
