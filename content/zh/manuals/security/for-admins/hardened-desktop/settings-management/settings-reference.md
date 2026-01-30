---
description: 设置管理配置的所有设置和功能的参考
keywords: admin, 管理, 控制, 设置管理, Settings Management, 参考
title: 设置参考
linkTitle: 设置参考
---

本参考列出了所有 Docker Desktop 设置，包括它们的配置位置、适用的操作系统，以及是否可以在 Docker Desktop 图形界面（GUI）、Docker 管理控制台（Admin Console）或 `admin-settings.json` 文件中进行配置。设置的分组与 Docker Desktop 界面的结构相匹配。

每个设置都包含：

- Docker Desktop 中使用的显示名称
- 包含取值、默认值和所需格式的表格
- 描述和使用场景
- 操作系统兼容性
- 配置方法：通过 [Docker Desktop](/manuals/desktop/settings-and-maintenance/settings.md)、管理控制台或 `admin-settings.json` 文件

使用此参考可以比较不同配置方法和平台之间的设置行为。

## 常规 (General)

### 登录计算机时启动 Docker Desktop (Start Docker Desktop when you sign in to your computer)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在启动机器时自动启动 Docker Desktop。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：确保 Docker Desktop 在开机后始终运行。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### Docker Desktop 启动时打开 Docker 控制面板 (Open Docker Dashboard when Docker Desktop starts)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`      | `true`, `false`  | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 启动时自动打开 Docker 控制面板（Dashboard）。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：启动 Docker Desktop 后快速访问 Docker 控制面板中的容器、镜像和卷。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 选择 Docker Desktop 主题 (Choose theme for Docker Desktop)

| 默认值 | 接受的值 | 格式 |
|---------------|----------------------------|--------|
| `system`      | `light`, `dark`, `system`  | 枚举 (Enum) |

- **描述**：选择 Docker Desktop 图形界面的主题。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：个性化 Docker Desktop 外观。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 配置 Shell 补全 (Configure shell completions)

| 默认值 | 接受的值 | 格式 |
|---------------|-------------------------|--------|
| `integrated`  | `integrated`, `system`  | 字符串 (String) |

- **描述**：如果已安装，则自动编辑您的 shell 配置。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：通过 shell 补全自定义开发人员体验。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 选择容器终端 (Choose container terminal)

| 默认值 | 接受的值 | 格式 |
|---------------|-------------------------|--------|
| `integrated`  | `integrated`, `system`  | 字符串 (String) |

- **描述**：选择从 Docker Desktop 启动 Docker CLI 的默认终端。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：使用首选终端自定义开发人员体验。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 启用 Docker 终端 (Enable Docker terminal)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用对 Docker Desktop 集成终端的访问。如果该值设置为 `false`，用户将无法使用 Docker 终端与宿主机交互并直接从 Docker Desktop 执行命令。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：允许或限制开发人员访问内置终端。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `desktopTerminalEnabled` 设置

### 默认启用 Docker 调试 (Enable Docker Debug by default)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：为 Docker CLI 命令默认启用调试日志记录。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：协助调试支持问题。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 在 Time Machine 备份中包含 VM (Include VM in Time Machine backup)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：备份 Docker Desktop 虚拟机。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}}
- **使用场景**：管理应用程序数据的持久性。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 使用 containerd 来拉取和存储镜像 (Use containerd for pulling and storing images)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：使用 containerd 原生快照程序（snapshotter）代替传统的快照程序。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：提高镜像处理性能和兼容性。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 选择虚拟机管理器 (Choose Virtual Machine Manager)

#### Docker VMM

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

#### Apple Virtualization 框架 (Apple Virtualization framework)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：使用 Apple Virtualization 框架来运行 Docker 容器。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}}
- **使用场景**：提高 Apple Silicon 上的 VM 性能。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

#### Rosetta

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：使用 Rosetta 在 Apple Silicon 上模拟 `amd64`。如果值设置为 `true`，Docker Desktop 会开启 Rosetta 以加速 Apple Silicon 上的 x86_64/amd64 二进制模拟。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}} 13+
- **使用场景**：在 Apple Silicon 宿主机上运行基于 Intel 的容器。

> [!NOTE]
>
> 在强化版（hardened）环境中，请禁用并锁定此设置，以便仅允许运行 ARM 原生镜像。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `useVirtualizationFrameworkRosetta` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Use Rosetta for x86_64/amd64 emulation on Apple Silicon** 设置

