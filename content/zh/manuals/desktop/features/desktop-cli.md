---
title: 使用 Docker Desktop CLI
linkTitle: Docker Desktop CLI
weight: 100
description: 如何使用 Docker Desktop CLI
keywords: cli, docker desktop, macos, windows, linux, 命令行
---

{{< summary-bar feature_name="Docker Desktop CLI" >}}

Docker Desktop CLI 允许您直接通过命令行执行关键操作，例如启动、停止、重新启动和更新 Docker Desktop。

Docker Desktop CLI 提供：

- **简化本地开发自动化**：在脚本和测试中更高效地执行 Docker Desktop 操作。
- **改善开发人员体验**：从命令行重新启动、退出或重置 Docker Desktop，减少对 Docker Desktop 控制面板的依赖，并提高灵活性和效率。

## 用法

```console
docker desktop COMMAND [OPTIONS]
```

## 命令

| 命令 | 说明 |
|:---------------------|:-----------------------------------------|
| `start`              | 启动 Docker Desktop |
| `stop`               | 停止 Docker Desktop |
| `restart`            | 重新启动 Docker Desktop |
| `status`             | 显示 Docker Desktop 正在运行还是已停止。 |
| `engine ls`          | 列出可用引擎（仅限 Windows） |
| `engine use`         | 在 Linux 和 Windows 容器之间切换（仅限 Windows） |
| `update`             | 管理 Docker Desktop 更新。Docker Desktop 4.38 版本仅限 Mac，4.39 及更高版本适用于所有操作系统。 |
| `logs`               | 打印日志条目 |
| `disable`            | 禁用某项功能 |
| `enable`             | 启用某项功能 | 
| `version`            | 显示 Docker Desktop CLI 插件版本信息 |
| `module`             | 管理 Docker Desktop 模块 |

有关各命令的更多详细信息，请参阅 [Docker Desktop CLI 参考](/reference/cli/docker/desktop/_index.md)。