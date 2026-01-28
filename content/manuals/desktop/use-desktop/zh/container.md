---
description: 了解在 Docker Dashboard 上使用 Containers 视图可以执行的操作
keywords: Docker Dashboard, manage, containers, gui, dashboard, images, user manual
title: 探索 Docker Desktop 中的 Containers 视图
linkTitle: Containers
weight: 10
---

**Containers**（容器）视图列出所有正在运行和已停止的容器及应用程序。它提供了一个简洁的界面来管理容器的生命周期、与正在运行的应用程序交互，以及检查 Docker 对象——包括 Docker Compose 应用程序。

## 容器操作

使用 **Search**（搜索）字段按名称查找特定容器。

从 **Containers** 视图，您可以：
- 启动、停止、暂停、恢复或重启容器
- 查看镜像包和 CVE
- 删除容器
- 在 VS Code 中打开应用程序
- 在浏览器中打开容器暴露的端口
- 复制 `docker run` 命令以便重用或修改
- 使用 [Docker Debug](#execdebug)

## 资源使用

从 **Containers** 视图，您可以监控容器随时间变化的 CPU 和内存使用情况。这可以帮助您了解容器是否存在问题，或者是否需要分配额外的资源。

当您[检查容器](#inspect-a-container)时，**Stats**（统计）选项卡会显示有关容器资源利用率的更多信息。您可以查看容器随时间变化的 CPU、内存、网络和磁盘空间使用情况。

## 检查容器

选择容器时，您可以获取有关该容器的详细信息。

在这里，您可以使用快速操作按钮执行各种操作，如暂停、恢复、启动或停止，或浏览 **Logs**（日志）、**Inspect**（检查）、**Bind mounts**（绑定挂载）、**Debug**（调试）、**Files**（文件）和 **Stats**（统计）选项卡。

### 日志

选择 **Logs** 以实时查看容器的输出。在查看日志时，您可以：

- 使用 `Cmd + f`/`Ctrl + f` 打开搜索栏并查找特定条目。搜索匹配项以黄色高亮显示。
- 按 `Enter` 或 `Shift + Enter` 分别跳转到下一个或上一个搜索匹配项。
- 使用右上角的 **Copy**（复制）图标将所有日志复制到剪贴板。
- 显示时间戳
- 使用右上角的 **Clear terminal**（清除终端）图标清除日志终端。
- 选择并查看日志中可能存在的外部链接。

您可以通过以下方式优化视图：

- 如果您正在运行多容器应用程序，可以筛选特定容器的日志。
- 使用正则表达式或精确匹配搜索词

### 检查

选择 **Inspect** 以查看容器的底层信息。它显示本地路径、镜像版本号、SHA-256、端口映射和其他详细信息。

### Exec/Debug

如果您没有在设置中启用 Docker Debug，会显示 **Exec** 选项卡。它允许您在正在运行的容器中快速运行命令。

使用 **Exec** 选项卡与运行以下命令相同：

- `docker exec -it <container-id> /bin/sh`
- `docker exec -it <container-id> cmd.exe`（访问 Windows 容器时）

有关更多详情，请参阅 [`docker exec` CLI 参考](/reference/cli/docker/exec/)。

如果您已在设置中启用 Docker Debug，或者在选项卡选项右侧切换打开 **Debug mode**（调试模式），会显示 **Debug** 选项卡。

调试模式需要 [Pro、Team 或 Business 订阅](/subscription/details/)。调试模式有几个优点，例如：

- 可自定义的工具箱。工具箱预装了许多标准 Linux 工具，如 `vim`、`nano`、`htop` 和 `curl`。有关更多详情，请参阅 [`docker debug` CLI 参考](/reference/cli/docker/debug/)。
- 能够访问没有 shell 的容器，例如精简版或 distroless 容器。

要使用调试模式：

1. 使用具有 Pro、Team 或 Business 订阅的账户登录 Docker Desktop。
2. 登录后，可以：

   - 将鼠标悬停在正在运行的容器上，在 **Actions** 列下选择 **Show container actions** 菜单。从下拉菜单中选择 **Use Docker Debug**（使用 Docker Debug）。
   - 或者，选择容器，然后选择 **Debug** 选项卡。

要默认使用调试模式，请导航到 **Settings** 中的 **General** 选项卡，然后选择 **Enable Docker Debug by default**（默认启用 Docker Debug）选项。

### 文件

选择 **Files** 以浏览正在运行或已停止容器的文件系统。您还可以：

- 查看最近添加、修改或删除的文件
- 直接从内置编辑器编辑文件
- 在主机和容器之间拖放文件和文件夹
- 右键单击文件时删除不需要的文件
- 将文件和文件夹从容器直接下载到主机

## 其他资源

- [什么是容器](/get-started/docker-concepts/the-basics/what-is-a-container.md)
- [运行多容器应用程序](/get-started/docker-concepts/running-containers/multi-container-applications.md)
