---
title: 使用 IPv6 网络
weight: 20
description: 如何在 Docker 守护进程中启用 IPv6 支持
keywords: daemon, network, networking, ipv6, 守护进程, 网络
---

仅在 Linux 主机上运行的 Docker 守护进程支持 IPv6。

## 创建 IPv6 网络

- 使用 `docker network create`：

  ```console
  $ docker network create --ipv6 ip6net
  ```

- 使用 `docker network create` 并指定 IPv6 子网：

  ```console
  $ docker network create --ipv6 --subnet 2001:db8::/64 ip6net
  ```

- 使用 Docker Compose 文件：

  ```yaml
   networks:
     ip6net:
       enable_ipv6: true
       ipam:
         config:
           - subnet: 2001:db8::/64
  ```

现在您可以运行连接到 `ip6net` 网络的容器。

```console
$ docker run --rm --network ip6net -p 80:80 traefik/whoami
```

这将在 IPv6 和 IPv4 上同时发布 80 端口。
您可以通过运行 curl 连接到 IPv6 回环地址上的 80 端口来验证 IPv6 连接：

```console
$ curl http://[::1]:80
Hostname: ea1cfde18196
IP: 127.0.0.1
IP: ::1
IP: 172.17.0.2
IP: 2001:db8::2
IP: fe80::42:acff:fe11:2
RemoteAddr: [2001:db8::1]:37574
GET / HTTP/1.1
Host: [::1]
User-Agent: curl/8.1.2
Accept: */*
```

## 为默认 bridge 网络使用 IPv6

以下步骤向您展示如何在默认 bridge 网络上使用 IPv6。

1. 编辑 Docker 守护进程配置文件 (通常位于 `/etc/docker/daemon.json`)。配置以下参数：

   ```json
   {
     "ipv6": true,
     "fixed-cidr-v6": "2001:db8:1::/64"
   }
   ```

   - `ipv6` 在默认网络上启用 IPv6 联网。
   - `fixed-cidr-v6` 为默认 bridge 网络分配一个子网，实现动态 IPv6 地址分配。
   - `ip6tables` 启用额外的 IPv6 数据包过滤规则，提供网络隔离和端口映射。该选项默认启用，但可以禁用。

2. 保存配置文件。
3. 重启 Docker 守护进程使更改生效。

   ```console
   $ sudo systemctl restart docker
   ```

现在您可以在默认 bridge 网络上运行容器。

```console
$ docker run --rm -p 80:80 traefik/whoami
```

这将在 IPv6 和 IPv4 上同时发布 80 端口。
您可以通过向 IPv6 回环地址上的 80 端口发出请求来验证 IPv6 连接：

```console
$ curl http://[::1]:80
Hostname: ea1cfde18196
IP: 127.0.0.1
IP: ::1
IP: 172.17.0.2
IP: 2001:db8:1::242:ac12:2
IP: fe80::42:acff:fe12:2
RemoteAddr: [2001:db8:1::1]:35558
GET / HTTP/1.1
Host: [::1]
User-Agent: curl/8.1.2
Accept: */*
```

## 动态 IPv6 子网分配

如果您在使用 `docker network create --subnet=<your-subnet>` 时没有为用户定义网络显式配置子网，那么这些网络将使用守护进程的默认地址池作为备选。这也适用于在 Docker Compose 文件中创建且 `enable_ipv6` 设置为 `true` 的网络。

如果 Docker Engine 的 `default-address-pools` 中未包含任何 IPv6 池，且未给出 `--subnet` 选项，则在启用 IPv6 时将使用 [唯一本地地址 (Unique Local Addresses, ULAs)][wikipedia-ipv6-ula]。这些 `/64` 子网包含一个基于 Docker Engine 随机生成 ID 的 40 位全局 ID，以提供极高的唯一性概率。

要为动态地址分配使用不同的 IPv6 子网池，您必须手动配置守护进程的地址池，以包含：

- 默认的 IPv4 地址池
- 一个或多个您自己的 IPv6 池

默认的地址池配置为：

```json
{
  "default-address-pools": [
    { "base": "172.17.0.0/16", "size": 16 },
    { "base": "172.18.0.0/16", "size": 16 },
    { "base": "172.19.0.0/16", "size": 16 },
    { "base": "172.20.0.0/14", "size": 16 },
    { "base": "172.24.0.0/14", "size": 16 },
    { "base": "172.28.0.0/14", "size": 16 },
    { "base": "192.168.0.0/16", "size": 20 }
  ]
}
```

以下示例显示了一个包含默认值和一个 IPv6 池的有效配置。示例中的 IPv6 池提供了多达 256 个大小为 `/64` 的 IPv6 子网，该池的前缀长度为 `/56`。

```json
{
  "default-address-pools": [
    { "base": "172.17.0.0/16", "size": 16 },
    { "base": "172.18.0.0/16", "size": 16 },
    { "base": "172.19.0.0/16", "size": 16 },
    { "base": "172.20.0.0/14", "size": 16 },
    { "base": "172.24.0.0/14", "size": 16 },
    { "base": "172.28.0.0/14", "size": 16 },
    { "base": "192.168.0.0/16", "size": 20 },
    { "base": "2001:db8::/56", "size": 64 }
  ]
}
```

> [!NOTE]
>
> 本例中的地址 `2001:db8::` 是 [专用于文档的保留地址][wikipedia-ipv6-reserved]。请将其替换为有效的 IPv6 网络地址。
>
> 默认的 IPv4 池属于私有地址范围，类似于默认的 IPv6 [ULA][wikipedia-ipv6-ula] 网络。

[wikipedia-ipv6-reserved]: https://en.wikipedia.org/wiki/Reserved_IP_addresses#IPv6
[wikipedia-ipv6-ula]: https://en.wikipedia.org/wiki/Unique_local_address

## Docker in Docker

在运行 `xtables` (传统 `iptables`) 而不是 `nftables` 的主机上，在创建 IPv6 Docker 网络之前必须加载内核模块 `ip6_tables`。通常在 Docker 启动时它会自动加载。

然而，如果您运行的 Docker in Docker 并非基于近期版本的 [官方 `docker` 镜像](https://hub.docker.com/_/docker)，您可能需要在主机上运行 `modprobe ip6_tables`。或者，使用守护进程选项 `--ip6tables=false` 为容器化 Docker Engine 禁用 `ip6tables`。

## 后续步骤

- [网络概览](/manuals/engine/network/_index.md)
