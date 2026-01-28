---
description: Docker Scout 如何处理镜像元数据
keywords: |
  scout, scanning, supply chain, security, purl, sbom, provenance, environment,
  materials, config, ports, labels, os, registry, timestamp, digest, layers,
  architecture, license, dependencies, base image
title: Docker Scout 中的数据收集和存储
aliases:
  /scout/data-handling/
---

Docker Scout 的镜像分析通过从您分析的容器镜像中收集元数据来工作。
这些元数据存储在 Docker Scout 平台上。

## 数据传输

本节描述 Docker Scout 收集并发送到平台的数据。

### 镜像元数据

Docker Scout 收集以下镜像元数据：

- 镜像创建时间戳
- 镜像摘要
- 镜像暴露的端口
- 环境变量名称和值
- 镜像标签的名称和值
- 镜像层的顺序
- 硬件架构
- 操作系统类型和版本
- 镜像仓库 URL 和类型

镜像摘要在构建镜像并推送到镜像仓库时为每个层创建。
它们是层内容的 SHA256 摘要。
Docker Scout 不创建摘要；它们是从镜像清单中读取的。

这些摘要与您自己的私有镜像和 Docker 的公共镜像数据库进行匹配，
以识别共享相同层的镜像。共享最多层的镜像被视为当前正在分析的镜像的基础镜像匹配。

### SBOM 元数据

软件物料清单（Software Bill of Material，SBOM）元数据用于将软件包类型和版本与漏洞数据进行匹配，
以推断镜像是否受到影响。
当 Docker Scout 平台从安全公告收到有关新 CVE 或其他风险因素（如泄露的密钥）的信息时，
它会将此信息与 SBOM 进行交叉引用。如果存在匹配，Docker Scout 会在显示 Docker Scout 数据的用户界面中显示结果，
例如 Docker Scout 仪表板和 Docker Desktop。

Docker Scout 收集以下 SBOM 元数据：

- 软件包 URL（PURL）
- 软件包作者和描述
- 许可证 ID
- 软件包名称和命名空间
- 软件包方案和大小
- 软件包类型和版本
- 镜像内的文件路径
- 直接依赖的类型
- 软件包总数

Docker Scout 中的 PURL 遵循
[purl-spec](https://github.com/package-url/purl-spec) 规范。软件包信息来源于镜像内容，
包括操作系统级别的程序和软件包，以及应用程序级别的软件包，如 maven、npm 等。

### 环境元数据

如果您通过 [Sysdig 集成](/manuals/scout/integrations/environment/sysdig.md)将 Docker Scout 与运行时环境集成，
Docker Scout 会收集以下关于您部署的数据点：

- Kubernetes 命名空间
- 工作负载名称
- 工作负载类型（例如 DaemonSet）

### 本地分析

对于在开发者机器上本地分析的镜像，Docker Scout 只传输 PURL 和层摘要。
这些数据不会持久存储在 Docker Scout 平台上；它们只用于运行分析。

### 来源（Provenance）

对于具有[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)的镜像，
Docker Scout 除了存储 SBOM 外还存储以下数据：

- Materials（材料）
- 基础镜像
- VCS 信息
- Dockerfile

## 数据存储

为了提供 Docker Scout 服务，数据存储使用：

- Amazon Web Services（AWS），服务器位于美国东部
- Google Cloud Platform（GCP），服务器位于美国东部

数据的使用遵循 [docker.com/legal](https://www.docker.com/legal/) 中描述的流程，
以提供 Docker Scout 的关键功能。
