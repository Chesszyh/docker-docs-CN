---
title: Docker 强化镜像的测试方式
linktitle: 镜像测试
description: 了解 Docker 强化镜像如何自动测试标准合规性、功能和安全性。
keywords: docker scout, test attestation, cosign verify, image testing, vulnerability scan
weight: 45
---

Docker 强化镜像（DHIs）设计为安全、精简和生产就绪。为了确保其可靠性和安全性，Docker 采用了全面的测试策略，您可以使用签名证明和开放工具独立验证。

每个镜像都经过标准合规性、功能和安全性测试。这些测试的结果作为签名证明嵌入，可以使用 Docker Scout CLI [检查和验证](#view-and-verify-the-test-attestation)。

## 测试策略概述

DHIs 的测试过程专注于两个主要领域：

- 镜像标准合规性：确保每个镜像遵守严格的大小、安全性和兼容性标准。
- 应用程序功能：验证镜像中的应用程序是否正确运行。

## 镜像标准合规性

每个 DHI 都经过严格检查以满足以下标准：

- 最小攻击面：镜像构建得尽可能小，移除不必要的组件以减少潜在漏洞。
- 接近零已知 CVE：使用 Docker Scout 等工具扫描镜像，确保它们不受已知常见漏洞和暴露（CVE）的影响。
- 多架构支持：DHIs 为多种架构构建（`linux/amd64` 和 `linux/arm64`），以确保广泛的兼容性。
- Kubernetes 兼容性：镜像经过测试可在 Kubernetes 集群中无缝运行，确保它们满足容器编排环境的要求。

## 应用程序功能测试

Docker 测试 Docker 强化镜像以确保它们在典型使用场景中按预期运行。这包括验证：

- 应用程序在容器化环境中成功启动和运行。
- 运行时行为与上游预期一致。
- 构建变体（如 `-dev` 镜像）支持常见的开发和构建任务。

目标是确保 DHIs 开箱即用地适用于最常见的用例，同时保持强化、精简的设计。

## 自动化测试和 CI/CD 集成

Docker 将自动化测试集成到其持续集成/持续部署（CI/CD）管道中：

- 自动扫描：每次镜像构建都会触发漏洞和合规性检查的自动扫描。
- 可重现构建：构建过程设计为可重现，确保在不同环境中的一致性。
- 持续监控：Docker 持续监控新漏洞并相应更新镜像以维护安全标准。

## 测试证明

Docker 提供测试证明，详细说明每个 DHI 经历的测试和验证过程。

### 查看和验证测试证明

您可以使用 Docker Scout CLI 查看和验证此证明。

1. 使用带有测试谓词类型的 `docker scout attest get` 命令：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     <your-namespace>/dhi-<image>:<tag> --platform <platform>
   ```

   例如：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     docs/dhi-python:3.13 --platform linux/amd64
   ```

   这包含测试列表及其结果。

   示例输出：

    ```console
        v SBOM obtained from attestation, 101 packages found
        v Provenance obtained from attestation
        {
          "reportFormat": "CTRF",
          "results": {
            "summary": {
              "failed": 0,
              "passed": 1,
              "skipped": 0,
              "start": 1749216533,
              "stop": 1749216574,
              "tests": 1
            },
            "tests": [
              {
                ...
   ```

2. 验证测试证明签名。要确保证明是真实的并由 Docker 签名，请运行：

   ```console
   docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --verify \
     <your-namespace>/dhi-<image>:<tag> --platform <platform>
   ```

   示例输出：

   ```console
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v cosign verify registry.scout.docker.com/docker/dhi-python@sha256:70c8299c4d3cb4d5432734773c45ae58d8acc2f2f07803435c65515f662136d5 \
        --key https://registry.scout.docker.com/keyring/dhi/latest.pub --experimental-oci11

      Verification for registry.scout.docker.com/docker/dhi-python@sha256:70c8299c4d3cb4d5432734773c45ae58d8acc2f2f07803435c65515f662136d5 --
      The following checks were performed on each of these signatures:
        - The cosign claims were validated
        - Existence of the claims in the transparency log was verified offline
        - The signatures were verified against the specified public key

    i Signature payload
    ...
    ```

如果证明有效，Docker Scout 将确认签名并显示匹配的 `cosign verify` 命令。

要查看其他证明，如 SBOM 或漏洞报告，请参阅[验证镜像](../how-to/verify.md)。
