---
title: 使用 Docker Desktop CLI
linkTitle: Docker Desktop CLI
weight: 100
description: 如何使用 Docker Desktop CLI
keywords: cli, docker desktop, macos, windows, linux
---

{{< summary-bar feature_name="Docker Desktop CLI" >}}

Docker Desktop CLI 允许您直接从命令行执行关键操作，例如启动、停止、重启和更新 Docker Desktop。

Docker Desktop CLI 提供：

- 简化本地开发的自动化：在脚本和测试中更高效地执行 Docker Desktop 操作。
- 改进的开发者体验：从命令行重启、退出或重置 Docker Desktop，减少对 Docker Desktop Dashboard 的依赖，提高灵活性和效率。

## 用法

```console
docker desktop COMMAND [OPTIONS]
```

## 命令

| 命令              | 描述                              |
|:---------------------|:-----------------------------------------|
| `start`              | 启动 Docker Desktop                    |
| `stop`               | 停止 Docker Desktop                     |
| `restart`            | 重启 Docker Desktop                  |
| `status`             | 显示 Docker Desktop 是正在运行还是已停止。       |
| `engine ls`          | 列出可用的引擎（仅限 Windows）   |
| `engine use`         | 在 Linux 和 Windows 容器之间切换（仅限 Windows） |
| `update`             | 管理 Docker Desktop 更新。仅适用于 Mac 上的 Docker Desktop 4.38 版本，或 Docker Desktop 4.39 及更高版本的所有操作系统。 |
| `logs`               | 打印日志条目                        |
| `disable`            | 禁用功能                        |
| `enable`             | 启用功能                         |
| `version`            | 显示 Docker Desktop CLI 插件版本信息 |
| `module`             | 管理 Docker Desktop 模块 |

有关每个命令的更多详细信息，请参阅 [Docker Desktop CLI 参考](/reference/cli/docker/desktop/_index.md)。
