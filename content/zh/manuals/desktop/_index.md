---
title: Docker Desktop
weight: 10
description: 探索 Docker Desktop，了解它的功能和关键特性。通过下载或查找其他资源迈出下一步。
keywords: how to use docker desktop, what is docker desktop used for, what does docker
  desktop do, using docker desktop, 如何使用 docker desktop, docker desktop 用途, docker desktop 功能, 使用 docker desktop
params:
  sidebar:
    group: Products
grid:
- title: 安装 Docker Desktop
  description: |
    在
    [Mac](/desktop/setup/install/mac-install/)、
    [Windows](/desktop/setup/install/windows-install/) 或
    [Linux](/desktop/setup/install/linux/) 上安装 Docker Desktop。
  icon: download
- title: 了解 Docker Desktop
  description: 浏览 Docker Desktop。
  icon: feature_search
  link: /desktop/use-desktop/
- title: 探索关键特性
  description: |
    查找有关 [Docker VMM](/desktop/features/vmm/)、[WSL](/desktop/features/wsl/)、[在 Kubernetes 上部署](/desktop/features/kubernetes/) 等信息。
  icon: category
- title: 查看发行说明
  description: 了解新功能、改进和错误修复。
  icon: note_add
  link: /desktop/release-notes/
- title: 浏览常见问题
  description: 探索常规问题或特定平台的问题。
  icon: help
  link: /desktop/troubleshoot-and-support/faqs/general/
- title: 提供反馈
  description: 提供有关 Docker Desktop 或 Docker Desktop 功能的反馈。
  icon: sms
  link: /desktop/troubleshoot-and-support/feedback/
aliases:
- /desktop/opensource/
- /docker-for-mac/dashboard/
- /docker-for-mac/opensource/
- /docker-for-windows/dashboard/
- /docker-for-windows/opensource/
---

Docker Desktop 是一款适用于 Mac、Linux 或 Windows 环境的一键安装应用程序，使您能够构建、共享和运行容器化应用程序和微服务。

它提供了一个直观的 GUI（图形用户界面），让您可以直接从计算机管理容器、应用程序和镜像。

Docker Desktop 减少了复杂设置所需的时间，因此您可以专注于编写代码。它处理端口映射、文件系统问题和其他默认设置，并定期更新错误修复和安全更新。

Docker Desktop 与您偏好的开发工具和语言集成，并通过 Docker Hub 让您访问庞大的可信镜像和模板生态系统。这使团队能够加速开发、自动化构建、启用 CI/CD 工作流程，并通过共享存储库安全地协作。

{{< tabs >}}
{{< tab name="Docker Desktop 包含什么？" >}}

- [Docker 引擎](/manuals/engine/_index.md)
- Docker CLI 客户端
- [Docker Scout](../scout/_index.md)
- [Docker Build](/manuals/build/_index.md)
- [Docker Compose](/manuals/compose/_index.md)
- [Ask Gordon](/manuals/ai/gordon/_index.md)
- [Docker Extensions](../extensions/_index.md)
- [Docker 内容信任](/manuals/engine/security/trust/_index.md)
- [Kubernetes](https://github.com/kubernetes/kubernetes/)
- [凭证助手](https://github.com/docker/docker-credential-helpers/)

{{< /tab >}}
{{< tab name="Docker Desktop 的关键特性是什么？">}}

* 能够将任何云平台上、使用多种语言和框架的任何应用程序容器化并共享。
* 快速安装和设置完整的 Docker 开发环境。
* 包含最新版本的 Kubernetes。
* 在 Windows 上，能够在 Linux 和 Windows 容器之间切换以构建应用程序。
* 通过原生 Windows Hyper-V 虚拟化实现快速可靠的性能。
* 能够在 Windows 机器上通过 WSL 2 原生在 Linux 上工作。
* 用于代码和数据的卷挂载，包括文件更改通知和对 localhost 网络上运行容器的轻松访问。

{{< /tab >}}
{{< /tabs >}}

{{< grid >}}