> [!NOTE]
>
> Rosetta 要求启用 Apple Virtualization 框架。

#### QEMU

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

### 选择文件共享实现 (Choose file sharing implementation)

#### VirtioFS

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：使用 VirtioFS 实现宿主机与容器之间快速的原生文件共享。如果值设置为 `true`，则将 VirtioFS 设置为文件共享机制。如果 VirtioFS 和 gRPC 都设置为 `true`，则 VirtioFS 优先。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}} 12.5+
- **使用场景**：提高卷挂载性能和兼容性。

> [!NOTE]
>
> 在强化版环境中，对于 macOS 12.5 及更高版本，请启用并锁定此设置。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `useVirtualizationFrameworkVirtioFS` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Use VirtioFS for file sharing** 设置

#### gRPC FUSE

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：为 macOS 文件共享启用 gRPC FUSE。如果值设置为 `true`，则将 gRPC Fuse 设置为文件共享机制。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}}
- **使用场景**：提高文件挂载的性能和兼容性。

> [!NOTE]
>
> 在强化版环境中，请禁用并锁定此设置。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `useGrpcfuse` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Use gRPC FUSE for file sharing** 设置

#### osxfs

| 默认值 | 接受的值 | 格式 |
| ------------- | --------------- | ------- |
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：为 macOS 启用旧版的 osxfs 文件共享驱动程序。设置为 true 时，Docker Desktop 使用 osxfs 而不是 VirtioFS 或 gRPC FUSE 来将宿主机目录挂载到容器中。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}}
- **使用场景**：当需要与较旧的工具或特定工作流兼容时，使用原始的文件共享实现。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 发送使用统计信息 (Send usage statistics)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：控制 Docker Desktop 是否收集本地使用统计信息和崩溃报告并发送给 Docker。此设置影响从 Docker Desktop 应用程序本身收集的遥测数据。它不影响通过 Docker Hub 或其他后端服务收集的服务器端遥测数据，例如登录时间戳、拉取或构建记录。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：启用分析以帮助 Docker 根据使用数据改进产品。

> [!NOTE]
>
> 在强化版环境中，请禁用并锁定此设置。这允许您控制所有数据流，并在需要时通过安全渠道收集支持日志。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `analyticsEnabled` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Send usage statistics** 设置

> [!NOTE]
>
> 使用 Insights 控制面板的组织可能需要启用此设置，以确保开发人员活动完全可见。如果用户选择退出且该设置未锁定，他们的活动可能会从分析视图中排除。

### 使用增强型容器隔离 (Use Enhanced Container Isolation)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用增强型容器隔离以实现安全的容器执行。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：防止容器修改配置或敏感的宿主机区域。

> [!NOTE]
>
> 在强化版环境中，请启用并锁定此设置。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `enhancedContainerIsolation` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Enable enhanced container isolation** 设置

### 显示 CLI 提示 (Show CLI hints)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在使用 Docker 命令时，在终端中显示有用的 CLI 提示。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：通过内联建议帮助用户发现并学习 Docker CLI 功能。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 启用 Scout 镜像分析 (Enable Scout image analysis)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用 Docker Scout 以生成并显示容器镜像的 SBOM 数据。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：开启 Docker Scout 分析功能以查看与镜像关联的漏洞、软件包和元数据。

> [!NOTE]
>
> 在强化版环境中，请启用并锁定此设置，以确保始终构建 SBOM 以满足合规性扫描。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `sbomIndexing` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **SBOM indexing** 设置

### 启用后台 Scout SBOM 索引 (Enable background Scout SBOM indexing)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在后台自动为镜像索引 SBOM 数据，无需用户交互。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：通过允许 Docker 在空闲时间或镜像拉取操作后执行 SBOM 索引，保持镜像元数据为最新。

> [!NOTE]
>
> 在强化版环境中，请启用并锁定此设置。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置

### 自动检查配置 (Automatically check configuration)

| 默认值 | 接受的值 | 格式 |
|-----------------------|-----------------|---------|
| `CurrentSettingsVersions` | 整数 (Integer) | 整数 (Integer) |

- **描述**：定期检查您的配置，以确保没有被其他应用程序进行意外更改。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：跟踪版本以保证兼容性。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **General** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `configurationFileVersion` 设置

