---
title: 同步文件共享
weight: 70
description: 开始使用 Docker Desktop 上的同步文件共享。
keyword: mutagen, file sharing, docker desktop, bind mounts
aliases:
- /desktop/synchronized-file-sharing/
---

{{< summary-bar feature_name="Synchronized file sharing" >}}

同步文件共享（Synchronized file shares）是一种替代文件共享机制，通过使用同步文件系统缓存来增强绑定挂载（bind mount）性能，提供快速灵活的主机到虚拟机文件共享。

![同步文件共享面板图像](../images/synched-file-shares.webp)

## 适用对象

同步文件共享非常适合以下开发者：
- 拥有包含 100,000 个或更多文件的大型仓库或单体仓库（monorepos），总计数百兆字节甚至数千兆字节。
- 正在使用虚拟文件系统（如 VirtioFS、gRPC FUSE 和 osxfs），这些系统已无法很好地扩展以适应其代码库。
- 经常遇到性能限制。
- 不想担心文件所有权或在修改多个容器时花时间解决冲突的文件所有权信息。

## 同步文件共享如何工作？

同步文件共享的行为与虚拟文件共享相同，但利用高性能、低延迟的代码同步引擎在 Docker Desktop 虚拟机内的 ext4 文件系统上创建主机文件的同步缓存。如果您在主机或虚拟机的容器中进行文件系统更改，它会通过双向同步传播。

创建文件共享实例后，任何使用绑定挂载且指向与指定同步文件共享位置匹配的主机文件系统位置（或其子目录）的容器都将使用同步文件共享功能。不满足此条件的绑定挂载将传递给普通虚拟文件系统[绑定挂载机制](/manuals/engine/storage/bind-mounts.md)，例如 VirtioFS 或 gRPC-FUSE。

> [!NOTE]
>
> 同步文件共享不被 Docker Desktop 中 Kubernetes 的 `hostPath` 卷使用。

> [!IMPORTANT]
>
> 同步文件共享在 WSL 上或使用 Windows 容器时不可用。

## 创建文件共享实例

要创建文件共享实例：
1. 登录 Docker Desktop。
2. 在 **Settings** 中，导航到 **Resources** 部分内的 **File sharing** 选项卡。
3. 在 **Synchronized file shares** 部分，选择 **Create share**。
4. 选择要共享的主机文件夹。同步文件共享应初始化并可用。

文件共享需要几秒钟来初始化，因为文件被复制到 Docker Desktop 虚拟机中。在此期间，状态指示器显示 **Preparing**。Docker Desktop Dashboard 页脚中也有一个状态图标，让您随时了解最新情况。

当状态指示器显示 **Watching for filesystem changes** 时，您的文件可通过所有标准绑定挂载机制供虚拟机使用，无论是命令行中的 `-v` 还是在 `compose.yml` 文件中指定。

> [!NOTE]
>
> 当您创建新服务时，将[绑定挂载选项 consistency](/reference/cli/docker/service/create.md#options-for-bind-mounts) 设置为 `:consistent` 会绕过同步文件共享。

> [!TIP]
>
> Docker Compose 可以自动为绑定挂载创建文件共享。
> 确保您已使用付费订阅登录 Docker，并在 Docker Desktop 的设置中启用了 **Access experimental features** 和 **Manage Synchronized file shares with Compose**。

## 浏览您的文件共享实例

**Synchronized file shares** 部分显示您所有的文件共享实例，并提供有关每个实例的有用信息，包括：
- 文件共享内容的来源
- 状态更新
- 每个文件共享使用的空间大小
- 文件系统条目计数
- 符号链接数量
- 哪个容器正在使用文件共享实例

选择一个文件共享实例会展开下拉列表并显示此信息。

## 使用 `.syncignore`

您可以在每个文件共享的根目录使用 `.syncignore` 文件，从文件共享实例中排除本地文件。它支持与 `.dockerignore` 文件相同的语法，可以排除和/或重新包含路径进行同步。位于文件共享根目录以外任何位置的 `.syncignore` 文件将被忽略。

您可能想要添加到 `.syncignore` 文件中的一些示例：
- 大型依赖目录，例如 `node_modules` 和 `composer` 目录（除非您依赖通过绑定挂载访问它们）
- `.git` 目录（同样，除非您需要它们）

通常，使用 `.syncignore` 文件排除对您的工作流程不重要的项目，特别是那些同步速度慢或使用大量存储的项目。

## 已知问题

- 对 `.syncignore` 所做的更改不会导致立即删除，除非重新创建文件共享。换句话说，由于 `.syncignore` 文件中的修改而新被忽略的文件将保留在其当前位置，但在同步期间不再更新。

- 文件共享实例目前限制为每个共享大约 200 万个文件。为获得最佳性能，如果您有这种大小的文件共享实例，请尝试将其分解为对应于各个绑定挂载位置的多个共享。

- 由于 Linux 区分大小写而 macOS/Windows 仅保留大小写导致的大小写冲突，在 GUI 中显示为 **File exists** 问题。这些可以忽略。但是，如果它们持续存在，您可以报告问题。

- 同步文件共享会主动报告临时问题，这可能导致在同步期间 GUI 中偶尔出现 **Conflict** 和 **Problem** 指示器。这些可以忽略。但是，如果它们持续存在，您可以报告问题。

- 如果您在 Windows 上从 WSL2 切换到 Hyper-V，Docker Desktop 需要完全重启。

- 不支持 POSIX 风格的 Windows 路径。避免在 Docker Compose 中设置 [`COMPOSE_CONVERT_WINDOWS_PATHS`](/manuals/compose/how-tos/environment-variables/envvars.md#compose_convert_windows_paths) 环境变量。

- 如果您没有创建符号链接的正确权限，而您的容器尝试在文件共享实例中创建符号链接，则会显示 **unable to create symbolic link** 错误消息。对于 Windows 用户，请参阅 Microsoft 的[创建符号链接文档](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/create-symbolic-links)了解最佳实践和 **Create symbolic links** 安全策略设置的位置。对于 Mac 和 Linux 用户，请检查您是否对该文件夹具有写入权限。
