---
description: Docker Scout 如何处理镜像元数据
keywords: |
  scout, 扫描, 供应链, 安全, purl, sbom, 来源, 环境,
  材料, 配置, 端口, 标签, 操作系统, 注册表, 时间戳, 摘要, 层,
  架构, 许可, 依赖关系, 基础镜像
title: Docker Scout 中的数据收集和存储
aliases:
  /scout/data-handling/
---

Docker Scout 的镜像分析通过从您分析的容器镜像中收集元数据来工作。这些元数据存储在 Docker Scout 平台上。

## 数据传输

本节描述了 Docker Scout 收集并发送到平台的数据。

### 镜像元数据

Docker Scout 收集以下镜像元数据：

- 镜像创建时间戳
- 镜像摘要 (Digest)
- 镜像暴露的端口
- 环境变量名称和值
- 镜像标签的名称和值
- 镜像层的顺序
- 硬件架构
- 操作系统类型和版本
- 注册表 URL 和类型

当镜像被构建并推送到注册表时，会为镜像的每一层创建镜像摘要。它们是层内容的 SHA256 摘要。Docker Scout 不创建这些摘要；它们是从镜像清单 (manifest) 中读取的。

这些摘要会与您自己的私有镜像以及 Docker 的公共镜像数据库进行匹配，以识别共享相同层的镜像。共享大部分层的镜像被认为与当前正在分析的镜像存在基础镜像匹配。

### SBOM 元数据

软件物料清单 (SBOM) 元数据用于将软件包类型和版本与漏洞数据进行匹配，以推断镜像是否受到影响。当 Docker Scout 平台从安全公告中接收到有关新 CVE 或其他风险因素 (如泄露的机密) 的信息时，它会将此信息与 SBOM 进行交叉引用。如果有匹配项，Docker Scout 会在显示 Docker Scout 数据的用户界面 (如 Docker Scout 控制面板和 Docker Desktop) 中显示结果。

Docker Scout 收集以下 SBOM 元数据：

- 软件包 URL (PURL)
- 软件包作者和描述
- 许可证 ID
- 软件包名称和命名空间
- 软件包方案和大小
- 软件包类型和版本
- 镜像内的文件路径
- 直接依赖的类型
- 软件包总数

Docker Scout 中的 PURL 遵循 [purl-spec](https://github.com/package-url/purl-spec) 规范。软件包信息源自镜像内容，包括操作系统级程序和软件包，以及应用程序级软件包 (如 maven、npm 等)。

### 环境元数据

如果您通过 [Sysdig 集成](/manuals/scout/integrations/environment/sysdig.md) 将 Docker Scout 与您的运行时环境集成，Docker Scout 会收集有关您部署的以下数据点：

- Kubernetes 命名空间
- 工作负载名称
- 工作负载类型 (例如，DaemonSet)

### 本地分析

对于在开发人员机器上本地分析的镜像，Docker Scout 仅传输 PURL 和层摘要。这些数据不会持久存储在 Docker Scout 平台上；它们仅用于运行分析。

### 来源 (Provenance)

对于具有 [来源证明](/manuals/build/metadata/attestations/slsa-provenance.md) 的镜像，Docker Scout 除存储 SBOM 外，还存储以下数据：

- 材料 (Materials)
- 基础镜像
- VCS 信息
- Dockerfile

## 数据存储

为了提供 Docker Scout 服务，数据存储使用：

- 位于美国东部服务器上的 Amazon Web Services (AWS)
- 位于美国东部服务器上的 Google Cloud Platform (GCP)

数据将根据 [docker.com/legal](https://www.docker.com/legal/) 中描述的流程使用，以提供 Docker Scout 的核心功能。