## 资源 (Resources)

### CPU 限制 (CPU limit)

| 默认值 | 接受的值 | 格式 |
|-----------------------------------------------|-----------------|---------|
| 宿主机上可用的逻辑 CPU 核心数 | 整数 (Integer) | 整数 (Integer) |

- **描述**：分配给 Docker Desktop 虚拟机的 CPU 数量。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：资源分配控制。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 资源设置

### 内存限制 (Memory limit)

| 默认值 | 接受的值 | 格式 |
|---------------------------|-----------------|---------|
| 基于系统资源 | 整数 (Integer) | 整数 (Integer) |

- **描述**：分配给 Docker 虚拟机的 RAM 量（以 MiB 为单位）。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：控制 Docker 在宿主机上可以使用多少内存。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 资源设置

### 交换空间 (Swap)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|---------|
| `1024`        | 整数 (Integer) | 整数 (Integer) |

- **描述**：分配给 Docker 虚拟机的交换空间量（以 MiB 为单位）。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：通过交换空间扩展可用内存。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 资源设置

### 磁盘使用限制 (Disk usage limit)

| 默认值 | 接受的值 | 格式 |
|-------------------------------|-----------------|---------|
| 机器的默认磁盘大小 | 整数 (Integer) | 整数 (Integer) |

- **描述**：分配给 Docker Desktop 的最大磁盘大小（以 MiB 为单位）。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：限制 Docker 虚拟磁盘大小以便进行存储管理。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 资源设置

### 磁盘镜像位置 (Disk image location)

| 默认值 | 接受的值 | 格式 |
|--------------------------------------------------|-----------------|--------|
| macOS: `~/Library/Containers/com.docker.docker/Data/vms/0`  <br> Windows: `%USERPROFILE%\AppData\Local\Docker\wsl\data` | 文件路径 (File path) | 字符串 (String) |

- **描述**：Docker Desktop 存储虚拟机数据的路径。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：将 Docker 数据重定向到自定义位置。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 资源设置

### 启用资源节约器 (Enable Resource Saver)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用 Docker Desktop 在空闲时暂停。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：在不活动期间节省系统资源。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 资源设置

### 文件共享目录 (File sharing directories)

| 默认值 | 接受的值 | 格式 |
|----------------------------------------|---------------------------------|--------------------------|
| 因操作系统而异 | 字符串形式的文件路径列表 | 字符串数组 (Array list of strings) |

- **描述**：允许在宿主机和容器之间共享的目录列表。添加路径后，其子目录也将被允许。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：限制或定义容器可用的文件路径。

> [!NOTE]
>
> 在强化版环境中，请锁定到明确的白名单并禁用最终用户编辑。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **File sharing** 资源设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `filesharingAllowedDirectories` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Allowed file sharing directories** 设置

### 代理排除 (Proxy exclude)

| 默认值 | 接受的值 | 格式 |
|---------------|--------------------|--------|
| `""`          | 地址列表 | 字符串 (String) |

- **描述**：配置容器在代理设置中应绕过的地址。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：微调容器网络的代理异常。

> [!NOTE]
>
> 在强化版环境中，请禁用并锁定此设置。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Proxies** 资源设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中带有 `manual` 和 `exclude` 模式的 `proxy` 设置

### Docker 子网 (Docker subnet)

| 默认值 | 接受的值 | 格式 |
|-------------------|-----------------|--------|
| `192.168.65.0/24` | IP 地址 | 字符串 (String) |

- **描述**：覆盖用于 `*.docker.internal` 的 vpnkit DHCP/DNS 的网络范围。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}}
- **使用场景**：自定义用于 Docker 容器网络的子网。
- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `vpnkitCIDR` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **VPN Kit CIDR** 设置

### 为 UDP 使用内核网络 (Use kernel networking for UDP)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：为 UDP 流量使用宿主机的内核网络栈，而不是 Docker 的虚拟网络驱动程序。这可以实现更快、更直接的 UDP 通信，但可能会绕过某些容器隔离功能。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：为严重依赖 UDP 流量的工作负载（如实时媒体、DNS 或游戏服务器）提高性能或兼容性。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Network** 资源设置

### 启用宿主机网络 (Enable host networking)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用实验性的宿主机网络支持。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：允许容器使用宿主机网络栈。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Network** 资源设置

