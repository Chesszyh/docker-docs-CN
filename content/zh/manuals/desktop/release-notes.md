#### 针对 Windows

- 修复了 WSL 2 中的一个 Bug：如果 Docker Desktop 被暂停、杀死然后重启，启动会挂起，除非先用 `wsl --shutdown` 关闭 WSL。
- 修复了 `wsl.exe` 不在 PATH 中时的 WSL 引擎问题 [docker/for-win#13547](https://github.com/docker/for-win/issues/13547)。
- 修复了 WSL 引擎检测某个 Docker Desktop 发行版驱动器丢失的能力 [docker/for-win#13554](https://github.com/docker/for-win/issues/13554)。
- 缓慢或无响应的 WSL 集成不再阻止 Docker Desktop 启动。修复了 [docker/for-win#13549](https://github.com/docker/for-win/issues/13549)。
- 修复了导致 Docker Desktop 在启动时崩溃的 Bug [docker/for-win#6890](https://github.com/docker/for-mac/issues/6890)。
- 增加了以下安装程序标志：
  - `--hyper-v-default-data-root`：指定 Hyper-V 虚拟机磁盘的默认位置。
  - `--windows-containers-default-data-root`：指定 Windows 容器的默认数据根目录。
  - `--wsl-default-data-root`：指定 WSL 发行版磁盘的默认位置。

## 4.20.1

{{< release-date date="2023-06-05" >}}

### 错误修复与增强

#### 适用于所有平台

- containerd 镜像存储：修复了加载包含证明 (attestations) 的镜像时导致 `docker load` 失败的 Bug。
- containerd 镜像存储：修复了构建过程中的默认镜像导出器。

#### 针对 Windows

- 修复了在非西方语言环境下难以解析宿主机 WSL 版本的 Bug。修复了 [docker/for-win#13518](https://github.com/docker/for-win/issues/13518) 和 [docker/for-win#13524](https://github.com/docker/for-win/issues/13524)。

## 4.20.0

{{< release-date date="2023-05-30" >}}

### 升级

- [Buildx v0.10.5](https://github.com/docker/buildx/releases/tag/v0.10.5)
- [Compose v2.18.1](https://github.com/docker/compose/releases/tag/v2.18.1)
- [Docker Engine v24.0.2](https://docs.docker.com/engine/release-notes/24.0/#2402)
- [Containerd v1.6.21](https://github.com/containerd/containerd/releases/tag/v1.6.21)
- [runc v1.1.7](https://github.com/opencontainers/runc/releases/tag/v1.1.5)

### 错误修复与增强

#### 适用于所有平台

- [Docker Scout CLI](https://docs.docker.com/scout/#docker-scout-cli) 现在会在未提供参数时查找最近构建的镜像。
- 优化了 [Docker Scout CLI](https://docs.docker.com/scout/#docker-scout-cli) 的 `compare` 命令。
- 增加了关于 [2023 年 11 月停止支持 Docker Compose ECS/ACS 集成](https://docs.docker.com/go/compose-ecs-eol/) 的警告。可以使用 `COMPOSE_CLOUD_EOL_SILENT=1` 抑制此警告。
- 修复了一个 HTTP 代理 Bug：即 HTTP 1.0 客户端可能会收到 HTTP 1.1 响应。
- 在 WSL-2 上启用了 Docker Desktop 的增强型容器隔离 (ECI) 功能。该功能随 Docker Business 订阅提供。
- 修复了 **Containers** 表格的一个 Bug：即全新安装 Docker Desktop 后，之前隐藏的列会再次显示。

#### 针对 Mac

- 现在在容器中删除文件后，可以更快速地回收磁盘空间。与 [docker/for-mac#371](https://github.com/docker/for-mac/issues/371) 相关。
- 修复了阻止容器访问 169.254.0.0/16 IP 的 Bug。修复了 [docker/for-mac#6825](https://github.com/docker/for-mac/issues/6825)。
- 修复了 `com.docker.diagnose check` 中即便 vpnkit 预期不运行时也会报其缺失错误的 Bug。与 [docker/for-mac#6825](https://github.com/docker/for-mac/issues/6825) 相关。

#### 针对 Windows

- 修复了导致 WSL 数据无法移动到其他磁盘的 Bug。修复了 [docker/for-win#13269](https://github.com/docker/for-win/issues/13269)。
- 修复了 Docker Desktop 关闭时未停止其 WSL 发行版（docker-desktop 和 docker-desktop-data）导致不必要占用宿主机内存的 Bug。
- 增加了新设置，允许 Windows Docker 守护进程在运行 Windows 容器时使用 Docker Desktop 的内部代理。参见 [Windows 代理设置](/manuals/desktop/settings-and-maintenance/settings.md#代理)。

#### 针对 Linux

- 修复了 Docker Compose V1/V2 兼容性设置的一个问题。

## 4.19.0

{{< release-date date="2023-04-27" >}}

### 新特性

- Docker 引擎和 CLI 更新至 [Moby 23.0](https://github.com/moby/moby/releases/tag/v23.0.0)。
- **Learning Center** 现在支持产品内演练。
- Docker init (Beta) 现在支持 Node.js 和 Python。
- 提升了 macOS 上虚拟机与宿主机之间的网络速度。
- 您现在可以在 Docker Desktop 中检查并分析远程镜像而无需先拉取它们。
- 优化了 **Artifactory images** 视图的易用性和性能。

### 移除

- 移除了 `docker scan` 命令。要继续了解镜像的漏洞以及使用更多功能，请使用全新的 `docker scout` 命令。运行 `docker scout --help` 或 [阅读文档了解更多](/reference/cli/docker/scout/_index.md)。

### 升级

- [Docker Engine v23.0.5](https://docs.docker.com/engine/release-notes/23.0/#2305)
- [Compose 2.17.3](https://github.com/docker/compose/releases/tag/v2.17.3)
- [Containerd v1.6.20](https://github.com/containerd/containerd/releases/tag/v1.6.20)
- [Kubernetes v1.25.9](https://github.com/kubernetes/kubernetes/releases/tag/v1.25.9)
- [runc v1.1.5](https://github.com/opencontainers/runc/releases/tag/v1.1.5)
- [Go v1.20.3](https://github.com/golang/go/releases/tag/go1.20.3)

### 错误修复与增强

#### 适用于所有平台

- 优化了用于对比两个镜像的 `docker scout compare` 命令，现在也设置了别名 `docker scout diff`。
- 在 `docker-compose` 操作失败时为控制面板错误增加了更多详情 ([docker/for-win#13378](https://github.com/docker/for-win/issues/13378))。
- 增加了在安装期间设置 HTTP 代理配置的支持。在 [Mac](/manuals/desktop/setup/install/mac-install.md#通过命令行安装) 和 [Windows](/manuals/desktop/setup/install/windows-install.md#通过命令行安装) 上通过 CLI 安装时，可以使用 `--proxy-http-mode`、`--overrider-proxy-http`、`--override-proxy-https` 和 `--override-proxy-exclude` 标志，或者在 `install-settings.json` 文件中设置对应值。
- Docker Desktop 现在在应用启动时停止覆盖 `.docker/config.json` 中的 `credsStore` 键。请注意，如果您使用自定义凭据辅助程序，那么 CLI 中的 `docker login` 和 `docker logout` 不会影响 UI 是否登录。通常建议通过 UI 登录 Docker，因为 UI 支持多重身份验证。
- 增加了关于 [即将从 Docker Desktop 中移除 Compose V1](/manuals/compose/releases/migrate.md) 的警告。可以使用 `COMPOSE_V1_EOL_SILENT=1` 抑制。
- 在 Compose 配置中，YAML 的布尔字段应为 `true` 或 `false`。弃用的 YAML 1.1 值（如 “on” 或 “no”）现在会产生警告。
- 优化了镜像表格的 UI，允许行使用更多可用空间。
- 修复了端口转发中的各种 Bug。
- 修复了一个 HTTP 代理 Bug：即不带服务器名称指示 (SNI) 记录的 HTTP 请求会被拒绝并报错。

#### 针对 Windows

- 在 Windows 上恢复为对 `etc/hosts` 的完全修补（再次包含 `host.docker.internal` 和 `gateway.docker.internal`）。对于 WSL，此行为由 **General** 选项卡中的新设置控制。修复了 [docker/for-win#13388](https://github.com/docker/for-win/issues/13388) 和 [docker/for-win#13398](https://github.com/docker/for-win/issues/13398)。
- 修复了更新 Docker Desktop 时桌面上出现多余 `courgette.log` 文件的问题。修复了 [docker/for-win#12468](https://github.com/docker/for-win/issues/12468)。
- 修复了“放大”快捷键 (ctrl+=)。修复了 [docker/for-win#13392](https://github.com/docker/for-win/issues/13392)。
- 修复了第二次切换容器类型后托盘菜单无法正确更新的 Bug。修复了 [docker/for-win#13379](https://github.com/docker/for-win/issues/13379)。

#### 针对 Mac

- 提升了在 macOS Ventura 及更高版本上使用 Virtualization framework 时的虚拟机网络性能。Mac 版 Docker Desktop 现在使用 gVisor 代替 VPNKit。要继续使用 VPNKit，请在位于 `~/Library/Group Containers/group.com.docker/settings.json` 的 `settings.json` 文件中添加 `"networkType":"vpnkit"`。
- 修复了卸载时显示错误窗口的 Bug。
- 修复了设置 `deprecatedCgroupv1` 被忽略的 Bug。修复了 [docker/for-mac#6801](https://github.com/docker/for-mac/issues/6801)。
- 修复了 `docker pull` 会返回 `EOF` 的情况。

#### 针对 Linux

- 修复了虚拟机网络运行 24 小时后崩溃的 Bug。修复了 [docker/desktop-linux#131](https://github.com/docker/desktop-linux/issues/131)。

### 安全

#### 适用于所有平台

- 修复了一个安全问题：允许用户通过从其 Docker CLI 配置文件中删除 `credsStore` 键，避开 `registry.json` 强制登录，从而绕过其组织配置的镜像访问管理 (IAM) 限制。仅影响 Docker Business 客户。
- 修复了 [CVE-2023-24532](https://github.com/advisories/GHSA-x2w5-7wp4-5qff)。
- 修复了 [CVE-2023-25809](https://github.com/advisories/GHSA-m8cg-xc2p-r3fc)。
- 修复了 [CVE-2023-27561](https://github.com/advisories/GHSA-vpvm-3wq2-2wvm)。
- 修复了 [CVE-2023-28642](https://github.com/advisories/GHSA-g2j6-57v7-gm8c)。
- 修复了 [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840)。
- 修复了 [CVE-2023-28841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28841)。
- 修复了 [CVE-2023-28842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28842)。

## 4.18.0

{{< release-date date="2023-04-03" >}}

### 新特性

- 根据 [路线图](https://github.com/docker/roadmap/issues/453) 发布了 `docker init` 的首个测试版。
- 增加了新的 **Learning Center** 选项卡，帮助用户入门 Docker。
- 为 Docker Compose 增加了实验性的文件监视（file-watch）命令，可在您编辑并保存代码时自动更新运行中的 Compose 服务。

### 升级

- [Buildx v0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4)
- [Compose 2.17.2](https://github.com/docker/compose/releases/tag/2.17.2)
- [Containerd v1.6.18](https://github.com/containerd/containerd/releases/tag/v1.6.18)，包含针对 [CVE-2023-25153](https://github.com/advisories/GHSA-259w-8hf6-59c2) 和 [CVE-2023-25173](https://github.com/advisories/GHSA-hmfx-3pcx-653p) 的修复。
- [Docker Engine v20.10.24](https://docs.docker.com/engine/release-notes/20.10/#201024)，包含针对 [CVE-2023-28841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28841)、[CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840) 和 [CVE-2023-28842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28842) 的修复。

### 错误修复与增强

#### 适用于所有平台

- [Docker Scout CLI](../scout/_index.md#docker-scout-cli) 现在可以对比两个镜像并显示软件包和漏洞差异。此命令处于 [早期体验 (Early Access)](../release-lifecycle.md) 阶段，未来可能会有变动。
- [Docker Scout CLI](../scout/_index.md#docker-scout-cli) 现在可以使用 `docker scout recommendations` 显示基础镜像更新和补救建议。还可以使用 `docker scout quickview` 命令显示镜像的简短概览。
- 您现在可以直接从 Marketplace 搜索扩展，也可以使用 **全局搜索 (Global Search)**。
- 修复了 `docker buildx` 容器构建器在 24 小时后失去网络访问权限的 Bug。
- 减少了提示用户提供 Docker Desktop 反馈的频率。
- 移除了虚拟机交换空间的最小尺寸限制。
- 在 HTTP 代理排除列表中增加了对子域名匹配、CIDR 匹配、`.` 和 `*.` 的支持。
- 修复了透明 TLS 代理中未设置服务器名称指示 (SNI) 字段时的 Bug。
- 修复了 Docker Desktop 引擎状态消息中的一个语法错误。

### 针对 Windows

- 修复了 `docker run --gpus=all` 挂起的 Bug。修复了 [docker/for-win#13324](https://github.com/docker/for-win/issues/13324)。
- 修复了注册表访问管理策略更新未能下载的 Bug。
- Docker Desktop 现在允许在 `C:` 开启 BitLocker 的情况下使用 Windows 容器。
- 带有 WSL 后端的 Docker Desktop 不再需要 `com.docker.service` 特权服务永久运行。更多信息请参见 [Windows 权限要求](https://docs.docker.com/desktop/windows/permission-requirements/)。

### 针对 Mac

- 修复了 VirtioFS 用户在宿主机存储属性时无法缓存的性能问题。
- Mac 版 Docker Desktop 首次启动时，会向用户显示一个安装窗口，以确认或调整需要特权访问的配置。更多信息请参见 [Mac 权限要求](https://docs.docker.com/desktop/mac/permission-requirements/)。
- 在 **Settings** 中增加了 **Advanced** 选项卡，用户可以在此调整需要特权访问的设置。

### 针对 Linux

- 修复了虚拟机网络运行 24 小时后崩溃的 Bug。[docker/for-linux#131](https://github.com/docker/desktop-linux/issues/131)。

### 安全

#### 适用于所有平台

- 修复了 [CVE-2023-1802](https://www.cve.org/CVERecord?id=CVE-2023-1802)：Artifactory 集成的安全问题导致如果 HTTPS 检查失败，它会回退到通过明文 HTTP 发送注册表凭据。仅开启了 `Access experimental features` 的用户受影响。修复了 [docker/for-win#13344](https://github.com/docker/for-win/issues/13344)。

#### 针对 Mac

- 移除了 `com.apple.security.cs.allow-dyld-environment-variables` 和 `com.apple.security.cs.disable-library-validation` 权限，这些权限曾允许通过 `DYLD_INSERT_LIBRARIES` 环境变量在 Docker Desktop 中加载任意动态库。

### 已知问题

- 从 **Troubleshoot** 页面卸载 Mac 版 Docker Desktop 可能会触发非预期的致命错误弹窗。

## 4.17.1

{{< release-date date="2023-03-20" >}}

### 错误修复与增强

#### 针对 Windows

- Docker Desktop 现在允许在 C: 开启 BitLocker 的情况下使用 Windows 容器。
- 修复了 `docker buildx` 容器构建器在 24 小时后失去网络访问权限的 Bug。
- 修复了注册表访问管理策略更新未能下载的 Bug。
- 优化了调试信息，以更好地表征 WSL 2 下的故障。

### 已知问题

- 在 WSL 2 后端的 Windows 上运行带 `--gpus` 的容器无法工作。这将在未来版本中修复。参见 [docker/for-win/13324](https://github.com/docker/for-win/issues/13324)。

## 4.17.0

{{< release-date date="2023-02-27" >}}

### 新特性

- Docker Desktop 现在内置了 Docker Scout。拉取并查看来自 Docker Hub 和 Artifactory 存储库镜像的分析，获取基础镜像更新及建议的标签和 digest，并根据漏洞信息过滤镜像。欲了解更多，请参阅 [Docker Scout](../scout/_index.md)。
- `docker scan` 已被 `docker scout` 取代。更多信息请参见 [Docker Scout CLI](../scout/_index.md#docker-scout-cli)。
- 您现在可以在扩展市场中发现自主发布的扩展。有关自主发布扩展的更多信息，请参见 [市场扩展 (Marketplace Extensions)](/manuals/extensions/marketplace.md)。
- **Container File Explorer (容器文件资源管理器)** 作为实验性功能推出。直接通过 GUI 调试容器内部的文件系统。
- 您现在可以在 **全局搜索 (Global Search)** 中搜索卷。

### 升级

- [Containerd v1.6.18](https://github.com/containerd/containerd/releases/tag/v1.6.18)，包含针对 [CVE-2023-25153](https://github.com/advisories/GHSA-259w-8hf6-59c2) 和 [CVE-2023-25173](https://github.com/advisories/GHSA-hmfx-3pcx-653p) 的修复。
- [Docker Engine v20.10.23](https://docs.docker.com/engine/release-notes/20.10/#201023)。
- [Go 1.19.5](https://github.com/golang/go/releases/tag/go1.19.5)。

### 错误修复与增强

#### 适用于所有平台

- 修复了收集诊断信息时可能因等待子进程退出而挂起的 Bug。
- 防止透明 HTTP 代理过度改写请求。修复了 Tailscale 扩展登录问题，参见 [tailscale/docker-extension#49](https://github.com/tailscale/docker-extension/issues/49)。
- 修复了透明 TLS 代理中未设置服务器名称指示 (SNI) 字段时的 Bug。
- 在 HTTP 代理排除列表中增加了对子域名匹配、CIDR 匹配、`.` 和 `*.` 的支持。
- 确保在上传诊断信息时遵循 HTTP 代理设置。
- 修复了从凭据辅助程序获取凭据时的致命错误。
- 修复了与并发日志记录相关的致命错误。
- 优化了 Marketplace 中扩展操作的 UI。
- 在扩展市场中增加了新的过滤器。您现在可以按类别和审核状态过滤扩展。
- 增加了向 Docker 举报恶意扩展的途径。
- 将 Dev Environments 更新至 v0.2.2，包含初始设置的可靠性与安全性修复。
- 仅为新用户增加了欢迎调查。
- 故障排除页面上的确认对话框现在与其他类似对话框风格保持一致。
- 修复了在 Kubernetes 集群启动前重置它导致的致命错误。
- 在 containerd 集成中实现了 `docker import`。
- 修复了 containerd 集成中使用现有标签对镜像进行标记的问题。
- 在 containerd 集成中实现了针对镜像的悬空 (dangling) 过滤器。
- 修复了 containerd 集成中 `docker ps` 在处理镜像已不存在的容器时失败的问题。

#### 针对 Mac

- 修复了在未安装特权辅助工具 `com.docker.vmnetd` 的系统上下载注册表访问管理策略的问题。
- 修复了如果 `/Library/PrivilegedHelperTools` 不存在则无法安装 `com.docker.vmnetd` 的 Bug。
- 修复了“系统”代理无法处理“自动代理”/“pac 文件”配置的 Bug。
- 修复了 vmnetd 安装在区分大小写的文件系统上读取 `Info.Plist` 失败的 Bug。实际文件名为 `Info.plist`。修复了 [docker/for-mac#6677](https://github.com/docker/for-mac/issues/6677)。
- 修复了每次启动都提示用户创建 Docker 套接字符号链接的 Bug。修复了 [docker/for-mac#6634](https://github.com/docker/for-mac/issues/6634)。
- 修复了 **Start Docker Desktop when you log in** 设置不起作用的 Bug。修复了 [docker/for-mac#6723](https://github.com/docker/for-mac/issues/6723)。
- 修复了 UDP 连接追踪和 `host.docker.internal`。修复了 [docker/for-mac#6699](https://github.com/docker/for-mac/issues/6699)。
- 优化了 kubectl 符号链接逻辑，使其遵循 `/usr/local/bin` 中现有的二进制文件。修复了 [docker/for-mac#6328](https://github.com/docker/for-mac/issues/6328)。
- 当您选择使用 Rosetta 但尚未安装时，Docker Desktop 现在会自动安装它。

### 针对 Windows

- 增加了对 WSL 集成工具与 `musl` 的静态链接，因此无需在用户发行版中安装 `alpine-pkg-glibc`。
- 增加了对 WSL 2 下 cgroupv2 的支持。通过在 `%USERPROFILE%\.wslconfig` 文件的 `[wsl2]` 部分添加 `kernelCommandLine = systemd.unified_cgroup_hierarchy=1 cgroup_no_v1=all` 即可激活。
- 修复了导致 Docker Desktop 在 WSL 2 模式下卡在“正在启动”阶段的问题（4.16 版本引入）。
- 修复了在 `%LOCALAPPDATA%` 开启了文件系统压缩或加密时 Docker Desktop 无法启动 WSL 2 后端的问题。
- 修复了 Docker Desktop 在启动时无法报告缺失或过时（无法运行 WSL 第 2 版发行版）的 WSL 安装的问题。
- 修复了如果目标路径包含空格，则无法在 Visual Studio Code 中打开的 Bug。
- 修复了导致 `~/.docker/context` 损坏并报 “unexpected end of JSON input” 错误的 Bug。您也可以通过移除 `~/.docker/context` 来解决此问题。
- 确保 WSL 2 中使用的凭据辅助程序已正确签名。与 [docker/for-win#10247](https://github.com/docker/for-win/issues/10247) 相关。
- 修复了导致 WSL 集成代理被错误终止的问题。与 [docker/for-win#13202](https://github.com/docker/for-win/issues/13202) 相关。
- 修复了启动时上下文损坏的问题。修复了 [docker/for-win#13180](https://github.com/docker/for-win/issues/13180) 和 [docker/for-win#12561](https://github.com/docker/for-win/issues/12561)。

### 针对 Linux

- 增加了 Linux 版 Docker Desktop 的 Docker Buildx 插件。
- 将 RPM 和 Arch Linux 发行版的压缩算法更改为 `xz`。
- 修复了导致 Debian 软件包在根目录下留下残留文件的 Bug。修复了 [docker/for-linux#123](https://github.com/docker/desktop-linux/issues/123)。

### 安全

#### 适用于所有平台

- 修复了 [CVE-2023-0628](https://www.cve.org/CVERecord?id=CVE-2023-0628)：该漏洞允许攻击者通过诱导用户打开精心制作的恶意 `docker-desktop://` URL，在初始化期间于 Dev Environments 容器内执行任意命令。
- 修复了 [CVE-2023-0629](https://www.cve.org/CVERecord?id=CVE-2023-0629)：该漏洞允许非特权用户通过 `-H` (`--host`) CLI 标志或 `DOCKER_HOST` 环境变量将 Docker 宿主机设置为 `docker.raw.sock`（Windows 上为 `npipe:////.pipe/docker_engine_linux`），从而绕过增强型容器隔离 (ECI) 限制，启动不带 ECI 额外加固特性的容器。这不影响已在运行的容器，也不影响通过通常方式（不使用 Docker 原始套接字）启动的容器。

## 4.16.3

{{< release-date date="2023-01-30" >}}

### 错误修复与增强

#### 针对 Windows

- 修复了在 `%LOCALAPPDATA%` 开启了文件系统压缩或加密时 Docker Desktop 无法启动 WSL 2 后端的问题。修复了 [docker/for-win#13184](https://github.com/docker/for-win/issues/13184)。
- 修复了 Docker Desktop 在启动时无法报告缺失或过时的 WSL 安装的问题。修复了 [docker/for-win#13184](https://github.com/docker/for-win/issues/13184)。

## 4.16.2

{{< release-date date="2023-01-19" >}}

### 错误修复与增强

#### 适用于所有平台

- 修复了开启 containerd 集成功能后，`docker build` 和 `docker tag` 命令会产生 `image already exists` 错误的问题。
- 修复了 Docker Desktop 4.16 中引入的一个回归问题：在 amd64 系统上破坏了来自目标平台为 linux/386 的容器的网络连接。修复了 [docker/for-mac/6689](https://github.com/docker/for-mac/issues/6689)。

#### 针对 Mac

- 修复了 `Info.plist` 的大小写问题，该问题曾导致 `vmnetd` 在区分大小写的文件系统上损坏。修复了 [docker/for-mac/6677](https://github.com/docker/for-mac/issues/6677)。

#### 针对 Windows

- 修复了 Docker Desktop 4.16 中引入的一个回归问题：导致其在 WSL2 模式下卡在“正在启动”阶段。修复了 [docker/for-win/13165](https://github.com/docker/for-win/issues/13165)。

## 4.16.1

{{< release-date date="2023-01-13" >}}

### 错误修复与增强

#### 适用于所有平台

- 修复了某些镜像在容器内执行 `sudo` 时因安全相关错误而失败的问题。修复了 [docker/for-mac/6675](https://github.com/docker/for-mac/issues/6675) 和 [docker/for-win/13161](https://github.com/docker/for-win/issues/13161)。

## 4.16.0

{{< release-date date="2023-01-12" >}}

### 新特性

- 扩展 (Extensions) 从测试版转为正式发布 (GA)。
- 快速搜索 (Quick Search) 从实验性阶段转为正式发布 (GA)。
- 扩展现已包含在快速搜索中。
- 分析大型镜像的速度提升高达 4 倍。
- 新的本地镜像视图从实验性阶段转为正式发布 (GA)。
- 针对 macOS 13 增加了新的测试版功能：Rosetta for Linux，用于在 Apple 芯片上更快速地模拟运行基于 Intel 的镜像。

### 升级

- [Compose v2.15.1](https://github.com/docker/compose/releases/tag/v2.15.1)
- [Containerd v1.6.14](https://github.com/containerd/containerd/releases/tag/v1.6.14)
- [Docker Engine v20.10.22](https://docs.docker.com/engine/release-notes/20.10/#201022)
- [Buildx v0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0)
- [Docker Scan v0.23.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.23.0)
- [Go 1.19.4](https://github.com/golang/go/releases/tag/go1.19.4)

### 错误修复与增强

#### 适用于所有平台

- 修复了开启 containerd 集成后 `docker build --quiet` 不输出镜像标识符的问题。
- 修复了开启 containerd 集成后镜像检查不显示镜像标签的问题。
- 增加了运行中和已停止容器图标之间的对比度，方便色盲用户扫描容器列表。
- 修复了重复提示用户输入 HTTP 代理凭据直到重启 Docker Desktop 的 Bug。
- 增加了诊断命令 `com.docker.diagnose login` 用以检查 HTTP 代理配置。
- 修复了对 compose 堆栈操作无法正常工作的问题。修复了 [docker/for-mac#6566](https://github.com/docker/for-mac/issues/6566)。
- 修复了 Docker Desktop 控制面板在启动时尝试获取磁盘使用信息并在引擎运行前显示错误横幅的问题。
- 在所有实验性功能旁边增加了包含如何退出实验性功能访问说明的信息横幅。
- Docker Desktop 现在支持通过 HTTP 代理下载 Kubernetes 镜像。
- 修复了工具提示遮挡操作按钮的问题。修复了 [docker/for-mac#6516](https://github.com/docker/for-mac/issues/6516)。
- 修复了 **Container** 视图中空白的 "An error occurred" 容器列表。

#### 针对 Mac

- 安装或更新 macOS 版 Docker Desktop 的最低 OS 版本要求现已提升为 macOS Big Sur (版本 11) 或更高。
- 修复了启用增强型容器隔离且使用旧版 `osxfs` 实现进行文件共享时 Docker 引擎无法启动的问题。
- 修复了在 VirtioFS 上创建的文件带有可执行位的问题。修复了 [docker/for-mac#6614](https://github.com/docker/for-mac/issues/6614)。
- 重新增加了通过命令行卸载 Docker Desktop 的方式。修复了 [docker/for-mac#6598](https://github.com/docker/for-mac/issues/6598)。
- 修复了硬编码的 `/usr/bin/kill`。修复了 [docker/for-mac#6589](https://github.com/docker/for-mac/issues/6589)。
- 修复了在 VirtioFS 上共享的超大文件（> 38GB）在截断（例如使用 `truncate` 命令）时大小显示不正确的问题。
- 更改了 **Settings** 中的磁盘镜像大小单位，使用十进制（以 10 为底）以与访达 (Finder) 显示磁盘容量的方式一致。
- 修复了网络负载下的 Docker 崩溃。修复了 [docker/for-mac#6530](https://github.com/docker/for-mac/issues/6530)。
- 修复了导致 Docker 在每次重启后都提示用户安装 `/var/run/docker.sock` 符号链接的问题。
- 确保安装 `/var/run/docker.sock` 符号链接的登录项已签名。
- 修复了恢复出厂设置时移除 `$HOME/.docker` 的 Bug。

### 针对 Windows

- 修复了 `docker build` 在打印 "load metadata for" 时挂起的问题。修复了 [docker/for-win#10247](https://github.com/docker/for-win/issues/10247)。
- 修复了 `diagnose.exe` 输出中的拼写错误。修复了 [docker/for-win#13107](https://github.com/docker/for-win/issues/13107)。
- 增加了对 WSL 2 下 cgroupv2 运行的支持。通过在 `%USERPROFILE%\.wslconfig` 文件的 `[wsl2]` 部分添加 `kernelCommandLine = systemd.unified_cgroup_hierarchy=1 cgroup_no_v1=all` 即可激活。

### 已知问题

- 某些镜像在容器内执行 `sudo` 会因安全相关错误而失败。参见 [docker/for-mac/6675](https://github.com/docker/for-mac/issues/6675) 和 [docker/for-win/13161](https://github.com/docker/for-win/issues/13161)。

## 4.15.0

{{< release-date date="2022-12-01" >}}

### 新特性

- 为 macOS 用户带来了实质性的性能提升：增加了开启全新 VirtioFS 文件共享技术的选项。适用于 macOS 12.5 及以上版本。
- Mac 版 Docker Desktop 在安装或首次运行时不再需要安装特权辅助进程 `com.docker.vmnetd`。更多信息请参见 [Mac 权限要求](https://docs.docker.com/desktop/mac/permission-requirements/)。
- 增加了 [WebAssembly 能力](/manuals/desktop/features/wasm.md)。请配合 [containerd 集成](/manuals/desktop/features/containerd.md) 使用。
- 优化了测试版和实验性设置的描述，以清晰解释其区别以及用户如何访问。
- Mac 和 Linux 版 Docker Desktop 控制面板的底部栏现在会显示虚拟机的可用磁盘空间。
- 如果可用空间低于 3GB，底部栏会显示磁盘空间警告。
- 调整了 Docker Desktop 的界面，使其更符合 ADA 无障碍标准并在视觉上更加统一。
- 在 **Extensions** 内增加了 **Build** 选项卡，包含构建扩展所需的所有资源。
- 增加了更轻松分享扩展的能力，可以通过 `docker extension share` CLI 或扩展 **Manage** 选项卡中的分享按钮进行。
- 扩展市场中的扩展现在会显示安装次数。您还可以按安装次数对扩展进行排序。
- 开发环境 (Dev Environments) 允许将 Git 仓库克隆到本地绑定挂载，以便您可以使用任何本地编辑器或 IDE。
- 更多 Dev Environments 改进：自定义名称、更好的私有仓库支持、优化的端口处理。

### 升级

- [Compose v2.13.0](https://github.com/docker/compose/releases/tag/v2.13.0)
- [Containerd v1.6.10](https://github.com/containerd/containerd/releases/tag/v1.6.10)
- [Docker Hub Tool v0.4.5](https://github.com/docker/hub-tool/releases/tag/v0.4.5)
- [Docker Scan v0.22.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.22.0)

### 错误修复与增强

#### 适用于所有平台

- 开启 containerd 集成后，容器现在能在重启后恢复。
- 修复了开启 containerd 集成后列出多平台镜像的问题。
- 优化了开启 containerd 集成后对悬空 (dangling) 镜像的处理。
- 在 containerd 集成中实现了镜像的 "reference" 过滤器。
- 增加了在容器、`docker pull` 等场景中通过 `proxy.pac` 自动选择上游 HTTP/HTTPS 代理的支持。
- 修复了拉取时解析镜像引用的回归问题。修复了 [docker/for-win#13053](https://github.com/docker/for-win/issues/13053)、[docker/for-mac#6560](https://github.com/docker/for-mac/issues/6560) 和 [docker/for-mac#6540](https://github.com/docker/for-mac/issues/6540)。

#### 针对 Mac

- 提升了 `docker pull` 的性能。

#### 针对 Windows

- 修复了 Docker 启动且开发人员登录时未应用系统 HTTP 代理的问题。
- 当 Docker Desktop 正在使用“系统”代理且 Windows 设置发生更改时，Docker Desktop 现在无需重启即可应用新的 Windows 设置。

#### 针对 Linux

- 修复了 Linux 上的热重载问题。修复了 [docker/desktop-linux#30](https://github.com/docker/desktop-linux/issues/30)。
- 禁用了 Linux 上的托盘图标动画，修复了部分用户的崩溃问题。

## 4.14.1

{{< release-date date="2022-11-17" >}}

### 错误修复与增强

#### 适用于所有平台

- 修复了使用注册表访问管理时的容器 DNS 查找问题。

#### 针对 Mac

- 修复了阻止 **Images** 选项卡中 **Analyze Image** 按钮工作的问题。
- 修复了如果 `/usr/local/lib` 尚不存在则无法为用户创建符号链接的 Bug。修复了 [docker/for-mac#6569](https://github.com/docker/for-mac/issues/6569)。

## 4.14.0

{{< release-date date="2022-11-10" >}}

### 新特性

- 针对 macOS >= 12.5，将 Virtualization framework 设置为默认虚拟机管理程序。
- 针对 macOS >= 12.5，将旧版本安装迁移至 Virtualization framework 虚拟机管理程序。
- 面向 Docker Business 用户，现在可以在常规设置中启用增强型容器隔离 (Enhanced Container Isolation) 功能。

### 更新

- [Docker Engine v20.10.21](/manuals/engine/release-notes/20.10.md#201021)，包含对 [CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253) 中追踪的 Git 漏洞的缓解，更新了对 `image:tag@digest` 镜像引用的处理，并包含对 [CVE-2022-36109](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-36109) 的修复。
- [Docker Compose v2.12.2](https://github.com/docker/compose/releases/tag/v2.12.2)
- [Containerd v1.6.9](https://github.com/containerd/containerd/releases/tag/v1.6.9)
- [Go 1.19.3](https://github.com/golang/go/releases/tag/go1.19.3)

### 错误修复与增强

#### 适用于所有平台

- Docker Desktop 现在要求内部网络子网大小为 /24。如果您之前使用的是 /28，它会自动扩展为 /24。如果遇到网络问题，请检查 Docker 子网是否与您的基础设施冲突。修复了 [docker/for-win#13025](https://github.com/docker/for-win/issues/13025)。
- 修复了当 Git URL 包含大写字符时阻止用户创建 Dev Environments 的问题。
- 修复了诊断信息中报告的 `vpnkit.exe is not running` 错误。
- 将 qemu 还原至 6.2.0，以修复运行模拟的 amd64 代码时出现的 `PR_SET_CHILD_SUBREAPER is unavailable` 等错误。
- 在扩展 (Extensions) 内部开启了 [contextIsolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation) 和 [sandbox](https://www.electronjs.org/docs/latest/tutorial/sandbox) 模式。现在扩展运行在独立上下文中，通过限制对大多数系统资源的访问来降低恶意代码可能造成的危害。
- 包含了 `unpigz` 以允许对拉取的镜像进行并行解压。
- 修复了对选中容器执行操作的相关问题。[修复：https://github.com/docker/for-win/issues/13005](https://github.com/docker/for-win/issues/13005)。
- 增加了允许为容器或项目视图显示时间戳的功能。
- 修复了使用 Control+C 中断 `docker pull` 时可能发生的段错误。
- 增加了默认的 DHCP 租约时间，以避免虚拟机网络每隔两小时出现闪断和连接丢失。
- 移除了容器列表上的无限加载动画。[修复：https://github.com/docker/for-mac/issues/6486](https://github.com/docker/for-mac/issues/6486)。
- 修复了 **Settings** 中已用空间显示错误数值的 Bug。
- 修复了开启 containerd 集成后 Kubernetes 无法启动的 Bug。
- 修复了开启 containerd 集成后 `kind` 无法启动的 Bug。
- 修复了开启 containerd 集成后 Dev Environments 无法工作的 Bug。
- 在 containerd 集成中实现了 `docker diff`。
- 在 containerd 集成中实现了 `docker run —-platform`。
- 修复了开启 containerd 集成后非安全注册表无法工作的 Bug。

#### 针对 Mac

- 修复了 Virtualization framework 用户启动失败的问题。
- 默认在 Mac 上重新添加了 `/var/run/docker.sock` 符号链接，以增强与 `tilt` 和 `docker-py` 等工具的兼容性。
- 修复了在全新安装的 Mac 上无法创建 Dev Environments 的问题（报错 "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?"）。

#### 针对 Windows

- 重新增加了 `DockerCli.exe -SharedDrives`。修复了 [docker/for-win#5625](https://github.com/docker/for-win#5625)。
- Docker Desktop 现在允许在禁用 PowerShell 的机器上运行 Docker。
- 修复了 Windows 上 Compose v2 未能始终默认启用的问题。
- Docker Desktop 现在在卸载时会删除 `C:\Program Files\Docker` 文件夹。

### 已知问题

- 对于部分 macOS 用户，安装程序存在一个已知问题，导致无法安装实验性的漏洞和软件包发现功能所需的新辅助工具。要修复此问题，需要创建一个符号链接，运行以下命令：`sudo ln -s /Applications/Docker.app/Contents/Resources/bin/docker-index /usr/local/bin/docker-index`。

## 4.13.1

{{< release-date date="2022-10-31" >}}

### 更新

- [Docker Compose v2.12.1](https://github.com/docker/compose/releases/tag/v2.12.1)

### 错误修复与增强

#### 适用于所有平台

- 修复了使用 `Control+C` 或 `CMD+C` 中断 `docker pull` 时可能发生的段错误。
- 增加了默认的 DHCP 租约时间，以避免虚拟机网络每隔两小时出现闪断和连接丢失。
- 将 `Qemu` 还原至 `6.2.0`，以修复运行模拟的 amd64 代码时出现的 `PR_SET_CHILD_SUBREAPER is unavailable` 等错误。

#### 针对 Mac

- 默认在 Mac 上重新添加了 `/var/run/docker.sock` 符号链接，以增强与 `tilt` 和 `docker-py` 等工具的兼容性。修复了 [docker/for-mac#6529](https://github.com/docker/for-mac/issues/6529)。
- 修复了在全新安装的 Mac 上无法创建 Dev Environments 的问题（报错 "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?"）。

#### 针对 Windows

- Docker Desktop 现在可以在禁用 PowerShell 的机器上正常运行。

## 4.13.0

{{< release-date date="2022-10-19" >}}

### 新特性

- 为 Docker Business 用户推出了两项新的安全特性：设置管理 (Settings Management) 和增强型容器隔离 (Enhanced Container Isolation)。欲了解更多，请参阅 Docker Desktop 的全新 [硬化 Docker Desktop 安全模型 (Hardened Docker Desktop security model)](/manuals/security/for-admins/hardened-desktop/_index.md)。
- 增加了全新的 Dev Environments CLI `docker dev`，您可以通过命令行创建、列出并运行 Dev Envs。现在更易于将 Dev Envs 集成到自定义脚本中。
- 现在可以使用 `--installation-dir` 标志将 Docker Desktop 安装到任意驱动器和文件夹。部分解决了 [docker/roadmap#94](https://github.com/docker/roadmap/issues/94)。

### 更新

- [Docker Scan v0.21.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.21.0)
- [Go 1.19.2](https://github.com/golang/go/releases/tag/go1.19.2)，修复了 [CVE-2022-2879](https://www.cve.org/CVERecord?id=CVE-2022-2879)、[CVE-2022-2880](https://www.cve.org/CVERecord?id=CVE-2022-2880) 和 [CVE-2022-41715](https://www.cve.org/CVERecord?id=CVE-2022-41715)。
- 将 Docker 引擎和 Docker CLI 更新至 [v20.10.20](/manuals/engine/release-notes/20.10.md#201020)，包含对 [CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253) 中追踪的 Git 漏洞的缓解，更新了对 `image:tag@digest` 镜像引用的处理，并包含对 [CVE-2022-36109](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-36109) 的修复。
- [Docker Credential Helpers v0.7.0](https://github.com/docker/docker-credential-helpers/releases/tag/v0.7.0)
- [Docker Compose v2.12.0](https://github.com/docker/compose/releases/tag/v2.12.0)
- [Kubernetes v1.25.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.25.2)
- [Qemu 7.0.0](https://wiki.qemu.org/ChangeLog/7.0)，用于 Docker Desktop 虚拟机内的 CPU 模拟。
- [Linux 内核 5.15.49](https://hub.docker.com/layers/docker/for-desktop-kernel/5.15.49-13422a825f833d125942948cf8a8688cef721ead/images/sha256-ebf1f6f0cb58c70eaa260e9d55df7c43968874d62daced966ef6a5c5cd96b493?context=explore)

### 错误修复与增强

#### 适用于所有平台

- Docker Desktop 现在允许在与 HTTP 和 HTTPS 代理通信时使用 TLS 以加密代理用户名和密码。
- Docker Desktop 现在将 HTTP 和 HTTPS 代理密码存储在操作系统的凭据存储中。
- 如果 Docker Desktop 检测到 HTTP 或 HTTPS 代理密码已更改，它将提示开发人员输入新密码。
- **Bypass proxy settings for these hosts and domains** 设置现在可以正确处理针对 HTTPS 的域名。
- **Remote Repositories** 视图和“每日提示 (Tip of the Day)”现在可以配合需要身份验证的 HTTP 和 HTTPS 代理工作。
- 我们为处于产品开发生命周期早期的特性引入了“静默启动 (dark launch)”。已选择加入的用户可以随时在设置的“beta features”部分选择退出。
- 为扩展市场增加了分类功能。
- 在鲸鱼菜单和 **Extension** 选项卡中增加了扩展更新可用的指示器。
- 修复了卸载镜像名称不含命名空间（如 'my-extension'）的扩展时失败的问题。
- 在 **Container** 选项卡中显式显示端口映射。
- 将镜像磁盘占用信息的自动刷新频率改为每天一次。
- 统一了 **Container** 和 **Volume** 选项卡的样式。
- 修复了 **Settings** 中 Grpcfuse 文件共享模式的启用问题。修复了 [docker/for-mac#6467](https://github.com/docker/for-mac/issues/6467)。
- 对于运行 macOS < 12.5 的用户，禁用了 Virtualization Framework 和 VirtioFS。
- **Containers** 选项卡中的端口现在可以点击。
- 扩展 SDK 现在允许 `ddClient.extension.vm.cli.exec`、`ddClient.extension.host.cli.exec`、`ddClient.docker.cli.exec` 通过 options 参数接受不同的工作目录并传递环境变量。
- 增加了一个微小改进：点击侧边栏的 **Extensions** 时将导航至扩展市场。
- 增加了用于识别市场中新扩展的徽章。
- 修复了开启 containerd 集成后 Kubernetes 无法启动的问题。
- 修复了开启 containerd 集成后 `kind` 无法启动的问题。
- 修复了开启 containerd 集成后开发环境无法工作的问题。
- 在 containerd 集成中实现了 `docker diff`。
- 在 containerd 集成中实现了 `docker run —-platform`。
- 修复了开启 containerd 集成后非安全注册表无法工作的问题。
- 修复了 **Settings** 中已用空间显示错误数值的 Bug。
- Docker Desktop 现在从 Github releases 安装凭据辅助程序。参见 [docker/for-win#10247](https://github.com/docker/for-win/issues/10247)、[docker/for-win#12995](https://github.com/docker/for-win/issues/12995)。
- 修复了用户在 7 天后被注销 Docker Desktop 的问题。

#### 针对 Mac

- 为 Docker Desktop 增加了 **Hide**（隐藏）、**Hide others**（隐藏其他）、**Show all**（显示全部）菜单项。参见 [docker/for-mac#6446](https://github.com/docker/for-mac/issues/6446)。
- 修复了从已安装的应用运行安装工具时会导致应用被删除的 Bug。修复了 [docker/for-mac#6442](https://github.com/docker/for-mac/issues/6442)。
- 默认情况下，Docker 不会在宿主机上创建 `/var/run/docker.sock` 符号链接，而是使用 `docker-desktop` CLI 上下文。

#### 针对 Linux

- 修复了阻止从控制面板推送镜像的 Bug。

## 4.12.0

{{< release-date date="2022-09-01" >}}

### 新特性

- 增加了使用 containerd 拉取和存储镜像的能力。这是一项实验性功能。
- Docker Desktop 现在支持运行未打标签的镜像。修复了 [docker/for-mac#6425](https://github.com/docker/for-mac/issues/6425)。
- 为 Docker 扩展市场增加了搜索功能。修复了 [docker/roadmap#346](https://github.com/docker/roadmap/issues/346)。
- 增加了放大、缩小或设置 Docker Desktop 为实际大小的功能。通过使用键盘快捷键 ⌘ + / CTRL +,、⌘ - / CTRL -、⌘ 0 / CTRL 0（分别对应 Mac 和 Windows），或通过 Mac 上的 View 菜单实现。
- 增加了 Compose 停止按钮（如果任何相关容器是可停止的）。
- 现在可以从 **Container** 视图删除单个 Compose 容器。
- 移除了针对 Fedora 35 上 `virtiofsd <-> qemu` 协议不匹配的变通方法，因为已不再需要。Fedora 35 用户应将 qemu 软件包升级到最新版本（截至编写时为 `qemu-6.1.0-15.fc35`）。
- 实现了容器的集成终端。
- 默认情况下，为所有外部链接增加了显示链接地址的工具提示。

### 更新

- [Docker Compose v2.10.2](https://github.com/docker/compose/releases/tag/v2.10.2)
- [Docker Scan v0.19.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.19.0)
- [Kubernetes v1.25.0](https://github.com/kubernetes/kubernetes/releases/tag/v1.25.0)
- [Go 1.19](https://github.com/golang/go/releases/tag/go1.19)
- [cri-dockerd v0.2.5](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.2.5)
- [Buildx v0.9.1](https://github.com/docker/buildx/releases/tag/v0.9.1)
- [containerd v1.6.8](https://github.com/containerd/containerd/releases/tag/v1.6.8)
- [containerd v1.6.7](https://github.com/containerd/containerd/releases/tag/v1.6.7)
- [runc v1.1.4](https://github.com/opencontainers/runc/releases/tag/v1.1.4)
- [runc v1.1.3](https://github.com/opencontainers/runc/releases/tag/v1.1.3)

### 安全

#### 适用于所有平台

- 修复了 [CVE-2023-0626](https://www.cve.org/CVERecord?id=CVE-2023-0626)：该漏洞允许在 Electron 客户端的 message-box 路由中通过查询参数执行 RCE。
- 修复了 [CVE-2023-0625](https://www.cve.org/CVERecord?id=CVE-2023-0625)：该漏洞允许通过精心制作的扩展描述/变更日志执行 RCE，可能被恶意扩展滥用。

#### 针对 Windows

- 修复了 [CVE-2023-0627](https://www.cve.org/CVERecord?id=CVE-2023-0627)：允许绕过 4.11 版本引入的 `--no-windows-containers` 安装标志。该标志允许管理员禁用 Windows 容器的使用。
- 修复了 [CVE-2023-0633](https://www.cve.org/CVERecord?id=CVE-2023-0633)：Docker Desktop 安装程序中的参数注入漏洞，可能导致本地权限提升。

### 错误修复与微小增强

#### 适用于所有平台

- 恢复出厂设置后默认开启 Compose V2。
- 对于 Docker Desktop 的新安装，默认开启 Compose V2。
- Compose 中环境变量的优先级更加一致，且已 [文档化](/manuals/compose/how-tos/environment-variables/envvars-precedence.md)。
- 内核升级至 5.10.124。
- 优化了计算磁盘大小时导致的整体性能问题。与 [docker/for-win#9401](https://github.com/docker/for-win/issues/9401) 相关。
- Docker Desktop 现在阻止未安装 Rosetta 的 ARM mac 用户切换回仅提供 Intel 二进制文件的 Compose V1。
- 将卷大小和 **Created** 列以及容器的 **Started** 列的默认排序顺序改为降级。
- 重新组织了容器行操作，仅保留启动/停止和删除操作始终可见，其他操作可通过行菜单项访问。
- 快速入门指南 (Quickstart guide) 现在会立即运行每条命令。
- 定义了容器/Compose **Status**（状态）列的排序顺序：running > some running > paused > some paused > exited > some exited > created。
- 修复了 Docker Desktop 中镜像列表即便存在镜像也显示为空的问题。与 [docker/for-win#12693](https://github.com/docker/for-win/issues/12693) 和 [docker/for-mac#6347](https://github.com/docker/for-mac/issues/6347) 相关。
- 定义了什么是“在用 (in use)”镜像：取决于是否显示系统容器。如果未显示与 Kubernetes 和扩展相关的系统容器，则相关镜像不被定义为“在用”。
- 修复了某些语言的 Docker 客户端在执行 `docker exec` 时挂起的 Bug。修复了 [https://github.com/apocas/dockerode/issues/534](https://github.com/apocas/dockerode/issues/534)。
- 构建扩展时生成的命令失败不再导致 Docker Desktop 意外退出。
- 修复了扩展在左侧菜单显示为已禁用但实际未禁用的 Bug。
- 修复了在启用注册表访问管理且屏蔽了 Docker Hub 访问时，向私有注册表执行 `docker login` 的问题。
- 修复了如果当前集群元数据未存储在 `.kube/config` 文件中时 Docker Desktop 无法启动 Kubernetes 集群的 Bug。
- 更新了 Docker Desktop 中的工具提示和 MUI 主题包，使其与整体系统设计对齐。
- 复制的终端内容中不再包含不间断空格。

#### 针对 Mac

- 安装或更新 macOS 版 Docker Desktop 的最低版本要求现已提升为 10.15。修复了 [docker/for-mac#6007](https://github.com/docker/for-mac/issues/6007)。
- 修复了托盘菜单在下载更新后错误显示 "Download will start soon..." 的 Bug。修复了 [for-mac/issues#5677](https://github.com/docker/for-mac/issues/5677) 中报告的部分问题。
- 修复了应用更新后无法重启 Docker Desktop 的 Bug。
- 修复了使用 virtualization.framework 且安装了限制性防火墙软件时，电脑休眠导致与 Docker 连接断开的 Bug。
- 修复了用户退出应用后 Docker Desktop 仍运行在后台的 Bug。修复了 [docker/for-mac##6440](https://github.com/docker/for-mac/issues/6440)。
- 针对运行 macOS < 12.5 的用户，同时禁用了 Virtualization Framework 和 VirtioFS。

#### 针对 Windows

- 修复了更新期间显示的版本号可能不正确的 Bug。修复了 [for-win/issues#12822](https://github.com/docker/for-win/issues/12822)。

## 4.11.1

{{< release-date date="2022-08-05" >}}

### 错误修复与增强

#### 适用于所有平台

- 修复了一个回归问题：曾阻止挂载虚拟机系统路径（例如 /var/lib/docker）[for-mac/issues#6433](https://github.com/docker/for-mac/issues/6433)。

#### 针对 Windows

- 修复了从 WSL2 发行版向私有注册表执行 `docker login` 的问题 [docker/for-win#12871](https://github.com/docker/for-win/issues/12871)。

## 4.11.0

{{< release-date date="2022-07-28" >}}

### 新特性

- Docker Desktop 现已全面支持 Docker Business 客户在 VMware ESXi 和 Azure 虚拟机内运行。更多信息请参见 [在虚拟机或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md)。
- 在扩展市场中增加了两个新扩展（[vcluster](https://hub.docker.com/extensions/loftsh/vcluster-dd-extension) 和 [PGAdmin4](https://hub.docker.com/extensions/mochoa/pgadmin4-docker-extension)）。
- 为扩展市场增加了对扩展进行排序的功能。
- 修复了导致某些用户被频繁提示提供反馈的 Bug。现在您每年只会被提示两次。
- 增加了 Docker Desktop 的自定义主题设置。这允许您独立于设备设置，为 Docker Desktop 指定深色或浅色模式。修复了 [docker/for-win#12747](https://github.com/docker/for-win/issues/12747)。
- 为 Windows 安装程序增加了新标志：`--no-windows-containers` 用于禁用 Windows 容器集成。
- 为 Mac 的安装命令增加了新标志：`--user <用户名>` 用于为特定用户设置 Docker Desktop，防止他们在首次运行时需要输入管理员密码。

### 更新

- [Docker Compose v2.7.0](https://github.com/docker/compose/releases/tag/v2.7.0)
- [Docker Compose "Cloud Integrations" v1.0.28](https://github.com/docker/compose-cli/releases/tag/v1.0.28)
- [Kubernetes v1.24.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.2)
- [Go 1.18.4](https://github.com/golang/go/releases/tag/go1.18.4)

### 错误修复与增强

#### 适用于所有平台

- 在容器界面增加了容器/Compose 图标，以及暴露的端口/退出代码。
- 更新了 Docker 主题色板数值以匹配我们的设计系统。
- 优化了当注册表访问管理阻止 Docker 引擎访问 Docker Hub 时来自 `docker login` 的错误消息。
- 提升了宿主机与 Docker 之间的吞吐量。例如提升了 `docker cp` 的性能。
- 缩短了收集诊断信息所需的时间。
- 在容器概览中选中或取消选中某个 Compose 应用，现在将同时选中/取消选中其下属的所有容器。
- 容器概览镜像列中的标签名现在可见。
- 为终端滚动条增加了搜索标记，以便能看到视口之外的匹配项。
- 修复了容器页面搜索功能工作不佳的问题 [docker/for-win#12828](https://github.com/docker/for-win/issues/12828)。
- 修复了导致 **Volume** 界面无限加载的问题 [docker/for-win#12789](https://github.com/docker/for-win/issues/12789)。
- 修复了容器 UI 中调整列宽或隐藏列不起作用的问题。修复了 [docker/for-mac#6391](https://github.com/docker/for-mac/issues/6391)。
- 修复了同时安装、更新或卸载多个扩展时，离开市场界面会导致状态丢失的 Bug。
- 修复了关于页面中 Compose 版本仅在重启 Docker Desktop 后才从 v2 更新为 v1 的问题。
- 修复了由于底层硬件不支持 WebGL2 渲染导致用户无法看到日志视图的问题。修复了 [docker/for-win#12825](https://github.com/docker/for-win/issues/12825)。
- 修复了容器和镜像 UI 不同步的 Bug。
- 修复了开启实验性虚拟化框架时的启动竞争。

#### 针对 Mac

- 修复了通过 UI 执行 Compose 命令的问题。修复了 [docker/for-mac#6400](https://github.com/docker/for-mac/issues/6400)。

#### 针对 Windows

- 修复了水平调整大小的问题。修复了 [docker/for-win#12816](https://github.com/docker/for-win/issues/12816)。
- 如果在 UI 中配置了 HTTP/HTTPS 代理，它将自动把镜像构建和运行容器的流量发送至代理。这避免了在每个容器或构建中单独配置环境变量的需要。
- 增加了 `--backend=windows` 安装程序选项，用于将 Windows 容器设置为默认后端。

#### 针对 Linux

- 修复了设置包含空格路径的文件共享时的 Bug。

## 4.10.1

{{< release-date date="2022-07-05" >}}

### 错误修复与增强

#### 针对 Windows

- 修复了 UI 操作对于从 WSL 创建的 Compose 应用失效的 Bug。修复了 [docker/for-win#12806](https://github.com/docker/for-win/issues/12806)。

#### 针对 Mac

- 修复了因路径未初始化导致安装命令失败的 Bug。修复了 [docker/for-mac#6384](https://github.com/docker/for-mac/issues/6384)。

## 4.10.0

{{< release-date date="2022-06-30" >}}

### 新特性

- 您现在可以在 Docker Desktop 运行镜像前添加环境变量。
- 增加了使容器日志处理更轻松的功能，如正则表达式搜索和在容器运行时清除日志的能力。
- 实现了针对容器表格的反馈：增加了端口信息，并分离了容器名和镜像名。
- 在扩展市场中增加了两个新扩展：Ddosify 和 Lacework。

### 移除

- 移除了首页 (Homepage)，我们正在重新设计。您可以 [在此提供反馈](https://docs.google.com/forms/d/e/1FAIpQLSfYueBkJHdgxqsWcQn4VzBn2swu4u_rMQRIMa8LExYb_72mmQ/viewform?entry.1237514594=4.10)。

### 更新

- [Docker Engine v20.10.17](/manuals/engine/release-notes/20.10.md#201017)
- [Docker Compose v2.6.1](https://github.com/docker/compose/releases/tag/v2.6.1)
- [Kubernetes v1.24.1](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.1)
- [cri-dockerd 更新至 v0.2.1](https://github.com/Mirantis/cri-dockerd/releases/tag/v0.2.1)
- [CNI plugins 更新至 v1.1.1](https://github.com/containernetworking/plugins/releases/tag/v1.1.1)
- [containerd 更新至 v1.6.6](https://github.com/containerd/containerd/releases/tag/v1.6.6)
- [runc 更新至 v1.1.2](https://github.com/opencontainers/runc/releases/tag/v1.1.2)
- [Go 1.18.3](https://github.com/golang/go/releases/tag/go1.18.3)

### 错误修复与增强

#### 适用于所有平台

- 在 **Containers** 选项卡中增加了用于启动/暂停/停止所选容器的额外批量操作。
- 在 **Containers** 选项卡中为 Compose 项目增加了暂停和重启操作。
- 在 **Containers** 选项卡中增加了图标以及暴露的端口或退出代码信息。
- 现在外部 URL 可以通过诸如 `docker-desktop://extensions/marketplace?extensionId=docker/logs-explorer-extension` 的链接指向扩展市场中的扩展详情。
- 现在会保留 Compose 应用的展开或折叠状态。
- Docker Desktop 现在默认提供 `docker extension` CLI 命令。
- 增大了扩展市场中显示的截图尺寸。
- 修复了一个 Bug：即如果 Docker 扩展的后端容器被停止，则该扩展会加载失败。修复了 [docker/extensions-sdk#162](https://github.com/docker/extensions-sdk/issues/162)。
- 修复了镜像搜索字段无故被清空的 Bug。修复了 [docker/for-win#12738](https://github.com/docker/for-win/issues/12738)。
- 修复了许可协议不显示并静默阻塞 Docker Desktop 启动的 Bug。
- 修复了未发布扩展显示的镜像和标签，使其显示真实的已安装未发布扩展的信息。
- 修复了“支持”屏幕上的重复页脚。
- 增加了从 GitHub 仓库子目录创建开发环境的功能。
- 移除了离线使用 Docker Desktop 时无法加载“每日提示”的错误消息。修复了 [docker/for-mac#6366](https://github.com/docker/for-mac/issues/6366)。

#### 针对 Mac

- 修复了 macOS 上 bash 补全文件位置的一个 Bug。修复了 [docker/for-mac#6343](https://github.com/docker/for-mac/issues/6343)。
- 修复了用户名超过 25 个字符时 Docker Desktop 无法启动的 Bug。修复了 [docker/for-mac#6122](https://github.com/docker/for-mac/issues/6122)。
- 修复了由于无效的系统代理配置导致 Docker Desktop 无法启动的 Bug。修复了 [docker/for-mac#6289](https://github.com/docker/for-mac/issues/6289) 中报告的部分问题。
- 修复了启用实验性虚拟化框架时 Docker Desktop 启动失败的 Bug。
- 修复了卸载 Docker Desktop 后托盘图标仍显示的 Bug。

#### 针对 Windows

- 修复了 Hyper-V 上导致高 CPU 占用的 Bug。修复了 [docker/for-win#12780](https://github.com/docker/for-win/issues/12780)。
- 修复了导致 Windows 版 Docker Desktop 启动失败的 Bug。修复了 [docker/for-win#12784](https://github.com/docker/for-win/issues/12784)。
- 修复了 `--backend=wsl-2` 安装标志未能将后端设置为 WSL 2 的问题。修复了 [docker/for-win#12746](https://github.com/docker/for-win/issues/12746)。

#### 针对 Linux

- 修复了设置只能应用一次的 Bug。
- 修复了“关于”屏幕中显示的 Compose 版本。

### 已知问题

- 有时在执行 `docker system prune` 时 Docker 引擎会重启。这是当前引擎使用的 BuildKit 版本的一个 [已知问题](https://github.com/moby/buildkit/pull/2177)，将在未来版本中修复。

## 4.9.1

{{< release-date date="2022-06-16" >}}

{{< desktop-install all=true version="4.9.1" build_path="/81317/" >}}

### 错误修复与增强

#### 适用于所有平台

- 修复了空白的控制面板屏幕。修复了 [docker/for-win#12759](https://github.com/docker/for-win/issues/12759)。

## 4.9.0

{{< release-date date="2022-06-02" >}}

### 新特性

- 在首页增加了更多引导指南，涵盖：Elasticsearch、MariaDB、Memcached、MySQL、RabbitMQ 和 Ubuntu。
- 在 Docker Desktop 控制面板增加了页脚，包含有关 Docker Desktop 更新状态和 Docker 引擎统计的通用信息。
- 重新设计了容器表格，增加了：
  - 一键复制容器 ID 到剪贴板的按钮。
  - 为每个容器增加了暂停按钮。
  - 容器表格支持调整列宽。
  - 保留容器表格的排序和列宽设置。
  - 容器表格支持批量删除。

### 更新

- [Docker Compose v2.6.0](https://github.com/docker/compose/releases/tag/v2.6.0)
- [Docker Engine v20.10.16](/manuals/engine/release-notes/20.10.md#201016)
- [containerd v1.6.4](https://github.com/containerd/containerd/releases/tag/v1.6.4)
- [runc v1.1.1](https://github.com/opencontainers/runc/releases/tag/v1.1.1)
- [Go 1.18.2](https://github.com/golang/go/releases/tag/go1.18.2)

### 错误修复与增强

#### 适用于所有平台

- 修复了在 Docker Desktop 暂停时退出应用会导致其挂起的问题。
- 修复了 PKI 过期后 Kubernetes 集群无法正确重置的问题。
- 修复了扩展市场未使用已定义 HTTP 代理的问题。
- 改进了 Docker Desktop 控制面板日志搜索功能，现在支持空格。
- 控制面板按钮上的鼠标中键点击现在与左键点击行为一致，而不是打开一个空白窗口。

#### 针对 Mac

- 优化了当 `/opt` 被添加到文件共享目录列表时，避免在宿主机上创建 `/opt/containerd/bin` 和 `/opt/containerd/lib` 的逻辑。

#### 针对 Windows

- 修复了 WSL 2 集成中的一个 Bug：即如果文件或目录被绑定挂载到容器且容器退出，该文件或目录会被同名的另一种对象替换。例如，文件变成了目录或目录变成了文件，导致后续绑定挂载该对象失败。
- 修复了托盘图标和控制面板 UI 不显示且 Docker Desktop 未能完全启动的 Bug。修复了 [docker/for-win#12622](https://github.com/docker/for-win/issues/12622)。

### 已知问题

#### 针对 Linux

- 更改绑定挂载中文件的所有权权限会失败。这是由于我们在宿主机和运行 Docker 引擎的虚拟机之间实现文件共享的方式所致。我们致力于在下个版本中解决此问题。

## 4.8.2

{{< release-date date="2022-05-18" >}}

### 更新

- [Docker Compose v2.5.1](https://github.com/docker/compose/releases/tag/v2.5.1)

### 错误修复与微小增强

- 修复了拉取镜像时导致问题的手动代理设置。修复了 [docker/for-win#12714](https://github.com/docker/for-win/issues/12714) 和 [docker/for-mac#6315](https://github.com/docker/for-mac/issues/6315)。
- 修复了禁用扩展时出现的高 CPU 占用问题。修复了 [docker/for-mac#6310](https://github.com/docker/for-mac/issues/6310)。
- Docker Desktop 现在会在日志文件和诊断信息中对 HTTP 代理密码进行脱敏处理。

### 已知问题

#### 针对 Linux

- 更改绑定挂载中文件的所有权权限会失败。这是由于我们在宿主机和运行 Docker 引擎的虚拟机之间实现文件共享的方式所致。我们致力于在下个版本中解决此问题。

## 4.8.1

{{< release-date date="2022-05-09" >}}

### 新特性

- 发布了 [Linux 版 Docker Desktop](/manuals/desktop/setup/install/linux/_index.md)。
- 开启 [Docker 扩展 (Docker Extensions)](/manuals/extensions/_index.md) 和扩展 SDK 的测试版。
- 创建了 Docker 首页，您可以在此运行热门镜像并了解如何使用它们。
- [Compose V2 现已正式发布 (GA)](https://www.docker.com/blog/announcing-compose-v2-general-availability/)。

### 错误修复与增强

- 修复了更新 Docker Desktop 时导致 Kubernetes 集群被删除的 Bug。

### 已知问题

#### 针对 Linux

- 更改绑定挂载中文件的所有权权限会失败。这是由于我们在宿主机和运行 Docker 引擎的虚拟机之间实现文件共享的方式所致。我们致力于在下个版本中解决此问题。

## 4.8.0

{{< release-date date="2022-05-06" >}}

### 新特性

- 发布了 [Linux 版 Docker Desktop](/manuals/desktop/setup/install/linux/_index.md)。
- 开启 [Docker 扩展 (Docker Extensions)](/manuals/extensions/_index.md) 和扩展 SDK 的测试版。
- 创建了 Docker 首页，您可以在此运行热门镜像并了解如何使用它们。
- [Compose V2 现已正式发布 (GA)](https://www.docker.com/blog/announcing-compose-v2-general-availability/)。

### 升级

- [Docker Compose v2.5.0](https://github.com/docker/compose/releases/tag/v2.5.0)
- [Go 1.18.1](https://github.com/golang/go/releases/tag/go1.18.1)
- [Kubernetes 1.24](https://github.com/kubernetes/kubernetes/releases/tag/v1.24.0)

### 错误修复与微小增强

#### 适用于所有平台

- 引入了对系统代理的读取。除非需要不同于 OS 层级的代理，否则您无需再手动配置代理。
- 修复了运行在代理后时控制面板中显示远程仓库的 Bug。
- 修复了即便服务器已不存在 vpnkit 仍建立并阻塞客户端连接的问题。参见 [docker/for-mac#6235](https://github.com/docker/for-mac/issues/6235)。
- 对 Docker Desktop 的卷选项卡进行了改进：
  - 显示卷大小。
  - 列支持调整宽度、隐藏和重新排序。
  - 列的排序顺序和隐藏状态将被保留，即使重启 Docker Desktop。
  - 选中行状态在切换选项卡时将被保留，即使重启 Docker Desktop。
- 修复了开发环境选项卡中增加项目后未出现滚动条的 Bug。
- 统一了控制面板中的标题头部和操作。
- 增加了通过 HTTP 代理下载注册表访问管理策略的支持。
- 修复了机器长时间进入睡眠模式后远程仓库显示为空的问题。
- 修复了一个 Bug：如果镜像名未被标记为 "&lt;none>" 但其标签是，则该悬空镜像在清理过程中未被选中。
- 优化了 `docker pull` 因需要 HTTP 代理而失败时的错误消息。
- 增加了在 Docker Desktop 中轻松清除搜索栏的能力。
- 将 "Containers / Apps" 选项卡重命名为 "Containers"。
- 修复了当 `C:\ProgramData\DockerDesktop` 为文件或符号链接时 Docker Desktop 安装程序的静默崩溃问题。
- 修复了一个 Bug：除非在设置中启用了对 Docker Hub 的访问，否则类似 `docker pull <私有注册表>/镜像` 的无命名空间镜像会被注册表访问管理错误地拦截。

#### 针对 Mac

- Docker Desktop 的图标现在符合 Big Sur 风格指南。参见 [docker/for-mac#5536](https://github.com/docker/for-mac/issues/5536)。
- 修复了程序坞 (Dock) 图标重复以及图标功能异常的问题。修复了 [docker/for-mac#6189](https://github.com/docker/for-mac/issues/6189)。
- 优化了对 `Cmd+Q` 快捷键的支持。

#### 针对 Windows

- 优化了对 `Ctrl+W` 快捷键的支持。

### 已知问题

#### 适用于所有平台

- 目前，如果您正在运行 Kubernetes 集群，升级到 Docker Desktop 4.8.0 将导致该集群被删除。我们致力于在下个版本中修复此问题。

#### 针对 Linux

- 更改绑定挂载中文件的所有权权限会失败。这是由于我们在宿主机和运行 Docker 引擎的虚拟机之间实现文件共享的方式所致。我们致力于在下个版本中解决此问题。

## 4.7.1

{{< release-date date="2022-04-19" >}}

### 错误修复与增强

#### 适用于所有平台

- 修复了快速入门指南最后屏幕的崩溃问题。

#### 针对 Windows

- 修复了由于符号链接错误导致更新失败的 Bug。修复了 [docker/for-win#12650](https://github.com/docker/for-win/issues/12650)。
- 修复了阻止使用 Windows 容器模式的 Bug。修复了 [docker/for-win#12652](https://github.com/docker/for-win/issues/12652)。

## 4.7.0

{{< release-date date="2022-04-07" >}}

### 新特性

- IT 管理员现在可以使用命令行远程安装 Docker Desktop。
- 增加了 Docker 软件物料清单 (SBOM) CLI 插件。该插件允许用户为 Docker 镜像生成 SBOM。
- 为新创建的 Kubernetes 集群使用 [cri-dockerd](https://github.com/Mirantis/cri-dockerd) 代替 `dockershim`。此更改对用户透明，Kubernetes 容器仍像以前一样运行在 Docker 引擎上。`cri-dockerd` 允许 Kubernetes 使用标准 [容器运行时接口 (Container Runtime Interface)](https://github.com/kubernetes/cri-api#readme) 来管理 Docker 容器，这也是控制其他容器运行时的同一接口。更多信息请参见 [The Future of Dockershim is cri-dockerd](https://www.mirantis.com/blog/the-future-of-dockershim-is-cri-dockerd/)。

### 更新

- [Docker Engine v20.10.14](/manuals/engine/release-notes/20.10.md#201014)
- [Docker Compose v2.4.1](https://github.com/docker/compose/releases/tag/v2.4.1)
- [Buildx 0.8.2](https://github.com/docker/buildx/releases/tag/v0.8.2)
- [containerd v1.5.11](https://github.com/containerd/containerd/releases/tag/v1.5.11)
- [Go 1.18](https://golang.org/doc/go1.18)

### 安全

- 更新 Docker 引擎至 v20.10.14 以修复 [CVE-2022-24769](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24769)。
- 更新 containerd 至 v1.5.11 以修复 [CVE-2022-24769](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24769)。

### 错误修复与增强

#### 适用于所有平台

- 修复了故障后注册表访问管理策略从未刷新的 Bug。
- UI 中的日志和终端现在在浅色和深色模式下均遵循您的 OS 主题。
- 现在可以通过多选复选框轻松一次性清理多个卷。
- 优化了登录反馈。

#### 针对 Mac

- 修复了导致 Docker Desktop 有时显示空白白色屏幕的问题。修复了 [docker/for-mac#6134](https://github.com/docker/for-mac/issues/6134)。
- 修复了使用 HyperKit 时从睡眠中唤醒后 gettimeofday() 性能下降的问题。修复了 [docker/for-mac#3455](https://github.com/docker/for-mac/issues/3455)。
- 修复了启动期间使用 `osxfs` 进行文件共享时导致 Docker Desktop 失去响应的问题。

#### 针对 Windows

- 修复了卷名称显示问题。修复了 [docker/for-win#12616](https://github.com/docker/for-win/issues/12616)。
- 修复了 WSL 2 集成中的一个 Bug：导致重启 Docker Desktop 或切换到 Windows 容器后 Docker 命令停止工作。

## 4.6.1

{{< release-date date="2022-03-22" >}}

### 更新

- [Buildx 0.8.1](https://github.com/docker/buildx/releases/tag/v0.8.1)

### 错误修复与增强

- 防止 vpnkit-forwarder 循环运行并在日志中填充大量错误消息。
- 修复了未设置 HTTP 代理时的诊断上传问题。修复了 [docker/for-mac#6234](https://github.com/docker/for-mac/issues/6234)。
- 移除了自诊断中误报的 "vm is not running" 错误。修复了 [docker/for-mac#6233](https://github.com/docker/for-mac/issues/6233)。

## 4.6.0

{{< release-date date="2022-03-14" >}}

### 新特性

#### 适用于所有平台

- Docker Desktop 控制面板的卷管理功能现在支持通过多选复选框高效清理卷。

#### 针对 Mac

- Docker Desktop 4.6.0 为 macOS 用户提供了启用名为 VirtioFS 的全新实验性文件共享技术的选项。在测试中，VirtioFS 显著减少了在宿主机和虚拟机之间同步更改所需的时间，带来了重大的性能提升。更多信息请参见 [VirtioFS](/manuals/desktop/settings-and-maintenance/settings.md#beta-功能)。

### 更新

#### 适用于所有平台

- [Docker Engine v20.10.13](/manuals/engine/release-notes/20.10.md#201013)
- [Docker Compose v2.3.3](https://github.com/docker/compose/releases/tag/v2.3.3)
- [Buildx 0.8.0](https://github.com/docker/buildx/releases/tag/v0.8.0)
- [containerd v1.4.13](https://github.com/containerd/containerd/releases/tag/v1.4.13)
- [runc v1.0.3](https://github.com/opencontainers/runc/releases/tag/v1.0.3)
- [Go 1.17.8](https://golang.org/doc/go1.17)
- [Linux 内核 5.10.104](https://hub.docker.com/layers/docker/for-desktop-kernel/5.10.104-379cadd2e08e8b25f932380e9fdaab97755357b3/images/sha256-7753b60f4544e5c5eed629d12151a49c8a4b48d98b4fb30e4e65cecc20da484d?context=explore)

### 安全

#### 适用于所有平台

- 修复了 [CVE-2022-0847](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0847)（即 “Dirty Pipe”）：该漏洞允许攻击者从容器内部修改宿主机镜像中的文件。如果使用 WSL 2 后端，必须运行 `wsl --update` 以更新 WSL 2。

#### 针对 Windows

- 修复了 [CVE-2022-26659](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-26659)：允许攻击者在 Docker Desktop 安装或更新期间覆盖系统上任何管理员可写的文件。

#### 针对 Mac

- [Qemu 6.2.0](https://wiki.qemu.org/ChangeLog/6.2)

### 错误修复与增强

#### 适用于所有平台

- 修复了设置了 HTTPS 代理时的诊断上传问题。
- 使托盘菜单中的检查更新选项能打开“软件更新 (Software updates)”设置部分。

#### 针对 Mac

- 修复了启动 Docker Desktop 后托盘菜单不显示所有菜单项的问题。修复了 [docker/for-mac#6192](https://github.com/docker/for-mac/issues/6192)。
- 修复了一个回归问题：曾导致 Docker Desktop 无法在后台启动。修复了 [docker/for-mac#6167](https://github.com/docker/for-mac/issues/6167)。
- 修复了 Docker Desktop 程序坞图标缺失的问题。修复了 [docker/for-mac#6173](https://github.com/docker/for-mac/issues/6173)。
- 优化了使用实验性 `virtualization.framework` 时的块设备访问速度。参见 [基准测试](https://github.com/docker/roadmap/issues/7#issuecomment-1050626886)。
- 将默认虚拟机内存分配改为物理内存的一半（最小 2GB，最大 8GB），以获得更好的开箱即用性能。

#### 针对 Windows

- 修复了即便 Docker Desktop 在命令行工作正常，UI 却一直卡在 `starting` 状态的问题。
- 修复了 Docker Desktop 托盘图标缺失的问题 [docker/for-win#12573](https://github.com/docker/for-win/issues/12573)。
- 修复了在最新的 5.10.60.1 内核下 WSL 2 的注册表访问管理问题。
- 修复了选中从 WSL 2 环境启动的 Compose 应用容器时发生的 UI 崩溃。修复了 [docker/for-win#12567](https://github.com/docker/for-win/issues/12567)。
- 修复了快速入门指南终端中的文本复制问题。修复了 [docker/for-win#12444](https://github.com/docker/for-win/issues/12444)。

### 已知问题

#### 针对 Mac

- 启用 VirtioFS 后，以不同 Unix 用户 ID 运行的容器进程可能会遇到缓存问题。例如，如果 `root` 用户进程查询了某个文件，随后用户 `nginx` 的进程尝试立即访问该文件，`nginx` 进程可能会收到 "Permission Denied" 错误。

## 4.5.1

{{< release-date date="2022-02-15" >}}

### 错误修复与增强

#### 针对 Windows

- 修复了新安装默认使用 Hyper-V 后端而非 WSL 2 的问题。
- 修复了 Docker Desktop 控制面板中导致托盘菜单消失的崩溃。

如果您运行的是 Windows 家庭版，安装 4.5.1 将自动切换回 WSL 2。如果您运行的是其他版本的 Windows 且希望使用 WSL 2 后端，必须在 **Settings > General** 部分开启 **Use the WSL 2 based engine** 选项来手动切换。或者，您可以编辑 `%APPDATA%\Docker\settings.json` 设置文件，将 `wslEngineEnabled` 字段的值改为 `true`。

## 4.5.0

{{< release-date date="2022-02-10" >}}

### 新特性

- Docker Desktop 4.5.0 引入了新版 Docker 菜单，在所有操作系统上提供一致的用户体验。更多信息请参见博客文章 [New Docker Menu & Improved Release Highlights with Docker Desktop 4.5](https://www.docker.com/blog/new-docker-menu-improved-release-highlights-with-docker-desktop-4-5/)。
- `docker version` 的输出现在会显示机器上安装的 Docker Desktop 版本。

### 更新

- [Amazon ECR Credential Helper v0.6.0](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.6.0)

### 安全

#### 针对 Mac

- 修复了 [CVE-2021-44719](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44719)：Docker Desktop 曾可被用于从容器内部访问宿主机上的任意用户文件，绕过共享文件夹的允许列表。

#### 针对 Windows

- 修复了 [CVE-2022-23774](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23774)：Docker Desktop 允许攻击者移动任意文件。

### 错误修复与增强

#### 适用于所有平台

- 修复了在退出并重新启动 Docker Desktop 后，系统会错误地提示用户登录的问题。
- 在 Linux 环境下，通过设置 `fs.inotify.max_user_watches=1048576` 和 `fs.inotify.max_user_instances=8192` 增加了文件系统监听 (inotify) 限制。修复了 [docker/for-mac#6071](https://github.com/docker/for-mac/issues/6071)。

#### 针对 Mac

- 修复了当使用 `osxfs` 且未向虚拟机共享任何宿主机目录时，导致虚拟机在启动时失去响应的问题。
- 修复了如果 Docker Compose 应用是在不同版本下启动的，则无法通过 Docker Desktop 控制面板停止该应用的问题。例如：用户在 V1 版本下启动了 Compose 应用，随后切换到 V2 版本，尝试停止应用将会失败。
- 修复了在退出并重新启动 Docker Desktop 后，系统会错误地提示用户登录的问题。
- 修复了 **About Docker Desktop** 窗口无法打开的问题。
- 在 M1 Mac 上将 CPU 数量限制为 8 个以修复启动问题。修复了 [docker/for-mac#6063](https://github.com/docker/for-mac/issues/6063)。

#### 针对 Windows

- 修复了 Compose 应用在 V2 版本启动但控制面板仅支持 V1 的相关问题。

### 已知问题

#### 针对 Windows

全新安装 Docker Desktop 4.5.0 存在一个 Bug，会将默认后端设为 Hyper-V 而非 WSL 2。这意味着 Windows 家庭版用户将无法启动 Docker Desktop（因为仅支持 WSL 2）。变通方法是先卸载 4.5.0，然后下载安装 4.5.1 或更高版本。或者，您可以编辑 `%APPDATA%\Docker\settings.json` 文件，将 `wslEngineEnabled` 字段改为 `true`。

## 4.4.4

{{< release-date date="2022-01-24" >}}

### 错误修复与增强

#### 针对 Windows

- 修复了从 WSL 2 登录的问题。修复了 [docker/for-win#12500](https://github.com/docker/for-win/issues/12500)。

### 已知问题

#### 针对 Windows

- 在浏览器完成登录后点击 **Proceed to Desktop** 有时不会将控制面板窗口置顶。
- 登录后，当控制面板获得焦点时，即使点击后台窗口，它有时仍会保持在最前端。变通方法是先点击控制面板，然后再点击其他应用窗口。
- 当通过 `registry.json` 文件启用组织限制时，“每周提示 (tips of the week)”会显示在强制登录对话框之上。

## 4.4.3

{{< release-date date="2022-01-14" >}}

### 错误修复与增强

#### 针对 Windows

- 禁用了控制面板快捷键，以防止其在窗口最小化或未聚焦时仍捕获按键。修复了 [docker/for-win#12495](https://github.com/docker/for-win/issues/12495)。

### 已知问题

#### 针对 Windows

- 在浏览器完成登录后点击 **Proceed to Desktop** 有时不会将控制面板窗口置顶。
- 登录后，当控制面板获得焦点时，即使点击后台窗口，它有时仍会保持在最前端。变通方法是先点击控制面板，然后再点击其他应用窗口。
- 当通过 `registry.json` 文件启用组织限制时，“每周提示 (tips of the week)”会显示在强制登录对话框之上。

## 4.4.2

{{< release-date date="22-01-13" >}}

### 新特性

- 配合 Auth0 和单点登录 (SSO) 实现简便安全的登录。
  - 单点登录 (SSO)：拥有 Docker Business 订阅的用户现在可以配置 SSO，通过其身份提供商 (IdPs) 进行身份验证以访问 Docker。更多信息请参见 [单点登录 (SSO)](../security/for-admins/single-sign-on/_index.md)。
  - 登录 Docker Desktop 现在将通过浏览器进行，以便您可以利用密码管理器的自动填充功能。

### 升级

- [Docker Engine v20.10.12](/manuals/engine/release-notes/20.10.md#201012)
- [Docker Compose v2.2.3](https://github.com/docker/compose/releases/tag/v2.2.3)
- [Kubernetes 1.22.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.22.5)
- [docker scan v0.16.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.16.0)

### 安全

- 修复了 [CVE-2021-45449](../security/_index.md#cve-2021-45449)，该漏洞影响当前处于 Docker Desktop 4.3.0 或 4.3.1 版本的用户。

Docker Desktop 4.3.0 和 4.3.1 存在一个 Bug，可能会在用户登录期间于本地机器上记录敏感信息（访问令牌或密码）。此漏洞仅在您处于 4.3.0/4.3.1 版本且在此期间执行了登录操作时才会产生影响。获取这些数据需要拥有对该用户本地文件的访问权限。

### 错误修复与增强

#### 适用于所有平台

- 如果 `registry.json` 在 `allowedOrgs` 字段中包含超过一个组织，Docker Desktop 现在会报错。如果您为不同开发小组使用多个组织，必须为每组提供独立的 `registry.json` 文件。
- 修复了 Compose 的一个回归问题：曾将容器名称分隔符从 `-` 改回了 `_`。修复了 [docker/compose-switch#24](https://github.com/docker/compose-switch/issues/24)。

#### 针对 Mac

- 修复了控制面板中容器的内存统计。修复了 [docker/for-mac/#6076](https://github.com/docker/for-mac/issues/6076)。
- 在 `settings.json` 中增加了一个弃用选项：`"deprecatedCgroupv1": true`，用于将 Linux 环境切回 cgroups v1。如果您的软件需要 cgroups v1，请更新其以兼容 cgroups v2。虽然 cgroups v1 仍可工作，但未来的特性很可能会依赖 cgroups v2。此外，某些 Linux 内核 Bug 也可能仅在 cgroups v2 中得到修复。
- 修复了暂停 Docker Desktop 后使机器进入睡眠模式，导致机器唤醒后 Docker Desktop 无法从暂停状态恢复的问题。修复了 [for-mac#6058](https://github.com/docker/for-mac/issues/6058)。

#### 针对 Windows

- 执行 `Reset to factory defaults`（恢复出厂设置）后不再关闭 Docker Desktop。

### 已知问题

#### 适用于所有平台

- 当通过 `registry.json` 文件启用组织限制时，“每周提示”会显示在强制登录对话框之上。

#### 针对 Windows

- 在浏览器完成登录后点击 **Proceed to Desktop** 有时不会将控制面板窗口置顶。
- 登录后，当控制面板获得焦点时，即使点击后台窗口，它有时仍会保持在最前端。变通方法是先点击控制面板，然后再点击其他应用窗口。
- 当控制面板打开时，即便未聚焦或已最小化，它仍会捕获键盘快捷键（例如 `Ctrl+R` 执行重启）。

## 4.3.2

{{< release-date date="2021-12-21" >}}

### 安全

- 修复了 [CVE-2021-45449](../security/_index.md#cve-2021-45449)，该漏洞影响当前处于 Docker Desktop 4.3.0 或 4.3.1 版本的用户。

Docker Desktop 4.3.0 和 4.3.1 存在一个 Bug，可能会在用户登录期间于本地机器上记录敏感信息（访问令牌或密码）。此漏洞仅在您处于 4.3.0/4.3.1 版本且在此期间执行了登录操作时才会产生影响。获取这些数据需要拥有对该用户本地文件的访问权限。

### 升级

[docker scan v0.14.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.14.0)

### 安全

**Log4j 2 CVE-2021-44228**：我们更新了 `docker scan` CLI 插件。此新版本的 `docker scan` 能够检测 [Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 和 [Log4j 2 CVE-2021-45046](https://nvd.nist.gov/vuln/detail/CVE-2021-45046)。

更多信息请阅读博客文章 [Apache Log4j 2 CVE-2021-44228](https://www.docker.com/blog/apache-log4j-2-cve-2021-44228/)。

## 4.3.1

{{< release-date date="2021-12-11" >}}

### 升级

[docker scan v0.11.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.11.0)

### 安全

**Log4j 2 CVE-2021-44228**：我们为您更新了 `docker scan` CLI 插件。Docker Desktop 4.3.0 及更早版本中的旧版 `docker scan` 无法检测 [Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228)。

更多信息请阅读博客文章 [Apache Log4j 2 CVE-2021-44228](https://www.docker.com/blog/apache-log4j-2-cve-2021-44228/)。

## 4.3.0

{{< release-date date="2021-12-02" >}}

### 升级

- [Docker Engine v20.10.11](/manuals/engine/release-notes/20.10.md#201011)
- [containerd v1.4.12](https://github.com/containerd/containerd/releases/tag/v1.4.12)
- [Buildx 0.7.1](https://github.com/docker/buildx/releases/tag/v0.7.1)
- [Docker Compose v2.2.1](https://github.com/docker/compose/releases/tag/v2.2.1)
- [Kubernetes 1.22.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.22.4)
- [Docker Hub Tool v0.4.4](https://github.com/docker/hub-tool/releases/tag/v0.4.4)
- [Go 1.17.3](https://golang.org/doc/go1.17)

### 错误修复与微小变更

#### 适用于所有平台

- 增加了自诊断警告：如果宿主机缺少互联网连接会发出提醒。
- 修复了无法通过卷 UI 中的 “Save As” 选项从卷中保存文件的问题。修复了 [docker/for-win#12407](https://github.com/docker/for-win/issues/12407)。
- Docker Desktop 现在使用 cgroupv2。如果您需要在容器中运行 `systemd`，那么：
  - 确保您的 `systemd` 版本支持 cgroupv2。[至少需要 `systemd` 247 版本](https://github.com/systemd/systemd/issues/19760#issuecomment-851565075)。考虑将 `centos:7` 镜像升级为 `centos:8`。
  - 运行 `systemd` 的容器需要以下选项：[`--privileged --cgroupns=host -v /sys/fs/cgroup:/sys/fs/cgroup:rw`](https://serverfault.com/questions/1053187/systemd-fails-to-run-in-a-docker-container-when-using-cgroupv2-cgroupns-priva)。

#### 针对 Mac

- 搭载 Apple 芯片的 Mac 上的 Docker Desktop 不再需要 Rosetta 2，但 [三个可选命令行工具](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md) 除外。

#### 针对 Windows

- 修复了如果家目录路径包含正则表达式使用的特殊字符时，导致 Docker Desktop 启动失败的问题。修复了 [docker/for-win#12374](https://github.com/docker/for-win/issues/12374)。

### 已知问题

Docker Desktop 控制面板在 Hyper-V 模式下的机器上会错误地将容器内存占用显示为零。您可以改用命令行中的 [`docker stats`](/reference/cli/docker/container/stats.md) 命令查看实际内存使用情况。参见 [docker/for-mac#6076](https://github.com/docker/for-mac/issues/6076)。

### 弃用

- 以下内部 DNS 名称已被弃用，并将从未来版本中移除：`docker-for-desktop`、`docker-desktop`、`docker.for.mac.host.internal`、`docker.for.mac.localhost`、`docker.for.mac.gateway.internal`。您现在必须使用 `host.docker.internal`、`vm.docker.internal` 和 `gateway.docker.internal`。
- 移除：从 Docker Desktop 中移除了自定义 RBAC 规则，因为它会给所有 Service Accounts 提供 `cluster-admin` 权限。修复了 [docker/for-mac/#4774](https://github.com/docker/for-mac/issues/4774)。

## 4.2.0

{{< release-date date="2021-11-09" >}}

### 新特性

**Pause/Resume（暂停/恢复）**：您现在可以在不活跃使用时暂停 Docker Desktop 会话，以节省机器的 CPU 资源。

- 交付了 [Docker Public Roadmap#226](https://github.com/docker/roadmap/issues/226)。

**Software Updates（软件更新）**：关闭自动检查更新的选项现已向所有 Docker 订阅方案开放，包括 Docker Personal 和 Docker Pro。所有与更新相关的设置已移至 **Software Updates** 界面。

- 交付了 [Docker Public Roadmap#228](https://github.com/docker/roadmap/issues/228)。

**Window management（窗口管理）**：现在 Docker Desktop 控制面板的窗口大小和位置在关闭并重新打开后会得到保留。

### 升级

- [Docker Engine v20.10.10](/manuals/engine/release-notes/20.10.md#201010)
- [containerd v1.4.11](https://github.com/containerd/containerd/releases/tag/v1.4.11)
- [runc v1.0.2](https://github.com/opencontainers/runc/releases/tag/v1.0.2)
- [Go 1.17.2](https://golang.org/doc/go1.17)
- [Docker Compose v2.1.1](https://github.com/docker/compose/releases/tag/v2.1.1)
- [docker-scan 0.9.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.9.0)

### 错误修复与微小变更

#### 适用于所有平台

- 优化：自诊断现在还会检查宿主机 IP 与 `docker networks` 之间的重叠。
- 修复了 Docker Desktop 控制面板上显示更新可用指示器的位置。

#### 针对 Mac

- 修复了点击致命错误对话框中的 **Exit** 后导致 Docker Desktop 停止响应的问题。
- 修复了极少数情况下影响在宿主机目录之上绑定挂载了 `docker volume` 的用户的启动失败问题。如果存在此情况，此修复还将移除宿主机相应目录上手动添加的 `DENY DELETE` ACL 条目。
- 修复了升级时 `Docker.qcow2` 文件被忽略且使用新的 `Docker.raw` 的 Bug，这曾导致容器和镜像“丢失”。请注意，如果系统同时拥有这两个文件（由之前的 Bug 引起），现在将使用最近修改的文件，以避免再次发生数据丢失。要强制使用旧的 `Docker.qcow2`，请删除较新的 `Docker.raw` 文件。修复了 [docker/for-mac#5998](https://github.com/docker/for-mac/issues/5998)。
- 修复了关机期间子进程可能意外失败并触发非预期致命错误弹窗的 Bug。修复了 [docker/for-mac#5834](https://github.com/docker/for-mac/issues/5834)。

#### 针对 Windows

- 修复了点击致命错误对话框中的 Exit 有时会导致 Docker Desktop 挂起的问题。
- 修复了在更新已下载但尚未应用时，频繁显示 **Download update** 弹窗的问题 [docker/for-win#12188](https://github.com/docker/for-win/issues/12188)。
- 修复了安装新更新时会在应用还来不及关闭之前就强制杀掉进程的问题。
- 修复：Docker Desktop 的安装现在即便在组策略阻止用户启动前提服务（如 LanmanServer）的情况下也能正常进行 [docker/for-win#12291](https://github.com/docker/for-win/issues/12291)。

## 4.1.1

{{< release-date date="2021-10-12" >}}

### 错误修复与微小变更

#### 针对 Mac

> 从 4.1.0 升级时，Docker 菜单不会变为 **Update and restart**，您可以直接等待下载完成（图标变化）然后选择 **Restart**。此 Bug 已在 4.1.1 中修复，不会再在未来的升级中出现。

- 修复了升级时 `Docker.qcow2` 文件被忽略且使用新的 `Docker.raw` 的 Bug，这曾导致容器和镜像“丢失”。如果系统同时拥有这两个文件（由之前的 Bug 引起），现在将使用最近修改的文件，以避免再次发生数据丢失。要强制使用旧的 `Docker.qcow2`，请删除较新的 `Docker.raw` 文件。修复了 [docker/for-mac#5998](https://github.com/docker/for-mac/issues/5998)。
- 修复了更新通知层有时在 **Settings** 按钮和 **Software update** 按钮之间同步失效的问题。
- 修复了安装新下载更新的菜单项。当更新准备好安装时，**Restart** 选项会变为 **Update and restart**。

#### 针对 Windows

- 修复了部分发行版（如 Arch 或 Alpine）的 WSL 2 集成的回归问题。修复了 [docker/for-win#12229](https://github.com/docker/for-win/issues/12229)。
- 修复了控制面板中 Settings 按钮和 Software update 按钮之间更新通知层同步失效的问题。

## 4.1.0

{{< release-date date="2021-09-30" >}}

### 新特性

- **Software Updates（软件更新）**：设置选项卡现在包含一个新部分，帮助您管理 Docker Desktop 更新。**Software Updates** 部分会在有新更新时通知您，并允许您下载更新或查看新版本包含的内容信息。
- **Compose V2**：您现在可以在常规设置中指定是否使用 Docker Compose V2。
- **Volume Management（卷管理）**：卷管理现已向所有订阅方案（包括 Docker Personal）开放。交付了 [Docker Public Roadmap#215](https://github.com/docker/roadmap/issues/215)。

### 升级

- [Docker Compose V2](https://github.com/docker/compose/releases/tag/v2.0.0)
- [Buildx 0.6.3](https://github.com/docker/buildx/releases/tag/v0.6.3)
- [Kubernetes 1.21.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.5)
- [Go 1.17.1](https://github.com/golang/go/releases/tag/go1.17.1)
- [Alpine 3.14](https://alpinelinux.org/posts/Alpine-3.14.0-released.html)
- [Qemu 6.1.0](https://wiki.qemu.org/ChangeLog/6.1)
- 基础发行版切换至 `debian:bullseye`。

### 错误修复与微小变更

#### 针对 Windows

- 修复了与防病毒软件误报触发相关的 Bug，自诊断功能避开了对 `net.exe` 工具的调用。
- 修复了自诊断中 WSL 2 Linux 虚拟机文件系统损坏的问题。这可能是由 [microsoft/WSL#5895](https://github.com/microsoft/WSL/issues/5895) 引起的。
- 修复了 `SeSecurityPrivilege` 特权要求问题。参见 [docker/for-win#12037](https://github.com/docker/for-win/issues/12037)。
- 修复了 CLI 上下文切换与 UI 的同步问题。参见 [docker/for-win#11721](https://github.com/docker/for-win/issues/11721)。
- 在 `settings.json` 中增加了 `vpnKitMaxPortIdleTime` 键，允许禁用或延长空闲网络连接超时。
- 修复了退出时的崩溃。参见 [docker/for-win#12128](https://github.com/docker/for-win/issues/12128)。
- 修复了 CLI 工具在部分 WSL 2 发行版中不可用的 Bug。
- 修复了由于 `panic.log` 的访问权限问题导致从 Linux 容器切换到 Windows 容器时卡住的问题。参见 [for-win#11899](https://github.com/docker/for-win/issues/11899)。

### 已知问题

#### 针对 Windows

在升级到 4.1.0 时，Docker Desktop 在某些基于 WSL 的发行版（如 ArchWSL）上可能会启动失败。参见 [docker/for-win#12229](https://github.com/docker/for-win/issues/12229)。

## 4.0.1

{{< release-date date="2021-09-13" >}}

### 升级

- [Docker Compose V2 RC3](https://github.com/docker/compose/releases/tag/v2.0.0-rc.3)
  - Compose v2 现在托管在 github.com/docker/compose。
  - 修复了使用 `compose up --scale` 缩减规模时的 Go panic。
  - 修复了在捕获退出代码时 `compose run --rm` 中的竞态条件。

### 错误修复与微小变更

#### 适用于所有平台

- 修复了 Docker Desktop 控制面板中无法执行复制粘贴的 Bug。

#### 针对 Windows

- 修复了 Docker Desktop 在 Hyper-V 引擎下无法正确启动的 Bug。参见 [docker/for-win#11963](https://github.com/docker/for-win/issues/11963)。

## 4.0.0

{{< release-date date="2021-08-31" >}}

### 新特性

Docker 已 [宣布](https://www.docker.com/blog/updating-product-subscriptions/) 更新并扩展了产品订阅方案，旨在提高生产力、加强协作并为开发人员和企业增强安全性。

更新后的 [Docker 订阅服务协议 (Docker Subscription Service Agreement)](https://www.docker.com/legal/docker-subscription-service-agreement) 包含针对 **Docker Desktop** 条款的变更：

- Docker Desktop 对于小型企业（员工少于 250 人且年营收低于 1000 万美元）、个人使用、教育及非商业开源项目 **保持免费**。
- 对于大型企业的专业用途，需要付费订阅 (**Pro, Team 或 Business**)，起价低至每月 5 美元。
- 这些条款的生效日期为 2021 年 8 月 31 日。对于那些需要付费订阅才能使用 Docker Desktop 的用户，有一个截至 2022 年 1 月 31 日的宽限期。
- Docker Pro 和 Docker Team 订阅现在 **包含对 Docker Desktop 的商业使用许可**。
- 现有的 Docker Free 订阅已更名为 **Docker Personal**。
- Docker 引擎或任何其他上游 **开源** Docker 或 Moby 项目 **没有任何更改**。

要了解这些变更对您的具体影响，请阅读 [常见问题解答 (FAQs)](https://www.docker.com/pricing/faq)。
更多信息请参见 [Docker 订阅概览](../subscription/_index.md)。

### 升级

- [Docker Compose V2 RC2](https://github.com/docker/compose-cli/releases/tag/v2.0.0-rc.2)
  - 修复了 `compose down` 时项目名称的大小写敏感性问题。参见 [docker/compose-cli#2023](https://github.com/docker/compose-cli/issues/2023)。
  - 修复了非规范化项目名称问题。
  - 修复了部分引用时的端口合并问题。
- [Kubernetes 1.21.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.21.4)

### 错误修复与微小变更

#### 针对 Mac

- 修复了从 Git URL 构建时 SSH 不可用的 Bug。修复了 [for-mac#5902](https://github.com/docker/for-mac/issues/5902)。

#### 针对 Windows

- 修复了 CLI 工具在部分 WSL 2 发行版中不可用的 Bug。
- 修复了由于 `panic.log` 权限问题导致在 Linux 和 Windows 容器之间切换时发生的 Bug。[for-win#11899](https://github.com/docker/for-win/issues/11899)。
