---
title: 在 Docker Desktop 中使用 USB/IP
linkTitle: USB/IP 支持
weight: 50
description: 了解如何在 Docker Desktop 中使用 USB/IP
keywords: usb, usbip, docker desktop, macos, windows, linux
toc_max: 3
aliases:
- /desktop/usbip/
---

{{< summary-bar feature_name="USB/IP 支持" >}}

USB/IP 让您能够通过网络共享 USB 设备，随后可以在 Docker 容器内部访问这些设备。本页重点介绍共享连接到运行 Docker Desktop 的机器上的 USB 设备。您可以根据需要重复以下过程来连接并使用更多的 USB 设备。

> [!NOTE]
>
> Docker Desktop 包含了许多常用 USB 设备的内置驱动程序，但 Docker 无法保证所有可能的 USB 设备都能在此设置下工作。

## 设置与使用

### 第一步：运行 USB/IP 服务器

要使用 USB/IP，您需要运行一个 USB/IP 服务器。本指南将使用 [jiegec/usbip](https://github.com/jiegec/usbip) 提供的实现。

1. 克隆仓库。

    ```console
    $ git clone https://github.com/jiegec/usbip
    $ cd usbip
    ```

2. 运行模拟的人机接口设备 (HID) 示例。

    ```console
    $ env RUST_LOG=info cargo run --example hid_keyboard
    ```

### 第二步：启动一个特权 Docker 容器

要连接 USB 设备，请启动一个 PID 命名空间设置为 `host` 的特权 Docker 容器：

```console
$ docker run --rm -it --privileged --pid=host alpine
```

`--privileged` 赋予容器对宿主机的完整访问权限，`--pid=host` 允许它共享宿主机的进程命名空间。

### 第三步：进入 PID 1 的挂载命名空间

在容器内部，进入 `init` 进程的挂载命名空间，以访问预装的 USB/IP 工具：

```console
$ nsenter -t 1 -m
```

### 第四步：使用 USB/IP 工具

现在您可以像在任何其他系统上一样使用 USB/IP 工具：

#### 列出 USB 设备

要列出宿主机可导出的 USB 设备：

```console
$ usbip list -r host.docker.internal
```

预期输出：

```console
Exportable USB devices
======================
 - host.docker.internal
      0-0-0: unknown vendor : unknown product (0000:0000)
           : /sys/bus/0/0/0
           : (Defined at Interface level) (00/00/00)
           :  0 - unknown class / unknown subclass / unknown protocol (03/00/00)
```

#### 连接 USB 设备

要连接特定的 USB 设备，在本例中即为模拟键盘：

```console
$ usbip attach -r host.docker.internal -d 0-0-0
```

#### 验证设备连接

连接模拟键盘后，检查 `/dev/input` 目录下的设备节点：

```console
$ ls /dev/input/
```

示例输出：

```console
event0  mice
```

### 第五步：从另一个容器访问设备

在第一个容器保持运行以维持 USB 设备操作的同时，您可以从另一个容器访问连接的设备。例如：

1. 启动一个带有已连接设备的新容器。

    ```console
    $ docker run --rm -it --device "/dev/input/event0" alpine
    ```

2. 安装类似 `evtest` 的工具来测试模拟键盘。

    ```console
    $ apk add evtest
    $ evtest /dev/input/event0
    ```

3. 与设备进行交互，并观察输出。

    示例输出：

    ```console
    Input driver version is 1.0.1
    Input device ID: bus 0x3 vendor 0x0 product 0x0 version 0x111
    ...
    Properties:
    Testing ... (interrupt to exit)
    Event: time 1717575532.881540, type 4 (EV_MSC), code 4 (MSC_SCAN), value 7001e
    Event: time 1717575532.881540, type 1 (EV_KEY), code 2 (KEY_1), value 1
    Event: time 1717575532.881540, -------------- SYN_REPORT ------------
    ...
    ```

> [!IMPORTANT]
>
> 第一个容器必须保持运行以维持与 USB 设备的连接。退出该容器将导致设备停止工作。
