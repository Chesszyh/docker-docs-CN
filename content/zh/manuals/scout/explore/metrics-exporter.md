---
title: Docker Scout 指标导出器
description: |
  了解如何使用 Prometheus 从 Docker Scout 抓取数据，以便使用 Grafana 创建您自己的漏洞和策略控制面板
keywords: scout, 导出器, prometheus, grafana, 指标, 控制面板, api, compose
---

Docker Scout 暴露了一个指标 HTTP 端点，允许您使用 Prometheus 或 Datadog 从 Docker Scout 抓取漏洞和策略数据。通过这种方式，您可以创建自己的自托管 Docker Scout 控制面板，用于可视化供应链指标。

## 指标

指标端点暴露了以下指标：

| 指标                            | 描述                                         | 标签                              | 类型  |
| ------------------------------- | -------------------------------------------- | --------------------------------- | ----- |
| `scout_stream_vulnerabilities`  | 数据流中的漏洞数                             | `streamName`, `severity`          | Gauge |
| `scout_policy_compliant_images` | 数据流中符合策略的镜像数                     | `id`, `displayName`, `streamName` | Gauge |
| `scout_policy_evaluated_images` | 数据流中根据策略评估的镜像总数               | `id`, `displayName`, `streamName` | Gauge |

> **Streams (数据流)**
>
> 在 Docker Scout 中，数据流概念是 [环境 (environments)](/manuals/scout/integrations/environment/_index.md) 的超集。
> 数据流包括您定义的所有运行时环境，以及特殊的 `latest-indexed` 流。
> `latest-indexed` 流包含每个仓库最近推送 (且分析过) 的标签。
>
> 数据流主要是一个 Docker Scout 的内部概念，但通过此指标端点公开的数据除外。
{ #stream }

## 创建访问令牌

要从您的组织导出指标，首先确保您的组织已注册到 Docker Scout。
然后，创建一个个人访问令牌 (PAT) —— 这是一个允许导出器通过 Docker Scout API 进行身份验证的秘密令牌。

PAT 不需要任何特定权限，但必须由作为 Docker 组织所有者的用户创建。
要创建 PAT，请按照 [创建访问令牌](/security/for-developers/access-tokens/#create-an-access-token) 中的步骤操作。

创建 PAT 后，请将其存储在安全的位置。在抓取指标时，您需要将此令牌提供给导出器。

## Prometheus

本节介绍如何使用 Prometheus 抓取指标端点。

### 为您的组织添加任务

在 Prometheus 配置文件中，为您的组织添加一个新任务。
该任务应包含以下配置；请将 `ORG` 替换为您的组织名称：

```yaml
scrape_configs:
  - job_name: <ORG>
    metrics_path: /v1/exporter/org/<ORG>/metrics
    scheme: https
    static_configs:
      - targets:
          - api.scout.docker.com
```

`targets` 字段中的地址设置为 Docker Scout API 的域名 `api.scout.docker.com`。
确保没有防火墙规则阻止服务器与该端点通信。

### 添加持票人令牌 (Bearer Token) 身份验证

要使用 Prometheus 从 Docker Scout 导出器端点抓取指标，您需要将 Prometheus 配置为使用 PAT 作为持票人令牌。
导出器要求在请求的 `Authorization` 标头中传递 PAT。

更新 Prometheus 配置文件以包含 `authorization` 配置块。
该块定义了存储在文件中的 PAT 作为持票人令牌：

```yaml
scrape_configs:
  - job_name: $ORG
    authorization:
      type: Bearer
      credentials_file: /etc/prometheus/token
```

文件的内容应为纯文本格式的 PAT：

```console
dckr_pat_...
```

如果您在 Docker 容器或 Kubernetes Pod 中运行 Prometheus，请使用卷 (volume) 或机密 (secret) 将该文件挂载到容器中。

最后，重启 Prometheus 以应用更改。

### Prometheus 示例项目

如果您没有设置 Prometheus 服务器，可以使用 Docker Compose 运行一个 [示例项目](https://github.com/dockersamples/scout-metrics-exporter)。
该示例包括一个抓取已注册到 Docker Scout 的 Docker 组织指标的 Prometheus 服务器，
以及一个带有预配置控制面板的 Grafana，用于可视化漏洞和策略指标。

1. 克隆用于引导一组 Compose 服务以抓取和可视化 Docker Scout 指标端点的入门模板：

   ```console
   $ git clone git@github.com:dockersamples/scout-metrics-exporter.git
   $ cd scout-metrics-exporter/prometheus
   ```

2. [创建一个 Docker 访问令牌](/security/for-developers/access-tokens/#create-an-access-token)
   并将其存储在模板目录下 `/prometheus/prometheus/token` 的纯文本文件中。

   ```plaintext {title=token}
   $ echo $DOCKER_PAT > ./prometheus/token
   ```

3. 在 `/prometheus/prometheus/prometheus.yml` 的 Prometheus 配置文件中，
   将第 6 行 `metrics_path` 属性中的 `ORG` 替换为您 Docker 组织的命名空间。

   ```yaml {title="prometheus/prometheus.yml",hl_lines="6",linenos=1}
   global:
     scrape_interval: 60s
     scrape_timeout: 40s
   scrape_configs:
     - job_name: Docker Scout policy
       metrics_path: /v1/exporter/org/<ORG>/metrics
       scheme: https
       static_configs:
         - targets:
             - api.scout.docker.com
       authorization:
         type: Bearer
         credentials_file: /etc/prometheus/token
   ```

4. 启动 compose 服务。

   ```console
   docker compose up -d
   ```

   此命令启动两个服务：Prometheus 服务器和 Grafana。
   Prometheus 从 Docker Scout 端点抓取指标，Grafana 使用预配置的控制面板可视化指标。

要停止演示并清理创建的所有资源，请运行：

```console
docker compose down -v
```

### 访问 Prometheus

启动服务后，您可以通过访问 <http://localhost:9090> 访问 Prometheus 表达式浏览器。
Prometheus 服务器在 Docker 容器中运行，可通过 9090 端口访问。

几秒钟后，您应该在 Prometheus UI 的 <http://localhost:9090/targets> 中看到指标端点作为一个目标。

![Docker Scout 指标导出器 Prometheus 目标](../images/scout-metrics-prom-target.png "Docker Scout 指标导出器 Prometheus 目标")

### 在 Grafana 中查看指标

要查看 Grafana 控制面板，请访问 <http://localhost:3000/dashboards>，
并使用 Docker Compose 文件中定义的凭据登录 (用户名：`admin`，密码：`grafana`)。

![Grafana 中的漏洞控制面板](../images/scout-metrics-grafana-vulns.png "Grafana 中的漏洞控制面板")

![Grafana 中的策略控制面板](../images/scout-metrics-grafana-policy.png "Grafana 中的策略控制面板")

控制面板已预先配置，用于可视化由 Prometheus 抓取的漏洞和策略指标。

## Datadog

本节介绍如何使用 Datadog 抓取指标端点。
Datadog 通过运行一个可自定义的 [代理 (agent)](https://docs.datadoghq.com/agent/?tab=Linux) 来拉取数据进行监控，
该代理会抓取任何暴露指标的可用端点。OpenMetrics 和 Prometheus 检查已包含在代理中，因此您无需在容器或宿主机上安装任何其他软件。

本指南假设您拥有 Datadog 帐户和 Datadog API 密钥。有关入门信息，请参阅 [Datadog 文档](https://docs.datadoghq.com/agent)。

### 配置 Datadog 代理

要开始收集指标，您需要编辑代理用于 OpenMetrics 检查的配置文件。如果您将代理作为容器运行，该文件必须挂载在 `/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml`。

以下示例显示了一个 Datadog 配置，它：

- 指定面向 `dockerscoutpolicy` Docker 组织的 OpenMetrics 端点
- 一个 `namespace`，所有收集的指标都将带此前缀
- 您希望代理抓取的 [`指标 (metrics)`](#metrics) (`scout_*`)
- 一个 `auth_token` 部分，用于 Datadog 代理使用 Docker PAT 作为持票人令牌向指标端点进行身份验证。

```yaml
instances:
  - openmetrics_endpoint: "https://api.scout.docker.com/v1/exporter/org/dockerscoutpolicy/metrics"
    namespace: "scout-metrics-exporter"
    metrics:
      - scout_*
    auth_token:
      reader:
        type: file
        path: /var/run/secrets/scout-metrics-exporter/token
      writer:
        type: header
        name: Authorization
        value: Bearer <TOKEN>
```

> [!IMPORTANT]
>
> 请勿替换上述配置示例中的 `<TOKEN>` 占位符。它必须保持原样。只需确保 Docker PAT 已正确挂载到 Datadog 代理指定的系统路径中即可。将文件保存为 `conf.yaml` 并重启代理。

在创建您自己的 Datadog 代理配置时，请务必通过将 `dockerscoutpolicy` 替换为您 Docker 组织的命名空间来编辑 `openmetrics_endpoint` 属性以指向您的组织。

### Datadog 示例项目

如果您没有设置 Datadog 服务器，可以使用 Docker Compose 运行一个 [示例项目](https://github.com/dockersamples/scout-metrics-exporter)。
该示例包含一个作为容器运行的 Datadog 代理，它抓取已注册到 Docker Scout 的 Docker 组织指标。此示例项目假设您拥有 Datadog 帐户、API 密钥和 Datadog 站点。

1. 克隆用于引导 Datadog Compose 服务以抓取 Docker Scout 指标端点的入门模板：

   ```console
   $ git clone git@github.com:dockersamples/scout-metrics-exporter.git
   $ cd scout-metrics-exporter/datadog
   ```

2. [创建一个 Docker 访问令牌](/security/for-developers/access-tokens/#create-an-access-token)
   并将其存储在模板目录下 `/datadog/token` 的纯文本文件中。

   ```plaintext {title=token}
   $ echo $DOCKER_PAT > ./token
   ```

3. 在 `/datadog/compose.yaml` 文件中，使用您 Datadog 部署的值更新 `DD_API_KEY` 和 `DD_SITE` 环境变量。

   ```yaml {hl_lines="5-6"}
     datadog-agent:
       container_name: datadog-agent
       image: gcr.io/datadoghq/agent:7
       environment:
         - DD_API_KEY=${DD_API_KEY} # 例如 1b6b3a42...
         - DD_SITE=${DD_SITE} # 例如 datadoghq.com
         - DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock:ro
         - ./conf.yaml:/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml:ro
         - ./token:/var/run/secrets/scout-metrics-exporter/token:ro
   ```

   `volumes` 部分将主机的 Docker 套接字挂载到容器中。当作为容器运行时，这是获得准确主机名所必需的 ([更多详情见此](https://docs.datadoghq.com/agent/troubleshooting/hostname_containers/))。

   它还挂载了代理的配置文件和 Docker 访问令牌。

4. 编辑 `/datadog/config.yaml` 文件，将 `openmetrics_endpoint` 属性中的占位符 `<ORG>` 替换为您要收集其指标的 Docker 组织的命名空间。

   ```yaml {hl_lines=2}
   instances:
     - openmetrics_endpoint: "https://api.scout.docker.com/v1/exporter/org/<<ORG>>/metrics"
       namespace: "scout-metrics-exporter"
   # ...
   ```

5. 启动 Compose 服务。

   ```console
   docker compose up -d
   ```

如果配置正确，当您运行代理的状态命令时，您应该在 Running Checks 下看到 OpenMetrics 检查，其输出应类似于：

```text
openmetrics (4.2.0)
-------------------
  Instance ID: openmetrics:scout-prometheus-exporter:6393910f4d92f7c2 [OK]
  Configuration Source: file:/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml
  Total Runs: 1
  Metric Samples: Last Run: 236, Total: 236
  Events: Last Run: 0, Total: 0
  Service Checks: Last Run: 1, Total: 1
  Average Execution Time : 2.537s
  Last Execution Date : 2024-05-08 10:41:07 UTC (1715164867000)
  Last Successful Execution Date : 2024-05-08 10:41:07 UTC (1715164867000)
```

有关完整的选项列表，请查看此通用 OpenMetrics 检查的 [示例配置文件](https://github.com/DataDog/integrations-core/blob/master/openmetrics/datadog_checks/openmetrics/data/conf.yaml.example)。

### 可视化您的数据

一旦代理配置为抓取 Prometheus 指标，您就可以使用它们来构建全面的 Datadog 图表、控制面板和警报。

进入您的 [指标摘要页面](https://app.datadoghq.com/metric/summary?filter=scout_prometheus_exporter)
以查看从此示例收集的指标。此配置将收集 `scout_metrics_exporter` 命名空间下所有以 `scout_` 开头的暴露指标。

![datadog_metrics_summary](../images/datadog_metrics_summary.png)

以下屏幕截图显示了 Datadog 控制面板的示例，其中包含有关特定 [数据流 (stream)](#stream) 的漏洞和策略合规性的图表。

![datadog_dashboard_1](../images/datadog_dashboard_1.png)
![datadog_dashboard_2](../images/datadog_dashboard_2.png)

> 图表中的线条看起来很平的原因在于漏洞自身的性质 (它们不会经常变化) 以及日期选择器中选择的时间间隔较短。

## 抓取间隔 (Scrape interval)

默认情况下，Prometheus 和 Datadog 以 15 秒的间隔抓取指标。
由于漏洞数据的自身性质，通过此 API 公开的指标不太可能以高频率发生变化。
出于这个原因，指标端点默认有 60 分钟的缓存，这意味着建议抓取间隔为 60 分钟或更长。
如果您将抓取间隔设置为小于 60 分钟，您将在该时间窗口内的多次抓取中看到指标中的相同数据。

更改抓取间隔：

- Prometheus：在 Prometheus 配置文件的全局或任务级别设置 `scrape_interval` 字段。
- Datadog：在 Datadog 代理配置文件中设置 `min_collection_interval` 属性，请参阅 [Datadog 文档](https://docs.datadoghq.com/developers/custom_checks/write_agent_check/#updating-the-collection-interval)。

## 撤销访问令牌

如果您怀疑您的 PAT 已泄露或不再需要，您可以随时撤销它。
要撤销 PAT，请按照 [创建和管理访问令牌](/security/for-developers/access-tokens/#modify-existing-tokens) 中的步骤操作。

撤销 PAT 会立即使该令牌失效，并防止 Prometheus 使用该令牌抓取指标。您将需要创建一个新的 PAT 并更新 Prometheus 配置以使用新令牌。
