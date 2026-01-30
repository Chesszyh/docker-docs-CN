---
title: 查看 Docker Scout 策略状态
description: |
  Docker Scout 控制面板和 `docker scout policy` 命令允许您查看镜像的策略状态。
keywords: scout, 策略, 状态, 漏洞, 供应链, cves, 许可证
---

您可以从 [Docker Scout 控制面板](#dashboard) 或使用 [CLI](#cli) 跟踪制品的策略状态。

## 控制面板

[Docker Scout 控制面板](https://scout.docker.com/) 的 **Overview** (概览) 选项卡显示了仓库策略最近变化的摘要。此摘要显示了在最新镜像与之前镜像之间策略评估变化最大的镜像。

![策略概览](../images/policy-overview.webp)

### 每个仓库的策略状态

**Images** (镜像) 选项卡显示了所选环境中所有镜像的当前策略状态和最近的策略趋势。列表中的 **Policy status** (策略状态) 列显示：

- 已达标策略数量与总策略数量的对比
- 最近的策略趋势

![镜像列表中的策略状态](../images/policy-image-list.webp)

由方向箭头表示的策略趋势指示了镜像在策略方面与同一环境中的前一个镜像相比是变好、变差还是保持不变。

- 向上指的绿色箭头显示了在最后推送的镜像中变好的策略数量。
- 向下指的红色箭头显示了在最后推送的镜像中变差的策略数量。
- 双向灰色箭头显示了此镜像最新版本中保持不变的策略数量。

如果您选择一个仓库，可以打开 **Policy** 选项卡，查看最近分析的镜像及其前身之间策略增量的详细描述。

### 详细结果与修复

要查看镜像的完整评估结果，请在 Docker Scout 控制面板中导航到该镜像标签并打开 **Policy** 选项卡。这将显示当前镜像所有违反策略的情况。

![详细的策略评估结果](../images/policy-detailed-results.webp)

此视图还提供了关于如何改善违反策略项状态的建议。

![标签视图中的策略详情](../images/policy-tag-view.webp)

对于与漏洞相关的策略，当存在修复版本时，策略详情视图会显示消除该漏洞的修复版本。要解决此问题，请将软件包版本升级到修复版本。

对于与许可相关的策略，列表显示了所有许可证不符合策略标准的软件包。要解决此问题，请寻找移除对违规软件包依赖的方法，例如寻找在更合适许可证下分发的替代软件包。

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

```