---
title: 加固的安全镜像
description: 了解 Docker Hardened Images 如何减少漏洞、强制非 root 执行，以及包含符合 SLSA 标准的元数据以保障供应链安全。
keywords: non-root containers, slsa build level 3, signed sbom, vex document, hardened container image
---

Docker Hardened Images（DHI）旨在为容器化应用提供强大的安全基础，应对软件供应链安全不断演变的挑战。

## 接近零漏洞和非 root 执行

每个 DHI 都经过精心构建以消除已知漏洞，通过持续扫描和更新实现接近零的通用漏洞披露（CVE，Common Vulnerabilities and Exposures）。通过遵循最小权限原则，DHI 镜像默认以非 root 用户运行，降低生产环境中权限提升攻击的风险。

## 全面的供应链安全

DHI 整合了多层安全元数据，以确保透明度和信任：

- SLSA Level 3 合规：每个镜像都包含详细的构建来源证明，符合软件制品供应链级别（SLSA，Supply-chain Levels for Software Artifacts）框架设定的标准。

- 软件物料清单（SBOM，Software Bill of Materials）：提供全面的 SBOM，详细列出镜像中的所有组件，以便于漏洞管理和合规审计。

- 漏洞可利用性交换（VEX，Vulnerability Exploitability eXchange）声明：每个镜像都附带 VEX 文档，提供有关已知漏洞及其可利用性状态的上下文信息。

- 加密签名和证明：所有镜像及相关元数据都经过加密签名，确保完整性和真实性。

## 最小化和开发者友好的选项

DHI 提供最小化和开发者友好的镜像变体：

- 最小化镜像：使用 distroless 方法构建，这些镜像移除了不必要的组件，将攻击面减少高达 95%，并改善启动时间。

- 开发镜像：配备必要的开发工具和库，这些镜像便于安全地构建和测试应用。
