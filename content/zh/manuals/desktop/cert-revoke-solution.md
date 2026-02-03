---
description: 了解如何解决影响 macOS 版 Docker Desktop 用户的问题，包括启动故障和虚假的恶意软件警告。提供升级、打补丁及临时避让方案。
keywords: Docker desktop, 修复, fix, mac, troubleshooting, 排查, macos, 虚假恶意软件警告, false malware warning, patch, upgrade solution
title: 解决近期 macOS 版 Docker Desktop 的问题
linkTitle: 修复 Mac 启动问题
weight: 220
---

本指南提供了解决近期影响部分 macOS 版 Docker Desktop 用户问题的步骤。该问题可能会阻止 Docker Desktop 启动，在某些情况下，还可能触发错误的恶意软件警告。有关该事件的更多详细信息，请参阅[博客文章](https://www.docker.com/blog/incident-update-docker-desktop-for-mac/)。

> [!NOTE]
>
> Docker Desktop 4.28 及更早版本不受此问题影响。

## 可用解决方案

根据您的具体情况，有几种方案可供选择：

### 升级到 Docker Desktop 4.37.2（推荐）

推荐的方法是升级到最新的 Docker Desktop 版本，即 4.37.2 版。

如果可能，请直接通过应用进行更新。如果无法直接更新且仍看到恶意软件弹出窗口，请按照以下步骤操作：

1. 杀掉无法正常启动的 Docker 进程：
   ```console
   $ sudo launchctl bootout system/com.docker.vmnetd 2>/dev/null || true
   $ sudo launchctl bootout system/com.docker.socket 2>/dev/null || true
    
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.vmnetd || true
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.socket || true
 
   $ ps aux | grep -i docker | awk '{print $2}' | sudo xargs kill -9 2>/dev/null
   ```
    
2. 确保恶意软件弹出窗口已永久关闭。

3. [下载并安装 4.37.2 版本](/manuals/desktop/release-notes.md#4372)。

4. 启动 Docker Desktop。5 到 10 秒后会显示一个特权操作弹出消息。

5. 输入您的密码。

现在您应该能看到 Docker Desktop 的控制面板。

> [!TIP]
>
> 如果完成这些步骤后恶意软件弹出窗口仍然存在，且 Docker 已在废纸篓中，请尝试清空废纸篓并重新运行上述步骤。

### 如果您使用的是 4.32 - 4.36 版本，请安装补丁

如果您无法升级到最新版本且正看到恶意软件弹出窗口，请按照以下步骤操作：

1. 杀掉无法正常启动的 Docker 进程：
   ```console
   $ sudo launchctl bootout system/com.docker.vmnetd 2>/dev/null || true
   $ sudo launchctl bootout system/com.docker.socket 2>/dev/null || true
    
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.vmnetd || true
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.socket || true
 
   $ ps aux | grep docker | awk '{print $2}' | sudo xargs kill -9 2>/dev/null
   ```

2. 确保恶意软件弹出窗口已永久关闭。

3. [下载并安装补丁安装程序](/manuals/desktop/release-notes.md)，该程序应与您当前的基础版本匹配。例如，如果您使用的是 4.36.0 版本，请安装 4.36.1。

4. 启动 Docker Desktop。5 到 10 秒后会显示一个特权操作弹出消息。

5. 输入您的密码。

现在您应该能看到 Docker Desktop 的控制面板。

> [!TIP]
>
> 如果完成这些步骤后恶意软件弹出窗口仍然存在，且 Docker 已在废纸篓中，请尝试清空废纸篓并重新运行上述步骤。

## MDM 脚本

如果您是 IT 管理员且您的开发人员看到了恶意软件弹出窗口：

1. 确保您的开发人员拥有经过重新签名的 Docker Desktop 4.32 或更高版本。
2. 运行以下脚本：

   ```console
   #!/bin/bash

   # 停止 docker 服务
   echo "Stopping Docker..."
   sudo pkill -i docker

   # 停止 vmnetd 服务
   echo "Stopping com.docker.vmnetd service..."
   sudo launchctl bootout system /Library/LaunchDaemons/com.docker.vmnetd.plist

   # 停止 socket 服务
   echo "Stopping com.docker.socket service..."
   sudo launchctl bootout system /Library/LaunchDaemons/com.docker.socket.plist

   # 移除 vmnetd 二进制文件
   echo "Removing com.docker.vmnetd binary..."
   sudo rm -f /Library/PrivilegedHelperTools/com.docker.vmnetd

   # 移除 socket 二进制文件
   echo "Removing com.docker.socket binary..."
   sudo rm -f /Library/PrivilegedHelperTools/com.docker.socket

   # 安装新的二进制文件
   echo "Install new binaries..."
   sudo cp /Applications/Docker.app/Contents/Library/LaunchServices/com.docker.vmnetd /Library/PrivilegedHelperTools/
   sudo cp /Applications/Docker.app/Contents/MacOS/com.docker.socket /Library/PrivilegedHelperTools/
   ```

## Homebrew 桶 (Casks)

如果您是使用 Homebrew casks 安装的 Docker Desktop，建议的解决方案是执行完整的重新安装以解决此问题。

要重新安装 Docker Desktop，请在终端中运行以下命令：

```console
$ brew update
$ brew reinstall --cask docker
```

这些命令将更新 Homebrew 并完全重新安装 Docker Desktop，确保您获得应用了修复补丁的最新版本。