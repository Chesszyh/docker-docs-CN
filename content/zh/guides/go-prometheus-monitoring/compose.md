---
title: 使用 Docker Compose 连接服务
linkTitle: 使用 Docker Compose 连接服务
weight: 30 #
keywords: go, golang, prometheus, grafana, containerize, monitor
description: 了解如何使用 Docker Compose 连接服务，以便使用 Prometheus 和 Grafana 监控 Golang 应用程序。
---

现在你已经容器化了 Golang 应用程序，你将使用 Docker Compose 连接你的服务。你将连接 Golang 应用程序、Prometheus 和 Grafana 服务，以便使用 Prometheus 和 Grafana 监控 Golang 应用程序。

## 创建 Docker Compose 文件

在 Golang 应用程序的根目录中创建一个名为 `compose.yml` 的新文件。Docker Compose 文件包含运行多个服务并将它们连接在一起的指令。

这是一个使用 Golang、Prometheus 和 Grafana 的项目的 Docker Compose 文件。你也可以在 `go-prometheus-monitoring` 目录中找到此文件。

```yaml
services:
  api:
    container_name: go-api
    build:
      context: .
      dockerfile: Dockerfile
    image: go-api:latest
    ports:
      - 8000:8000
    networks:
      - go-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
    develop:
      watch:
        - path: .
          action: rebuild
      
  prometheus:
    container_name: prometheus
    image: prom/prometheus:v2.55.0
    volumes:
      - ./Docker/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
    networks:
      - go-network
  
  grafana:
    container_name: grafana
    image: grafana/grafana:11.3.0
    volumes:
      - ./Docker/grafana.yml:/etc/grafana/provisioning/datasources/datasource.yaml
      - grafana-data:/var/lib/grafana
    ports:
      - 3000:3000
    networks:
      - go-network
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=password

volumes:
  grafana-data:

networks:
  go-network:
    driver: bridge
```

## 了解 Docker Compose 文件

Docker Compose 文件包含三个服务：

- **Golang 应用程序服务**：此服务使用 Dockerfile 构建 Golang 应用程序并在容器中运行它。它公开应用程序的端口 `8000` 并连接到 `go-network` 网络。它还定义了一个健康检查来监控应用程序的运行状况。你还使用了 `healthcheck` 来监控应用程序的健康状况。健康检查每 30 秒运行一次，如果健康检查失败，则重试 5 次。健康检查使用 `curl` 命令检查应用程序的 `/health` 端点。除了健康检查之外，你还添加了一个 `develop` 部分来监视应用程序源代码的更改，并使用 Docker Compose Watch 功能重建应用程序。

- **Prometheus 服务**：此服务在容器中运行 Prometheus 服务器。它使用官方 Prometheus 镜像 `prom/prometheus:v2.55.0`。它在端口 `9090` 上公开 Prometheus 服务器，并连接到 `go-network` 网络。你还挂载了 `Docker` 目录中的 `prometheus.yml` 文件，该文件位于项目的根目录中。`prometheus.yml` 文件包含从 Golang 应用程序抓取指标的 Prometheus 配置。这就是你将 Prometheus 服务器连接到 Golang 应用程序的方式。

    ```yaml
    global:
      scrape_interval: 10s
      evaluation_interval: 10s

    scrape_configs:
      - job_name: myapp
        static_configs:
          - targets: ["api:8000"]
    ```

    在 `prometheus.yml` 文件中，你定义了一个名为 `myapp` 的作业来从 Golang 应用程序抓取指标。`targets` 字段指定要从中抓取指标的目标。在这种情况下，目标是在端口 `8000` 上运行的 Golang 应用程序。`api` 是 Docker Compose 文件中 Golang 应用程序的服务名称。Prometheus 服务器将每 10 秒从 Golang 应用程序抓取一次指标。

- **Grafana 服务**：此服务在容器中运行 Grafana 服务器。它使用官方 Grafana 镜像 `grafana/grafana:11.3.0`。它在端口 `3000` 上公开 Grafana 服务器，并连接到 `go-network` 网络。你还挂载了 `Docker` 目录中的 `grafana.yml` 文件，该文件位于项目的根目录中。`grafana.yml` 文件包含添加 Prometheus 数据源的 Grafana 配置。这就是你将 Grafana 服务器连接到 Prometheus 服务器的方式。在环境变量中，你设置了 Grafana 管理员用户和密码，这将用于登录 Grafana 仪表板。

    ```yaml
    apiVersion: 1
    datasources:
    - name: Prometheus (Main)
      type: prometheus
      url: http://prometheus:9090
      isDefault: true
    ```
      
    在 `grafana.yml` 文件中，你定义了一个名为 `Prometheus (Main)` 的 Prometheus 数据源。`type` 字段指定数据源的类型，即 `prometheus`。`url` 字段指定要从中获取指标的 Prometheus 服务器的 URL。在这种情况下，URL 是 `http://prometheus:9090`。`prometheus` 是 Docker Compose 文件中 Prometheus 服务器的服务名称。`isDefault` 字段指定数据源是否为 Grafana 中的默认数据源。

