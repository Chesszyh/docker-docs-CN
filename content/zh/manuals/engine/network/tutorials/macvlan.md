---
title: 使用 macvlan 网络进行联网
description: 使用 macvlan bridge 网络和 802.1Q trunk bridge 网络进行联网的教程
keywords: networking, macvlan, 802.1Q, standalone, 网络, 独立运行
---

本系列教程涉及连接到 `macvlan` 网络的独立容器的联网。在这种类型的网络中，Docker 主机在其 IP 地址处接受多个 MAC 地址的请求，并将这些请求路由到相应的容器。有关其他联网主题，请参阅 [概览](/manuals/engine/network/_index.md)。

## 目标

这些教程的目标是设置一个桥接的 `macvlan` 网络并向其附加一个容器，然后设置一个 802.1Q trunked `macvlan` 网络并向其附加一个容器。

## 前提条件

- 大多数云提供商会阻断 `macvlan` 联网。您可能需要对您的网络设备拥有物理访问权限。

- `macvlan` 联网驱动程序仅在 Linux 主机上工作，在 Docker Desktop 或 Windows 上的 Docker Engine 上不受支持。

- 您至少需要 3.9 版本的 Linux 内核，建议使用 4.0 或更高版本。

- 示例假设您的以太网接口为 `eth0`。如果您的设备名称不同，请改用该名称。

- `macvlan` 驱动程序在无根模式 (rootless mode) 下不受支持。

## Bridge 示例

在简单的 bridge 示例中，您的流量通过 `eth0` 流动，Docker 使用容器的 MAC 地址将流量路由到您的容器。对于您网络上的网络设备，您的容器看起来像是物理连接到网络上的。

1.  创建一个名为 `my-macvlan-net` 的 `macvlan` 网络。将 `subnet`、`gateway` 和 `parent` 的值修改为适合您环境的值。

    ```console
    $ docker network create -d macvlan \
      --subnet=172.16.86.0/24 \
      --gateway=172.16.86.1 \
      -o parent=eth0 \
      my-macvlan-net
    ```

    您可以使用 `docker network ls` 和 `docker network inspect my-macvlan-net` 命令来验证该网络是否存在且为 `macvlan` 网络。

2.  启动一个 `alpine` 容器并将其附加到 `my-macvlan-net` 网络。`-dit` 标志在后台启动容器但允许您附加到它。`--rm` 标志意味着容器在停止时会被移除。

    ```console
    $ docker run --rm -dit \
      --network my-macvlan-net \
      --name my-macvlan-alpine \
      alpine:latest \
      ash
    ```

3.  检查 `my-macvlan-alpine` 容器并注意 `Networks` 键内的 `MacAddress` 键：

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

4.  通过运行几个 `docker exec` 命令来查看容器如何看待自己的网络接口。

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

5.  停止容器 (Docker 会因为 `--rm` 标志而将其移除)，并移除该网络。

    ```console
    $ docker container stop my-macvlan-alpine

    $ docker network rm my-macvlan-net
    ```

## 802.1Q trunked bridge 示例

在 802.1Q trunked bridge 示例中，您的流量通过 `eth0` 的一个子接口 (称为 `eth0.10`) 流动，Docker 使用容器的 MAC 地址将流量路由到您的容器。对于您网络上的网络设备，您的容器看起来像是物理连接到网络上的。

1.  创建一个名为 `my-8021q-macvlan-net` 的 `macvlan` 网络。将 `subnet`、`gateway` 和 `parent` 的值修改为适合您环境的值。

    ```console
    $ docker network create -d macvlan \
      --subnet=172.16.86.0/24 \
      --gateway=172.16.86.1 \
      -o parent=eth0.10 \
      my-8021q-macvlan-net
    ```

    您可以使用 `docker network ls` 和 `docker network inspect my-8021q-macvlan-net` 命令来验证该网络是否存在、是 `macvlan` 网络，并且具有父接口 `eth0.10`。您可以在 Docker 主机上使用 `ip addr show` 来验证接口 `eth0.10` 是否存在并具有独立的 IP 地址。

2.  启动一个 `alpine` 容器并将其附加到 `my-8021q-macvlan-net` 网络。`-dit` 标志在后台启动容器但允许您附加到它。`--rm` 标志意味着容器在停止时会被移除。

    ```console
    $ docker run --rm -itd \
      --network my-8021q-macvlan-net \
      --name my-second-macvlan-alpine \
      alpine:latest \
      ash
    ```

3.  检查 `my-second-macvlan-alpine` 容器并注意 `Networks` 键内的 `MacAddress` 键：

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

4.  通过运行几个 `docker exec` 命令来查看容器如何看待自己的网络接口。

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

5.  停止容器 (Docker 会因为 `--rm` 标志而将其移除)，并移除该网络。

    ```console
    $ docker container stop my-second-macvlan-alpine

    $ docker network rm my-8021q-macvlan-net
    ```

## 其他联网教程

- [独立运行网络教程](/manuals/engine/network/tutorials/standalone.md)
- [Overlay 网络教程](/manuals/engine/network/tutorials/overlay.md)
- [Host 网络教程](/manuals/engine/network/tutorials/host.md)
