---
title: Docker Scout 健康评分
description: |
  Docker Scout 健康评分为 Docker Hub 镜像提供供应链评估，
  根据各种安全策略将其评级从 A 到 F。
keywords: scout, health scores, evaluation, checks, grades, docker hub
---

{{< summary-bar feature_name="Docker Scout health scores" >}}

Docker Scout 健康评分为 Docker Hub 上的镜像提供安全评估和整体供应链健康状况，帮助您确定镜像是否符合既定的安全最佳实践。评分范围从 A 到 F，其中 A 代表最高安全级别，F 代表最低级别，为您的镜像安全状况提供一目了然的视图。

只有属于拥有仓库的组织成员，并且至少对仓库具有"read"访问权限的用户才能查看健康评分。组织外部的用户或没有"read"访问权限的成员无法看到评分。

## 查看健康评分

{{< tabs >}}
{{< tab name="Docker Hub" >}}

在 Docker Hub 中查看镜像的健康评分：

1. 前往 Docker Hub 并登录。
2. 导航到您组织的页面。

在仓库列表中，您可以看到每个仓库基于最新推送标签的健康评分。

![仓库健康评分](../images/score-badges-repolist.png)

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

在 Docker Desktop 中查看镜像的健康评分：

1. 打开 Docker Desktop 并登录您的 Docker 账户。
2. 导航到 **Images** 视图并选择 **Hub** 标签页。

在仓库列表中，**Health** 列显示已推送到 Docker Hub 的不同标签的评分。

![仓库健康评分](../images/score-badges-dd.png)

{{< /tab >}}
{{< /tabs >}}

健康评分徽章使用颜色编码来指示仓库的整体健康状况：

- **绿色**：评分为 A 或 B。
- **黄色**：评分为 C。
- **橙色**：评分为 D。
- **红色**：评分为 E 或 F。
- **灰色**：`N/A` 评分。

评分也显示在给定仓库的 Docker Hub 页面上，以及对评分有贡献的每个策略。

![Scout "A" 健康评分](../images/score-a-shiny.png?w=450px)

## 评分系统

健康评分通过根据 Docker Scout [策略](./_index.md)评估镜像来确定。这些策略与软件供应链的最佳实践保持一致。

如果您的镜像仓库已经加入 Docker Scout，健康评分将根据为您的组织启用的策略自动计算。这还包括您配置的任何自定义策略。

如果您没有使用 Docker Scout，健康评分显示您的镜像与默认策略的合规性，这是 Docker 推荐的一套供应链规则，作为镜像的基础标准。您可以为您的组织启用 Docker Scout 并编辑策略配置，以根据您的特定策略获得更相关的健康评分。

### 评分过程

每个策略根据其[类型](/manuals/scout/policy/_index.md#policy-types)被分配一个分值。如果镜像符合策略，它将获得该策略类型的分值。镜像的健康评分根据获得的分数占总可能分数的百分比来计算。

1. 评估镜像的策略合规性。
2. 根据策略合规性授予分数。
3. 计算获得分数的百分比：

   ```text
   Percentage = (Points / Total) * 100
   ```

4. 根据获得分数的百分比分配最终评分，如下表所示：

   | 分数百分比（获得/总分）    | 评分 |
   | ---------------------------------------- | ----- |
   | 超过 90%                                 | A     |
   | 71% 到 90%                               | B     |
   | 51% 到 70%                               | C     |
   | 31% 到 50%                               | D     |
   | 11% 到 30%                               | E     |
   | 低于 10%                                 | F     |

### N/A 评分

镜像也可能被分配 `N/A` 评分，这可能发生在以下情况：

- 镜像大于 4GB（压缩大小）。
- 镜像架构不是 `linux/amd64` 或 `linux/arm64`。
- 镜像太旧，没有用于评估的新数据。

如果您看到 `N/A` 评分，请考虑以下事项：

- 如果镜像太大，尝试减小镜像大小。
- 如果镜像具有不支持的架构，为支持的架构重新构建镜像。
- 如果镜像太旧，推送新标签以触发新的评估。

### 策略权重

不同的策略类型具有不同的权重，这会影响评估期间分配给镜像的分数，如下表所示。

| 策略类型                                                                                  | 分数 |
| -------------------------------------------------------------------------------------------- | ------ |
| [Severity-Based Vulnerability](/manuals/scout/policy/_index.md#severity-based-vulnerability) | 20     |
| [High-Profile Vulnerabilities](/manuals/scout/policy/_index.md#high-profile-vulnerabilities) | 20     |
| [Supply Chain Attestations](/manuals/scout/policy/_index.md#supply-chain-attestations)       | 15     |
| [Approved Base Images](/manuals/scout/policy/_index.md#approved-base-images)                 | 15     |
| [Up-to-Date Base Images](/manuals/scout/policy/_index.md#up-to-date-base-images)             | 10     |
| [SonarQube Quality Gates](/manuals/scout/policy/_index.md#sonarqube-quality-gates) \*        | 10     |
| [Default Non-Root User](/manuals/scout/policy/_index.md#default-non-root-user)               | 5      |
| [Compliant Licenses](/manuals/scout/policy/_index.md#compliant-licenses)                     | 5      |

\* *此策略默认不启用，必须由用户配置。*

### 评估

健康评分是在启用该功能后为推送到 Docker Hub 的新镜像计算的。健康评分帮助您维护高安全标准，并确保您的应用程序构建在安全可靠的镜像上。

### 仓库评分

除了单个镜像评分（按标签或摘要），每个仓库还会根据最新推送的标签获得健康评分，提供仓库安全状态的整体视图。

### 示例

对于总可能分数为 100 分的镜像：

- 如果镜像仅偏离一个策略（价值 5 分），其分数将是 100 分中的 95 分。由于此分数高于第 90 百分位，镜像将获得 A 健康评分。
- 如果镜像不符合更多策略并获得 100 分中的 65 分，它将获得 C 健康评分，反映其较低的合规性。

## 提高您的健康评分

要提高镜像的健康评分，请采取措施确保镜像符合 Docker Scout 推荐的[策略](./_index.md)。

1. 前往 [Docker Scout 仪表板](https://scout.docker.com/)。
2. 使用您的 Docker ID 登录。
3. 前往[仓库设置](https://scout.docker.com/settings/repos)，为您的 Docker Hub 镜像仓库启用 Docker Scout。
4. 分析您仓库的[策略合规性](./_index.md)，并采取措施确保您的镜像符合策略。

由于策略的权重不同，优先考虑得分最高的策略，以对镜像的整体评分产生更大影响。
