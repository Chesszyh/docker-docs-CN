---
description: 查找适用于 Mac、Linux 和 Windows 的 Docker Desktop 发行说明。
keywords: Docker desktop, 发行说明, linux, mac, windows
title: Docker Desktop 发行说明
linkTitle: 发行说明
tags: [发行说明]
toc_max: 2
aliases:
- /docker-for-mac/release-notes/
- /docker-for-mac/edge-release-notes/
- /desktop/mac/release-notes/
- /docker-for-windows/edge-release-notes/
- /docker-for-windows/release-notes/
- /desktop/windows/release-notes/
- /desktop/linux/release-notes/
- /mackit/release-notes/
weight: 220
---

本页面包含 Docker Desktop 发行版中的新特性、改进、已知问题和 Bug 修复信息。 

发行版会逐步推出以确保质量控制。如果您还无法获取最新版本，请稍等片刻——更新通常会在发布日期后的一周内提供。

发布时间超过 6 个月的旧版 Docker Desktop 将不再提供下载。之前的发行说明可在我们的 [文档仓库](https://github.com/docker/docs/tree/main/content/manuals/desktop/previous-versions) 中找到。

有关更多常见问题，请参阅 [FAQ](/manuals/desktop/troubleshoot-and-support/faqs/releases.md)。

> [!WARNING]
>
> 如果您在 Mac 上遇到恶意软件检测问题，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 4.43.1

{{< release-date date="2025-07-04" >}}

{{< desktop-install-v2 all=true beta_win_arm=true version="4.43.1" build_path="/198352/" >}}

### Bug 修复和增强

#### 适用于所有平台

- 修复了当 Ask Gordon 的回复包含 HTML 标签时导致 Docker Desktop UI 损坏的问题。
- 修复了阻止扩展程序与其后端通信的问题。

## 4.43.0

{{< release-date date="2025-07-03" >}}

{{< desktop-install-v2 all=true beta_win_arm=true version="4.43.0" build_path="/198134/" >}}

### 新增

- [Compose Bridge](/manuals/compose/bridge/_index.md) 现已正式发布（GA）。

### 升级

- [Docker Buildx v0.25.0](https://github.com/docker/buildx/releases/tag/v0.25.0)
- [Docker Compose v2.38.1](https://github.com/docker/compose/releases/tag/v2.38.1)
- [Docker Engine v28.3.0](https://docs.docker.com/engine/release-notes/28/#2830)
- [NVIDIA Container Toolkit v1.17.8](https://github.com/NVIDIA/nvidia-container-toolkit/releases/tag/v1.17.8)

### 安全 

- 修复了 [CVE-2025-6587](https://www.cve.org/CVERecord?id=CVE-2025-6587)，即敏感的系统环境变量被包含在 Docker Desktop 诊断日志中，从而导致潜在的机密泄露。

### Bug 修复和增强

#### 适用于所有平台

- 修复了导致 `docker start` 丢弃正在运行容器的端口映射的 Bug。
- 修复了导致容器重启时 GUI 无法显示容器端口的 Bug。
- 修复了导致 Docker API 出现 `500 Internal Server Error for API route and version` 错误的 Bug。
- 设置中的 **Apply & restart** 按钮现已标记为 **Apply**。在应用更改的设置时，虚拟机不再重启。 
- 修复了如果 Docker 在 `fsck` 期间关闭会导致磁盘损坏的 Bug。
- 修复了在使用 `kind` Kubernetes 集群时导致 WSL2 中 `~/.kube/config` 错误的 Bug。
- 如果 Docker Desktop 已手动暂停，则向 Docker API / `docker` CLI 命令返回明确的错误。
- 修复了管理和云设置中的未知键导致失败的问题。

#### 适用于 Linux

- 将 `virtiofsd` 提升至 `1.13.1`。

#### 适用于 Mac

- 移除了阻塞 `io_uring` 的 `eBPF`。要在容器中启用 `io_uring`，请使用 `--security-opt seccomp=unconfined`。修复了 [docker/for-mac#7707](https://github.com/docker/for-mac/issues/7707)。

#### 适用于 Windows

- 修复了当当前用户没有 `SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall` 注册表项时导致 Docker Desktop 安装程序崩溃的问题。
- 修复了 Docker Desktop 可能会泄露 `com.docker.build` 进程并导致启动失败的 Bug。修复了 [docker/for-win#14840](https://github.com/docker/for-win/issues/14840)。

### 已知问题

#### 适用于所有平台

- `docker buildx bake` 不会构建具有顶级 models 属性的 Compose 文件中的镜像。请改用 `docker compose build`。
- 包含 HTML 的 Gordon 回复可能会导致 Desktop UI 永久损坏。作为变通方法，您可以删除 `persisted-state.json` 文件以重置 UI。该文件位于以下目录中：
  - Windows: `%APPDATA%\Docker Desktop\persisted-state.json`
  - Linux: `$XDG_CONFIG_HOME/Docker Desktop/persisted-state.json` 或 `~/.config/Docker Desktop/persisted-state.json`
  - Mac: `~/Library/Application Support/Docker Desktop/persisted-state.json`

#### 适用于 Windows

- Docker Desktop 的“主机网络”功能与最新的 WSL 2 Linux 内核之间可能存在不兼容性。如果您遇到此类问题，请将 WSL 2 降级到 2.5.7。

## 4.42.1

{{< release-date date="2025-06-18" >}}

{{< desktop-install-v2 all=true beta_win_arm=true version="4.42.1" build_path="/196648/" >}}

### 升级

- [Docker Compose v2.37.1](https://github.com/docker/compose/releases/tag/v2.37.1)

### Bug 修复和增强

#### 适用于所有平台

- 修复了当代理配置无效时无法访问 Docker 域的问题。
- 修复了在暴露端口时可能出现的死锁。
- 修复了可能导致 `docker run -p` 端口消失的竞态条件。

#### 适用于 Mac

- 修复了容器创建后立即检查（例如使用脚本时）端口列表显示为空的 Bug。[docker/for-mac#7693](https://github.com/docker/for-mac/issues/7693)

#### 适用于 Windows

- 在 WSL 2 中禁用了资源保存模式（Resource Saver mode），以防止 `docker` CLI 命令在 WSL 2 发行版中挂起。[docker/for-win#14656](https://github.com/docker/for-win/issues/14656#issuecomment-2960285463)

... (此处省略历史版本)