### 网络模式 (Networking mode)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `dual-stack` | `ipv4only`, `ipv6only` | 字符串 (String) |

- **描述**：设置网络模式。
- **操作系统**：{{< badge color=blue text="Windows 和 Mac" >}}
- **使用场景**：选择 Docker 创建新网络时使用的默认 IP 协议。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Network** 资源设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `defaultNetworkingMode` 设置

有关更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

#### 抑制 IPv4/IPv6 的 DNS 解析 (Inhibit DNS resolution for IPv4/IPv6)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `auto` | `ipv4`, `ipv6`, `none` | 字符串 (String) |

- **描述**：过滤不支持的 DNS 记录类型。
- **操作系统**：{{< badge color=blue text="Windows 和 Mac" >}}
- **使用场景**：控制 Docker 如何过滤返回给容器的 DNS 记录，从而在仅支持 IPv4 或 IPv6 的环境中提高可靠性。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Network** 资源设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `dnsInhibition` 设置

有关更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

### 启用 WSL 引擎 (Enable WSL engine)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：如果值设置为 `true`，Docker Desktop 将使用基于 WSL 2 的引擎。这会覆盖在安装时使用 `--backend=<backend name>` 标志设置的任何内容。
- **操作系统**：{{< badge color=blue text="仅限 Windows" >}} + WSL
- **使用场景**：通过 WSL 2 后端启用 Linux 容器。

> [!NOTE]
>
> 在强化版环境中，请启用并锁定此设置。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **WSL Integration** 资源设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `wslEngineEnabled` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Windows Subsystem for Linux (WSL) Engine** 设置

## Docker Engine

Docker Engine 设置允许您通过原始 JSON 对象配置底层守护进程设置。这些设置将直接传递给驱动 Docker Desktop 容器管理的 `dockerd` 进程。

| 键 | 示例 | 描述 | 接受的值 / 格式 | 默认值 |
| --------------------- | --------------------------- | -------------------------------------------------- | ------------------------------ | ------- |
| `debug`               | `true`                      | 在 Docker 守护进程中启用详细日志记录 | 布尔值 (Boolean) | `false` |
| `experimental`        | `true`                      | 启用实验性的 Docker CLI 和守护进程功能 | 布尔值 (Boolean) | `false` |
| `insecure-registries` | `["myregistry.local:5000"]` | 允许在没有 TLS 的情况下从 HTTP 注册表拉取 | 字符串数组 (`host:port`) | `[]`    |
| `registry-mirrors`    | `["https://mirror.gcr.io"]` | 定义备用注册表端点 | URL 数组 | `[]`    |

- **描述**：使用直接传递给 `dockerd` 的结构化 JSON 配置自定义 Docker 守护进程的行为。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：微调注册表访问、启用调试模式或选择使用实验性功能。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Docker Engine** 设置

> [!NOTE]
>
> 此设置的值将按原样传递给 Docker 守护进程。无效或不受支持的字段可能会导致 Docker Desktop 无法启动。

## 构建器 (Builders)

构建器设置允许您为高级镜像构建场景管理 Buildx 构建器实例，包括多平台构建和自定义后端。

| 键 | 示例 | 描述 | 接受的值 / 格式 | 默认值 |
| ----------- | -------------------------------- | -------------------------------------------------------------------------- | ------------------------- | --------- |
| `name`      | `"my-builder"`                   | 构建器实例的名称 | 字符串 (String) | —         |
| `driver`    | `"docker-container"`             | 构建器使用的后端 (`docker`, `docker-container`, `remote` 等) | 字符串 (String) | `docker`  |
| `platforms` | `["linux/amd64", "linux/arm64"]` | 构建器支持的目标平台 | 平台字符串数组 | 宿主机架构 |

- **描述**：为 Docker Desktop 配置自定义 Buildx 构建器，包括驱动程序类型和支持的平台。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：设置高级构建配置，如跨平台镜像或远程构建器。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Builders** 设置

> [!NOTE]
>
> 构建器定义结构化为对象数组，每个对象描述一个构建器实例。冲突或不受支持的配置可能会导致构建错误。

## Kubernetes

### 启用 Kubernetes (Enable Kubernetes)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用 Docker Desktop 中的集成 Kubernetes 集群。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：为开发人员启用或禁用 Kubernetes 支持。

