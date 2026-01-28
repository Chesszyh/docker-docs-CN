---
title: 在 Docker Desktop 中使用 USB/IP
linkTitle: USB/IP 支持
weight: 50
description: 如何在 Docker Desktop 中使用 USB/IP
keywords: usb, usbip, docker desktop, macos, windows, linux
toc_max: 3
aliases:
- /desktop/usbip/
---

{{< summary-bar feature_name="USB/IP support" >}}

USB/IP 使您能够通过网络共享 USB 设备，然后可以从 Docker 容器内部访问这些设备。本页重点介绍共享连接到运行 Docker Desktop 的机器上的 USB 设备。您可以根据需要重复以下过程来附加和使用其他 USB 设备。

> [!NOTE]
>
> Docker Desktop 包含许多常见 USB 设备的内置驱动程序，但 Docker 无法保证每个可能的 USB 设备都能与此设置配合使用。

## 设置和使用

### 步骤一：运行 USB/IP 服务器

要使用 USB/IP，您需要运行一个 USB/IP 服务器。在本指南中，将使用 [jiegec/usbip](https://github.com/jiegec/usbip) 提供的实现。

1. 克隆仓库。

    ```console
    $ git clone https://github.com/jiegec/usbip
    $ cd usbip
    ```

2. 运行模拟的人机接口设备（Human Interface Device，HID）设备示例。

    ```console
    $ env RUST_LOG=info cargo run --example hid_keyboard
    ```

### 步骤二：启动特权 Docker 容器

要附加 USB 设备，请启动一个特权 Docker 容器，并将 PID 命名空间设置为 `host`：

```console
$ docker run --rm -it --privileged --pid=host alpine
```

`--privileged` 使容器对主机具有完全访问权限，`--pid=host` 允许它共享主机的进程命名空间。

### 步骤三：进入 PID 1 的挂载命名空间

在容器内，进入 `init` 进程的挂载命名空间以获得对预装 USB/IP 工具的访问权限：

```console
$ nsenter -t 1 -m
```

### 步骤四：使用 USB/IP 工具

现在您可以像在任何其他系统上一样使用 USB/IP 工具：

#### 列出 USB 设备

列出主机上可导出的 USB 设备：

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

#### 附加 USB 设备

附加特定的 USB 设备，或在本例中为模拟键盘：

```console
$ usbip attach -r host.docker.internal -d 0-0-0
```

#### 验证设备附加

附加模拟键盘后，检查 `/dev/input` 目录中的设备节点：

```console
$ ls /dev/input/
```

示例输出：

```console
event0  mice
```

### 步骤五：从另一个容器访问设备

当初始容器保持运行以保持 USB 设备正常工作时，您可以从另一个容器访问附加的设备。例如：

1. 使用附加的设备启动新容器。

    ```console
    $ docker run --rm -it --device "/dev/input/event0" alpine
    ```

2. 安装 `evtest` 等工具来测试模拟键盘。

    ```console
    $ apk add evtest
    $ evtest /dev/input/event0
    ```

3. 与设备交互，并观察输出。

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
> 初始容器必须保持运行以维持与 USB 设备的连接。退出容器将导致设备停止工作。