除了服务之外，Docker Compose 文件还定义了一个名为 `grafana-data` 的卷来持久化 Grafana 数据，以及一个名为 `go-network` 的网络来将服务连接在一起。你创建了一个自定义网络 `go-network` 来连接这些服务。`driver: bridge` 字段指定用于网络的网络驱动程序。

## 构建并运行服务

现在你有了 Docker Compose 文件，你可以构建服务并使用 Docker Compose 一起运行它们。

要构建并运行服务，请在终端中运行以下命令：

```console
$ docker compose up
```

`docker compose up` 命令构建 Docker Compose 文件中定义的服务并将它们一起运行。你将在终端中看到类似的输出：

```console
 ✔ Network go-prometheus-monitoring_go-network  Created                                                           0.0s 
 ✔ Container grafana                            Created                                                           0.3s 
 ✔ Container go-api                             Created                                                           0.2s 
 ✔ Container prometheus                         Created                                                           0.3s 
Attaching to go-api, grafana, prometheus
go-api      | [GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.
go-api      | 
go-api      | [GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
go-api      |  - using env:     export GIN_MODE=release
go-api      |  - using code:    gin.SetMode(gin.ReleaseMode)
go-api      | 
go-api      | [GIN-debug] GET    /metrics                  --> main.PrometheusHandler.func1 (3 handlers)
go-api      | [GIN-debug] GET    /health                   --> main.main.func1 (4 handlers)
go-api      | [GIN-debug] GET    /v1/users                 --> main.main.func2 (4 handlers)
go-api      | [GIN-debug] [WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.
go-api      | Please check https://pkg.go.dev/github.com/gin-gonic/gin#readme-don-t-trust-all-proxies for details.
go-api      | [GIN-debug] Listening and serving HTTP on :8000
prometheus  | ts=2025-03-15T05:57:06.676Z caller=main.go:627 level=info msg="No time or size retention was set so using the default time retention" duration=15d
prometheus  | ts=2025-03-15T05:57:06.678Z caller=main.go:671 level=info msg="Starting Prometheus Server" mode=server version="(version=2.55.0, branch=HEAD, revision=91d80252c3e528728b0f88d254dd720f6be07cb8)"
grafana     | logger=settings t=2025-03-15T05:57:06.865335506Z level=info msg="Config overridden from command line" arg="default.log.mode=console"
grafana     | logger=settings t=2025-03-15T05:57:06.865337131Z level=info msg="Config overridden from Environment variable" var="GF_PATHS_DATA=/var/lib/grafana"
grafana     | logger=ngalert.state.manager t=2025-03-15T05:57:07.088956839Z level=info msg="State
.
.
grafana     | logger=plugin.angulardetectorsprovider.dynamic t=2025-03-15T05:57:07.530317298Z level=info msg="Patterns update finished" duration=440.489125ms
```

服务将开始运行，你可以通过 `http://localhost:8000` 访问 Golang 应用程序，通过 `http://localhost:9090/health` 访问 Prometheus，通过 `http://localhost:3000` 访问 Grafana。你也可以使用 `docker ps` 命令检查正在运行的容器。

```console
$ docker ps
```

## 总结

在本节中，你学习了如何使用 Docker Compose 连接服务。你创建了一个 Docker Compose 文件来同时运行多个服务并使用网络将它们连接起来。你还学习了如何使用 Docker Compose 构建并运行服务。

相关信息：

 - [Docker Compose 概览](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)

接下来，你将学习如何使用 Docker Compose 开发 Golang 应用程序，并使用 Prometheus 和 Grafana 对其进行监控。

## 后续步骤

在下一节中，你将学习如何使用 Docker 开发 Golang 应用程序。你还将学习如何使用 Docker Compose Watch 在更改代码时重新构建镜像。最后，你将测试应用程序并使用 Prometheus 作为数据源在 Grafana 中可视化指标。
