---
description: 使用 Prometheus 收集 Docker 指标
keywords: prometheus, metrics, 指标, 监控
title: 使用 Prometheus 收集 Docker 指标
alias:
  - /engine/admin/prometheus/
  - /config/thirdparty/monitoring/
  - /config/thirdparty/prometheus/
  - /config/daemon/prometheus/
---

[Prometheus](https://prometheus.io/) 是一个开源的系统监控和报警工具套件。您可以将 Docker 配置为一个 Prometheus 目标 (target)。

> [!WARNING]
>
> 可用的指标及这些指标的名称正处于活跃开发中，随时可能发生变化。

目前，您只能监控 Docker 本身。目前无法使用 Docker 目标监控您的应用程序。

## 示例

以下示例向您展示如何配置 Docker 守护进程，设置 Prometheus 在本地机器上以容器形式运行，并使用 Prometheus 监控您的 Docker 实例。

### 配置守护进程

要将 Docker 守护进程配置为 Prometheus 目标，您需要在 `daemon.json` 配置文件中指定 `metrics-address`。守护进程默认期望该文件位于以下位置之一。如果文件不存在，请创建它。

- **Linux**: /etc/docker/daemon.json
- **Windows Server**: C:\ProgramData\docker\config\daemon.json
- **Docker Desktop**: 打开 Docker Desktop 设置并选择 **Docker Engine** 来编辑文件。

添加以下配置：

```json
{
  "metrics-addr": "127.0.0.1:9323"
}
```

保存文件，如果是 Docker Desktop for Mac 或 Docker Desktop for Windows，请保存配置。重启 Docker。

Docker 现在通过回环接口在 9323 端口暴露兼容 Prometheus 的指标。您可以将其配置为使用通配符地址 `0.0.0.0` 代替，但这会将 Prometheus 端口暴露给更广泛的网络。在决定哪个选项最适合您的环境时，请仔细考虑您的威胁模型。

### 创建 Prometheus 配置

复制以下配置文件并将其保存到您选择的位置，例如 `/tmp/prometheus.yml`。这是一个标准的 Prometheus 配置文件，除了在文件末尾添加了 Docker 任务定义。

```yml
# 我的全局配置
global:
  scrape_interval: 15s # 将抓取间隔设置为每 15 秒。默认为每 1 分钟。
  evaluation_interval: 15s # 每 15 秒评估一次规则。默认为每 1 分钟。
  # scrape_timeout 设置为全局默认值 (10s)。

  # 在与外部系统 (联邦、远程存储、Alertmanager) 通信时，将这些标签附加到任何时间序列或警报。
  external_labels:
    monitor: "codelab-monitor"

# 加载规则一次，并根据全局 'evaluation_interval' 定期评估它们。
rule_files:
  # - "first.rules"
  # - "second.rules"

# 包含恰好一个要抓取的端点的抓取配置：
# 这里是 Prometheus 本身。
scrape_configs:
  # 任务名称作为标签 `job=<job_name>` 添加到从此配置中抓取的任何时间序列中。
  - job_name: prometheus

    # metrics_path 默认为 '/metrics'
    # scheme 默认为 'http'。

    static_configs:
      - targets: ["localhost:9090"]

  - job_name: docker
      # metrics_path 默认为 '/metrics'
      # scheme 默认为 'http'。

    static_configs:
      - targets: ["host.docker.internal:9323"]
```

### 在容器中运行 Prometheus

接下来，使用此配置启动一个 Prometheus 容器。

```console
$ docker run --name my-prometheus \
    --mount type=bind,source=/tmp/prometheus.yml,destination=/etc/prometheus/prometheus.yml \
    -p 9090:9090 \
    --add-host host.docker.internal=host-gateway \
    prom/prometheus
```

如果您使用的是 Docker Desktop，`--add-host` 标志是可选的。此标志确保主机的内部 IP 被暴露给 Prometheus 容器。Docker Desktop 默认会这样做。主机 IP 被暴露为 `host.docker.internal` 主机名。这与上一步中 `prometheus.yml` 中定义的配置相匹配。

### 打开 Prometheus 控制面板

验证 Docker 目标是否列在 `http://localhost:9090/targets/` 中。

![Prometheus 目标页面](images/prometheus-targets.webp)

> [!NOTE]
>
> 如果您使用 Docker Desktop，则无法直接访问此页面上的端点 URL。

### 使用 Prometheus

创建一个图表。在 Prometheus UI 中选择 **Graphs** 链接。从 **Execute** 按钮右侧的组合框中选择一个指标，然后点击 **Execute**。下面的截图显示了 `engine_daemon_network_actions_seconds_count` 的图表。

![空闲的 Prometheus 报告](images/prometheus-graph_idle.webp)

该图表显示了一个相当空闲的 Docker 实例，除非您的系统上已经在运行活跃的工作负载。

为了使图表更有趣，运行一个通过使用软件包管理器下载一些软件包来使用网络操作的容器：

```console
$ docker run --rm alpine apk add git make musl-dev go
```

等待几秒钟 (默认抓取间隔为 15 秒) 并重新加载您的图表。您应该看到图表中有一次上涨，显示了由您刚刚运行的容器引起的网络流量增加。

![显示流量的 Prometheus 报告](images/prometheus-graph_load.webp)

## 后续步骤

此处提供的示例展示了如何在本地系统上以容器形式运行 Prometheus。在实践中，您可能会在另一个系统上运行 Prometheus，或者作为某种云服务运行。您也可以在这些情况下将 Docker 守护进程设置为 Prometheus 目标。配置守护进程的 `metrics-addr`，并在您的 Prometheus 配置中将守护进程的地址添加为抓取端点。

```yaml
- job_name: docker
  static_configs:
    - targets: ["docker.daemon.example:<PORT>"]
```

有关 Prometheus 的更多信息，请参考 [Prometheus 文档](https://prometheus.io/docs/introduction/overview/)。
