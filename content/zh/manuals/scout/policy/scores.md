---
title: Docker Scout 健康评分
description: |
  Docker Scout 健康评分通过各种安全策略对 Docker Hub 镜像进行评估，分级从 A 到 F。
keywords: scout, 健康评分, 评估, 检查, 等级, docker hub
---

{{< summary-bar feature_name="Docker Scout health scores" >}}

Docker Scout 健康评分对 Docker Hub 上的镜像提供安全评估和整体供应链健康状况分析，帮助您确定镜像是否符合既定的安全最佳实践。评分范围从 A 到 F，其中 A 代表最高安全级别，F 代表最低，让您能够一目了然地查看镜像的安全状况。

只有作为拥有该仓库的组织成员，且至少具有该仓库“读取”权限的用户才能查看健康评分。组织外部的用户或没有“读取”权限的成员无法看到该评分。

## 查看健康评分

{{< tabs >}}
{{< tab name="Docker Hub" >}}

要在 Docker Hub 中查看镜像的健康评分：

1. 前往 Docker Hub 并登录。
2. 导航到您组织的页面。

在仓库列表中，您可以看到每个仓库基于最近推送标签的健康评分。

![仓库健康评分](../images/score-badges-repolist.png)

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

要在 Docker Desktop 中查看镜像的健康评分：

1. 打开 Docker Desktop 并登录您的 Docker 帐户。
2. 导航到 **Images** 视图并选择 **Hub** 选项卡。

在仓库列表中，**Health** 列显示了已推送到 Docker Hub 的不同标签的评分。

![仓库健康评分](../images/score-badges-dd.png)

{{< /tab >}}
{{< /tabs >}}

健康评分徽章通过颜色编码来指示仓库的整体健康状况：

- **绿色**：A 或 B 评分。
- **黄色**：C 评分。
- **橙色**：D 评分。
- **红色**：E 或 F 评分。
- **灰色**：`N/A` (不适用) 评分。

评分也会显示在给定仓库的 Docker Hub 页面上，同时列出对该评分有贡献的各项策略。

![Scout "A" 健康评分](../images/score-a-shiny.png?w=450px)

## 评分系统

健康评分通过根据 Docker Scout [策略](./_index.md) 对镜像进行评估来确定。这些策略符合软件供应链的最佳实践。

如果您的镜像仓库已经注册了 Docker Scout，系统会根据为您组织启用的策略自动计算健康评分。这还包括您配置的任何自定义策略。

如果您没有使用 Docker Scout，健康评分将显示您的镜像对默认策略的合规性，这些默认策略是 Docker 推荐的一组作为镜像基础标准的供应链规则。您可以为您组织启用 Docker Scout 并编辑策略配置，以根据您的特定策略获得更相关的健康评分。

### 评分过程

每项策略根据其 [类型](/manuals/scout/policy/_index.md#policy-types) 被分配一个分值。如果镜像符合某项策略，它将获得该策略类型的分值。镜像的健康评分是根据相对于总可能分值的得分百分比计算的。

1. 评估镜像的策略合规性。
2. 根据对策略的合规情况授予分数。
3. 计算得分百分比：

   ```text
   百分比 = (得分 / 总分) * 100
   ```

4. 根据得分百分比分配最终分数，如下表所示：

   | 得分百分比 (占总分的比例) | 评分 |
   | ------------------------- | ---- |
   | 大于 90%                  | A    |
   | 71% 到 90%                | B    |
   | 51% 到 70%                | C    |
   | 31% 到 50%                | D    |
   | 11% 到 30%                | E    |
   | 小于 10%                  | F    |

### N/A 评分

镜像也可能被分配 `N/A` 评分，这可能发生在以下情况：

- 镜像大于 4GB (压缩后的大小)。
- 镜像架构不是 `linux/amd64` 或 `linux/arm64`。
- 镜像太旧，没有用于评估的新鲜数据。

如果您看到 `N/A` 评分，请考虑以下建议：

- 如果镜像太大，尝试减小镜像大小。
- 如果镜像架构不受支持，针对受支持的架构重新构建镜像。
- 如果镜像太旧，推送一个新标签以触发新的评估。

### 策略权重

不同的策略类型带有不同的权重，这会影响评估期间分配给镜像的分数，如下表所示。

| 策略类型                                                                                     | 分值 |
| -------------------------------------------------------------------------------------------- | ---- |
| [Severity-Based Vulnerability](/manuals/scout/policy/_index.md#severity-based-vulnerability) | 20   |
| [High-Profile Vulnerabilities](/manuals/scout/policy/_index.md#high-profile-vulnerabilities) | 20   |
| [Supply Chain Attestations](/manuals/scout/policy/_index.md#supply-chain-attestations)       | 15   |
| [Approved Base Images](/manuals/scout/policy/_index.md#approved-base-images)                 | 15   |
| [Up-to-Date Base Images](/manuals/scout/policy/_index.md#up-to-date-base-images)             | 10   |
| [SonarQube Quality Gates](/manuals/scout/policy/_index.md#sonarqube-quality-gates) \*        | 10   |
| [Default Non-Root User](/manuals/scout/policy/_index.md#default-non-root-user)               | 5    |
| [Compliant Licenses](/manuals/scout/policy/_index.md#compliant-licenses)                     | 5    |

\* _此策略默认不启用，必须由用户配置。_

### 评估

健康评分是针对功能启用后推送到 Docker Hub 的新镜像计算的。健康评分可帮助您维持高安全标准，并确保您的应用程序构建在安全可靠的镜像之上。

### 仓库评分

除了单个镜像评分 (按标签或摘要) 之外，每个仓库还会根据最近推送的标签获得一个健康评分，从而提供仓库安全状况的整体视图。

### 示例

对于总可能得分为 100 分的镜像：

- 如果镜像仅违反了一项价值 5 分的策略，其得分为 100 分中的 95 分。由于该分数高于 90%，镜像将获得 A 健康评分。
- 如果镜像不符合更多策略，得分为 100 分中的 65 分，它将获得 C 健康评分，反映出其合规性较低。

## 提高您的健康评分

要提高镜像的健康评分，请采取措施确保镜像符合 Docker Scout 推荐的 [策略](./_index.md)。

1. 前往 [Docker Scout 控制面板](https://scout.docker.com/)。
2. 使用您的 Docker ID 登录。
3. 转到 [Repository settings](https://scout.docker.com/settings/repos) 并为您的 Docker Hub 镜像仓库启用 Docker Scout。
4. 分析您仓库的 [策略合规情况](./_index.md)，并采取行动确保您的镜像符合策略。

由于策略的权重不同，请优先处理得分最高的策略，以对镜像的整体评分产生更大的影响。
