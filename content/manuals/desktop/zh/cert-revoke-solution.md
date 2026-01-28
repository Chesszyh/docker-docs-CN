---
description: 了解如何解决影响 macOS 用户的 Docker Desktop 问题，包括启动问题和虚假恶意软件警告，以及升级、补丁和解决方案。
keywords: Docker desktop, fix, mac, troubleshooting, macos, false malware warning, patch, upgrade solution
title: 解决 macOS 上最近的 Docker Desktop 问题
linkTitle: 修复 Mac 启动问题
weight: 220
---

本指南提供了解决影响部分 macOS 用户的最近 Docker Desktop 问题的步骤。该问题可能导致 Docker Desktop 无法启动，在某些情况下，还可能触发不准确的恶意软件警告。有关此事件的更多详细信息，请参阅[博客文章](https://www.docker.com/blog/incident-update-docker-desktop-for-mac/)。

> [!NOTE]
>
> Docker Desktop 4.28 及更早版本不受此问题影响。

## 可用的解决方案

根据您的情况，有几个可用的选项：

### 升级到 Docker Desktop 4.37.2 版本（推荐）

推荐的方法是升级到最新的 Docker Desktop 版本，即 4.37.2 版本。

如果可能，直接通过应用程序进行更新。如果无法更新，并且您仍然看到恶意软件弹出窗口，请按照以下步骤操作：

1. 终止无法正常启动的 Docker 进程：
   ```console
   $ sudo launchctl bootout system/com.docker.vmnetd 2>/dev/null || true
   $ sudo launchctl bootout system/com.docker.socket 2>/dev/null || true

   $ sudo rm /Library/PrivilegedHelperTools/com.docker.vmnetd || true
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.socket || true

   $ ps aux | grep -i docker | awk '{print $2}' | sudo xargs kill -9 2>/dev/null
   ```

2. 确保恶意软件弹出窗口已永久关闭。

3. [下载并安装 4.37.2 版本](/manuals/desktop/release-notes.md#4372)。

4. 启动 Docker Desktop。5 到 10 秒后将显示特权弹出消息。

5. 输入您的密码。

您现在应该可以看到 Docker Desktop Dashboard。

> [!TIP]
>
> 如果在完成这些步骤后恶意软件弹出窗口仍然存在，并且 Docker 在废纸篓中，请尝试清空废纸篓并重新运行这些步骤。

### 如果您使用的是 4.32 - 4.36 版本，请安装补丁

如果您无法升级到最新版本并且看到恶意软件弹出窗口，请按照以下步骤操作：

1. 终止无法正常启动的 Docker 进程：
   ```console
   $ sudo launchctl bootout system/com.docker.vmnetd 2>/dev/null || true
   $ sudo launchctl bootout system/com.docker.socket 2>/dev/null || true

   $ sudo rm /Library/PrivilegedHelperTools/com.docker.vmnetd || true
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.socket || true

   $ ps aux | grep docker | awk '{print $2}' | sudo xargs kill -9 2>/dev/null
   ```

2. 确保恶意软件弹出窗口已永久关闭。

3. [下载并安装](/manuals/desktop/release-notes.md)与您当前基础版本匹配的补丁安装程序。例如，如果您使用的是 4.36.0 版本，请安装 4.36.1。

4. 启动 Docker Desktop。5 到 10 秒后将显示特权弹出消息。

5. 输入您的密码。

您现在应该可以看到 Docker Desktop Dashboard。

> [!TIP]
>
> 如果在完成这些步骤后恶意软件弹出窗口仍然存在，并且 Docker 在废纸篓中，请尝试清空废纸篓并重新运行这些步骤。

## MDM 脚本

如果您是 IT 管理员，并且您的开发人员看到恶意软件弹出窗口：

1. 确保您的开发人员拥有重新签名的 Docker Desktop 4.32 或更高版本。
2. 运行以下脚本：

   ```console
   #!/bin/bash

   # Stop the docker services
   echo "Stopping Docker..."
   sudo pkill -i docker

   # Stop the vmnetd service
   echo "Stopping com.docker.vmnetd service..."
   sudo launchctl bootout system /Library/LaunchDaemons/com.docker.vmnetd.plist

   # Stop the socket service
   echo "Stopping com.docker.socket service..."
   sudo launchctl bootout system /Library/LaunchDaemons/com.docker.socket.plist

   # Remove vmnetd binary
   echo "Removing com.docker.vmnetd binary..."
   sudo rm -f /Library/PrivilegedHelperTools/com.docker.vmnetd

   # Remove socket binary
   echo "Removing com.docker.socket binary..."
   sudo rm -f /Library/PrivilegedHelperTools/com.docker.socket

   # Install new binaries
   echo "Install new binaries..."
   sudo cp /Applications/Docker.app/Contents/Library/LaunchServices/com.docker.vmnetd /Library/PrivilegedHelperTools/
   sudo cp /Applications/Docker.app/Contents/MacOS/com.docker.socket /Library/PrivilegedHelperTools/
   ```

## Homebrew casks

如果您使用 Homebrew casks 安装了 Docker Desktop，推荐的解决方案是执行完全重新安装以解决此问题。

要重新安装 Docker Desktop，请在终端中运行以下命令：

```console
$ brew update
$ brew reinstall --cask docker
```

这些命令将更新 Homebrew 并完全重新安装 Docker Desktop，确保您拥有已应用修复的最新版本。
