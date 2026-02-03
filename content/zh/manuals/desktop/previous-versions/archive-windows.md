---
description: Windows 版 Docker Desktop 较旧版本的发行说明
keywords: Docker Desktop for Windows, release notes, 发行说明
title: 历史版本发行说明
toc_min: 1
toc_max: 2
aliases:
- /desktop/windows/release-notes/archive/
sitemap: false
---

本页包含 Windows 版 Docker Desktop 较旧版本的发行说明。

## 2018 年稳定版

### Docker Community Edition 18.06.1-ce-win73 2018-08-29

* 升级
  - [Docker 18.06.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.1-ce)

* 错误修复与微调
  - 修复了虚拟机活动检测中的 Bug，防止 Docker Desktop 无法启动。修复了 [docker/for-win#2404](https://github.com/docker/for-win/issues/2404)。
  - 修复了检测 Windows 服务未运行时的 Bug，并建议重启服务。
  - 修复了容器内部无法解析本地 DNS 的问题。修复了 [docker/for-win#2301](https://github.com/docker/for-win/issues/2301)、[docker/for-win#2304](https://github.com/docker/for-win/issues/2304)。
  - 修复了恢复出厂设置后 Kubernetes 状态的显示问题。
  - 修复了在某些情况下无法解析 `host.docker.internal` 的 Bug。修复了 [docker/for-win#2402](https://github.com/docker/for-win/issues/2402)。
  - 使用 1MB 的 vhdx 块大小，而不是默认的 32MB。参见 [docker/for-win#244](https://github.com/docker/for-win/issues/244)。另请参阅 [Microsoft 在 Hyper-V 上运行 Linux 的最佳实践](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/best-practices-for-running-linux-on-hyper-v)。
  - 修复了 Windows 服务未启动时的特定诊断场景。
  - 更改了 Samba 默认文件权限，以避免权限过大的问题。修复了 [docker/for-win#2170](https://github.com/docker/for-win/issues/2170)。
  - 在 RS5 Insider 版本上，修复了错误检测到缺失“Containers”功能并要求安装后重启的问题。

### Docker Community Edition 18.06.0-ce-win72 2018-07-26

* 新特性
  - 更新了签名证书。在更新后的证书被列入允许列表之前，安装程序可能会显示 Windows Defender 弹窗。点击“更多信息 (More info)”以查看应用是由 “Docker Inc” 发布的并运行。

* 错误修复与微调
  - 修复了启动 Docker Desktop 时，如果“Hyper-V”和“Containers” Windows 功能尚未启用，自动启用功能的 Bug。

### Docker Community Edition 18.06.0-ce-win70 2018-07-25

* 升级
  - [Docker 18.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.0-ce)
  - [Docker Machine 0.15.0](https://github.com/docker/machine/releases/tag/v0.15.0)
  - [Docker Compose 1.22.0](https://github.com/docker/compose/releases/tag/1.22.0)
  - [LinuxKit v0.4](https://github.com/linuxkit/linuxkit/releases/tag/v0.4)
  - Linux 内核 4.9.93，启用了 CEPH、DRBD、RBD、MPLS_ROUTING 和 MPLS_IPTUNNEL

* 新特性
  - **Kubernetes 支持**：您现在可以从 Windows 版 Docker 设置中的“Kubernetes”面板运行单节点 Kubernetes 集群，并使用 kubectl 命令以及 Docker 命令。参见 [Kubernetes 章节](/manuals/desktop/features/kubernetes.md)。

* 错误修复与微调
  - AUFS 存储驱动程序在 Docker Desktop 中已被弃用，且 AUFS 支持将在下一个主要版本中移除。您可以在 Docker Desktop 18.06.x 中继续使用 AUFS，但在更新到下一个主要版本之前，您需要重置磁盘镜像（在 Settings > Reset 菜单中）。您可以查看文档以 [保存镜像](/reference/cli/docker/image/save/#examples) 和 [备份卷](/manuals/engine/storage/volumes.md#备份-还原或迁移数据卷)。
  - 修复了某些情况下导致虚拟机日志被写入 RAM 而非磁盘，从而导致虚拟机挂起的 Bug。
  - 修复了与 Docker 服务的命名管道连接相关的安全问题。
  - 修复了 VPNKit 内存泄漏。修复了 [docker/for-win#2087](https://github.com/docker/for-win/issues/2087)、[moby/vpnkit#371](https://github.com/moby/vpnkit/issues/371)。
  - 修复了在最新的 1709 Windows 更新上使用 Windows 快速启动时的重启问题。修复了 [docker/for-win#1741](https://github.com/docker/for-win/issues/1741)。
  - DNS 名称 `host.docker.internal` 可用于从 Windows 容器解析宿主机。修复了 [docker/for-win#1976](https://github.com/docker/for-win/issues/1976)。
  - 修复了诊断窗口中损坏的链接。
  - 在虚拟机内部为 docker-ce 日志添加了日志轮转。
  - 更改了 SMB 权限，以避免在容器中尝试由不同用户操作文件时出现的问题。修复了 [docker/for-win#2170](https://github.com/docker/for-win/issues/2170)。

### Docker Community Edition 18.03.1-ce-win65 2018-04-30

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker Compose 1.21.1](https://github.com/docker/compose/releases/tag/1.21.1)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* 错误修复与微调
  - 修复了当 HOME 环境变量已定义时（通常从命令行启动）的启动失败问题。修复了 [docker/for-win#1880](https://github.com/docker/for-win/issues/1880)。
  - 修复了因与其他程序（如 Razer Synapse 3）不兼容导致的启动失败问题。修复了 [docker/for-win#1723](https://github.com/docker/for-win/issues/1723)。

### Docker Community Edition 18.03.1-ce-win64 2018-04-26

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker Compose 1.21.0](https://github.com/docker/compose/releases/tag/1.21.0)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* 错误修复与微调
  - 修复了当 HOME 环境变量已定义时（通常从命令行启动）的启动失败问题。修复了 [docker/for-win#1880](https://github.com/docker/for-win/issues/1880)。
  - 修复了因与其他程序（如 Razer Synapse 3）不兼容导致的启动失败问题。修复了 [docker/for-win#1723](https://github.com/docker/for-win/issues/1723)。

### Docker Community Edition 18.03.0-ce-win59 2018-03-26

* 升级
  - [Docker 18.03.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.0-ce)
  - [Docker Machine 0.14.0](https://github.com/docker/machine/releases/tag/v0.14.0)
  - [Docker Compose 1.20.1](https://github.com/docker/compose/releases/tag/1.20.1)
  - [Notary 0.6.0](https://github.com/docker/notary/releases/tag/v0.6.0)
  - Linux 内核 4.9.87
  - AUFS 20180312

* 新特性
  - 虚拟机磁盘大小现在可以在设置中更改。修复了 [docker/for-win#105](https://github.com/docker/for-win/issues/105)。
  - 虚拟机交换空间（Swap）大小现在可以在设置中更改。
  - 新增重启 Docker 的菜单项。
  - 支持 NFS 卷共享。参见 [docker/for-win#1700](https://github.com/docker/for-win/issues/1700)。
  - 允许在安装期间激活 Windows 容器（在仅使用 Windows 容器时，避免创建虚拟机磁盘和启动虚拟机）。参见 [docker/for-win#217](https://github.com/docker/for-win/issues/217)。
  - 实验性功能：LCOW 容器现在可以与 Windows 容器并排运行（在 Windows RS3 内部版本 16299 及更高版本上）。在 Windows 容器模式下使用 `--platform=linux` 运行 Windows 上的 Linux 容器。请注意，LCOW 处于实验阶段，需要开启守护进程的 `experimental` 选项。

* 错误修复与微调
  - 修复了 Windows 10 内部版本 16299 在 KB4074588 之后的 Windows 容器端口转发问题。修复了 [docker/for-win#1707](https://github.com/docker/for-win/issues/1707)、[docker/for-win#1737](https://github.com/docker/for-win/issues/1737)。
  - 修复了设置 TLS 相关选项时守护进程无法正常启动的问题。
  - 容器解析宿主机应使用 DNS 名称 `host.docker.internal`。旧的别名（仍有效）已被弃用，建议改用此名称。（参见 https://tools.ietf.org/html/draft-west-let-localhost-be-localhost-06）。
  - 修复了使用 "localhost" 名称（例如 `host.docker.internal`）时的 HTTP/S 透明代理问题。修复了 [docker/for-win#1130](https://github.com/docker/for-win/issues/1130)。
  - 修复了 LinuxKit 在 Windows RS4 Insider 版本上的启动问题。修复了 [docker/for-win#1458](https://github.com/docker/for-win/issues/1458)、[#1514](https://github.com/docker/for-win/issues/1514)、[#1640](https://github.com/docker/for-win/issues/1640)。
  - 修复了权限提升风险。(https://www.tenable.com/sc-report-templates/microsoft-windows-unquoted-service-path-vulnerability)
  - 现在 `docker-users` 组中的所有用户都可以使用 Docker。修复了 [docker/for-win#1732](https://github.com/docker/for-win/issues/1732)。
  - Windows 版 Docker 安装程序不再建议迁移 Docker Toolbox 镜像（仍可手动迁移 Toolbox 镜像）。
  - 优化了重置/卸载时 Windows 容器和镜像的清理工作。修复了 [docker/for-win#1580](https://github.com/docker/for-win/issues/1580)、[#1544](https://github.com/docker/for-win/issues/1544)、[#191](https://github.com/docker/for-win/issues/191)。
  - 安装程序中创建桌面图标为可选；升级时不再重复创建桌面图标（下次升级生效）。修复了 [docker/for-win#246](https://github.com/docker/for-win/issues/246)、[#925](https://github.com/docker/for-win/issues/925)、[#1551](https://github.com/docker/for-win/issues/1551)。

### Docker Community Edition 17.12.0-ce-win47 2018-01-12

* 错误修复与微调
  - 修复了 LinuxKit 端口转发器有时无法启动的问题。修复了 [docker/for-win#1506](https://github.com/docker/for-win/issues/1506)。
  - 修复了连接私有注册表时的证书管理问题。修复了 [docker/for-win#1512](https://github.com/docker/for-win/issues/1512)。
  - 修复了使用 `-v //c/...` 挂载驱动器时的挂载兼容性问题，现在挂载在 LinuxKit 虚拟机中的 `/host_mnt/c` 下。修复了 [docker/for-win#1509](https://github.com/docker/for-win/issues/1509)、[#1516](https://github.com/docker/for-win/issues/1516)、[#1497](https://github.com/docker/for-win/issues/1497)。
  - 修复了显示 Edge 版本的图标问题。修复了 [docker/for-win#1508](https://github.com/docker/for-win/issues/1508)。

### Docker Community Edition 17.12.0-ce-win46 2018-01-09

* 升级
  - [Docker 17.12.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.12.0-ce)
  - [Docker Compose 1.18.0](https://github.com/docker/compose/releases/tag/1.18.0)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)
  - Linux 内核 4.9.60

* 新特性
  - 虚拟机完全由 LinuxKit 构建。
  - 为 Windows 增加了 localhost 端口转发器（感谢 @simonferquel）。在可用时使用 Microsoft 的 localhost 端口转发器（RS4 Insider 内部版本）。

* 错误修复与微调
  - 在“关于”框中显示各种组件的版本。
  - 修复了用户名包含空格时的 vpnkit 问题。参见 [docker/for-win#1429](https://github.com/docker/for-win/issues/1429)。
  - 诊断改进：在虚拟机关闭前获取其日志。
  - 修复了安装程序针对不受支持的 Windows `CoreCountrySpecific` 版本的检查。
  - 修复了由于数据库启动失败导致的一类启动失败问题。参见 [docker/for-win#498](https://github.com/docker/for-win/issues/498)。
  - 更新变更日志中的链接现在通过默认浏览器打开，而不是 IE。（修复了 [docker/for-win#1311](https://github.com/docker/for-win/issues/1311)）。

## 2017 年稳定版

### Docker Community Edition 17.09.1-ce-win42 2017-12-11

* 升级
  - [Docker 17.09.1-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.1-ce)
  - [Docker Compose 1.17.1](https://github.com/docker/compose/releases/tag/1.17.1)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)

* 错误修复与微调
  - 修复了 Windows 快速启动过程中的 Bug。修复了 [for-win/#953](https://github.com/docker/for-win/issues/953)。
  - 修复了卸载程序问题（在某些特定情况下 `dockerd` 进程未被正确杀死）。
  - 修复了净推荐值（NPS）GUI Bug。修复了 [for-win/#1277](https://github.com/docker/for-win/issues/1277)。
  - 修复了 `docker.for.win.localhost` 在代理设置中不起作用的问题。修复了 [for-win/#1130](https://github.com/docker/for-win/issues/1130)。
  - 将虚拟机引导启动的超时时间增加到 2 分钟。


### Docker Community Edition 17.09.0-ce-win33 2017-10-06

* 错误修复
  - 修复了 Windows 版 Docker 在某些情况下无法启动的问题：移除了有时会导致 vpnkit 进程退出的 libgmp 使用。

### Docker Community Edition 17.09.0-ce-win32 2017-10-02

* 升级
  - [Docker 17.09.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.0-ce)
  - [Docker Compose 1.16.1](https://github.com/docker/compose/releases/tag/1.16.1)
  - [Docker Machine 0.12.2](https://github.com/docker/machine/releases/tag/v0.12.2)
  - [Docker Credential Helpers 0.6.0](https://github.com/docker/docker-credential-helpers/releases/tag/v0.6.0)
  - Linux 内核 4.9.49
  - AUFS 20170911

* 新特性
  - Windows Docker 守护进程现在作为服务启动，以实现更好的生命周期管理。
  - 将 Linux 守护进程配置存储在 `~\.docker\daemon.json` 中，而不是设置文件中。
  - 将 Windows 守护进程配置存储在 `C:\ProgramData\Docker\config\daemon.json` 中，而不是设置文件中。
  - VPNKit：增加了对 ping 的支持！
  - VPNKit：增加了 `slirp/port-max-idle-timeout` 选项，允许调整甚至禁用超时。
  - VPNKit：现在所有平台默认均为桥接模式。
  - 在更新窗口中增加了“跳过此版本”按钮。

* 安全修复
  - VPNKit：安全修复，降低了 DNS 缓存中毒攻击的风险（由 Hannes Mehnert 报告 https://hannes.nqsb.io/）。

* 错误修复与微调
  - 内核：启用了 `TASK_XACCT` 和 `TASK_IO_ACCOUNTING`。
  - 增加了虚拟机内日志轮转的频率 ([docker/for-win#244](https://github.com/docker/for-win/issues/244))。
  - “恢复为默认设置”会停止所有引擎并移除设置，包括所有 `daemon.json` 文件。
  - 优化了后端服务检查（与 https://github.com/docker/for-win/issues/953 相关）。
  - 修复了自动更新复选框，无需重启应用程序。
  - 修复了当自动更新被禁用时的“检查更新”菜单。
  - VPNKit：在 ICMP 权限被拒绝时不阻塞启动。（修复了 [docker/for-win#1036](https://github.com/docker/for-win/issues/1036)、[#1035](https://github.com/docker/for-win/issues/1035)、[#1040](https://github.com/docker/for-win/issues/1040)）。
  - VPNKit：更改协议以支持从服务器传回的错误消息。
  - VPNKit：修复了如果相应的 TCP 连接空闲超过 5 分钟会导致套接字泄漏的 Bug（与 [docker/for-mac#1374](https://github.com/docker/for-mac/issues/1374) 相关）。
  - VPNKit：改进了 UNIX 域套接字连接周围的日志记录。
  - VPNKit：自动修剪整数或布尔值数据库键中的空格。
  - 启动时不再尝试将凭据移入凭据存储。

### Docker Community Edition 17.06.2-ce-win27 2017-09-06

* 升级
  - [Docker 17.06.2-ce](https://github.com/docker/docker-ce/releases/tag/v17.06.2-ce)
  - [Docker Machine 0.12.2](https://github.com/docker/machine/releases/tag/v0.12.2)

### Docker Community Edition 17.06.1-ce-rc1-win24 2017-08-24

**升级**

- [Docker 17.06.1-ce-rc1](https://github.com/docker/docker-ce/releases/tag/v17.06.1-ce-rc1)
- Linux 内核 4.9.36
- AUFS 20170703

**错误修复与微调**

- 修复了锁定的容器 ID 文件（修复了 [docker/for-win#818](https://github.com/docker/for-win/issues/818)）。
- 避免在 PATH 环境变量中展开变量（修复了 [docker/for-win#859](https://github.com/docker/for-win/issues/859)）。

### Docker Community Edition 17.06.0-ce-win18 2017-06-28

**升级**

- [Docker 17.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.06.0-ce)
- [Docker Credential Helpers 0.5.2](https://github.com/docker/docker-credential-helpers/releases/tag/v0.5.2)
- [Docker Machine 0.12.0](https://github.com/docker/machine/releases/tag/v0.12.0)
- [Docker Compose 1.14.0](https://github.com/docker/compose/releases/tag/1.14.0)
- Linux 内核 4.9.31

**新特性**

- 支持 Windows Server 2016。
- Windows 10586 已被标记为弃用；在未来的稳定版中将不再支持。
- 与 Docker Cloud 集成：支持通过本地命令行界面 (CLI) 控制远程 Swarm 并查看您的存储库。
- Docker CLI 与 Docker Hub、Docker Cloud 之间的统一登录。
- 支持按需共享驱动器，即在首次请求挂载时进行共享。
- 增加了针对宿主机的实验性 DNS 名称：`docker.for.win.localhost`。
- 支持客户端（即“登录”）证书用于验证注册表访问（修复了 [docker/for-win#569](https://github.com/docker/for-win/issues/569)）。
- 全新的安装程序体验。

**错误修复与微调**

- 修复了使用 Active Directory 登录用户的组访问权限检查（修复了 [docker/for-win#785](https://github.com/docker/for-win/issues/785)）。
- 检查了环境变量，并在日志中添加了一些可能导致 Docker 运行失败的警告。
- 许多以前以管理员模式运行的进程现在在用户身份下运行。
- 云联盟命令行现在在用户家目录下打开。
- 命名管道现在以更严格的安全描述符创建，以提高安全性。
- 安全修复：用户必须属于特定组 `docker-users` 才能运行 Windows 版 Docker。
- “恢复为默认设置 / 卸载”操作也会重置 Docker CLI 设置并注销 Docker Cloud 和注册表用户。
- 检测到一项阻止 Windows 容器运行的 BitLocker 策略。
- 修复了在 vmswitch 接口上被显式禁用时的文件共享问题。
- 修复了当机器名称过长时虚拟机无法启动的问题。
- 修复了未写入 Windows `daemon.json` 文件的 Bug（修复了 [docker/for-win#670](https://github.com/docker/for-win/issues/670)）。
- 为内核添加了补丁以修复 VMBus 崩溃问题。
- 命名管道客户端连接在执行带有标准输入（stdin）数据的 `docker run` 时不应再触发死锁。
- 当 Docker 客户端请求升级为原始流时，缓冲数据应得到正确处理。

### Docker Community Edition 17.03.1-ce-win12  2017-05-12

**升级**

- 修复了 CVE-2017-7308 安全问题。

### Docker Community Edition 17.03.0, 2017-03-02

**新特性**

- 重命名为 Docker Community Edition。
- 与 Docker Cloud 集成：通过本地 CLI 控制远程 Swarm 并查看您的存储库。此功能将逐步向所有用户推出。

**升级**

- [Docker 17.03.0-ce](https://github.com/docker/docker/releases/tag/v17.03.0-ce)
- [Docker Compose 1.11.2](https://github.com/docker/compose/releases/tag/1.11.2)
- [Docker Machine 0.10.0](https://github.com/docker/machine/releases/tag/v0.10.0)
- Linux 内核 4.9.12

**错误修复与微调**

- 通过 ID 而非名称匹配 Hyper-V 集成服务。
- 在服务停止时不再消耗 100% 的 CPU。
- 上传时记录诊断 ID。
- 改进了防火墙处理：停止列出规则，因为这会消耗大量时间。
- 当期望的引擎无法启动时，不再回滚到上一个引擎。
- 不要在 Linux 虚拟机内部使用 4222 端口。
- 修复了 `Set-VMFirmware` 中 `ObjectNotFound` 的启动错误。
- 配置防火墙时增加了详细日志。
- 增加了指向实验性功能文档的链接。
- 修复了“关于”对话框中的版权信息。
- VPNKit：修复了包含“指向标签的指针的指针”的 DNS 报文的解析问题。
- VPNKit：在来自缓存的 DNS 响应中设置“递归可用”位。
- VPNKit：避免诊断信息捕获过多数据。
- VPNKit：修复了虚拟以太网链路上偶尔发生的数据包丢失（截断）源。
- 修复了通过内核更新协商 TimeSync 协议版本的问题。

### Docker for Windows 1.13.1, 2017-02-09

- [Docker 1.13.1](https://github.com/docker/docker/releases/tag/v1.13.1)
- [Docker Compose 1.11.1](https://github.com/docker/compose/releases/tag/1.11.1)
- Linux 内核 4.9.8

**错误修复与微调**

- 添加了指向实验性功能的链接。
- 新的 1.13 可取消操作现在应能由桌面版 Docker 正确处理。
- 修复了各种拼写错误。
- 修复了 Hyper-V 虚拟机设置（应能修复 `ObjectNotFound` 错误）。

### Docker for Windows 1.13.0, 2017-01-19
- [Docker 1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)
- [Docker Compose 1.10](https://github.com/docker/compose/releases/tag/1.10.0)
- [Docker Machine 0.9.0](https://github.com/docker/machine/releases/tag/v0.9.0)
- [Notary 0.4.3](https://github.com/docker/notary/releases/tag/v0.4.3)
- Linux 内核 4.9.4

**新特性**

- 支持 Windows 容器。
- 改进了 `daemon.json` 编辑的 UI。
- 包含镜像和非宿主机挂载卷的 VHDX 文件现在可以移动（通过 UI 中的“Advanced”选项卡）。
- 通过 QEMU 支持 ARM、aarch64、ppc64le 架构。
- 磁盘支持 TRIM（收缩虚拟磁盘）。
- 宿主机从睡眠模式唤醒后，强制执行虚拟机的时间同步。
- Docker 实验性模式可以切换。

**错误修复与微调**

- 改进了代理 UI。
- 改进了日志和诊断。
- “关于”框现已支持复制/粘贴。
- 优化了驱动器共享代码。
- 优化了引导过程。
- 修复了 Trend Micro Office Scan 导致 API 代理认为未共享任何驱动器的问题。
- 显示指向虚拟化文档的链接。
- 恢复出厂设置时始终移除磁盘。
- VPNKit：改进了诊断。
- VPNKit：转发的 UDP 数据报具有正确的源端口号。
- VPNKit：如果一个请求失败，允许其他并发请求成功。例如，这允许在 IPv6 损坏时 IPv4 服务器仍能工作。
- VPNKit：修复了可能导致连接追踪低估活跃连接数量的 Bug。
- VPNKit：增加了 DNS 响应的本地缓存。

## 2016 年稳定版

### Docker for Windows 1.12.5, 2016-12-20
- Docker 1.12.5
- Docker Compose 1.9.0

### 跳过 Docker for Windows 1.12.4

我们没有发布 1.12.4 稳定版。

### Docker for Windows 1.12.3, 2016-11-09

**新特性**

- 在用户更改配置后恢复虚拟机的配置。
- 检测可能阻塞文件共享的防火墙配置。
- 发送更多 GUI 使用统计信息以帮助我们改进产品。
- Hyper-V 磁盘的路径不再硬编码，使 Toolbox 导入支持非标准路径。
- 验证所有 Hyper-V 特性均已启用。
- 在日志中增加了 Moby 控制台输出。
- 将当前引擎状态随其他设置一同保存。
- 已安装 Notary 0.4.2 版本。
- 重新设计了文件共享对话框及底层机制：
  - 自动填充用户名。
  - 用户名/密码无效时，反馈更快、更可靠。
  - 更好地支持域用户。
  - 增加了文件共享因其他原因失败时的日志错误消息。

**升级**

- Docker 1.12.3
- Linux 内核 4.4.27
- Docker Machine 0.8.2
- Docker Compose 1.8.1
- AUFS 20160912

**错误修复与微调**

**常规**

- 在诊断信息中增加了设置数据。
- 确保不使用来自 GAC 的旧版 NLog 库。
- 修复了一个密码转义的回归问题。
- 支持向数据库写入大型数值，特别是针对受信任的 CA。
- 保留了 PowerShell 的堆栈追踪。
- 在每个日志文件顶部写入操作系统和应用程序版本。
- 如果仅设置了 DNS 服务器，则不重新创建虚拟机。
- 如果无法正常停止服务，卸载程序现在会强制杀死该服务。
- 改进了调试信息。

**网络**

- VPNKit 现在会在停止后自动重启。
- VPNKit：实施了连接限制以避免耗尽文件描述符。
- VPNKit：处理大于 2035 字节的 UDP 数据报。
- VPNKit：减少了 DNS 消耗的文件描述符数量。

**文件共享**

- 加快了共享驱动器的挂载/卸载速度。
- 为共享驱动器的挂载/卸载增加了超时机制。

**Hyper-V**

- 确保不使用无效的 "DockerNat" 交换机。

**Moby**

- 增加了 `memlock` 的默认 `ulimit` 限制（修复了 [https://github.com/docker/for-mac/issues/801](https://github.com/docker/for-mac/issues/801)）。

### Docker for Windows 1.12.1, 2016-09-16

**新特性**

* 为透明支持受信任注册表，Windows 宿主机上所有受信任的 CA（根或中间 CA）会自动复制到 Moby。
* “重置凭据 (Reset Credentials)” 也会取消共享已共享的驱动器。
* 日志现在每天轮转。
* 支持多个 DNS 服务器。
* 增加了 `mfsymlinks` SMB 选项，以在绑定挂载文件夹上支持符号链接。
* 增加了 `nobrl` SMB 选项，以在绑定挂载文件夹上支持 `sqlite`。
* 检测过时版本的 Kitematic。

**升级**

* Docker 1.12.1
* Docker machine 0.8.1
* Linux 内核 4.4.20
* AUFS 20160905

**错误修复与微调**

**常规**

* 上传诊断信息现在会在设置中显示正确的状态消息。
* 升级后 Docker 不再询问是否从 Toolbox 导入。
* Docker 现在可以在 Hyper-V 激活后立即从 Toolbox 导入。
* 在诊断信息中增加了更多调试信息。
* 当 Mixpanel 不可用时，发送匿名统计信息不再导致挂起。
* 发行说明支持换行符。
* 改进了 Docker 守护进程未响应时的错误消息。
* 配置数据库现在存储在内存中。
* 保留了 PowerShell 错误堆栈追踪。
* 在错误窗口中显示服务堆栈追踪。

**网络**

* 改进了名称服务器发现。
* VPNKit 支持搜索域。
* VPNKit 现在使用 OCaml 4.03 而不是 4.02.3 编译。

**文件共享**

* 将 `cifs` 版本设置为 3.02。
* VPNKit：减少了 UDP NAT 使用的套接字数量。
* `slirp`：减少了 UDP NAT 使用的套接字数量，降低了 NAT 规则过早超时的概率。
* 修复了宿主机文件系统共享的密码处理问题。

**Hyper-V**

* 自动禁用导致 Docker 无法启动或使用网络的残留网络适配器。
* 在“恢复出厂设置”时自动删除重复的 MobyLinuxVM。
* 改进了 Hyper-V 的检测和激活机制。

**Moby**

* 修复了 Moby 诊断和内核更新。
* 使用默认 `sysfs` 设置，禁用了透明大页。
* `Cgroup` 挂载以支持容器中的 `systemd`。

**已知问题**

* Docker 会自动禁用残留的网络适配器。移除它们的唯一方法是使用 `devmgmt.msc` 手动操作。

### Docker for Windows 1.12.0, 2016-07-28
 
- 首个稳定版。

**组件**

* Docker 1.12.0
* Docker Machine 0.8.0
* Docker Compose 1.8.0
