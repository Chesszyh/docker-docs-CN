---
title: 构建器设置
description: 设置与私有镜像库、磁盘分配相关的构建器设置。
keywords: build, cloud build, 优化, 远程, 本地, 云, 镜像库, 软件包仓库, vpn
---

Docker Build Cloud 中的 **Builder settings**（构建器设置）页面允许您为组织中的云构建器配置磁盘分配、私有资源访问和防火墙设置。这些配置有助于优化存储、实现对私有镜像库的访问并保障出站网络流量的安全。

## 存储和缓存管理

### 磁盘分配

**Disk allocation**（磁盘分配）设置允许您控制有多少可用存储专用于构建缓存。较低的分配额会增加可用于活动构建的存储空间。

要更改磁盘分配，请导航至 Docker Build Cloud 中的 **Builder settings**，然后调整 **Disk allocation** 滑块以指定用于构建缓存的存储百分比。

任何更改都会立即生效。

### 构建缓存空间

您的订阅包含以下构建缓存空间：

| 订阅 | 构建缓存空间 |
|--------------|-------------------|
| 个人 (Personal)     | 不适用               |
| Pro          | 50GB              |
| Team         | 100GB             |
| Business     | 200GB             |

### 多架构存储分配

Docker Build Cloud 会自动为 amd64 和 arm64 架构配置构建器。您的总构建缓存空间将平均分配给这两个构建器：

- Pro（总计 50GB）：amd64 构建器 25GB + arm64 构建器 25GB
- Team（总计 100GB）：amd64 构建器 50GB + arm64 构建器 50GB
- Business（总计 200GB）：amd64 构建器 100GB + arm64 构建器 100GB

> [!IMPORTANT]
>
> 如果您仅针对一种架构进行构建，请注意您的有效缓存空间仅为订阅总分配额的一半。

### 获取更多构建缓存空间

要获取更多构建缓存空间，请 [升级您的订阅](/manuals/subscription/scale.md)。

> [!TIP]
>
> 如果您构建大型镜像，请考虑分配较少的存储空间用于缓存，以便为活动构建留出更多空间。

## 私有资源访问

私有资源访问允许云构建器从私有资源中拉取镜像和软件包。当构建依赖于自托管的构件仓库或私有 OCI 镜像库时，此功能非常有用。

例如，如果您组织在私有网络上托管了一个私有 [PyPI](https://pypi.org/) 仓库，默认情况下 Docker Build Cloud 将无法访问它，因为云构建器未连接到您的私有网络。

要允许您的云构建器访问私有资源，请输入私有资源的主机名和端口，然后选择 **Add**（添加）。

### 身份验证

如果您的内部构件需要身份验证，请确保在构建之前或构建期间通过仓库的身份验证。对于 npm 或 PyPI 的内部软件包仓库，请使用 [构建密钥](/manuals/build/building/secrets.md) 在构建期间进行身份验证。对于内部 OCI 镜像库，请在构建前使用 `docker login` 进行身份验证。

请注意，如果您使用需要身份验证的私有镜像库，则在构建前需要进行两次 `docker login` 身份验证。这是因为云构建器需要先通过 Docker 身份验证才能使用，然后再通过私有镜像库的身份验证。

```console
$ echo $DOCKER_PAT | docker login docker.io -u <username> --password-stdin
$ echo $REGISTRY_PASSWORD | docker login registry.example.com -u <username> --password-stdin
$ docker build --builder <cloud-builder> --tag registry.example.com/<image> --push .
```

## 防火墙

防火墙设置允许您将云构建器的出站流量限制在特定的 IP 地址。这有助于通过限制来自构建器的外部网络出站流量来增强安全性。

1. 勾选 **Enable firewall: Restrict cloud builder egress to specific public IP address**（启用防火墙：将云构建器出站限制在特定的公共 IP 地址）复选框。
2. 输入您想要允许的 IP 地址。
3. 选择 **Add**（添加）以应用限制。
