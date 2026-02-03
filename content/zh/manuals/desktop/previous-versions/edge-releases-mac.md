--- 
description: 针对每次 Edge 版本的变更日志 / 发行说明
keywords: Docker Desktop for Mac, edge, release notes, 发行说明
title: Mac 版 Docker Desktop Edge 发行说明
toc_min: 1
toc_max: 2
alias:
- /desktop/mac/release-notes/edge-releases/
sitemap: false
---

本页包含关于 Docker Desktop Edge 版本的信息。Edge 版本让您可以提前体验我们的最新功能。请注意，其中一些功能可能处于实验阶段，有些功能可能永远不会进入稳定版 (Stable)。

有关 Docker Desktop 的系统要求，请参阅 [安装前须知](/manuals/desktop/setup/install/mac-install.md#system-requirements)。

## Docker Desktop Community 2.5.4
2020-12-07

### 升级

- [Docker Engine 20.10.0-rc2](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Go 1.15.6](https://github.com/golang/go/issues?q=milestone%3AGo1.15.6+label%3ACherryPickApproved+)

### 错误修复与微调

- 将菜单项 «Update and quit» 更改为 «Update and restart»。
- 修复了检查更新对话框中显示构建号而不是新版本版本号的问题。
- 将内核降级至 [4.19.121](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.121-2a1dbedf3f998dac347c499808d7c7e029fbc4d3-amd64/images/sha256-4e7d94522be4f25f1fbb626d5a0142cbb6e785f37e437f6fd4285e64a199883a?context=repo) 以降低 hyperkit 的 CPU 占用。修复了 [docker/for-mac#5044](https://github.com/docker/for-mac/issues/5044)。
- 修复了当名称存在但未找到对应记录类型时，DNS 会返回 `NXDOMAIN` 的 Bug。修复了 [docker/for-mac#5020](https://github.com/docker/for-mac/issues/5020)。与 https://gitlab.alpinelinux.org/alpine/aports/-/issues/11879 相关。
- 避免在使用 `osxfs` 时缓存错误的文件大小和模式。修复了 [docker/for-mac#5045](https://github.com/docker/for-mac/issues/5045)。

## Docker Desktop Community 2.5.3
2020-11-30

### 升级

- [Compose CLI v1.0.3](https://github.com/docker/compose-cli/releases/tag/v1.0.3)

### 错误修复与微调

- 修复了文件共享中的一个可能错误：即当宿主机上的文件被修改时，容器内该文件的大小可能显示不正确。这是对 [docker/for-mac#4999](https://github.com/docker/for-mac/issues/4999) 的部分修复。
- 移除了会减慢文件系统事件注入的冗余日志消息。

## Docker Desktop Community 2.5.2
2020-11-26

### 新特性

- 使用三位数的版本号。
- 从 Docker Desktop 2.5.2 开始，更新将采用增量补丁技术，更新包体积会小得多。

### 错误修复与微调

- 重新启用了实验性的 SOCKS 代理。修复了 [docker/for-mac#5048](https://github.com/docker/for-mac/issues/5048)。
- 修复了尝试使用 `-v /var/run/docker.sock:` 启动一个不存在的容器时出现的“意外 EOF”错误。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。
- 当应用程序需要对特定目录的写权限时显示错误消息，而不是直接崩溃。参见 [docker/for-mac#5068](https://github.com/docker/for-mac/issues/5068)。

## Docker Desktop Community 2.5.1.0
2020-11-18

此版本包含 Kubernetes 升级。请注意，安装 Docker Desktop 后，您的本地 Kubernetes 集群将被重置。

### 升级

- [Docker Engine 20.10.0-rc1](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Compose CLI v1.0.2](https://github.com/docker/compose-cli/releases/tag/v1.0.2)
- [Snyk v1.424.4](https://github.com/snyk/snyk/releases/tag/v1.424.4)
- [Kubernetes 1.19.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.3)

### 错误修复与微调

- 将 “Run Diagnostics” 重命名为 “Get support”。
- 修复了在同时安装了 VirtualBox 的情况下，Docker Desktop 在 MacOS 11.0 (Big Sur) 上崩溃的问题。参见 [docker/for-mac#4997](https://github.com/docker/for-mac/issues/4997)。
- 移除了 BlueStacks 警告消息。修复了 [docker/for-mac#4863](https://github.com/docker/for-mac/issues/4863)。
- 优化了在共享卷包含大量文件时的容器启动速度。修复了 [docker/for-mac#4957](https://github.com/docker/for-mac/issues/4957)。
- 文件共享：修复了更改只读文件所有权的问题。修复了 [docker/for-mac#4989](https://github.com/docker/for-mac/issues/4989)、[docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964)。
- 修复了尝试启动不存在的容器时出现的“意外 EOF”错误。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。

## Docker Desktop Community 2.4.2.0
2020-10-19

### 新特性

- 如果您在 Docker Hub 中启用了 [漏洞扫描](/docker-hub/repos/manage/vulnerability-scanning/)，扫描结果现在将显示在 Docker Desktop 中。

### 升级

- [Docker Engine 20.10.0 beta1](https://github.com/docker/docker-ce/blob/0fc7084265b3786a5867ec311d3f916af7bf7a23/CHANGELOG.md)
- [Docker Compose CLI - 0.1.22](https://github.com/docker/compose-cli/releases/tag/v0.1.22)
- [Linux 内核 5.4.39](https://hub.docker.com/layers/linuxkit/kernel/5.4.39-f39f83d0d475b274938c86eaa796022bfc7063d2/images/sha256-8614670219aca0bb276d4749e479591b60cd348abc770ac9ecd09ee4c1575405?context=explore)。
- [Kubernetes 1.19.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.2)
- [Go 1.15.2](https://github.com/golang/go/issues?q=milestone:Go1.15.2+label:CherryPickApproved)

### 错误修复与微调

- 在与容器共享 Linux 目录（`/var`、`/bin` 等）时，Docker Desktop 会避免监视宿主机文件系统中的路径。
- 在将文件共享到容器中时（例如 `docker run -v ~/.gitconfig`），Docker Desktop 不再监视其父目录。修复了 [docker/for-mac#4981](https://github.com/docker/for-mac/issues/4981)。
- gRPC FUSE：修复了只读文件的 `chown` 问题。修复了 `rabbitmq` 相关问题，参见 [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964)。
- gRPC FUSE：除了 `MODIFY` 事件外，还会生成 `ATTRIB` inotify 事件。修复了 [docker/for-mac#4962](https://github.com/docker/for-mac/issues/4962)。
- gRPC FUSE：对于不支持的模式，`fallocate` 返回 `EOPNOTSUPP`。修复了 `minio` 相关问题。参见 [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964)。
- 修复了与 NFS 挂载相关的问题。参见 [docker/for-mac#4958](https://github.com/docker/for-mac/issues/4958)。
- 容器启动时始终同步刷新文件系统缓存。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。
- 允许符号链接指向共享卷之外。修复了 [docker/for-mac#4862](https://github.com/docker/for-mac/issues/4862)。
- 诊断：避免在 Kubernetes 处于损坏状态时挂起。
- 修复了登录时自动启动的问题。参见 [docker/for-mac#4877](https://github.com/docker/for-mac/issues/4877) 和 [docker/for-mac#4890](https://github.com/docker/for-mac/issues/4890)。

## Docker Desktop Community 2.4.1.0
2020-10-01

### 升级

- [Docker Compose CLI - 0.1.18](https://github.com/docker/compose-cli)
- [Docker Compose 1.27.4](https://github.com/docker/compose/releases/tag/1.27.4)
- [Snyk v1.399.1](https://github.com/snyk/snyk/releases/tag/v1.399.1)
- [Docker Engine 19.03.13](https://github.com/docker/docker-ce/releases/tag/v19.03.13)

### 错误修复与微调

- 容器启动时始终同步刷新文件系统缓存。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。
- Docker Desktop 现在在共享文件系统上的 `chmod(2)` 调用中支持 `S_ISUID`、`S_ISGID` 和 `S_ISVTX`。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。
- 修复了使用 `gRPC-FUSE` 时可能过早关闭文件句柄的问题。

## Docker Desktop Community 2.3.7.0
2020-09-17

### 新特性

- [Amazon ECR 凭据辅助程序](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.4.0)

### 升级

- [Docker ACI 集成 0.1.15](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.15)
- [Snyk v0.393.0](https://github.com/snyk/snyk/releases/tag/v1.393.0)

### 错误修复与微调

- 修复了登录时自动启动的问题。参见 [docker/for-mac#4877](https://github.com/docker/for-mac/issues/4877) 和 [docker/for-mac#4890](https://github.com/docker/for-mac/issues/4890)。
- Docker Desktop 现在允许符号链接指向共享卷之外。修复了 [docker/for-mac#4862](https://github.com/docker/for-mac/issues/4862)。
- 移除了 `10240` 的人为文件描述符限制 (`setrlimit`)。Docker Desktop 现在依赖内核通过 `kern.maxfiles` 和 `kern.maxfilesperproc` 来施加限制。
- 修复了用于底层调试的虚拟机调试 shell。
- 修复了与 Go 1.15 客户端的兼容性问题。参见 [docker/for-mac#4855](https://github.com/docker/for-mac/issues/4855)。
- 避免在 `docker container inspect` 和 `docker volume inspect` 中暴露 `/host_mnt` 路径。修复了 [docker/for-mac#4859](https://github.com/docker/for-mac/issues/4859)。
- 修复了高负载下容器日志滞后的问题。参见 [docker/for-win#8216](https://github.com/docker/for-win/issues/8216)。

### 已知问题

- 在 i386 镜像中，`clock_gettime64` 系统调用返回 `EPERM` 而不是 `ENOSYS`。要解决此问题，请通过使用 `--privileged` 标志禁用 `seccomp`。参见 [docker/for-win#8326](https://github.com/docker/for-win/issues/8326)。

## Docker Desktop Community 2.3.6.1
2020-09-08

### 升级

- [Docker Compose 1.27.0](https://github.com/docker/compose/releases/tag/1.27.0)

### 错误修复与微调

- Docker Desktop 现在在 UI 中正确显示 “Use gRPC FUSE for file sharing” 的状态。修复了 [docker/for-mac#4864](https://github.com/docker/for-mac/issues/4864)。

## Docker Desktop Community 2.3.6.0
2020-09-01

### 新特性

- 通过与 Snyk 合作，Docker Desktop 推出了针对 Docker 本地镜像的漏洞扫描。
- Docker ECS 插件已被 ECS 云集成取代。
- Docker UI：
  - 镜像视图现在具有搜索和过滤选项。
  - 您现在可以使用“远程存储库”下拉菜单将镜像推送到 Docker Hub。
- 现在的 Windows Docker CLI 支持挂载 WSL 2 文件和目录，例如 `docker run -v \wsl$"Ubuntu"/my-files:/my-files ...`。

### 移除

- 已停止对 MacOS 10.13 的支持，您需要更新系统以继续使用 Docker Desktop。

### 升级

- [Alpine 3.12](https://alpinelinux.org/posts/Alpine-3.12.0-released.html)
- [Kubernetes 1.18.8](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.8)

### 错误修复与微调

- 通过从 `hyperkit` 移除串行控制台，修复了 Mac CPU 占用过高的 Bug，参见 [docker/roadmap#12]( https://github.com/docker/roadmap/issues/12#issuecomment-663163280)。要在虚拟机中打开 shell，请在 Mac 上使用 `nc -U ~/Library/Containers/com.docker.docker/Data/debug-shell.sock`，或在 Windows 上使用 `putty -serial \.\