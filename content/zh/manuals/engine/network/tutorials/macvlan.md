---
title: 使用 macvlan 网络进行网络连接
description: 使用 macvlan 桥接网络和 802.1Q 中继桥接网络进行网络连接的教程
keywords: networking, macvlan, 802.1Q, standalone
aliases:
  - /network/network-tutorial-macvlan/
---

本系列教程介绍如何将独立容器连接到 `macvlan` 网络。在这种类型的网络中，Docker 主机在其 IP 地址上接受多个 MAC 地址的请求，并将这些请求路由到相应的容器。有关其他网络主题，请参阅[概述](/manuals/engine/network/_index.md)。

## 目标

这些教程的目标是设置一个桥接的 `macvlan` 网络并将容器连接到它，然后设置一个 802.1Q 中继的 `macvlan` 网络并将容器连接到它。

## 先决条件

- 大多数云服务提供商会阻止 `macvlan` 网络。您可能需要物理访问您的网络设备。

- `macvlan` 网络驱动程序仅适用于 Linux 主机，在 Docker Desktop 或 Windows 上的 Docker Engine 中不受支持。

- 您需要至少 3.9 版本的 Linux 内核，建议使用 4.0 或更高版本。

- 示例假设您的以太网接口是 `eth0`。如果您的设备有不同的名称，请改用该名称。

- `macvlan` 驱动程序在 rootless 模式下不受支持。

## 桥接示例

在简单的桥接示例中，您的流量通过 `eth0`，Docker 使用其 MAC 地址将流量路由到您的容器。对于网络上的网络设备，您的容器看起来像是物理连接到网络。

1.  创建一个名为 `my-macvlan-net` 的 `macvlan` 网络。将 `subnet`、`gateway` 和 `parent` 值修改为适合您环境的值。

    ```console
    $ docker network create -d macvlan \
      --subnet=172.16.86.0/24 \
      --gateway=172.16.86.1 \
      -o parent=eth0 \
      my-macvlan-net
    ```

    您可以使用 `docker network ls` 和 `docker network inspect my-macvlan-net` 命令来验证网络是否存在以及是否为 `macvlan` 网络。

2.  启动一个 `alpine` 容器并将其连接到 `my-macvlan-net` 网络。`-dit` 标志在后台启动容器，但允许您连接到它。`--rm` 标志表示容器在停止时将被删除。

    ```console
    $ docker run --rm -dit \
      --network my-macvlan-net \
      --name my-macvlan-alpine \
      alpine:latest \
      ash
    ```

3.  检查 `my-macvlan-alpine` 容器，并注意 `Networks` 键中的 `MacAddress` 键：

    ```console
    $ docker container inspect my-macvlan-alpine

    ...truncated...
    "Networks": {
      "my-macvlan-net": {
          "IPAMConfig": null,
          "Links": null,
          "Aliases": [
              "bec64291cd4c"
          ],
          "NetworkID": "5e3ec79625d388dbcc03dcf4a6dc4548644eb99d58864cf8eee2252dcfc0cc9f",
          "EndpointID": "8caf93c862b22f379b60515975acf96f7b54b7cf0ba0fb4a33cf18ae9e5c1d89",
          "Gateway": "172.16.86.1",
          "IPAddress": "172.16.86.2",
          "IPPrefixLen": 24,
          "IPv6Gateway": "",
          "GlobalIPv6Address": "",
          "GlobalIPv6PrefixLen": 0,
          "MacAddress": "02:42:ac:10:56:02",
          "DriverOpts": null
      }
    }
    ...truncated
    ```

4.  通过运行一些 `docker exec` 命令来查看容器如何看待其自身的网络接口。

    ```console
    $ docker exec my-macvlan-alpine ip addr show eth0

    9: eth0@tunl0: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:ac:10:56:02 brd ff:ff:ff:ff:ff:ff
    inet 172.16.86.2/24 brd 172.16.86.255 scope global eth0
       valid_lft forever preferred_lft forever
    ```

    ```console
    $ docker exec my-macvlan-alpine ip route

    default via 172.16.86.1 dev eth0
    172.16.86.0/24 dev eth0 scope link  src 172.16.86.2
    ```

