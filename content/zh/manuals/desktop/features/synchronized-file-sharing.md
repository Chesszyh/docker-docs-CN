---
title: 同步文件共享 (Synchronized file shares)
weight: 70
description: Docker Desktop 同步文件共享入门。
keyword: mutagen, 文件共享, docker desktop, 绑定挂载, bind mounts
aliases:
- /desktop/synchronized-file-sharing/
---

{{< summary-bar feature_name="同步文件共享" >}}

同步文件共享是一种替代性的文件共享机制，提供快速且灵活的“宿主机到虚拟机”文件共享。它通过使用同步的文件系统缓存，显著增强了绑定挂载（bind mount）的性能。

![同步文件共享面板图片](../images/synched-file-shares.webp)
 
## 适用对象

同步文件共享非常适合以下开发人员：
- 拥有庞大的存储库或单体仓库（monorepos），包含 10 万个或更多文件，总大小达数百 MB 甚至 GB 级别。
- 正在使用的虚拟文件系统（如 VirtioFS、gRPC FUSE 和 osxfs）已无法很好地适应其庞大的代码库。
- 经常遇到性能瓶颈。
- 不想担心文件所有权问题，或不想在修改多个容器时花时间解决冲突的文件所有权信息。

## 同步文件共享的工作原理

同步文件共享的行为与虚拟文件共享类似，但它利用高性能、低延迟的代码同步引擎，在 Docker Desktop 虚拟机内的 ext4 文件系统上创建宿主机文件的同步缓存。如果您在宿主机上或在虚拟机的容器中进行了文件系统更改，该更改将通过双向同步进行传播。

创建文件共享实例后，任何使用绑定挂载且指向宿主机文件系统位置（该位置与指定的同步文件共享位置或其子目录匹配）的容器，都将利用同步文件共享功能。不满足此条件的绑定挂载将通过普通的虚拟文件系统[绑定挂载机制](/manuals/engine/storage/bind-mounts.md)（例如 VirtioFS 或 gRPC-FUSE）进行处理。

> [!NOTE]
>
> Docker Desktop 中的 Kubernetes `hostPath` 卷不使用同步文件共享。

> [!IMPORTANT]
>
> 同步文件共享在 WSL 上或使用 Windows 容器时不可用。

## 创建文件共享实例

要创建文件共享实例：
1. 登录 Docker Desktop。
2. 在 **Settings（设置）** 中，导航到 **Resources（资源）** 部分下的 **File sharing（文件共享）** 选项卡。
3. 在 **Synchronized file shares** 部分，选择 **Create share（创建共享）**。
4. 选择要共享的宿主机文件夹。同步文件共享将开始初始化并可供使用。

由于需要将文件复制到 Docker Desktop 虚拟机中，文件共享需要几秒钟的时间进行初始化。在此期间，状态指示器显示为 **Preparing（准备中）**。Docker Desktop 控制面板的页脚也有一个状态图标，为您提供实时更新。

当状态指示器显示 **Watching for filesystem changes（正在监视文件系统更改）** 时，您的文件即可通过所有标准的绑定挂载机制（无论是命令行中的 `-v` 还是 `compose.yml` 文件中的指定）供虚拟机使用。

> [!NOTE]
>
> 当您创建新服务时，如果将 [绑定挂载选项的一致性](/reference/cli/docker/service/create.md#options-for-bind-mounts) 设置为 `:consistent`，则会绕过同步文件共享。

> [!TIP]
>
> Docker Compose 可以自动为绑定挂载创建文件共享。
> 请确保您已使用付费订阅登录 Docker，并在 Docker Desktop 的设置中启用了 **Access experimental features（访问实验性功能）** 和 **Manage Synchronized file shares with Compose（使用 Compose 管理同步文件共享）**。

## 探索您的文件共享实例

**Synchronized file shares** 部分显示了您所有的文件共享实例，并提供了每个实例的有用信息，包括：
- 文件共享内容的来源
- 状态更新
- 每个文件共享占用的空间
- 文件系统条目总数
- 符号链接数量
- 哪些容器正在使用该文件共享实例

选择一个文件共享实例可展开下拉列表并查看这些信息。

## 使用 `.syncignore`

您可以在每个文件共享的根目录下使用 `.syncignore` 文件，以在文件共享实例中排除本地文件。它支持与 `.dockerignore` 文件相同的语法，用于从同步中排除和/或重新包含路径。`.syncignore` 文件仅在文件共享的根目录下生效，在其他位置会被忽略。

您可能想要添加到 `.syncignore` 文件中的一些示例包括：
- 大型依赖目录，例如 `node_modules` 和 `composer` 目录（除非您依赖通过绑定挂载访问它们）
- `.git` 目录（同样，除非您需要它们）

通常，使用 `.syncignore` 文件排除对您的工作流非关键的项目，特别是那些同步缓慢或占用大量存储空间的项目。

## 已知问题

- 对 `.syncignore` 所做的更改不会导致立即删除，除非重新创建文件共享。换句话说，由于修改 `.syncignore` 文件而新被忽略的文件将保留在其当前位置，但在同步期间不再更新。

- 目前每个文件共享实例限制在约 200 万个文件以内。为了获得最佳性能，如果您有如此规模的文件共享实例，请尝试将其拆分为对应于各个绑定挂载位置的多个共享。

- 由于 Linux 区分大小写而 macOS/Windows 仅保留大小写，因此大小写冲突会在 GUI 中显示为 **File exists（文件已存在）** 问题。这些可以忽略。但是，如果问题持续存在，您可以报告该问题。

- 同步文件共享会主动报告临时问题，这可能会导致同步期间 GUI 中偶尔出现 **Conflict（冲突）** 和 **Problem（问题）** 指示。这些可以忽略。但是，如果问题持续存在，您可以报告该问题。

- 在 Windows 上如果您从 WSL2 切换到 Hyper-V，Docker Desktop 需要完全重启。

- 不支持 POSIX 风格的 Windows 路径。避免在 Docker Compose 中设置 [`COMPOSE_CONVERT_WINDOWS_PATHS`](/manuals/compose/how-tos/environment-variables/envvars.md#compose_convert_windows_paths) 环境变量。

- 如果您没有创建符号链接的正确权限，且您的容器尝试在文件共享实例中创建符号链接，将显示 **unable to create symbolic link（无法创建符号链接）** 错误消息。对于 Windows 用户，请参阅 Microsoft 的 [创建符号链接文档](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/create-symbolic-links) 了解最佳实践以及 **Create symbolic links** 安全策略设置的位置。对于 Mac 和 Linux 用户，请检查您是否对该文件夹具有写权限。