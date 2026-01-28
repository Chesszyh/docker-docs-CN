---
description: 了解如何诊断和排除 Docker Desktop 故障，以及如何查看日志。
keywords: Linux, Mac, Windows, troubleshooting, logs, issues, Docker Desktop
toc_max: 2
title: Docker Desktop 故障排除
linkTitle: 故障排除和诊断
aliases:
 - /desktop/linux/troubleshoot/
 - /desktop/mac/troubleshoot/
 - /desktop/windows/troubleshoot/
 - /docker-for-mac/troubleshoot/
 - /mackit/troubleshoot/
 - /windows/troubleshoot/
 - /docker-for-win/troubleshoot/
 - /docker-for-windows/troubleshoot/
 - /desktop/troubleshoot/overview/
 - /desktop/troubleshoot/
tags: [ Troubleshooting ]
weight: 10
---

本页包含有关如何诊断和排除 Docker Desktop 故障以及如何查看日志的信息。

> [!WARNING]
>
> 如果您在 Mac 上遇到恶意软件检测问题，请按照 [docker/for-mac#7527](https://github.com/docker/for-mac/issues/7527) 中记录的步骤操作。

## 故障排除菜单

要导航到 **Troubleshoot**，您可以：

- 选择 Docker 菜单 Docker menu {{< inline-image src="../../images/whale-x.svg" alt="whale menu" >}}，然后选择 **Troubleshoot**。
- 选择 Docker Dashboard 右上角附近的 **Troubleshoot** 图标。

**Troubleshooting** 菜单包含以下选项：

- **Restart Docker Desktop**。

- **Reset Kubernetes cluster**。选择此选项可删除所有堆栈和 Kubernetes 资源。有关更多信息，请参阅 [Kubernetes](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes)。

- **Clean / Purge data**。此选项会重置所有 Docker 数据而不恢复出厂默认设置。选择此选项会导致现有设置丢失。

- **Reset to factory defaults**：选择此选项可将 Docker Desktop 上的所有选项重置为初始状态，与首次安装 Docker Desktop 时相同。

如果您是 Mac 或 Linux 用户，您还可以选择从系统中**卸载** Docker Desktop。

## 诊断

> [!TIP]
>
> 如果您在故障排除中找不到解决方案，请浏览 GitHub 仓库或创建新 issue：
>
> - [docker/for-mac](https://github.com/docker/for-mac/issues)
> - [docker/for-win](https://github.com/docker/for-win/issues)
> - [docker/for-linux](https://github.com/docker/for-linux/issues)

### 从应用程序诊断

1. 从 **Troubleshoot** 中，选择 **Get support**。这将打开应用内支持页面并开始收集诊断信息。
2. 诊断信息收集过程完成后，选择 **Upload to get a Diagnostic ID**。
3. 诊断信息上传后，Docker Desktop 会打印一个诊断 ID。复制此 ID。
4. 使用您的诊断 ID 获取帮助：
    - 如果您拥有付费 Docker 订阅，选择 **Contact support**。这将打开 Docker Desktop 支持表单。填写所需信息，并将您在第三步复制的 ID 添加到 **Diagnostics ID field**。然后，选择 **Submit ticket** 请求 Docker Desktop 支持。
        > [!NOTE]
        >
        > 您必须登录 Docker Desktop 才能访问支持表单。有关 Docker Desktop 支持涵盖内容的信息，请参阅[支持](/manuals/desktop/troubleshoot-and-support/support.md)。
    - 如果您没有付费 Docker 订阅，选择 **Report a Bug** 在 GitHub 上打开新的 Docker Desktop issue。填写所需信息，并确保添加您在第三步复制的诊断 ID。

### 从错误消息诊断

1. 当出现错误消息时，选择 **Gather diagnostics**。
2. 诊断信息上传后，Docker Desktop 会打印一个诊断 ID。复制此 ID。
3. 使用您的诊断 ID 获取帮助：
    - 如果您拥有付费 Docker 订阅，选择 **Contact support**。这将打开 Docker Desktop 支持表单。填写所需信息，并将您在第三步复制的 ID 添加到 **Diagnostics ID field**。然后，选择 **Submit ticket** 请求 Docker Desktop 支持。
        > [!NOTE]
        >
        > 您必须登录 Docker Desktop 才能访问支持表单。有关 Docker Desktop 支持涵盖内容的信息，请参阅[支持](/manuals/desktop/troubleshoot-and-support/support.md)。
    - 如果您没有付费 Docker 订阅，您可以在 GitHub 上为 [Mac](https://github.com/docker/for-mac/issues)、[Windows](https://github.com/docker/for-win/issues) 或 [Linux](https://github.com/docker/for-linux/issues) 打开新的 Docker Desktop issue。填写所需信息，并确保添加您在第二步打印的诊断 ID。

### 从终端诊断

在某些情况下，自己运行诊断很有用，例如当 Docker Desktop 无法启动时。

{{< tabs group="os" >}}
{{< tab name="Windows" >}}

1. 找到 `com.docker.diagnose` 工具：

   ```console
   $ C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe
   ```

2. 创建并上传诊断 ID。在 PowerShell 中，运行：

   ```console
   $ & "C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe" gather -upload
   ```

诊断完成后，终端会显示您的诊断 ID 和诊断文件的路径。诊断 ID 由您的用户 ID 和时间戳组成。例如 `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`。

{{< /tab >}}
{{< tab name="Mac" >}}

1. 找到 `com.docker.diagnose` 工具：

   ```console
   $ /Applications/Docker.app/Contents/MacOS/com.docker.diagnose
   ```

2. 创建并上传诊断 ID。运行：

   ```console
   $ /Applications/Docker.app/Contents/MacOS/com.docker.diagnose gather -upload
   ```

诊断完成后，终端会显示您的诊断 ID 和诊断文件的路径。诊断 ID 由您的用户 ID 和时间戳组成。例如 `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`。

{{< /tab >}}
{{< tab name="Linux" >}}

1. 找到 `com.docker.diagnose` 工具：

   ```console
   $ /opt/docker-desktop/bin/com.docker.diagnose
   ```

2. 创建并上传诊断 ID。运行：

   ```console
   $ /opt/docker-desktop/bin/com.docker.diagnose gather -upload
   ```

诊断完成后，终端会显示您的诊断 ID 和诊断文件的路径。诊断 ID 由您的用户 ID 和时间戳组成。例如 `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`。

{{< /tab >}}
{{< /tabs >}}

要查看诊断文件的内容：

{{< tabs group="os" >}}
{{< tab name="Windows" >}}

1. 解压文件。在 PowerShell 中，将诊断文件的路径复制粘贴到以下命令中，然后运行。它应类似于以下示例：

   ```powershell
   $ Expand-Archive -LiteralPath "C:\Users\testUser\AppData\Local\Temp\5DE9978A-3848-429E-8776-950FC869186F\20230607101602.zip" -DestinationPath "C:\Users\testuser\AppData\Local\Temp\5DE9978A-3848-429E-8776-950FC869186F\20230607101602"
   ```

2. 在您喜欢的文本编辑器中打开文件。运行：

   ```powershell
   $ code <path-to-file>
   ```

{{< /tab >}}
{{< tab name="Mac" >}}

运行：

```console
$ open /tmp/<your-diagnostics-ID>.zip
```

{{< /tab >}}
{{< tab name="Linux" >}}

运行：

```console
$ unzip –l /tmp/<your-diagnostics-ID>.zip
```

{{< /tab >}}
{{< /tabs >}}

#### 使用诊断 ID 获取帮助

如果您拥有付费 Docker 订阅，选择 **Contact support**。这将打开 Docker Desktop 支持表单。填写所需信息，并将您在第三步复制的 ID 添加到 **Diagnostics ID field**。然后，选择 **Submit ticket** 请求 Docker Desktop 支持。

如果您没有付费 Docker 订阅，请在 GitHub 上创建 issue：

- [For Linux](https://github.com/docker/desktop-linux/issues)
- [For Mac](https://github.com/docker/for-mac/issues)
- [For Windows](https://github.com/docker/for-win/issues)

### 自诊断工具

> [!IMPORTANT]
>
> 此工具已被弃用。

## 查看日志

除了使用诊断选项提交日志外，您还可以自己浏览日志。

{{< tabs group="os" >}}
{{< tab name="Windows" >}}

在 PowerShell 中，运行：

```powershell
$ code $Env:LOCALAPPDATA\Docker\log
```

这将在您喜欢的文本编辑器中打开所有日志供您探索。

{{< /tab >}}
{{< tab name="Mac" >}}

### 从终端

要在命令行中实时查看 Docker Desktop 日志流，请从您喜欢的 shell 运行以下脚本。

```console
$ pred='process matches ".*(ocker|vpnkit).*" || (process in {"taskgated-helper", "launchservicesd", "kernel"} && eventMessage contains[c] "docker")'
$ /usr/bin/log stream --style syslog --level=debug --color=always --predicate "$pred"
```

或者，要将最近一天的日志（`1d`）收集到文件中，运行：

```console
$ /usr/bin/log show --debug --info --style syslog --last 1d --predicate "$pred" >/tmp/logs.txt
```

### 从控制台应用程序

Mac 提供了一个内置的日志查看器，名为 **Console**，您可以使用它来查看 Docker 日志。

Console 位于 `/Applications/Utilities`。您可以使用 Spotlight 搜索找到它。

要读取 Docker 应用程序日志消息，请在 Console 窗口搜索栏中输入 `docker` 并按 Enter。然后选择 `ANY` 以展开 `docker` 搜索条目旁边的下拉列表，并选择 `Process`。

![Mac Console 搜索 Docker 应用程序](../../images/console.png)

您可以使用 Console Log Query 搜索日志、以各种方式过滤结果并创建报告。

{{< /tab >}}
{{< tab name="Linux" >}}

您可以通过运行以下命令访问 Docker Desktop 日志：

```console
$ journalctl --user --unit=docker-desktop
```

您还可以在 `$HOME/.docker/desktop/log/` 找到 Docker Desktop 内部组件的日志。

{{< /tab >}}
{{< /tabs >}}

## 查看 Docker 守护进程日志

请参阅[阅读守护进程日志](/manuals/engine/daemon/logs.md)部分了解如何查看 Docker 守护进程日志。

## 更多资源

- 查看特定的[故障排除主题](topics.md)。
- 查看[已知问题](known-issues.md)信息