> [!NOTE]
>
> 在强化版环境中，请禁用并锁定此设置。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Kubernetes** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `kubernetes` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Allow Kubernetes** 设置

### 选择集群配置方法 (Choose cluster provisioning method)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `kubeadm`     | `kubeadm`, `kind`  | 字符串 (String) |

- **描述**：设置 Kubernetes 节点模式（单节点或多节点）。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：控制集成 Kubernetes 集群的拓扑结构。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Kubernetes** 设置

### Kubernetes 节点数 (kind 配置) (Kubernetes node count (kind provisioning))

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|---------|
| `1`           | 整数 (Integer) | 整数 (Integer) |

- **描述**：在多节点 Kubernetes 集群中创建的节点数量。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：扩展用于开发或测试的 Kubernetes 节点数量。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Kubernetes** 设置

### Kubernetes 节点版本 (kind 配置) (Kubernetes node version (kind provisioning))

| 默认值 | 接受的值 | 格式 |
|---------------|-------------------------------|--------|
| `1.31.1`      | 语义化版本 (例如 1.29.1) | 字符串 (String) |

- **描述**：用于创建集群节点的 Kubernetes 版本。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：固定特定的 Kubernetes 版本以保证一致性或兼容性。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Kubernetes** 设置

### 显示系统容器 (Show system containers)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker 控制面板容器列表中显示 Kubernetes 系统容器。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：允许开发人员查看 `kube-system` 容器以便进行调试。

> [!NOTE]
>
> 在强化版环境中，请禁用并锁定此设置。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Kubernetes** 设置

## 软件更新 (Software updates)

### 自动检查更新 (Automatically check for updates)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：禁用 Docker Desktop 的自动更新轮询。如果该值设置为 `true`，则禁用对 Docker Desktop 更新的检查和通知。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：在企业环境中冻结当前版本。

> [!NOTE]
>
> 在强化版环境中，请启用并锁定此设置。这可以保证仅安装经过内部审核的版本。

- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `disableUpdate` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Disable update** 设置

### 始终下载更新 (Always download updates)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：有可用更新时自动下载 Docker Desktop 更新。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：管理自动更新行为。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Software updates** 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Disable updates** 设置

## 扩展 (Extensions)

### 启用 Docker 扩展 (Enable Docker extensions)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用或禁用 Docker 扩展。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：控制对扩展市场和已安装扩展的访问。

> [!NOTE]
>
> 在强化版环境中，请禁用并锁定此设置。这可以防止安装第三方或未经审核的插件。

- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Extensions** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `extensionsEnabled` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **Allow Extensions** 设置

### 仅允许通过 Docker 市场分发的扩展 (Allow only extensions distributed through the Docker Marketplace)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：限制 Docker Desktop 仅运行来自市场的扩展。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：防止运行第三方或本地扩展。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Extensions** 设置

### 显示 Docker 扩展系统容器 (Show Docker Extensions system containers)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在容器列表中显示 Docker 扩展使用的系统容器。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：帮助开发人员排查故障或查看扩展系统容器。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Extensions** 设置

## Beta 功能 (Beta features)

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，这些设置位于 **Features in development**（开发中功能）页面的 **Experimental features**（实验性功能）选项卡下。

### 启用 Docker AI (Enable Docker AI)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 体验中启用 Docker AI 功能。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：启用或禁用 AI 功能，如“Ask Gordon”。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Beta** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `enableDockerAI` 设置

### 启用 Docker Model Runner (Enable Docker Model Runner)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 中启用 Docker Model Runner 功能。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：启用或禁用 Docker Model Runner 功能。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Beta** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `enableDockerAI` 设置

#### 启用宿主机侧 TCP 支持 (Enable host-side TCP support)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 中启用 Docker Model Runner 功能。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：启用或禁用 Docker Model Runner 功能。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Beta** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `enableDockerAI` 设置
    
> [!NOTE]
>
> 此设置要求先启用 Docker Model Runner 设置。

##### 端口 (Port)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|---------|
| 12434         | 整数 (Integer) | 整数 (Integer) |

- **描述**：指定公开的 TCP 端口。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：通过 TCP 连接到 Model Runner。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Beta features** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `enableInferenceTCP` 设置

##### CORS 允许的源 (CORS Allowed Origins)

