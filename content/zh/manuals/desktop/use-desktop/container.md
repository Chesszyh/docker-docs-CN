---
description: 了解您可以如何通过 Docker 控制面板的“容器 (Containers)”视图进行操作
keywords: Docker Dashboard, 管理, 容器, gui, 控制面板, dashboard, images, 镜像, 用户手册
title: 探索 Docker Desktop 中的容器 (Containers) 视图
linkTitle: 容器 (Containers)
weight: 10
---

**容器 (Containers)** 视图列出了所有运行中及已停止的容器和应用程序。它提供了一个整洁的界面，用于管理容器的生命周期、与运行中的应用程序交互以及检查 Docker 对象（包括 Docker Compose 应用）。

## 容器操作

使用 **Search** 字段可以通过名称查找特定的容器。

在 **Containers** 视图中，您可以：
- 启动、停止、暂停、恢复或重启容器
- 查看镜像软件包和 CVE（常见漏洞与披露）
- 删除容器
- 在 VS Code 中打开应用程序
- 在浏览器中打开容器暴露的端口
- 复制 `docker run` 命令以便重用或修改
- 使用 [Docker Debug](#execdebug)

## 资源占用

在 **Containers** 视图中，您可以监控容器随时间变化的 CPU 和内存使用情况。这可以帮助您了解容器是否存在异常，或者是否需要分配额外的资源。

当您 [检查容器](#检查容器) 时，**Stats** 选项卡会显示有关容器资源利用率的进一步信息。您可以查看容器随时间变化的 CPU、内存、网络和磁盘空间使用情况。

## 检查容器

选中容器后，您可以获取其详细信息。

在这里，您可以使用快速操作按钮执行各种操作，如暂停、恢复、启动或停止，也可以探索 **Logs**、**Inspect**、**Bind mounts**、**Debug**、**Files** 和 **Stats** 选项卡。

### 日志 (Logs)

选择 **Logs** 可实时查看容器的输出。在查看日志时，您可以：

- 使用 `Cmd + f`/`Ctrl + f` 打开搜索栏查找特定条目。匹配项将以黄色高亮显示。
- 分别按 `Enter` 或 `Shift + Enter` 跳转到下一个或上一个匹配项。
- 使用右上角的 **Copy** 图标将所有日志复制到剪贴板。
- 显示时间戳。
- 使用右上角的 **Clear terminal** 图标清除日志终端。
- 选择并查看日志中可能存在的外部链接。

您可以通过以下方式优化视图：

- 如果您运行的是多容器应用，可以按特定容器过滤日志。
- 使用正则表达式或精确匹配搜索词。

### 检查 (Inspect)

选择 **Inspect** 查看有关容器的底层信息。它显示了本地路径、镜像版本号、SHA-256、端口映射等详情。

### 执行与调试 (Exec/Debug)

如果您未在设置中启用 Docker Debug，将显示 **Exec** 选项卡。它让您可以在运行中的容器内快速运行命令。

使用 **Exec** 选项卡等同于运行以下命令之一：

- `docker exec -it <container-id> /bin/sh`
- 访问 Windows 容器时运行 `docker exec -it <container-id> cmd.exe`

有关更多详情，请参阅 [`docker exec` CLI 参考](/reference/cli/docker/exec/)。

如果您在设置中启用了 Docker Debug，或者开启了选项卡右侧的 **Debug mode** 开关，将显示 **Debug** 选项卡。

调试模式需要 [Pro、Team 或 Business 订阅](/subscription/details/)。调试模式具有多项优势，例如：

- **可定制的工具箱**：工具箱预装了许多标准的 Linux 工具，如 `vim`、`nano`、`htop` 和 `curl`。有关更多详情，请参阅 [`docker debug` CLI 参考](/reference/cli/docker/debug/)。
- **访问无 shell 容器的能力**：例如可以访问 slim 或 distroless 容器。

要使用调试模式：

1. 使用拥有 Pro、Team 或 Business 订阅的帐户登录 Docker Desktop。
2. 登录后，您可以采取以下任一操作：
   - 将鼠标悬停在运行中的容器上，在 **Actions** 列下，点击 **Show container actions** 菜单。从下拉菜单中选择 **Use Docker Debug**。
   - 或者，选择容器，然后选择 **Debug** 选项卡。

若要默认使用调试模式，请前往 **Settings** 中的 **General** 选项卡，并勾选 **Enable Docker Debug by default** 选项。

### 文件 (Files)

选择 **Files** 可探索运行中或已停止容器的文件系统。您还可以：

- 查看最近添加、修改或删除的文件
- 直接通过内置编辑器编辑文件
- 在宿主机和容器之间拖放文件和文件夹
- 右键点击文件以删除不需要的文件
- 将文件和文件夹从容器直接下载到宿主机

## 额外资源

- [什么是容器？](/get-started/docker-concepts/the-basics/what-is-a-container.md)
- [运行多容器应用程序](/get-started/docker-concepts/running-containers/multi-container-applications.md)
