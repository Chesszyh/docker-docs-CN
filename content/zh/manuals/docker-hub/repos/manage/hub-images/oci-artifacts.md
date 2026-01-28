---
title: Docker Hub 上的软件制品
linkTitle: 软件制品
weight: 20
keywords: oci, artifacts, docker hub
description: 您可以使用 Docker Hub 存储打包为 OCI 制品的软件制品。
aliases:
- /docker-hub/oci-artifacts/
---

您可以使用 Docker Hub 存储任何类型的软件制品，不仅限于容器镜像。软件制品是软件开发过程中产生的任何项目，它们有助于软件的创建、维护或理解。Docker Hub 通过利用镜像清单上的 config 属性来支持 OCI 制品。

## 什么是 OCI 制品？

OCI 制品是与软件应用程序相关的任何任意文件。一些示例包括：

- Helm charts
- 软件物料清单（SBOM，Software Bill of Materials）
- 数字签名
- 来源数据
- 证明
- 漏洞报告

Docker Hub 支持 OCI 制品意味着您可以使用一个仓库来存储和分发容器镜像以及其他资产。

OCI 制品的一个常见用例是 [Helm charts](https://helm.sh/docs/topics/charts/)。Helm charts 是一种定义应用程序 Kubernetes 部署的打包格式。由于 Kubernetes 是容器的流行运行时，因此将应用程序镜像和部署模板都托管在一个地方是有意义的。

## 在 Docker Hub 中使用 OCI 制品

您在 Docker Hub 上管理 OCI 制品的方式与管理容器镜像类似。

向注册表推送和拉取 OCI 制品是使用注册表客户端完成的。[ORAS CLI](https://oras.land/docs/installation) 是一个命令行工具，提供在注册表中管理 OCI 制品的功能。如果您使用 Helm charts，[Helm CLI](https://helm.sh/docs/intro/install/) 提供了内置功能，用于向注册表推送和拉取 charts。

注册表客户端调用 HTTP 请求到 Docker Hub 注册表 API。注册表 API 符合 [OCI 分发规范](https://github.com/opencontainers/distribution-spec) 中定义的标准协议。

## 示例

本节展示了在 Docker Hub 中使用 OCI 制品的一些示例。

### 推送 Helm chart

以下步骤展示了如何将 Helm chart 作为 OCI 制品推送到 Docker Hub。

前提条件：

- Helm 版本 3.0.0 或更高版本

步骤：

1. 创建一个新的 Helm chart

   ```console
   $ helm create demo
   ```

   此命令生成一个样板模板 chart。

2. 将 Helm chart 打包成 tarball。

   ```console
   $ helm package demo
   Successfully packaged chart and saved it to: /Users/hubuser/demo-0.1.0.tgz
   ```

3. 使用您的 Docker 凭据通过 Helm 登录 Docker Hub。

   ```console
   $ helm registry login registry-1.docker.io -u hubuser
   ```

4. 将 chart 推送到 Docker Hub 仓库。

   ```console
   $ helm push demo-0.1.0.tgz oci://registry-1.docker.io/docker
   ```

   这会将 Helm chart tarball 上传到 `docker` 命名空间中的 `demo` 仓库。

5. 转到 Docker Hub 上的仓库页面。页面的 **Tags** 部分显示 Helm chart 标签。

   ![List of repository tags](./images/oci-helm.png)

6. 选择标签名称以转到该标签的页面。

   该页面列出了一些用于处理 Helm charts 的有用命令。

   ![Tag page of a Helm chart artifact](./images/oci-helm-tagview.png)

### 推送卷

以下步骤展示了如何将容器卷作为 OCI 制品推送到 Docker Hub。

前提条件：

- ORAS CLI 版本 0.15 或更高版本

步骤：

1. 创建一个用作卷内容的虚拟文件。

   ```console
   $ touch myvolume.txt
   ```

2. 使用 ORAS CLI 登录 Docker Hub。

   ```console
   $ oras login -u hubuser registry-1.docker.io
   ```

3. 将文件推送到 Docker Hub。

   ```console
   $ oras push registry-1.docker.io/docker/demo:0.0.1 \
     --artifact-type=application/vnd.docker.volume.v1+tar.gz \
     myvolume.txt:text/plain
   ```

   这会将卷上传到 `docker` 命名空间中的 `demo` 仓库。`--artifact-type` 标志指定一个特殊的媒体类型，使 Docker Hub 将该制品识别为容器卷。

4. 转到 Docker Hub 上的仓库页面。该页面上的 **Tags** 部分显示卷标签。

   ![Repository page showing a volume in the tag list](./images/oci-volume.png)

### 推送通用制品文件

以下步骤展示了如何将通用 OCI 制品推送到 Docker Hub。

前提条件：

- ORAS CLI 版本 0.15 或更高版本

步骤：

1. 创建您的制品文件。

   ```console
   $ touch myartifact.txt
   ```

2. 使用 ORAS CLI 登录 Docker Hub。

   ```console
   $ oras login -u hubuser registry-1.docker.io
   ```

3. 将文件推送到 Docker Hub。

   ```console
   $ oras push registry-1.docker.io/docker/demo:0.0.1 myartifact.txt:text/plain
   ```

4. 转到 Docker Hub 上的仓库页面。该页面上的 **Tags** 部分显示制品标签。

   ![Repository page showing an artifact in the tag list](./images/oci-artifact.png)