| 默认值 | 接受的值 | 格式 |
|---------------|---------------------------------------------------------------------------------|--------|
| 空字符串 | 空字符串表示拒绝所有，`*` 表示接受所有，或使用逗号分隔的值列表 | 字符串 (String) |

- **描述**：指定允许的 CORS 源。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：与 Web 应用程序集成。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Beta features** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `enableInferenceCORS` 设置

### 启用 Docker MCP 工具包 (Enable Docker MCP Toolkit)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 中启用 [Docker MCP 工具包](/manuals/ai/mcp-catalog-and-toolkit/_index.md)。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Beta** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `enableDockerMCPToolkit` 设置
    

### 启用 Wasm (Enable Wasm)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用 [Wasm](/manuals/desktop/features/wasm.md) 以运行 Wasm 工作负载。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Beta** 设置    

### 启用 Compose Bridge (Enable Compose Bridge)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启用 [Compose Bridge](/manuals/compose/bridge/_index.md)。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Beta** 设置

## 通知 (Notifications)

### 任务和流程的状态更新 (Status updates on tasks and processes)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 内部显示一般的常规信息。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：自定义应用内通信的可视化。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Notifications** 设置

### 来自 Docker 的推荐 (Recommendations from Docker)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 内部显示促销公告和横幅。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：控制对 Docker 新闻和功能推广的接触。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Notifications** 设置

### Docker 公告 (Docker announcements)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 内部显示一般公告。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：在图形界面中启用或抑制 Docker 范围内的公告。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Notifications** 设置

### Docker 调查 (Docker surveys)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：显示邀请用户参与调查的通知。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：启用或禁用产品内调查提示。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Notifications** 设置

### Docker Scout 通知弹窗 (Docker Scout Notification pop-ups)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在 Docker Desktop 内部启用 Docker Scout 弹窗。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：显示或隐藏漏洞扫描通知。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Notifications** 设置

### Docker Scout 操作系统通知 (Docker Scout OS notifications)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：通过操作系统启用 Docker Scout 通知。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：通过系统通知中心推送 Scout 更新。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Notifications** 设置

## 高级 (Advanced)

### 配置 Docker CLI 的安装 (Configure installation of Docker CLI)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `system`      | 文件路径 | 字符串 (String) |

- **描述**：Docker CLI 二进制文件的安装位置。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：为满足合规性或工具链需求而自定义 CLI 安装位置。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 设置

### 允许使用默认 Docker 套接字 (Allow the default Docker socket to be used)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：默认情况下，增强型容器隔离会阻止将 Docker Engine 套接字绑定挂载到容器中（例如 `docker run -v /var/run/docker.sock:/var/run/docker.sock ...`）。此设置允许您以受控方式放宽此限制。有关更多信息，请参阅 ECI 配置。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：允许容器访问 Docker 套接字，适用于 Docker-in-Docker 或容器化 CI 代理等场景。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 设置
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `dockerSocketMount` 设置

### 允许特权端口映射 (Allow privileged port mapping)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `true`        | `true`, `false` | 布尔值 (Boolean) |

- **描述**：启动特权辅助进程，用于绑定 1 到 1024 之间的特权端口。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}}
- **使用场景**：为网络支持强制执行提升的特权。
- **配置此设置的方法**：
    - [Docker Desktop 图形界面](/manuals/desktop/settings-and-maintenance/settings.md)中的 **Advanced** 设置

## Docker Desktop 图形界面中不可用的设置 (Settings not available in the Docker Desktop GUI)

以下设置不会在 Docker Desktop 图形界面中显示。您只能使用管理控制台的设置管理或通过 `admin-settings.json` 文件来配置它们。

### 阻止 `docker load` (Block `docker load`)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：阻止用户使用 `docker load` 命令加载本地 Docker 镜像。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：通过限制本地镜像导入来强制执行镜像来源管理。

> [!NOTE]
>
> 在强化版环境中，请启用并锁定此设置。这会强制所有镜像必须来自您安全的、经过扫描的注册表。

- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `blockDockerLoad` 设置

### 在 TCP 2375 上公开 Docker API (Expose Docker API on TCP 2375)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：在端口 2375 上通过未经身份验证的 TCP 套接字公开 Docker API。仅建议在隔离且受保护的环境中使用。
- **操作系统**：{{< badge color=blue text="仅限 Windows" >}}
- **使用场景**：旧版集成或不支持命名管道的环境所必需。

