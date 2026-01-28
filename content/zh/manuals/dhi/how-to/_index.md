---
title: 操作指南
description: 使用 Docker Hardened Images 的分步指南，从发现到调试。
weight: 20
params:
  grid_howto:
    - title: 探索 Docker Hardened Images
      description: 了解如何在 Docker Hub 上的 DHI 目录中查找和评估镜像仓库、变体、元数据和证明。
      icon: travel_explore
      link: /dhi/how-to/explore/
    - title: 镜像 Docker Hardened Image 仓库
      description: 了解如何将镜像镜像到您组织的命名空间，并可选择推送到另一个私有镜像仓库。
      icon: compare_arrows
      link: /dhi/how-to/mirror/
    - title: 使用 Docker Hardened Image
      description: 了解如何在 Dockerfile、CI 流水线和标准开发工作流中拉取、运行和引用 Docker Hardened Images。
      icon: play_arrow
      link: /dhi/how-to/use/
    - title: 迁移现有应用以使用 Docker Hardened Images
      description: 按照分步指南更新您的 Dockerfile，采用 Docker Hardened Images 实现安全、最小化和生产就绪的构建。
      icon: directions_run
      link: /dhi/how-to/migrate/
    - title: 验证 Docker Hardened Image
      description: 使用 Docker Scout 或 cosign 验证 Docker Hardened Images 的签名证明，如 SBOM、来源证明和漏洞数据。
      icon: check_circle
      link: /dhi/how-to/verify/
    - title: 扫描 Docker Hardened Image
      description: 了解如何使用 Docker Scout、Grype 或 Trivy 扫描 Docker Hardened Images 中的已知漏洞。
      icon: bug_report
      link: /dhi/how-to/scan/
    - title: 通过策略强制使用 Docker Hardened Image
      description: 了解如何将镜像策略与 Docker Scout 配合用于 Docker Hardened Images。
      icon: policy
      link: /dhi/how-to/policies/
    - title: 调试 Docker Hardened Image
      description: 使用 Docker Debug 检查基于加固镜像运行的容器，而无需修改它。
      icon: terminal
      link: /dhi/how-to/debug/
---

本节提供使用 Docker Hardened Images（DHI）的实用分步指南。无论您是首次评估 DHI 还是将其集成到生产 CI/CD 流水线中，这些主题都将指导您完成采用过程的每个阶段，从发现到调试。

为了帮助您入门并保持安全，这些主题按照使用 DHI 的典型生命周期进行组织。

## 生命周期流程

1. 在 DHI 目录中探索可用的镜像和元数据。
2. 将受信任的镜像镜像到您的命名空间或镜像仓库中。
3. 通过拉取、在开发和 CI 中使用以及将现有应用迁移到使用安全、最小化的基础镜像，在您的工作流中采用 DHI。
4. 通过验证签名、SBOM 和来源证明以及扫描漏洞来分析镜像。
5. 强制执行策略以维护安全性和合规性。
6. 在不修改镜像的情况下调试基于 DHI 的容器。

以下每个主题都与此生命周期中的一个步骤对应，因此您可以自信地完成探索、实施和持续维护的过程。

## 分步主题

{{< grid
  items="grid_howto"
>}}
