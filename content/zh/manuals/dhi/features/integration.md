---
title: 无缝集成
description: 了解 Docker Hardened Images 如何集成到您现有的开发和部署工作流中，在不影响可用性的情况下增强安全性。
description_short: 了解 Docker Hardened Images 如何与您工具链中的 CI/CD 流水线、漏洞扫描器和容器镜像仓库进行集成
keywords: ci cd containers, vulnerability scanning, slsa build level 3, signed sbom, oci compliant registry
---

Docker Hardened Images（DHI）旨在无缝集成到您现有的开发和部署工作流中，确保增强的安全性不会以牺牲可用性为代价。

## 在 Docker Hub 上探索镜像

在您的组织[注册](https://www.docker.com/products/hardened-images/#getstarted)后，团队可以直接在 Docker Hub 上探索完整的 DHI 目录。在那里，开发人员和安全团队可以：

- 查看可用的镜像和语言/框架变体
- 了解支持的发行版
- 比较开发版与运行时版变体

每个仓库都包含元数据，如支持的标签、基础镜像配置和镜像特定文档，帮助您为项目选择合适的变体。

## 在 CI/CD 工作流中使用 DHI

您可以在任何使用 Dockerfile 构建的 CI/CD 流水线中将 DHI 用作基础镜像。它们可以轻松集成到您团队已经使用的平台中，如 GitHub Actions、GitLab CI/CD、Jenkins、CircleCI 和其他自动化系统。

## 专为您的 DevSecOps 技术栈打造

Docker Hardened Images 旨在与您现有的 DevSecOps 工具链无缝协作。它们可以与团队已经使用的扫描工具、镜像仓库、CI/CD 系统和策略引擎集成。

Docker 已与广泛的生态系统合作伙伴建立合作关系，以确保 DHI 能够与您现有的工作流和工具开箱即用。这些合作伙伴帮助将增强的扫描、元数据验证和合规洞察直接交付到您的流水线中。

所有 DHI 都包含：

- 签名的软件物料清单（SBOM，Software Bill of Materials）
- CVE 数据
- 漏洞可利用性交换（VEX，Vulnerability Exploitability eXchange）文档
- SLSA Build Level 3 来源证明

由于元数据是签名且结构化的，您可以将其输入到策略引擎和仪表板中，用于审计或合规工作流。

## 通过您首选的镜像仓库分发

DHI 会被镜像到您组织在 Docker Hub 上的命名空间。从那里，您可以选择性地将它们推送到任何 OCI 兼容的镜像仓库，例如：

- Amazon ECR
- Google Artifact Registry
- GitHub Container Registry
- Azure Container Registry
- Harbor
- JFrog Artifactory
- 其他 OCI 兼容的本地或云镜像仓库

镜像功能确保团队可以从其首选位置拉取镜像，而不会破坏策略或构建系统。

## 总结

Docker Hardened Images 可与您已经使用的工具集成，从开发和 CI 到扫描和部署。它们：

- 与标准 Docker 工具和流水线配合使用
- 支持流行的扫描器和镜像仓库
- 包含可接入您现有合规系统的安全元数据

这意味着您可以采用更强的安全控制，而不会中断您的工程工作流。