5.  停止容器（由于 `--rm` 标志，Docker 会删除它），并删除网络。

    ```console
    $ docker container stop my-macvlan-alpine

    $ docker network rm my-macvlan-net
    ```

## 802.1Q 中继桥接示例

在 802.1Q 中继桥接示例中，您的流量通过 `eth0` 的子接口（称为 `eth0.10`），Docker 使用其 MAC 地址将流量路由到您的容器。对于网络上的网络设备，您的容器看起来像是物理连接到网络。

1.  创建一个名为 `my-8021q-macvlan-net` 的 `macvlan` 网络。将 `subnet`、`gateway` 和 `parent` 值修改为适合您环境的值。

    ```console
    $ docker network create -d macvlan \
      --subnet=172.16.86.0/24 \
      --gateway=172.16.86.1 \
      -o parent=eth0.10 \
      my-8021q-macvlan-net
    ```

    您可以使用 `docker network ls` 和 `docker network inspect my-8021q-macvlan-net` 命令来验证网络是否存在、是否为 `macvlan` 网络以及父接口是否为 `eth0.10`。您可以在 Docker 主机上使用 `ip addr show` 来验证接口 `eth0.10` 是否存在并具有单独的 IP 地址。

2.  启动一个 `alpine` 容器并将其连接到 `my-8021q-macvlan-net` 网络。`-dit` 标志在后台启动容器，但允许您连接到它。`--rm` 标志表示容器在停止时将被删除。

    ```console
    $ docker run --rm -itd \
      --network my-8021q-macvlan-net \
      --name my-second-macvlan-alpine \
      alpine:latest \
      ash
    ```

3.  检查 `my-second-macvlan-alpine` 容器，并注意 `Networks` 键中的 `MacAddress` 键：

    ```console
    $ docker container inspect my-second-macvlan-alpine

    ...truncated...
    "Networks": {
      "my-8021q-macvlan-net": {
          "IPAMConfig": null,
          "Links": null,
          "Aliases": [
              "12f5c3c9ba5c"
          ],
          "NetworkID": "c6203997842e654dd5086abb1133b7e6df627784fec063afcbee5893b2bb64db",
          "EndpointID": "aa08d9aa2353c68e8d2ae0bf0e11ed426ea31ed0dd71c868d22ed0dcf9fc8ae6",
          "Gateway": "172.16.86.1",
          "IPAddress": "172.16.86.2",
          "IPPrefixLen": 24,
          "IPv6Gateway": "",
          "GlobalIPv6Address": "",
          "GlobalIPv6PrefixLen": 0,
          "MacAddress": "02:42:ac:10:56:02",
          "DriverOpts": null
      }
    }
    ...truncated
    ```

4.  通过运行一些 `docker exec` 命令来查看容器如何看待其自身的网络接口。

    ```console
    $ docker exec my-second-macvlan-alpine ip addr show eth0

    11: eth0@if10: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:ac:10:56:02 brd ff:ff:ff:ff:ff:ff
    inet 172.16.86.2/24 brd 172.16.86.255 scope global eth0
       valid_lft forever preferred_lft forever
    ```

    ```console
    $ docker exec my-second-macvlan-alpine ip route

    default via 172.16.86.1 dev eth0
    172.16.86.0/24 dev eth0 scope link  src 172.16.86.2
    ```

5.  停止容器（由于 `--rm` 标志，Docker 会删除它），并删除网络。

    ```console
    $ docker container stop my-second-macvlan-alpine

    $ docker network rm my-8021q-macvlan-net
    ```

## 其他网络教程

- [独立网络教程](/manuals/engine/network/tutorials/standalone.md)
- [Overlay 网络教程](/manuals/engine/network/tutorials/overlay.md)
- [主机网络教程](/manuals/engine/network/tutorials/host.md)
