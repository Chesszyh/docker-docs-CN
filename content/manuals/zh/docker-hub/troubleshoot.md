---
description: 了解如何排查常见的 Docker Hub 问题。
keywords: hub, troubleshoot
title: Docker Hub 故障排除
linkTitle: 故障排除
weight: 60
tags: [Troubleshooting]
toc_max: 2
---

如果您在使用 Docker Hub 时遇到问题，请参阅以下解决方案。

## 您已达到拉取速率限制（429 响应代码）

### 错误消息

当此问题发生时，您会在 Docker CLI 或 Docker Engine 日志中收到以下错误消息：

```text
You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits
```

### 可能的原因

- 作为已认证的 Docker Personal 用户，您已达到拉取速率限制。
- 作为未认证用户，基于您的 IPv4 地址或 IPv6 /64 子网，您已达到拉取速率限制。

### 解决方案

您可以使用以下解决方案之一：

- [认证](./usage/pulls.md#authentication)或[升级](../subscription/change.md#upgrade-your-subscription)您的 Docker 账户。
- [查看您的拉取速率限制](./usage/pulls.md#view-hourly-pull-rate-and-limit)，等待您的拉取速率限制降低，然后重试。

## 请求过多（429 响应代码）

### 错误消息

当此问题发生时，您会在 Docker CLI 或 Docker Engine 日志中收到以下错误消息：

```text
Too Many Requests
```

### 可能的原因

- 您已达到[滥用速率限制](./usage/_index.md#abuse-rate-limit)。

### 解决方案

1. 检查访问 Docker Hub 的损坏 CI/CD 管道并修复它们。
2. 在您的自动化脚本中实现带退避的重试解决方案，以确保您不会每分钟重新发送数千个请求。

## 500 响应代码

### 错误消息

当此问题发生时，以下错误消息在 Docker CLI 或 Docker Engine 日志中很常见：

```text
Unexpected status code 500
```

### 可能的原因

- Docker Hub 服务存在临时问题。

### 解决方案

1. 查看 [Docker 系统状态页面](https://www.dockerstatus.com/)并验证所有服务是否正常运行。
2. 尝试再次访问 Docker Hub。这可能是一个临时问题。
3. [联系 Docker 支持](https://www.docker.com/support/)报告问题。
