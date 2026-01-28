---
title: 查看 Docker Scout 策略状态
description: |
  Docker Scout 仪表板和 `docker scout policy` 命令让您可以查看镜像的策略状态。
keywords: scout, policy, status, vulnerabilities, supply chain, cves, licenses
---

您可以从 [Docker Scout 仪表板](#dashboard)或使用 [CLI](#cli) 跟踪构建产物的策略状态。

## 仪表板

[Docker Scout 仪表板](https://scout.docker.com/)的 **Overview** 标签页显示您仓库最近策略变更的摘要。此摘要显示在最近镜像和之前镜像之间策略评估变化最大的镜像。

![策略概览](../images/policy-overview.webp)

### 每个仓库的策略状态

**Images** 标签页显示所选环境中所有镜像的当前策略状态和最近策略趋势。列表中的 **Policy status** 列显示：

- 已满足的策略数量与策略总数的对比
- 最近的策略趋势

![镜像列表中的策略状态](../images/policy-image-list.webp)

由方向箭头表示的策略趋势指示镜像在策略方面相对于同一环境中的先前镜像是更好、更差还是保持不变。

- 向上指的绿色箭头显示在最新推送的镜像中变好的策略数量。
- 向下指的红色箭头显示在最新推送的镜像中变差的策略数量。
- 双向的灰色箭头显示在此镜像最新版本中保持不变的策略数量。

如果您选择一个仓库，可以打开 **Policy** 标签页，查看最近分析的镜像及其前身的策略差异的详细描述。

### 详细结果和修复

要查看镜像的完整评估结果，请在 Docker Scout 仪表板中导航到镜像标签并打开 **Policy** 标签页。这显示了当前镜像所有策略违规的细分。

![详细的策略评估结果](../images/policy-detailed-results.webp)

此视图还提供了如何改善违规策略的策略状态的建议。

![标签视图中的策略详情](../images/policy-tag-view.webp)

对于与漏洞相关的策略，策略详情视图显示可消除漏洞的修复版本（如果有修复版本可用）。要修复问题，请将软件包版本升级到修复版本。

对于与许可证相关的策略，列表显示所有许可证不符合策略标准的软件包。要修复问题，请找到一种方法移除对违规软件包的依赖，例如寻找以更合适许可证分发的替代软件包。

## CLI

要从 CLI 查看镜像的策略状态，请使用 `docker scout policy` 命令。

```console
$ docker scout policy \
  --org dockerscoutpolicy \
  --platform linux/amd64 \
  dockerscoutpolicy/email-api-service:0.0.2

    ✓ Pulled
    ✓ Policy evaluation results found


​## Overview
​
​             │               Analyzed Image
​─────────────┼──────────────────────────────────────────────
​  Target     │  dockerscoutpolicy/email-api-service:0.0.2
​    digest   │  17b1fde0329c
​    platform │ linux/amd64
​
​
​## Policies
​
​Policy status  FAILED  (2/8 policies met, 3 missing data)
​
​  Status │                  Policy                             │           Results
​─────────┼─────────────────────────────────────────────────────┼──────────────────────────────
​  ✓      │ No copyleft licenses                                │    0 packages
​  !      │ Default non-root user                               │
​  !      │ No fixable critical or high vulnerabilities         │    2C     1H     0M     0L
​  ✓      │ No high-profile vulnerabilities                     │    0C     0H     0M     0L
​  ?      │ No outdated base images                             │    No data
​         │                                                     │    Learn more ↗
​  ?      │ SonarQube quality gates passed                      │    No data
​         │                                                     │    Learn more ↗
​  !      │ Supply chain attestations                           │    2 deviations
​  ?      │ No unapproved base images                           │    No data

...
```

有关该命令的更多信息，请参阅 [CLI 参考](/reference/cli/docker/scout/policy.md)。
