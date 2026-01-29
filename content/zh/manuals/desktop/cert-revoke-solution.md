---
description: 了解如何通过升级、打补丁和变通方法解决影响 macOS 用户使用 Docker Desktop 的问题，包括启动问题和错误的恶意软件警告。
keywords: Docker desktop, 修复, mac, 故障排除, macos, 错误恶意软件警告, 补丁, 升级方案
title: 解决近期 macOS 上的 Docker Desktop 问题
linkTitle: 修复 Mac 启动问题
weight: 220
---

本指南提供了解决近期影响部分 macOS Docker Desktop 用户的问题的步骤。该问题可能会阻止 Docker Desktop 启动，在某些情况下，还可能触发不准确的恶意软件警告。有关此事件的更多详情，请参阅[博客文章](https://www.docker.com/blog/incident-update-docker-desktop-for-mac/)。

> [!NOTE]
>
> Docker Desktop 4.28 及更早版本不受此问题影响。 

## 可用解决方案

根据您的情况，有几种可供选择的方案：

### 升级到 Docker Desktop 4.37.2 版本（推荐）

推荐的方法是升级到最新的 Docker Desktop 版本，即 4.37.2 版本。 

如果可能，直接通过应用程序进行更新。如果不行，且您仍然看到恶意软件弹窗，请按照以下步骤操作：

1. 杀掉无法正常启动的 Docker 进程：
   ```console
   $ sudo launchctl bootout system/com.docker.vmnetd 2>/dev/null || true
   $ sudo launchctl bootout system/com.docker.socket 2>/dev/null || true
    
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.vmnetd || true
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.socket || true
 
   $ ps aux | grep -i docker | awk '{print $2}' | sudo xargs kill -9 2>/dev/null
   ```
    
2. 确保恶意软件弹窗已永久关闭。 

3. [下载并安装 4.37.2 版本](/manuals/desktop/release-notes.md#4372)。

4. 启动 Docker Desktop。5 到 10 秒后会显示一个特权请求弹窗。

5. 输入您的密码。

您现在应该能看到 Docker Desktop 控制面板了。

> [!TIP]
>
> 如果完成这些步骤后恶意软件弹窗仍然存在，且 Docker 已在废纸篓中，请尝试清空废纸篓并重新运行上述步骤。

### 如果您使用的是 4.32 - 4.36 版本，请安装补丁

如果您无法升级到最新版本且看到了恶意软件弹窗，请按照以下步骤操作：

1. 杀掉无法正常启动的 Docker 进程：
   ```console
   $ sudo launchctl bootout system/com.docker.vmnetd 2>/dev/null || true
   $ sudo launchctl bootout system/com.docker.socket 2>/dev/null || true
    
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.vmnetd || true
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.socket || true
 
   $ ps aux | grep docker | awk '{print $2}' | sudo xargs kill -9 2>/dev/null
   ```

2. 确保恶意软件弹窗已永久关闭。

3. [下载并安装与您当前基础版本匹配的补丁安装程序](/manuals/desktop/release-notes.md)。例如，如果您使用的是 4.36.0 版本，请安装 4.36.1。

4. 启动 Docker Desktop。5 到 10 秒后会显示一个特权请求弹窗。

5. 输入您的密码。

您现在应该能看到 Docker Desktop 控制面板了。

> [!TIP]
>
> 如果完成这些步骤后恶意软件弹窗仍然存在，且 Docker 已在废纸篓中，请尝试清空废纸篓并重新运行上述步骤。

## MDM 脚本

如果您是 IT 管理员，且您的开发人员看到了恶意软件弹窗：

1. 确保您的开发人员拥有经过重新签名的 Docker Desktop 4.32 或更高版本。
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

## Homebrew 桶 (Casks)

如果您是使用 Homebrew 桶安装的 Docker Desktop，推荐的解决方案是执行完整重新安装以解决此问题。

要重新安装 Docker Desktop，请在终端中运行以下命令：

```console
$ brew update
$ brew reinstall --cask docker
```

这些命令将更新 Homebrew 并完全重新安装 Docker Desktop，确保您拥有应用了修复程序的最新版本。
