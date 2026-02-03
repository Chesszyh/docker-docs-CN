---
description: 如何卸载 Docker Desktop
keywords: Windows, 卸载, uninstall, Mac, Linux, Docker Desktop
title: 卸载 Docker Desktop
linkTitle: 卸载
weight: 210
---

> [!WARNING]
>
> 卸载 Docker Desktop 会销毁机器本地的 Docker 容器、镜像、卷以及其他 Docker 相关数据，并移除应用程序生成的文件。要了解如何在卸载前保存重要数据，请参考[备份与还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md)部分。

{{< tabs >}}
{{< tab name="Windows" >}}

#### 通过图形界面 (GUI)

1. 从 Windows **开始 (Start)** 菜单中，选择 **设置 (Settings)** > **应用 (Apps)** > **应用和功能 (Apps & features)**。
2. 从 **应用和功能** 列表中选择 **Docker Desktop**，然后选择 **卸载 (Uninstall)**。
3. 选择 **卸载 (Uninstall)** 进行确认。

#### 通过命令行 (CLI)

1. 找到安装程序：
   ```console
   $ C:\Program Files\Docker\Docker\Docker Desktop Installer.exe
   ```
2. 卸载 Docker Desktop。
 - 在 PowerShell 中运行：
    ```console
    $ Start-Process 'Docker Desktop Installer.exe' -Wait uninstall
    ```
 - 在命令提示符 (Command Prompt) 中运行：
    ```console
    $ start /w "" "Docker Desktop Installer.exe" uninstall
    ```

卸载 Docker Desktop 后，可能会残留一些文件，您可以手动移除它们。这些文件包括：

```console
C:\ProgramData\Docker
C:\ProgramData\DockerDesktop
C:\Program Files\Docker
C:\Users\<您的用户名>\AppData\Local\Docker
C:\Users\<您的用户名>\AppData\Roaming\Docker
C:\Users\<您的用户名>\AppData\Roaming\Docker Desktop
C:\Users\<您的用户名>\.docker
```
 
{{< /tab >}}
{{< tab name="Mac" >}}

#### 通过图形界面 (GUI)

1. 打开 Docker Desktop。
2. 在 Docker Desktop 控制面板的右上角，选择 **故障排除 (Troubleshoot)** 图标（即小虫子图标）。
3. 选择 **卸载 (Uninstall)**。
4. 出现提示时，再次选择 **卸载 (Uninstall)** 进行确认。

之后，您可以将 Docker 应用程序移动到废纸篓。

#### 通过命令行 (CLI)

运行：

```console
$ /Applications/Docker.app/Contents/MacOS/uninstall
```

之后，您可以将 Docker 应用程序移动到废纸篓。

> [!NOTE]
> 使用卸载命令卸载 Docker Desktop 时，您可能会遇到以下错误：
>
> ```console
> $ /Applications/Docker.app/Contents/MacOS/uninstall
> Password:
> Uninstalling Docker Desktop...
> Error: unlinkat /Users/<USER_HOME>/Library/Containers/com.docker.docker/.com.apple.containermanagerd.metadata.plist: > operation not permitted
> ```
>
> 这种“操作不允许 (operation not permitted)”的错误通常出现在文件 `.com.apple.containermanagerd.metadata.plist` 或其父目录 `/Users/<USER_HOME>/Library/Containers/com.docker.docker/` 上。您可以忽略此错误，因为 Docker Desktop 已经成功卸载。
> 您可以稍后通过为所使用的终端应用程序开启“完全磁盘访问权限 (Full Disk Access)”（依次进入 **系统设置** > **隐私与安全性** > **完全磁盘访问权限**）来手动移除 `/Users/<USER_HOME>/Library/Containers/com.docker.docker/` 目录。

卸载 Docker Desktop 后，可能会残留一些文件，您可以移除它们：

```console
$ rm -rf ~/Library/Group\ Containers/group.com.docker
$ rm -rf ~/.docker
```

对于 Docker Desktop 4.36 及更早版本，文件系统中可能还会残留以下文件。您可以使用管理员权限移除它们：

```console
/Library/PrivilegedHelperTools/com.docker.vmnetd
/Library/PrivilegedHelperTools/com.docker.socket
```

{{< /tab >}}
{{< tab name="Ubuntu" >}}

要在 Ubuntu 上卸载 Docker Desktop：

1. 移除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo apt remove docker-desktop
   ```

   这会移除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动移除残留文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo apt purge docker-desktop
   ```

   这会移除 `$HOME/.docker/desktop` 处的配置和数据文件、`/usr/local/bin/com.docker.cli` 处的符号链接，并清除残留的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，移除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 在哪里存储凭据以及哪个上下文是活动的。如果在卸载 Docker Desktop 后保留这些条目，它们可能会与未来的 Docker 设置产生冲突。

{{< /tab >}}
{{< tab name="Debian" >}}

要在 Debian 上卸载 Docker Desktop，请运行：

1. 移除 Docker Desktop 应用程序：

   ```console
   $ sudo apt remove docker-desktop
   ```

   这会移除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动移除残留文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo apt purge docker-desktop
   ```

   这会移除 `$HOME/.docker/desktop` 处的配置和数据文件、`/usr/local/bin/com.docker.cli` 处的符号链接，并清除残留的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，移除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 在哪里存储凭据以及哪个上下文是活动的。如果在卸载 Docker Desktop 后保留这些条目，它们可能会与未来的 Docker 设置产生冲突。

{{< /tab >}}
{{< tab name="Fedora" >}}

要在 Fedora 上卸载 Docker Desktop：

1. 移除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo dnf remove docker-desktop
   ```

   这会移除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动移除残留文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo apt purge docker-desktop
   ```

   这会移除 `$HOME/.docker/desktop` 处的配置和数据文件、`/usr/local/bin/com.docker.cli` 处的符号链接，并清除残留的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，移除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 在哪里存储凭据以及哪个上下文是活动的。如果在卸载 Docker Desktop 后保留这些条目，它们可能会与未来的 Docker 设置产生冲突。

{{< /tab >}}
{{< tab name="Arch" >}}

要在 Arch 上卸载 Docker Desktop：

1. 移除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo pacman -Rns docker-desktop
   ```

   这会移除 Docker Desktop 软件包及其配置文件，以及其他软件包不需要的依赖项。

2. 手动移除残留文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   ```

   这会移除 `$HOME/.docker/desktop` 处的配置和数据文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，移除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 在哪里存储凭据以及哪个上下文是活动的。如果在卸载 Docker Desktop 后保留这些条目，它们可能会与未来的 Docker 设置产生冲突。

{{< /tab >}}
{{< /tabs >}}