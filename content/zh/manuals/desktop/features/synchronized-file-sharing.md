---
title: 同步文件共享 (Synchronized file shares)
weight: 70
description: 开始使用 Docker Desktop 上的同步文件共享功能。
keyword: mutagen, 文件共享, docker desktop, 绑定挂载
aliases:
- /desktop/synchronized-file-sharing/
---

{{< summary-bar feature_name="同步文件共享" >}}

同步文件共享是一种备选的文件共享机制，提供快速、灵活的宿主机到虚拟机的映射，通过使用同步的文件系统缓存来增强绑定挂载（bind mount）的性能。

![同步文件共享面板图像](../images/synched-file-shares.webp)
 
## 适用人群

同步文件共享非常适合以下开发者： 
- 拥有包含 100,000 个或更多文件，总计数百 MB 甚至 GB 大型仓库或单体仓库（monorepos）的开发者。
- 正在使用 VirtioFS、gRPC FUSE 和 osxfs 等虚拟文件系统，但这些系统已无法很好地适应其代码规模的开发者。 
- 经常遇到性能瓶颈的开发者。
- 不想在修改多个容器时担心文件所有权问题，或花时间解决冲突的文件所有权信息的开发者。

## 同步文件共享是如何工作的？

同步文件共享的行为与虚拟文件共享完全一样，但它利用高性能、低延迟的代码同步引擎，在 Docker Desktop 虚拟机内的 ext4 文件系统上创建宿主机文件的同步缓存。如果您在宿主机上或虚拟机的容器中进行文件系统更改，更改会通过双向同步进行传播。

创建文件共享实例后，任何使用指向宿主机文件系统上与指定同步文件共享位置（或其子目录）匹配的绑定挂载的容器，都将利用同步文件共享功能。不满足此条件的绑定挂载将传递给正常的虚拟文件系统 [绑定挂载机制](/manuals/engine/storage/bind-mounts.md)，例如 VirtioFS 或 gRPC-FUSE。

> [!NOTE]
>
> Docker Desktop 中的 Kubernetes `hostPath` 卷不使用同步文件共享。

> [!IMPORTANT]
>
> 同步文件共享在 WSL 上或使用 Windows 容器时不可用。 

## 创建文件共享实例 

创建文件共享实例的步骤：
1. 登录 Docker Desktop。
2. 在 **Settings**（设置）中，导航到 **Resources**（资源）部分下的 **File sharing**（文件共享）选项卡。 
3. 在 **Synchronized file shares**（同步文件共享）部分，选择 **Create share**（创建共享）。
4. 选择要共享的宿主机文件夹。同步文件共享随后将进行初始化并可供使用。

由于文件需要复制到 Docker Desktop 虚拟机中，文件共享需要几秒钟时间进行初始化。在此期间，状态指示器显示为 **Preparing**（正在准备）。Docker Desktop 控制面板页脚中也有一个状态图标，可让您随时了解进度。

当状态指示器显示 **Watching for filesystem changes**（正在监听文件系统更改）时，您的文件即可通过所有标准的绑定挂载机制（无论是命令行中的 `-v` 还是 `compose.yml` 文件中指定的内容）供虚拟机使用。

> [!NOTE]
>
> 创建新服务时，将 [绑定挂载选项 consistency](/reference/cli/docker/service/create.md#绑定挂载的选项) 设置为 `:consistent` 会绕过同步文件共享。 

> [!TIP]
>
> Docker Compose 可以自动为绑定挂载创建文件共享。确保您已使用付费订阅登录 Docker，并在 Docker Desktop 设置中同时启用了 **Access experimental features**（访问实验性功能）和 **Manage Synchronized file shares with Compose**（使用 Compose 管理同步文件共享）。

## 探索您的文件共享实例

**Synchronized file shares** 部分显示了您所有的文件共享实例，并提供了关于每个实例的有用信息，包括：
- 文件共享内容的来源
- 状态更新
- 每个文件共享使用的空间大小
- 文件系统条目计数
- 符号链接数量
- 哪些容器正在使用该文件共享实例

选择一个文件共享实例可展开下拉列表并查看这些信息。

## 使用 `.syncignore`

您可以在每个文件共享的根目录下使用 `.syncignore` 文件，以从您的文件共享实例中排除本地文件。它支持与 `.dockerignore` 文件相同的语法，用于排除和/或重新包含同步路径。`.syncignore` 文件在除文件共享根目录以外的任何位置都会被忽略。
 
您可能希望添加到 `.syncignore` 文件中的一些示例包括：
- 大型依赖目录，例如 `node_modules` 和 `composer` 目录（除非您需要通过绑定挂载访问它们）
- `.git` 目录（同样，除非您需要它们）

通常，使用您的 `.syncignore` 文件来排除对您的工作流不重要的项目，特别是那些同步缓慢或占用大量存储空间的项目。

## 已知问题

- 对 `.syncignore` 的更改不会导致立即删除，除非重新创建文件共享。换句话说，由于修改 `.syncignore` 文件而新被忽略的文件仍保留在其当前位置，但在同步期间不再更新。

- 文件共享实例目前限制为每份共享约 200 万个文件。为了获得最佳性能，如果您有这种规模的文件共享实例，请尝试将其分解为对应于各个绑定挂载位置的多个共享。

- 由于 Linux 区分大小写而 macOS/Windows 仅保留大小写，大小写冲突在 GUI 中显示为 **File exists**（文件已存在）问题。这些可以忽略。但是，如果问题持续存在，您可以报告该问题。

- 同步文件共享会主动报告临时问题，这可能会导致在同步期间 GUI 中偶尔出现 **Conflict**（冲突）和 **Problem**（问题）指示器。这些可以忽略。但是，如果问题持续存在，您可以报告该问题。

- 如果您在 Windows 上从 WSL2 切换到 Hyper-V，则需要完全重启 Docker Desktop。

- 不支持 POSIX 风格的 Windows 路径。避免在 Docker Compose 中设置 [`COMPOSE_CONVERT_WINDOWS_PATHS`](/manuals/compose/how-tos/environment-variables/envvars.md#compose_convert_windows_paths) 环境变量。

- 如果您没有创建符号链接的正确权限，且您的容器尝试在文件共享实例中创建符号链接，则会显示 **unable to create symbolic link**（无法创建符号链接）错误消息。对于 Windows 用户，请参阅微软的 [创建符号链接文档](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/create-symbolic-links) 以获取最佳实践以及 **Create symbolic links** 安全策略设置的位置。对于 Mac 和 Linux 用户，请检查您是否对该文件夹具有写权限。
