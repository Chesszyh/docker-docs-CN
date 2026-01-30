---
title: Macvlan 网络驱动程序
description: 关于使用 Macvlan 让您的容器在网络上看起来像物理机的一切
keywords: network, macvlan, standalone, 网络, 独立运行
alias:
- /config/containers/macvlan/
- /engine/userguide/networking/get-started-macvlan/
- /network/macvlan/
- /network/drivers/macvlan/
---

某些应用程序，特别是遗留应用程序或监控网络流量的应用程序，期望直接连接到物理网络。在这种情况下，您可以使用 `macvlan` 网络驱动程序为每个容器的虚拟网络接口分配一个 MAC 地址，使其看起来像一个直接连接到物理网络的物理网络接口。在这种情况下，您需要指定 Docker 主机上的一个物理接口用于 Macvlan，以及网络的子网和网关。您甚至可以使用不同的物理网络接口来隔离您的 Macvlan 网络。

请记住以下几点：

- 由于 IP 地址耗尽或“VLAN 扩散”(即网络中存在过多唯一的 MAC 地址)，您可能会无意中降低网络性能。

- 您的网络设备需要能够处理“混杂模式 (promiscuous mode)”，即一个物理接口可以被分配多个 MAC 地址。

- 如果您的应用程序可以使用 bridge (在单个 Docker 主机上) 或 overlay (跨多个 Docker 主机通信)，那么从长远来看，这些解决方案可能会更好。

## 选项 (Options)

下表描述了在使用 `macvlan` 驱动程序创建网络时可以传递给 `--opt` 的特定于驱动程序的选项。

| 选项           | 默认值   | 描述                                                                          |
| -------------- | -------- | ----------------------------------------------------------------------------- |
| `macvlan_mode` | `bridge` | 设置 Macvlan 模式。可以是：`bridge`, `vepa`, `passthru`, `private`            |
| `parent`       |          | 指定要使用的父接口。                                                          |

## 创建 Macvlan 网络

当您创建 Macvlan 网络时，它可以是 bridge 模式或 802.1Q trunk bridge 模式。

- 在 bridge 模式下，Macvlan 流量通过主机上的物理设备。

- 在 802.1Q trunk bridge 模式下，流量通过 Docker 实时创建的 802.1Q 子接口。这允许您以更细的粒度控制路由和过滤。

### Bridge 模式

要创建一个与给定物理网络接口桥接的 `macvlan` 网络，请在 `docker network create` 命令中使用 `--driver macvlan`。您还需要指定 `parent`，即流量在 Docker 主机上物理通过的接口。

```console
$ docker network create -d macvlan \
  --subnet=172.16.86.0/24 \
  --gateway=172.16.86.1 \
  -o parent=eth0 pub_net
```

如果您需要排除某些 IP 地址不被 `macvlan` 网络使用 (例如当给定的 IP 地址已被使用时)，请使用 `--aux-addresses`：

```console
$ docker network create -d macvlan \
  --subnet=192.168.32.0/24 \
  --ip-range=192.168.32.128/25 \
  --gateway=192.168.32.254 \
  --aux-address="my-router=192.168.32.129" \
  -o parent=eth0 macnet32
```

### 802.1Q trunk bridge 模式

如果您指定的 `parent` 接口名称包含点号，例如 `eth0.50`，Docker 会将其解释为 `eth0` 的子接口并自动创建该子接口。

```console
$ docker network create -d macvlan \
    --subnet=192.168.50.0/24 \
    --gateway=192.168.50.1 \
    -o parent=eth0.50 macvlan50
```

### 使用 IPvlan 代替 Macvlan

在上面的示例中，您仍在使用 L3 桥接。您可以改为使用 `ipvlan` 来获得 L2 桥接。指定 `-o ipvlan_mode=l2`。

```console
$ docker network create -d ipvlan \
    --subnet=192.168.210.0/24 \
    --subnet=192.168.212.0/24 \
    --gateway=192.168.210.254 \
    --gateway=192.168.212.254 \
     -o ipvlan_mode=l2 -o parent=eth0 ipvlan210
```

## 使用 IPv6

如果您已经 [配置 Docker 守护进程允许 IPv6](/manuals/engine/daemon/ipv6.md)，您可以使用双栈 IPv4/IPv6 `macvlan` 网络。

```console
$ docker network create -d macvlan \
    --subnet=192.168.216.0/24 --subnet=192.168.218.0/24 \
    --gateway=192.168.216.1 --gateway=192.168.218.1 \
    --subnet=2001:db8:abc8::/64 --gateway=2001:db8:abc8::10 \
     -o parent=eth0.218 \
     -o macvlan_mode=bridge macvlan216
```

## 后续步骤

在 [Macvlan 网络教程](/manuals/engine/network/tutorials/macvlan.md) 中了解如何使用 Macvlan 驱动程序。
