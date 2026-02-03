---
description: Mac 版 Docker Desktop 较旧版本的发行说明
keywords: Docker Desktop for Mac, release notes, 发行说明
title: 历史版本发行说明
toc_min: 1
toc_max: 2
aliases:
- /desktop/mac/release-notes/archive/
sitemap: false
---

本页包含 Mac 版 Docker Desktop 较旧版本的发行说明。

## 2018 年稳定版

### Docker Community Edition 18.06.1-ce-mac73 2018-08-29

* 升级
  - [Docker 18.06.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.1-ce)

* 错误修复与微调
  - 修复了容器内部无法解析本地 DNS 的问题。

### Docker Community Edition 18.06.0-ce-mac70 2018-07-25

* 升级
  - [Docker 18.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.0-ce)
  - [Docker Machine 0.15.0](https://github.com/docker/machine/releases/tag/v0.15.0)
  - [Docker Compose 1.22.0](https://github.com/docker/compose/releases/tag/1.22.0)
  - [LinuxKit v0.5](https://github.com/linuxkit/linuxkit/releases/tag/v0.5)
  - Linux 内核 4.9.93，启用了 CEPH、DRBD、RBD、MPLS_ROUTING 和 MPLS_IPTUNNEL

* 新特性
  - **Kubernetes 支持**：您现在可以从 Mac 版 Docker 偏好设置中的“Kubernetes”面板运行单节点 Kubernetes 集群，并使用 kubectl 命令以及 docker 命令。参见 [Kubernetes 章节](/manuals/desktop/features/kubernetes.md)。
  - 增加了实验性 SOCKS 服务器以允许访问容器网络，参见 [docker/for-mac#2670](https://github.com/docker/for-mac/issues/2670#issuecomment-372365274)。另请参阅 [docker/for-mac#2721](https://github.com/docker/for-mac/issues/2721)。
  - 为运行 macOS 10.13.4 及更高版本的用户重新启用 raw 作为默认磁盘格式。请注意，此更改仅在执行“恢复出厂设置”或“删除所有数据”后生效。与 [docker/for-mac#2625](https://github.com/docker/for-mac/issues/2625) 相关。

* 错误修复与微调
  - AUFS 存储驱动程序在 Docker Desktop 中已被弃用，且 AUFS 支持将在下一个主要版本中移除。您可以在 Docker Desktop 18.06.x 中继续使用 AUFS，但在更新到下一个主要版本之前，您需要重置磁盘镜像（在 Preferences > Reset 菜单中）。您可以查看文档以 [保存镜像](/reference/cli/docker/image/save/#examples) 和 [备份卷](/manuals/engine/storage/volumes.md#备份-还原或迁移数据卷)。
  - OS X El Capitan 10.11 在 Docker Desktop 中已被弃用。在 Docker Desktop 18.06.x 之后，您将无法安装更新。我们建议升级到最新版本的 macOS。
  - 修复了在某些情况下导致虚拟机日志被写入 RAM 而非磁盘，从而导致虚拟机挂起的 Bug。参见 [docker/for-mac#2984](https://github.com/docker/for-mac/issues/2984)。
  - 修复了由 haproxy TCP 健康检查触发的网络连接泄漏问题 [docker/for-mac#1132](https://github.com/docker/for-mac/issues/1132)。
  - 在 vmnetd 被禁用时，提供了更好的重置提示消息。参见 [docker/for-mac#3035](https://github.com/docker/for-mac/issues/3035)。
  - 修复了 VPNKit 内存泄漏。修复了 [moby/vpnkit#371](https://github.com/moby/vpnkit/issues/371)。
  - 虚拟机默认磁盘路径现在相对于 `$HOME` 存储。修复了 [docker/for-mac#2928](https://github.com/docker/for-mac/issues/2928)、[docker/for-mac#1209](https://github.com/docker/for-mac/issues/1209)。
  - 使用 Simple NTP 来最小化虚拟机与宿主机之间的时钟偏移。修复了 [docker/for-mac#2076](https://github.com/docker/for-mac/issues/2076)。
  - 修复了在对文件调用 `stat` 与关闭引用该文件的文件描述符之间的竞态条件，该条件可能导致 `stat` 失败并提示 EBADF（通常表现为“文件未找到”）。修复了 [docker/for-mac#2870](https://github.com/docker/for-mac/issues/2870)。
  - 不再允许在 macOS Yosemite 10.10 上安装 Mac 版 Docker，自 Docker for Mac 17.09.0 起已不再支持此版本。
  - 修复了重置对话框窗口中的按钮顺序。修复了 [docker/for-mac#2827](https://github.com/docker/for-mac/issues/2827)。
  - 修复了直接从 17.12 之前的版本升级时，Docker for Mac 升级后无法重启的问题。修复了 [docker/for-mac#2739](https://github.com/docker/for-mac/issues/2739)。
  - 在虚拟机内部为 docker-ce 日志添加了日志轮转。

### Docker Community Edition 18.03.1-ce-mac65 2018-04-30

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker Compose 1.21.1](https://github.com/docker/compose/releases/tag/1.21.1)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* 错误修复与微调
  - 修复了因套接字文件路径过长（通常是由于 HOME 文件夹路径过长）导致 Docker for Mac 无法启动的问题。修复了 [docker/for-mac#2727](https://github.com/docker/for-mac/issues/2727)、[docker/for-mac#2731](https://github.com/docker/for-mac/issues/2731)。

### Docker Community Edition 18.03.1-ce-mac64 2018-04-26

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker Compose 1.21.0](https://github.com/docker/compose/releases/tag/1.21.0)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* 错误修复与微调
  - 修复了因套接字文件路径过长导致 Docker for Mac 无法启动的问题。修复了 [docker/for-mac#2727](https://github.com/docker/for-mac/issues/2727)、[docker/for-mac#2731](https://github.com/docker/for-mac/issues/2731)。

### Docker Community Edition 18.03.0-ce-mac60 2018-03-30

* 错误修复与微调
  - 修复了直接从 17.09 版本升级时，Docker for Mac 升级后无法重启的问题。修复了 [docker/for-mac#2739](https://github.com/docker/for-mac/issues/2739)。

### Docker Community Edition 18.03.0-ce-mac59 2018-03-26

* 升级
  - [Docker 18.03.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.0-ce)
  - [Docker Machine 0.14.0](https://github.com/docker/machine/releases/tag/v0.14.0)
  - [Docker Compose 1.20.1](https://github.com/docker/compose/releases/tag/1.20.1)
  - [Notary 0.6.0](https://github.com/docker/notary/releases/tag/v0.6.0)
  - Linux 内核 4.9.87
  - AUFS 20180312

* 新特性
  - 虚拟机交换空间（Swap）大小现在可以在设置中更改。参见 [docker/for-mac#2566](https://github.com/docker/for-mac/issues/2566)、[docker/for-mac#2389](https://github.com/docker/for-mac/issues/2389)。
  - 新增重启 Docker 的菜单项。
  - 支持 NFS 卷共享。
  - 存放磁盘镜像的目录已重命名（从 `~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux` 更改为 `~/Library/Containers/com.docker.docker/Data/vms/0`）。

* 错误修复与微调
  - 修复了设置 TLS 相关选项时守护进程无法正常启动的问题。修复了 [docker/for-mac#2663](https://github.com/docker/for-mac/issues/2663)。
  - 容器解析宿主机应使用 DNS 名称 `host.docker.internal`。旧的别名（仍有效）已被弃用，建议改用此名称。（参见 https://tools.ietf.org/html/draft-west-let-localhost-be-localhost-06）。
  - 修复了使用 "localhost" 名称（如 `host.docker.internal`）时的 HTTP/S 透明代理问题。
  - 修复了在偏好设置守护进程面板中某些情况下错误添加空注册表的问题。修复了 [docker/for-mac#2537](https://github.com/docker/for-mac/issues/2537)。
  - 检测到不兼容硬件时，提供了更清晰的错误消息。
  - 修复了某些在发生错误后选择“重置”却无法正常重置的情况。
  - 修复了不正确的 NTP 配置。修复了 [docker/for-mac#2529](https://github.com/docker/for-mac/issues/2529)。
  - Mac 版 Docker 安装程序不再建议迁移 Docker Toolbox 镜像（仍可手动迁移 Toolbox 镜像）。

### Docker Community Edition 17.12.0-ce-mac55 2018-02-27

* 错误修复与微调
  - 为运行 macOS 10.13 (High Sierra) 的用户将默认磁盘格式恢复为 qcow2。有确切报告称，在 APFS 上使用 raw 格式（使用稀疏文件）会导致文件损坏。请注意，此更改仅在执行“恢复出厂设置”后生效。与 [docker/for-mac#2625](https://github.com/docker/for-mac/issues/2625) 相关。
  - 修复了 `docker.for.mac.http.internal` 的 VPNKit 代理。

### Docker Community Edition 17.12.0-ce-mac49 2018-01-19

* 错误修复与微调
  - 修复了某些情况下在调整/创建 `Docker.raw` 磁盘镜像时出现的错误。修复了 [docker/for-mac#2383](https://github.com/docker/for-mac/issues/2383)、[docker/for-mac#2447](https://github.com/docker/for-mac/issues/2447)、[docker/for-mac#2453](https://github.com/docker/for-mac/issues/2453)、[docker/for-mac#2420](https://github.com/docker/for-mac/issues/2420)。
  - 修复了额外分配的磁盘空间在容器内不可用的问题。修复了 [docker/for-mac#2449](https://github.com/docker/for-mac/issues/2449)。
  - VPNKit 端口最大空闲时间默认值恢复为 300 秒。修复了 [docker/for-mac#2442](https://github.com/docker/for-mac/issues/2442)。
  - 修复了使用带有身份验证的 HTTP 代理的问题。修复了 [docker/for-mac#2386](https://github.com/docker/for-mac/issues/2386)。
  - 允许将 HTTP 代理排除项写为 `.docker.com` 以及 `*.docker.com`。
  - 允许将单个 IP 地址添加到 HTTP 代理排除项中。
  - 在上游 DNS 服务器较慢或缺失时，避免在查询 `docker.for.mac.*` 时触发 DNS 超时。

### Docker Community Edition 17.12.0-ce-mac47 2018-01-12

* 错误修复与微调
  - 修复了向非安全注册表执行 `docker push` 的问题。修复了 [docker/for-mac#2392](https://github.com/docker/for-mac/issues/2392)。
  - 分离了用于代理 HTTP 和 HTTPS 内容的内部端口。

### Docker Community Edition 17.12.0-ce-mac46 2018-01-09

* 升级
  - [Docker 17.12.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.12.0-ce)
  - [Docker Compose 1.18.0](https://github.com/docker/compose/releases/tag/1.18.0)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)
  - Linux 内核 4.9.60

* 新特性
  - 虚拟机完全由 LinuxKit 构建。
  - 虚拟机磁盘大小现在可以在磁盘偏好设置中更改。（参见 [docker/for-mac#1037](https://github.com/docker/for-mac/issues/1037)）。
  - 对于在 High Sierra 上使用 SSD 且运行 APFS 的系统，默认使用 `raw` 格式的虚拟机磁盘。这提高了磁盘吞吐量（在 2015 款 MacBook Pro 上，`dd` 测试从 320MiB/s 提升到 600MiB/s）以及磁盘空间处理。现有磁盘将保持 qcow 格式，如果您想切换到 raw 格式，需要选择“删除所有数据”或“恢复出厂设置”。
  - 容器解析宿主机应使用 DNS 名称 `docker.for.mac.host.internal`，而不是 `docker.for.mac.localhost`（虽仍有效但已弃用），因为有一项 RFC 禁止使用 localhost 的子域名。参见 https://tools.ietf.org/html/draft-west-let-localhost-be-localhost-06。

* 错误修复与微调
  - 在“关于”对话框中显示各种组件的版本。
  - 更改宿主机代理设置时避免重启虚拟机。
  - 不要通过外部代理转发容器间的 HTTP 流量，以免造成中断。（参见 [docker/for-mac#981](https://github.com/docker/for-mac/issues/981)）。
  - 文件共享设置现在存储在 `settings.json` 中。
  - 守护进程重启按钮已移动到设置 / 重置（Reset）选项卡。
  - 优化了虚拟机崩溃时的状态处理和错误消息。
  - 修复了登录带有证书问题的私有仓库时的问题。（参见 [docker/for-mac#2201](https://github.com/docker/for-mac/issues/2201)）。

## 2017 年稳定版

### Docker Community Edition 17.09.1-ce-mac42 2017-12-11

* 升级
  - [Docker 17.09.1-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.1-ce)
  - [Docker Compose 1.17.1](https://github.com/docker/compose/releases/tag/1.17.1)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)

* 错误修复与微调
  - 修复了某些情况下无法移动 qcow 磁盘的 Bug。

### Docker Community Edition 17.09.0-ce-mac35 2017-10-06

* 错误修复
  - 修复了 Mac 版 Docker 在某些情况下无法启动的问题：移除了有时会导致 vpnkit 进程退出的 libgmp 使用。

### Docker Community Edition 17.09.0-ce-mac33 2017-10-03
  - 当存在已有的 Mac 版 Docker 数据时，不再显示 Toolbox 迁移助手。

### Docker Community Edition 17.09.0-ce-mac32 2017-10-02

* 升级
  - [Docker 17.09.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.0-ce)
  - [Docker Compose 1.16.1](https://github.com/docker/compose/releases/tag/1.16.1)
  - [Docker Machine 0.12.2](https://github.com/docker/machine/releases/tag/v0.12.2)
  - [Docker Credential Helpers 0.6.0](https://github.com/docker/docker-credential-helpers/releases/tag/v0.6.0)
  - Linux 内核 4.9.49
  - AUFS 20170911
  - DataKit 更新（修复了 High Sierra 上的不稳定性）

* 新特性
  - 增加了守护进程选项验证。
  - VPNKit：增加了对 ping 的支持！
  - VPNKit：增加了 `slirp/port-max-idle-timeout` 选项，允许调整甚至禁用超时。
  - VPNKit：现在所有平台默认均为桥接模式。
  - 直接使用 macOS 系统代理（如果已定义）实现透明代理。
  - GUI 设置现在存储在 `~/Library/Group Containers/group.com.docker/settings.json` 中。`daemon.json` 现在是 `~/.docker/` 目录下的一个文件。
  - 如果 HyperKit 使用的默认 IP 地址与您的网络冲突，您现在可以更改它。

* 错误修复与微调
  - 修复了 High Sierra 上的不稳定性问题（docker/for-mac#2069, #2062, #2052, #2029, #2024）。
  - 修复了密码编码/解码问题（docker/for-mac#2008, #2016, #1919, #712, #1220）。
  - 内核：启用了 `TASK_XACCT` 和 `TASK_IO_ACCOUNTING` (docker/for-mac#1608)。
  - 增加了虚拟机内日志轮转的频率。
  - VPNKit：更改协议以支持从服务器传回的错误消息。
  - VPNKit：修复了如果相应的 TCP 连接空闲超过 5 分钟会导致套接字泄漏的 Bug（与 [docker/for-mac#1374](https://github.com/docker/for-mac/issues/1374) 相关）。
  - VPNKit：改进了 Unix 域套接字连接周围的日志记录。
  - VPNKit：自动修剪整数或布尔值数据库键中的空格。
  - 诊断可以被取消并改进了帮助信息。修复了 [docker/for-mac#1134](https://github.com/docker/for-mac/issues/1134)、[docker/for-mac#1474](https://github.com/docker/for-mac/issues/1474)。
  - 支持 docker-cloud 存储库和组织的翻页。修复了 [docker/for-mac#1538](https://github.com/docker/for-mac/issues/1538)。

### Docker Community Edition 17.06.2-ce-mac27 2017-09-06

**升级**

  - [Docker 17.06.2-ce](https://github.com/docker/docker-ce/releases/tag/v17.06.2-ce)
  - [Docker Machine 0.12.2](https://github.com/docker/machine/releases/tag/v0.12.2)

### Docker Community Edition 17.06.1-ce-mac24, 2017-08-21

**升级**

- [Docker 17.06.1-ce-rc1](https://github.com/docker/docker-ce/releases/tag/v17.06.1-ce-rc1)
- Linux 内核 4.9.36
- AUFS 20170703

**错误修复与微调**

- DNS 修复。修复了 [docker/for-mac#1763](https://github.com/docker/for-mac/issues/176)、[docker/for-mac#1811](https://github.com/docker/for-mac/issues/1811)、[docker/for-mac#1803](https://github.com/docker/for-mac/issues/1803)。
- 避免不必要的虚拟机重启（当更改代理排除项但未设置代理时）。修复了 [docker/for-mac#1809](https://github.com/docker/for-mac/issues/1809)、[docker/for-mac#1801](https://github.com/docker/for-mac/issues/1801)。

### Docker Community Edition 17.06.0-ce-mac18, 2017-06-28

**升级**

- [Docker 17.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.06.0-ce)
- [Docker Credential Helpers 0.5.2](https://github.com/docker/docker-credential-helpers/releases/tag/v0.5.2)
- [Docker Machine 0.12.0](https://github.com/docker/machine/releases/tag/v0.12.0)
- [Docker Compose 1.14.0](https://github.com/docker/compose/releases/tag/1.14.0)
- `qcow-tool` v0.10.0（提高了 `compact` 操作的性能：mirage/ocaml-qcow#94）
- OSX Yosemite 10.10 已被标记为弃用
- Linux 内核 4.9.31

**新特性**

- 与 Docker Cloud 集成：通过本地 CLI 控制远程 Swarm 并查看您的存储库。
- GUI 选项支持选择退出凭据存储。
- GUI 选项支持在不丢失所有设置的情况下重置 Docker 数据（修复了 [docker/for-mac#1309](https://github.com/docker/for-mac/issues/1309)）。
- 增加了针对宿主机的实验性 DNS 名称：`docker.for.mac.localhost`。
- 支持客户端（即“登录”）证书用于验证注册表访问（修复了 [docker/for-mac#1320](https://github.com/docker/for-mac/issues/1320)）。
- OSXFS：支持 `cached` 挂载标志，在不需要严格一致性时提高 macOS 挂载的性能。

**错误修复与微调**

- 应用程序启动时重新同步 HTTP(S) 代理设置。
- 正确解释系统代理设置为 `localhost` 的情况（参见 [docker/for-mac#1511](https://github.com/docker/for-mac/issues/1511)）。
- Mac 版 Docker 捆绑的所有 Docker 二进制文件现在均已签名。
- 在鲸鱼菜单中显示所有 Docker Cloud 组织和存储库（修复了 [docker/for-mac#1538](https://github.com/docker/for-mac/issues/1538)）。
- OSXFS：针对读写等常见操作，将延迟降低了约 25%。
- 修复了选择文本表格视图并重新打开窗口时导致的 GUI 崩溃（修复了 [docker/for-mac#1477](https://github.com/docker/for-mac/issues/1477)）。
- 重置为默认 / 卸载操作也会移除 `config.json` 和 `osxkeychain` 凭据。
- 提供了更详细的 VirtualBox 卸载要求 ([docker/for-mac#1343](https://github.com/docker/for-mac/issues/1343))。
- 唤醒后请求时间同步，以改进 [docker/for-mac#17](https://github.com/docker/for-mac/issues/17)。
- VPNKit：改进了 DNS 超时处理（修复了 [docker/for-mac#202](https://github.com/docker/vpnkit/issues/202)）。
- VPNKit：默认使用 `DNSServiceRef` API（仅对新安装或恢复出厂设置后生效）。
- 应用程序崩溃时增加了恢复出厂设置的按钮。
- Toolbox 导入对话框现在默认为“跳过”。
- 当 Docker 客户端请求升级为原始流时，缓冲数据应得到正确处理。
- 移除了输出中与实验性功能处理相关的错误消息。
- `vmnetd` 不应在用户家目录位于外部驱动器时崩溃。
- 改进了设置数据库方案的处理。
- 磁盘修剪 (Disk trimming) 应按预期工作。
- 诊断信息现在包含更多设置数据。

### Docker Community Edition 17.03.1-ce-mac12, 2017-05-12

**升级**

- 修复了 CVE-2017-7308 安全问题。

### Docker Community Edition 17.03.1-ce-mac5, 2017-03-29

**升级**

- [Docker Credential Helpers 0.4.2](https://github.com/docker/docker-credential-helpers/releases/tag/v0.4.2)


### Docker Community Edition 17.03.0-ce-mac1, 2017-03-02 —— 重命名为 Docker Community Edition

**新特性** 

- 与 Docker Cloud 集成：通过本地 CLI 控制远程 Swarm 并查看您的存储库。此功能将逐步向所有用户推出。
- Docker 现在将安全地将您的 ID 存储在 macOS 钥匙串中。

**升级**

- [Docker 17.03.0-ce](https://github.com/docker/docker/releases/tag/v17.03.0-ce)
- [Docker Compose 1.11.2](https://github.com/docker/compose/releases/tag/1.11.2)
- [Docker Machine 0.10.0](https://github.com/docker/machine/releases/tag/v0.10.0)
- Linux 内核 4.9.12

**错误修复与微调**

- 允许通过高级子面板中的链接重置有问题的 `daemon.json`。
- 移动磁盘镜像时提供更多选项。
- 添加了指向实验性功能的链接。
- 文件共享和守护进程表格的空字段现在可编辑。
- 隐藏了设置窗口中的重启按钮。
- 修复了应用未聚焦时更新窗口隐藏的 Bug。
- 不要在 Linux 虚拟机内部使用 4222 端口。
- 在引导参数中添加了 `page_poison=1`。
- 增加了一个新的磁盘刷新选项。
- DNS 转发器忽略来自故障服务器的响应 ([docker/for-mac#1025](https://github.com/docker/for-mac/issues/1025))。
- DNS 转发器并行发送所有查询，并按顺序处理结果。
- DNS 转发器在一般搜索中包含带有区域（Zones）的服务器 ([docker/for-mac#997](https://github.com/docker/for-mac/issues/997))。
- 从 `/etc/hosts` 中解析别名 ([docker/for-mac#983](https://github.com/docker/for-mac/issues/983))。
- 可以通过宿主机 `/etc/resolver` 目录下列出的服务器解析 DNS 请求。
- 将 vCPU 限制为 64 个。
- 修复了交换空间未挂载的问题。
- 修复了 AUFS xattr 删除问题 ([docker/docker#30245](https://github.com/docker/docker/issues/30245))。
- osxfs：读取非文件的扩展属性时捕获 `EPERM`。
- VPNKit：修复了包含“指向标签的指针的指针”的 DNS 报文的解析问题。
- VPNKit：在来自缓存的 DNS 响应中设置“递归可用”位。
- VPNKit：避免诊断信息捕获过多数据。
- VPNKit：修复了虚拟以太网链路上偶尔发生的数据包丢失（截断）源。
- HyperKit：在转储状态时从 VMCS 转储客户机物理地址和线性地址。
- HyperKit：内核引导时带有 `panic=1` 参数。

### Docker for Mac 1.13.1, 2017-02-09

**升级**

- [Docker 1.13.1](https://github.com/docker/docker/releases/tag/v1.13.1)
- [Docker Compose 1.11.1](https://github.com/docker/compose/releases/tag/1.11.1)
- Linux 内核 4.9.8

**错误修复与微调**

- 添加了指向实验性功能的链接。
- 新的 1.13 可取消操作现在应能由桌面版 Docker 正确处理。
- `daemon.json` 在 UI 中应呈现得更好。
- 允许通过高级子面板中的链接重置有问题的 `daemon.json`。

### Docker for Mac 1.13.0, 2017-01-19

**升级**

- [Docker 1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)
- [Docker Compose 1.10](https://github.com/docker/compose/releases/tag/1.10.0)
- [Docker Machine 0.9.0](https://github.com/docker/machine/releases/tag/v0.9.0)
- [Notary 0.4.3](https://github.com/docker/notary/releases/tag/v0.4.3)
- Linux 内核 4.9.4
- `qcow-tool` 0.7.2

**新特性**

- 现在可以移动 Linux 卷的存储位置。
- 重启时回收磁盘空间。
- 您现在可以编辑文件共享路径。
- 内存分配步长改为 256 MiB。
- 代理现在可以被完全禁用。
- 通过 QEMU 支持 ARM、aarch64、ppc64le 架构。
- 为 Docker 守护进程的高级配置提供了专门的偏好设置面板（编辑 `daemon.json`）。
- Docker 实验性模式可以切换。
- 更好地支持 Split DNS VPN 配置。
- 使用更多 DNS 服务器，并遵循其顺序。

**错误修复与微调**

- Docker 重启期间无法编辑设置。
- “关于”框支持复制/粘贴。
- 每 24 小时进行一次自动更新轮询。
- 内核引导时带有 `vsyscall=emulate` 参数，且 Moby 中 `CONFIG_LEGACY_VSYSCALL` 设置为 `NONE`。
- 修复了重写负载下的 vsock 死锁问题。
- 如果您选择退出分析，在发送 Bug 报告之前会提示您批准。
- 修复了搜索域可能被读取为 `DomainName` 的 Bug。
- 为 HTTP 代理设置提供了专门的偏好设置面板。
- 为 CPU 和内存计算资源提供了专门的偏好设置面板。
- 隐私设置移动到了“常规”偏好设置面板。
- 修复了欢迎鲸鱼菜单关闭时偏好设置面板消失的问题。
- HyperKit：代码清理和细微修复。
- 改进了日志和诊断。
- osxfs：切换到 libev/kqueue 以降低延迟。
- VPNKit：改进了 DNS 处理。
- VPNKit：改进了诊断。
- VPNKit：转发的 UDP 数据报应具有正确的源端口号。
- VPNKit：增加了 DNS 响应的本地缓存。
- VPNKit：如果一个请求失败，允许其他并发请求成功。例如，这允许在 IPv6 损坏时 IPv4 服务器仍能工作。
- VPNKit：修复了可能导致连接追踪低估活跃连接数量的 Bug。

## 2016 年稳定版

### Docker for Mac 1.12.5, 2016-12-20

**升级**

- Docker 1.12.5
- Docker Compose 1.9.0

### 跳过 Docker for Mac 1.12.4

我们没有发布 1.12.4 稳定版。

### Docker for Mac 1.12.3, 2016-11-09

**升级**

- Docker 1.12.3
- Linux 内核 4.4.27
- Notary 0.4.2
- Docker Machine 0.8.2
- Docker Compose 1.8.1
- 内核 vsock 驱动 v7
- AUFS 20160912

**错误修复与微调**

**常规**

- 修复了更改设置期间鲸鱼动画不一致的问题。
- 修复了某些窗口被隐藏在其他应用后面的问题。
- 修复了虚拟机已正确启动但 Docker 状态仍显示为黄色/动态的问题。
- 修复了 Mac 版 Docker 被错误报告为已更新的问题。
- 频道现在显示在“关于”框中。
- 崩溃报告通过 Bugsnag 而非 HockeyApp 发送。
- 修复了某些窗口无法正确获得焦点的问题。
- 增加了切换频道时的 UI，以防止用户丢失容器和设置。
- 在导入 Toolbox 之前检查磁盘容量。
- 在 `etc/ssl/certs/ca-certificates.crt` 中导入证书。
- 磁盘：使针对类数据库工作负载的“刷新（flush）”行为可配置。这解决了 1.12.1 中的性能下降问题。

**网络**

- 代理：修复了容器重启时系统或自定义代理设置的应用问题。
- DNS：减少宿主机上消耗的 UDP 套接字数量。
- VPNkit：改进了连接限制代码，以避免耗尽宿主机上的套接字。
- UDP：处理大于 2035 字节的数据报，直至达到配置的 macOS 内核限制。
- UDP：使转发更加健壮；丢弃异常包并继续运行，而不是停止运行。

**文件共享**

- osxfs：修复了对只读文件或 mode 0 文件执行 chown 的禁令（修复了 [docker/for-mac#117](https://github.com/docker/for-mac/issues/117)、[#263](https://github.com/docker/for-mac/issues/263)、[#633](https://github.com/docker/for-mac/issues/633)）。
- osxfs：修复了导致某些读取操作无限期运行的竞态条件。
- osxfs：修复了可能导致崩溃的并发卷挂载竞态条件。

**Moby**

- 增加了 `memlock` 的默认 `ulimit` 限制（修复了 [docker/for-mac#801](https://github.com/docker/for-mac/issues/801)）。

### Docker for Mac 1.12.1, 2016-09-16

**新特性**

* 支持 macOS 10.12 Sierra。

**升级**

* Docker 1.12.1
* Docker machine 0.8.1
* Linux 内核 4.4.20
* AUFS 20160905

**错误修复与微调**

**常规**

* 修复了 UI 与 `com.docker.vmnetd` 通信时的闪断。修复了 [docker/for-mac#90](https://github.com/docker/for-mac/issues/90)。
* `docker-diagnose`：显示并记录捕获诊断信息的时间。
* 不要在 `com.docker.vmnetd` 中计算容器文件夹。修复了 [docker/for-mac#47](https://github.com/docker/for-mac/issues/47)。
* 警告用户是否安装了 BlueStacks（可能导致内核恐慌）。
* 自动更新间隔从 1 小时改为 24 小时。
* 包含 Zsh 补全脚本。
* UI 修复。

**网络**

* VPNKit 支持搜索域。
* `slirp`：支持多达 8 个外部 DNS 服务器。
* `slirp`：减少了 UDP NAT 使用的套接字数量，降低了 NAT 规则过早超时的概率。
* `/etc/hosts` 中的条目现在应能从容器内部解析。
* 允许端口绑定在 `0.0.0.0` 和 `127.0.0.1` 之外的宿主机地址上。修复了 [docker/for-mac#68](https://github.com/docker/for-mac/issues/68) 中报告的问题。
* 使用 Mac 系统配置数据库检测 DNS。

**文件共享 (osxfs)**

* 修复了线程泄漏。
* 修复了新目录与仍处于打开状态的旧目录同名时发生的功能异常。
* 重命名事件现在会触发 `inotify` 的 DELETE 和/或 MODIFY 事件（现在使用 TextEdit 保存已正常工作）。
* 修复了导致 `inotify` 失败和崩溃的问题。
* 修复了目录文件描述符泄漏。
* 修复了套接字 `chowns`。

**Moby**

* 使用默认 `sysfs` 设置，禁用了透明大页（Transparent Huge Pages）。
* `cgroup` 挂载以支持容器中的 `systemd`。
* 将 Moby 的 `fs.file-max` 增加到 524288。
* 修复了 Moby 诊断和内核更新。

**HyperKit**

* HyperKit 更新了 `dtrace` 支持和锁修复。

### Docker for Mac 2016-08-11 1.12.0-a 修正版

此版本包含 osxfs 的改进。

修复的问题可能曾表现为容器中 `apt-get` 和 `npm` 的失败、丢失 `inotify` 事件或意外的卸载。

**错误修复**

* osxfs：修复了导致访问已重命名目录的子项失败的问题（症状：npm 失败、apt-get 失败）。
* osxfs：修复了导致某些 ATTRIB 和 CREATE inotify 事件交付失败以及其他 inotify 事件停止的问题。
* osxfs：修复了当挂载目录的父级目录被挂载时导致所有 inotify 事件停止的问题。
* osxfs：修复了导致在其他挂载下挂载的卷自发卸载的问题。


### Docker for Mac 1.12.0, 2016-07-28 稳定版

**组件**

* Docker 1.12.0
* Docker Machine 0.8.0
* Docker Compose 1.8.0
