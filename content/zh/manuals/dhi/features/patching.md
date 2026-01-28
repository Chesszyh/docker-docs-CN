---
title: 持续补丁和安全维护
linktitle: 持续补丁
description: 了解 Docker Hardened Images 如何自动重建、测试和更新，以与上游安全补丁保持同步。
keywords: docker hardened images, secure base image, automatic patching, CVE updates, compatibility, dev containers, runtime containers, image maintenance
---

Docker Hardened Images（DHI）为容器化应用提供安全且企业就绪的基础，由强大的自动化补丁流程支持，帮助维护合规性并减少漏洞暴露。

## 具有强兼容性的安全基础镜像

DHI 包含一组精选的最小化基础镜像，旨在跨广泛的环境和语言生态系统工作。这些镜像提供具有高兼容性的安全构建块，使其更容易集成到您现有的基础设施和开发工作流中，同时不牺牲安全性。

## 开发和运行时变体

为了支持软件生命周期的不同阶段，DHI 提供两种关键变体：

- 开发镜像：包含安全构建和测试应用所需的基本工具和库。
- 运行时镜像：仅包含运行应用所需的核心组件，提供更小的攻击面和更高的运行时效率。

这种变体结构支持多阶段构建，使开发人员能够在安全的开发容器中编译代码，并在生产环境中使用精简的运行时镜像进行部署。

## 自动化补丁和安全更新

Docker 监控上游开源软件包和安全公告中的漏洞（CVE）及其他更新。当检测到变更时，受影响的 Docker Hardened Images 会自动重建和测试。

更新后的镜像会附带加密来源证明（provenance attestations），以支持验证和合规工作流。这种自动化流程减少了手动补丁的运营负担，帮助团队与安全软件开发实践保持一致。
