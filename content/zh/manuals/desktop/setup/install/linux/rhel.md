---
description: 在 RHEL 上安装 Docker Desktop 的说明
keywords: red hat, red hat enterprise linux, rhel, rpm, 更新安装, 卸载, 升级, 更新, linux, desktop, docker desktop, docker desktop for linux, dd4l
title: 在 RHEL 上安装 Docker Desktop
linkTitle: RHEL
download-url-base: https://download.docker.com/linux/rhel
aliases:
- /desktop/install/linux/rhel/
---

{{< summary-bar feature_name="Docker Desktop RHEL" >}}

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页包含有关如何在 Red Hat Enterprise Linux (RHEL) 发行版上安装、启动和升级 Docker Desktop 的信息。

## 前提条件

要成功安装 Docker Desktop，您必须：

- 满足[通用系统要求](_index.md#通用系统要求)。
- 拥有 RHEL 8 或 RHEL 9 的 64 位版本。
- 拥有一个 [Docker 帐户](/manuals/accounts/create-account.md)，因为在 RHEL 上使用 Docker Desktop 需要进行身份验证。

- 如果未安装 `pass` 或无法安装，您必须启用 [CodeReady Linux Builder (CRB) 存储库](https://access.redhat.com/articles/4348511) 和 [Extra Packages for Enterprise Linux (EPEL)](https://docs.fedoraproject.org/en-US/epel/)。

   {{< tabs group="os_version" >}}
   {{< tab name="RHEL 9" >}}
   ```console
   $ sudo subscription-manager repos --enable codeready-builder-for-rhel-9-$(arch)-rpms
   $ sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
   $ sudo dnf install pass
   ```

   {{< /tab >}}
   {{< tab name="RHEL 8" >}}
   ```console
   $ sudo subscription-manager repos --enable codeready-builder-for-rhel-8-$(arch)-rpms
   $ sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
   $ sudo dnf install pass
   ```

   {{< /tab >}}
   {{< /tabs >}}

- 对于 GNOME 桌面环境，您必须安装 AppIndicator 和 KStatusNotifierItem [GNOME 扩展](https://extensions.gnome.org/extension/615/appindicator-support/)。您还必须启用 EPEL。

   {{< tabs group="os_version" >}}
   {{< tab name="RHEL 9" >}}
   ```console
   $ # 按照上述说明启用 EPEL
   $ sudo dnf install gnome-shell-extension-appindicator
   $ sudo gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
   ```

   {{< /tab >}}
   {{< tab name="RHEL 8" >}}
   ```console
   $ # 按照上述说明启用 EPEL
   $ sudo dnf install gnome-shell-extension-appindicator
   $ sudo dnf install gnome-shell-extension-desktop-icons
   $ sudo gnome-shell-extension-tool -e appindicatorsupport@rgcjonas.gmail.com
   ```

   {{< /tab >}}
   {{< /tabs >}}

- 如果您不使用 GNOME，则必须安装 `gnome-terminal` 以便从 Docker Desktop 访问终端：

   ```console
   $ sudo dnf install gnome-terminal
   ```

## 安装 Docker Desktop

在 RHEL 上安装 Docker Desktop：

1. 如下设置 Docker 的软件包存储库：

   ```console
   $ sudo dnf config-manager --add-repo {{% param "download-url-base" %}}/docker-ce.repo
   ```

2. 下载最新的 [RPM 软件包](https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64-rhel.rpm?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。

3. 使用 dnf 安装软件包，如下所示：

   ```console
   $ sudo dnf install ./docker-desktop-x86_64-rhel.rpm
   ```

RPM 软件包包含一个安装后脚本，可自动完成额外的设置步骤。

安装后脚本会执行以下操作：

- 在 Docker Desktop 二进制文件上设置功能位（capability），以便映射特权端口和设置资源限制。
- 将 Kubernetes 的 DNS 名称添加到 `/etc/hosts`。
- 创建从 `/usr/local/bin/com.docker.cli` 到 `/usr/bin/docker` 的符号链接。
  这是因为经典的 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还会在 `/usr/local/bin/com.docker.cli` 安装一个包含云集成功能的 Docker CLI 二进制文件，它本质上是 Compose CLI 的包装器。符号链接确保该包装器可以访问经典的 Docker CLI。
- 创建从 `/usr/libexec/qemu-kvm` 到 `/usr/local/bin/qemu-system-x86_64` 的符号链接。

## 启动 Docker Desktop

{{% include "desktop-linux-launch.md" %}}

> [!IMPORTANT]
>
> 启动 RHEL 版 Docker Desktop 后，您必须登录 Docker 帐户才能开始使用。

> [!TIP]
>
> 要将 Red Hat 订阅数据挂载到容器中，请参阅 [Red Hat 验证的解决方案](https://access.redhat.com/solutions/5870841)。
>
> 例如：
> ```console
> $ docker run --rm -it -v "/etc/pki/entitlement:/etc/pki/entitlement" -v "/etc/rhsm:/etc/rhsm-host" -v "/etc/yum.repos.d/redhat.repo:/etc/yum.repos.d/redhat.repo" registry.access.redhat.com/ubi9
> ```

## 升级 Docker Desktop

发布新版本的 Docker Desktop 后，Docker UI 会显示通知。每次升级 Docker Desktop 时，您需要先删除旧版本，然后下载并安装新软件包。运行：

```console
$ sudo dnf remove docker-desktop
$ sudo dnf install ./docker-desktop-<arch>-rhel.rpm
```

## 下一步

- 了解 [Docker 订阅方案](https://www.docker.com/pricing/)，查看 Docker 还能为您提供什么。
- 参加 [Docker 工作坊](/get-started/workshop/_index.md)，学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有特性。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 介绍了常见问题、解决方案、如何运行并提交诊断以及提交问题。
- [常见问题解答 (FAQ)](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的解答。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 发行版相关的组件更新、新功能和改进。
- [备份与还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了有关备份和还原 Docker 相关数据的说明。
