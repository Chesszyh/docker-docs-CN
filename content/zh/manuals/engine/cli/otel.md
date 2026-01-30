---
title: 适用于 Docker CLI 的 OpenTelemetry
description: 了解如何为 Docker 命令行捕获 OpenTelemetry 指标
keywords: otel, opentelemetry, telemetry, traces, tracing, metrics, logs, 遥测, 指标, 日志
---

{{< summary-bar feature_name="Docker CLI OpenTelemetry" >}}

Docker CLI 支持 [OpenTelemetry](https://opentelemetry.io/docs/) 埋点，用于发布有关命令调用的指标。此功能默认禁用。您可以配置 CLI 开始向您指定的端点发布指标。这允许您捕获有关 `docker` 命令调用的信息，从而更深入地了解您的 Docker 使用情况。

导出指标是可选的，您可以通过指定指标收集器的目标地址来控制数据的发送位置。

## 什么是 OpenTelemetry？

OpenTelemetry (简称 OTel) 是一个开放的可观测性框架，用于创建和管理遥测数据，如追踪 (traces)、指标 (metrics) 和日志 (logs)。OpenTelemetry 与供应商和工具无关，这意味着它可以与各种可观测性后端配合使用。

Docker CLI 对 OpenTelemetry 埋点的支持意味着 CLI 可以使用 Open Telemetry 规范中定义的协议和约定，发布有关发生的事件的信息。

## 工作原理

Docker CLI 默认不发布遥测数据。只有在您的系统上设置了环境变量后，Docker CLI 才会尝试向您指定的端点发布 OpenTelemetry 指标。

```bash
DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT=<endpoint>
```

该变量指定了 OpenTelemetry 收集器的端点，有关 `docker` CLI 调用的遥测数据应发送到该端点。为了捕获数据，您需要一个在该端点监听的 OpenTelemetry 收集器。

收集器的目的是接收遥测数据，对其进行处理，并将其导出到后端。后端是存储遥测数据的地方。您可以从许多不同的后端中进行选择，例如 Prometheus 或 InfluxDB。

一些后端提供了直接可视化指标的工具。或者，您也可以运行一个支持生成更有用图表的专用前端，例如 Grafana。

## 设置

要开始为 Docker CLI 捕获遥测数据，您需要：

- 设置 `DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT` 环境变量以指向 OpenTelemetry 收集器端点
- 运行一个接收来自 CLI 命令调用的信号的 OpenTelemetry 收集器
- 运行一个后端用于存储从收集器接收的数据

以下 Docker Compose 文件引导了一组服务以开始使用 OpenTelemetry。它包括一个 CLI 可以向其发送指标的 OpenTelemetry 收集器，以及一个从收集器抓取指标的 Prometheus 后端。

```yaml {collapse=true,title=compose.yaml}
name: cli-otel
services:
  prometheus:
    image: prom/prometheus
    command:
      - "--config.file=/etc/prometheus/prom.yml"
    ports:
      # 在 localhost:9091 发布 Prometheus 前端
      - 9091:9090
    restart: always
    volumes:
      # 将 Prometheus 数据存储在卷中：
      - prom_data:/prometheus
      # 挂载 prom.yml 配置文件
      - ./prom.yml:/etc/prometheus/prom.yml
  otelcol:
    image: otel/opentelemetry-collector
    restart: always
    depends_on:
      - prometheus
    ports:
      - 4317:4317
    volumes:
      # 挂载 otelcol.yml 配置文件
      - ./otelcol.yml:/etc/otelcol/config.yaml

volumes:
  prom_data:
```

该服务假设 `compose.yaml` 同级目录下存在以下两个配置文件：

- ```yaml {collapse=true,title=otelcol.yml}
  # 通过 gRPC 和 HTTP 接收信号
  receivers:
    otlp:
      protocols:
        grpc:
        http:

  # 建立一个供 Prometheus 抓取的端点
  exporters:
    prometheus:
      endpoint: "0.0.0.0:8889"

  service:
    pipelines:
      metrics:
        receivers: [otlp]
        exporters: [prometheus]
  ```

- ```yaml {collapse=true,title=prom.yml}
  # 配置 Prometheus 抓取 OpenTelemetry 收集器端点
  scrape_configs:
    - job_name: "otel-collector"
      scrape_interval: 1s
      static_configs:
        - targets: ["otelcol:8889"]
  ```

准备好这些文件后：

1. 启动 Docker Compose 服务：

   ```console
   $ docker compose up
   ```

2. 配置 Docker CLI 将遥测数据导出到 OpenTelemetry 收集器。

   ```console
   $ export DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
   ```

3. 运行一个 `docker` 命令来触发 CLI 向 OpenTelemetry 收集器发送指标信号。

   ```console
   $ docker version
   ```

4. 要查看由 CLI 创建的遥测指标，请访问 <http://localhost:9091/graph> 打开 Prometheus 表达式浏览器。

5. 在 **Query** (查询) 字段中输入 `command_time_milliseconds_total`，并执行查询以查看遥测数据。

## 可用指标

Docker CLI 目前导出一个单一指标 `command.time`，它以毫秒为单位测量命令的执行时长。该指标具有以下属性：

- `command.name`: 命令的名称
- `command.status.code`: 命令的退出代码
- `command.stderr.isatty`: 如果 stderr 连接到了 TTY 则为 true
- `command.stdin.isatty`: 如果 stdin 连接到了 TTY 则为 true
- `command.stdout.isatty`: 如果 stdout 连接到了 TTY 则为 true