> [!NOTE]
>
> 在强化版环境中，请禁用并锁定此设置。这可以确保只能通过安全内部套接字访问 Docker API。

- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `exposeDockerAPIOnTCP2375` 设置

### 物理隔离容器代理 (Air-gapped container proxy)

| 默认值 | 接受的值 | 格式 |
| ------------- | --------------- | ----------- |
| 见示例 | 对象 | JSON 对象 |

- **描述**：为容器配置手动 HTTP/HTTPS 代理。在容器需要受限访问的物理隔离（air-gapped）环境中很有用。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：重定向或阻止容器网络，以符合离线或安全的网络环境。
- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `containersProxy` 设置

#### 示例 (Example)

```json
"containersProxy": {
  "locked": true,
  "mode": "manual",
  "http": "",
  "https": "",
  "exclude": [],
  "pac": "",
  "transparentPorts": ""
}
```

Docker 套接字访问控制 (ECI 异常) (Docker socket access control (ECI exceptions))

| 默认值 | 接受的值 | 格式 |
| ------------- | --------------- | ----------- |
| -           | 对象 | JSON 对象 |

- **描述**：在启用增强型容器隔离时，允许特定镜像或命令使用 Docker 套接字。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：支持像 Testcontainers 或 LocalStack 这样需要 Docker 套接字访问权限的工具，同时保持安全的默认设置。
- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `enhancedContainerIsolation` > `dockerSocketMount`

#### 示例 (Example)

```json
"enhancedContainerIsolation": {
  "locked": true,
  "value": true,
  "dockerSocketMount": {
    "imageList": {
      "images": [
        "docker.io/localstack/localstack:*",
        "docker.io/testcontainers/ryuk:*"
      ]
    },
    "commandList": {
      "type": "deny",
      "commands": ["push"]
    }
  }
}
```

### 允许 Beta 功能 (Allow beta features)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：允许访问 Docker Desktop 中的 Beta 功能。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：让开发人员尽早访问处于公开 Beta 阶段的功能。

> [!NOTE]
>
> 在强化版环境中，请禁用并锁定此设置。

- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `allowBetaFeatures` 设置

### Docker 守护进程选项（Linux 或 Windows） (Docker daemon options (Linux or Windows))

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|----------|
| `{}`          | JSON 对象 | 字符串化的 JSON |

- **描述**：覆盖 Linux 或 Windows 容器中使用的 Docker 守护进程配置。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：在不编辑本地配置文件的情况下配置底层 Docker 守护进程选项（例如日志记录、存储驱动程序）。

> [!NOTE]
>
> 在强化版环境中，请提供经过审核的 JSON 配置并将其锁定，以便无法进行任何覆盖。

- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `linuxVM.dockerDaemonOptions` 或 `windowsContainers.dockerDaemonOptions`

### VPNKit CIDR

| 默认值 | 接受的值 | 格式 |
|-------------------|-----------------|--------|
| `192.168.65.0/24` | CIDR 表示法 | 字符串 (String) |

- **描述**：设置用于内部 VPNKit DHCP/DNS 服务的子网。
- **操作系统**：{{< badge color=blue text="仅限 Mac" >}}
- **使用场景**：在子网重叠的环境中防止 IP 冲突。

> [!NOTE]
>
> 在强化版环境中，请锁定到经批准的、不冲突的 CIDR。

- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `vpnkitCIDR` 设置
    - 设置管理：[管理控制台](/manuals/security/for-admins/hardened-desktop/settings-management/configure-admin-console.md)中的 **VPN Kit CIDR** 设置

### 启用 Kerberos 和 NTLM 身份验证 (Enable Kerberos and NTLM authentication)

| 默认值 | 接受的值 | 格式 |
|---------------|-----------------|--------|
| `false`       | `true`, `false` | 布尔值 (Boolean) |

- **描述**：为企业环境启用 Kerberos 和 NTLM 代理身份验证。
- **操作系统**：{{< badge color=blue text="所有" >}}
- **使用场景**：允许用户通过需要 Kerberos 或 NTLM 的企业代理服务器进行身份验证。
- **配置此设置的方法**：
    - 设置管理：[`admin-settings.json` 文件](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md)中的 `proxy.enableKerberosNtlm` 设置
