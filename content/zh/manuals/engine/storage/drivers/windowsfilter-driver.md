---
description: 了解 windowsfilter 存储驱动程序
keywords: container, storage, driver, windows, windowsfilter, 容器, 存储, 驱动程序
title: windowsfilter 存储驱动程序
---

windowsfilter 存储驱动程序是 Windows 上 Docker Engine 的默认存储驱动程序。windowsfilter 驱动程序使用 Windows 原生文件系统层在磁盘上存储 Docker 层和卷数据。windowsfilter 存储驱动程序仅适用于格式化为 NTFS 的文件系统。

## 配置 windowsfilter 存储驱动程序

对于大多数用例，不需要配置 windowsfilter 存储驱动程序。

Windows 上 Docker Engine 的默认存储限制为 127GB。要使用不同的存储大小，请为 windowsfilter 存储驱动程序设置 `size` 选项。参见 [windowsfilter 选项](/reference/cli/dockerd.md#windowsfilter-options)。

默认情况下，数据存储在 Docker 主机 `C:\ProgramData\docker` 目录下的 `image` 和 `windowsfilter` 子目录中。您可以通过在 [守护进程配置文件](/reference/cli/dockerd.md#on-windows) 中配置 `data-root` 选项来更改存储位置：

```json
{
  "data-root": "d:\\docker"
}
```

您必须重启守护进程使配置更改生效。

## 附加信息

有关 Windows 上容器存储如何工作的更多信息，请参阅微软的 [Windows 上的容器文档](https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/container-storage)。

