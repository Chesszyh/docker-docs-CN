---
title: OpenTelemetry 支持
description: 分析构建的遥测数据
keywords: build, buildx buildkit, opentelemetry
aliases:
- /build/building/opentelemetry/
---

Buildx 和 BuildKit 都支持 [OpenTelemetry](https://opentelemetry.io/)。

要将跟踪捕获到 [Jaeger](https://github.com/jaegertracing/jaeger)，请使用 `driver-opt` 将 `JAEGER_TRACE` 环境变量设置为收集地址。

首先创建一个 Jaeger 容器：

```console
$ docker run -d --name jaeger -p "6831:6831/udp" -p "16686:16686" --restart unless-stopped jaegertracing/all-in-one
```

然后[创建一个 `docker-container` 构建器](/manuals/build/builders/drivers/docker-container.md)，通过 `JAEGER_TRACE` 环境变量使用 Jaeger 实例：

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "network=host" \
  --driver-opt "env.JAEGER_TRACE=localhost:6831"
```

启动并[检查 `mybuilder`](/reference/cli/docker/buildx/inspect.md)：

```console
$ docker buildx inspect --bootstrap
```

Buildx 命令应在 `http://127.0.0.1:16686/` 被跟踪：

![OpenTelemetry Buildx Bake](../images/opentelemetry.png)
