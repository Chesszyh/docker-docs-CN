---
title: 调试 Docker Hardened Image 容器
linkTitle: 调试容器
weight: 60
keywords: debug, hardened images, DHI, troubleshooting, ephemeral container, docker debug
description: 了解如何使用 Docker Debug 在本地或生产环境中对 Docker Hardened Images（DHI）进行故障排除。
keywords: docker debug, ephemeral container, non-root containers, hardened container image, debug secure container
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

Docker Hardened Images（DHI）优先考虑最小化和安全性，这意味着它们有意省略了许多常见的调试工具（如 shell 或包管理器）。这使得直接故障排除变得困难，同时不会引入风险。为了解决这个问题，您可以使用 [Docker Debug](../../../reference/cli/docker/debug.md)，这是一个安全的工作流，可以临时将一个临时调试容器附加到正在运行的服务或镜像，而无需修改原始镜像。

本指南展示了如何在开发过程中在本地调试 Docker Hardened Images。您也可以使用 `--host` 选项远程调试容器。

以下示例使用已镜像的 `dhi-python:3.13` 镜像，但相同的步骤适用于任何镜像。

## 步骤 1：从 Hardened Image 运行容器

从基于 DHI 的容器开始，模拟一个问题：

```console
$ docker run -d --name myapp <YOUR_ORG>/dhi-python:3.13 python -c "import time; time.sleep(300)"
```

此容器不包含 shell 或 `ps`、`top` 或 `cat` 等工具。

如果您尝试：

```console
$ docker exec -it myapp sh
```

您将看到：

```console
exec: "sh": executable file not found in $PATH
```

## 步骤 2：使用 Docker Debug 检查容器

使用 `docker debug` 命令将临时的、功能丰富的调试容器附加到正在运行的实例。

```console
$ docker debug myapp
```

从这里，您可以检查正在运行的进程、网络状态或挂载的文件。

例如，检查正在运行的进程：

```console
$ ps aux
```

使用以下命令退出调试会话：

```console
$ exit
```

## 接下来

Docker Debug 帮助您对加固容器进行故障排除，而不会影响原始镜像的完整性。由于调试容器是临时的且独立的，它避免了向生产环境引入安全风险。

如果您遇到与权限、端口、缺少 shell 或包管理器相关的问题，请参阅[Docker Hardened Images 故障排除](../troubleshoot.md)以获取推荐的解决方案和变通方法。
