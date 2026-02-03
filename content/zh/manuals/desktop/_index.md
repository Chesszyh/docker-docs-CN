---
title: Docker Desktop
weight: 10
description: 探索 Docker Desktop，了解它的功能及关键特性。立即下载或查找更多资源。
keywords: 如何使用 docker desktop, docker desktop 用途, docker desktop 功能, 使用 docker desktop
params:
  sidebar:
    group: Products
grid:
- title: 安装 Docker Desktop
  description: |
    在 [Mac](/desktop/setup/install/mac-install/)、
    [Windows](/desktop/setup/install/windows-install/) 或
    [Linux](/desktop/setup/install/linux/) 上安装 Docker Desktop。
  icon: download
- title: 了解 Docker Desktop
  description: 浏览 Docker Desktop 功能。
  icon: feature_search
  link: /desktop/use-desktop/
- title: 探索关键特性
  description: |
    查找有关 [Docker VMM](/desktop/features/vmm/)、[WSL](/desktop/features/wsl/)、[在 Kubernetes 上部署](/desktop/features/kubernetes/) 等的信息。
  icon: category
- title: 查看发行说明
  description: 了解新特性、改进和错误修复。
  icon: note_add
  link: /desktop/release-notes/
- title: 浏览常见问题 (FAQ)
  description: 探索通用常见问题或特定平台的常见问题。
  icon: help
  link: /desktop/troubleshoot-and-support/faqs/general/
- title: 提供反馈
  description: 对 Docker Desktop 或其功能提供反馈。
  icon: sms
  link: /desktop/troubleshoot-and-support/feedback/
aliases:
- /desktop/opensource/
- /docker-for-mac/dashboard/
- /docker-for-mac/opensource/
- /docker-for-windows/dashboard/
- /docker-for-windows/opensource/
---

Docker Desktop 是一款适用于 Mac、Linux 或 Windows 环境的一键安装应用程序，让您可以构建、分享和运行容器化应用程序及微服务。

它提供了一个直观的 GUI（图形用户界面），让您可以直接在机器上管理容器、应用程序和镜像。

Docker Desktop 减少了花在复杂配置上的时间，让您可以专注于编写代码。它负责处理端口映射、文件系统问题以及其他默认设置，并定期通过错误修复和安全性更新进行维护。

Docker Desktop 与您偏好的开发工具和语言集成，并通过 Docker Hub 为您提供访问海量可信镜像和模板的生态系统。这使得团队能够加速开发、自动化构建、启用 CI/CD 工作流，并通过共享存储库进行安全协作。

{{< tabs >}}
{{< tab name="Docker Desktop 包含什么？" >}}

- [Docker Engine](/manuals/engine/_index.md)
- Docker CLI 客户端
- [Docker Scout](../scout/_index.md)
- [Docker Build](/manuals/build/_index.md)
- [Docker Compose](/manuals/compose/_index.md)
- [Ask Gordon](/manuals/ai/gordon/_index.md)
- [Docker Extensions](../extensions/_index.md)
- [Docker Content Trust](/manuals/engine/security/trust/_index.md)
- [Kubernetes](https://github.com/kubernetes/kubernetes/)
- [Credential Helper](https://github.com/docker/docker-credential-helpers/)

{{< /tab >}}
{{< tab name="Docker Desktop 的关键特性有哪些？">}}

* 能够使用多种语言和框架，在任何云平台上容器化并分享任何应用程序。
* 快速安装和设置完整的 Docker 开发环境。
* 包含最新版本的 Kubernetes。
* 在 Windows 上，能够切换 Linux 和 Windows 容器以构建应用程序。
* 凭借原生 Windows Hyper-V 虚拟化实现快速可靠的性能。
* 在 Windows 机器上通过 WSL 2 实现原生的 Linux 工作体验。
* 针对代码和数据进行卷挂载，包括文件更改通知以及对本地主机网络上运行的容器的便捷访问。

{{< /tab >}}
{{< /tabs >}}

{{< grid >}}