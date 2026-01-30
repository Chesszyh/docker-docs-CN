---
title: None 网络驱动程序
description: 如何使用 none 驱动程序隔离容器的网络栈
keywords: network, none, standalone, 网络, 独立运行
aliases:
- /network/none/
- /network/drivers/none/
---

如果您想完全隔离容器的网络栈，可以在启动容器时使用 `--network none` 标志。在容器内，只会创建回环 (loopback) 设备。

以下示例显示了在使用 `none` 网络驱动程序的 `alpine` 容器中执行 `ip link show` 的输出。

```console
$ docker run --rm --network none alpine:latest ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

对于使用 `none` 驱动程序的容器，没有配置 IPv6 回环地址。

```console
$ docker run --rm --network none --name no-net-alpine alpine:latest ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
```

## 后续步骤

- 学习 [host 网络教程](/manuals/engine/network/tutorials/host.md)
- 了解 [从容器角度看的网络](../_index.md)
- 了解 [bridge 网络](bridge.md)
- 了解 [overlay 网络](overlay.md)
- 了解 [Macvlan 网络](macvlan.md)
