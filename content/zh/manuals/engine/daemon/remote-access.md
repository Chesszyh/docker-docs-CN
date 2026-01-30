---
description: 配置远程访问允许 Docker 通过 IP 地址和端口以及 Unix 套接字接收来自远程主机的请求
keywords: configuration, daemon, remote access, engine, 远程访问, 配置
title: 配置 Docker 守护进程的远程访问
---

默认情况下，Docker 守护进程在 Unix 套接字上监听连接，以接收来自本地客户端的请求。您可以配置 Docker 通过在 IP 地址和端口以及 Unix 套接字上进行监听，来接收来自远程客户端的请求。

<!-- prettier-ignore -->
> [!WARNING]
>
> 配置 Docker 接收来自远程客户端的连接可能会使您容易受到对主机的未经授权访问和其他攻击。
>
> 了解开放 Docker 到网络的安全影响至关重要。如果不采取措施保护连接，远程非 root 用户可能会获得主机的 root 访问权限。
>
> **不推荐** 在没有 TLS 的情况下进行远程访问，并且在未来的版本中将需要显式选择开启。有关如何使用 TLS 证书保护此连接的更多信息，请参阅 [保护 Docker 守护进程套接字](/manuals/engine/security/protect-access.md)。

## 启用远程访问

您可以对使用 systemd 的 Linux 发行版使用 `docker.service` systemd 单元文件启用对守护进程的远程访问。或者，如果您的发行版不使用 systemd，您可以使用 `daemon.json` 文件。

同时使用 systemd 单元文件和 `daemon.json` 文件配置 Docker 监听连接会导致冲突，从而阻止 Docker 启动。

### 使用 systemd 单元文件配置远程访问

1. 使用命令 `sudo systemctl edit docker.service` 在文本编辑器中打开 `docker.service` 的覆盖文件。

2. 添加或修改以下行，替换为您自己的值。

   ```systemd
   [Service]
   ExecStart=
   ExecStart=/usr/bin/dockerd -H fd:// -H tcp://127.0.0.1:2375
   ```

3. 保存文件。

4. 重新加载 `systemctl` 配置。

   ```console
   $ sudo systemctl daemon-reload
   ```

5. 重启 Docker。

   ```console
   $ sudo systemctl restart docker.service
   ```

6. 验证更改是否已生效。

   ```console
   $ sudo netstat -lntp | grep dockerd
   tcp        0      0 127.0.0.1:2375          0.0.0.0:*               LISTEN      3758/dockerd
   ```

### 使用 `daemon.json` 配置远程访问

1. 在 `/etc/docker/daemon.json` 中设置 `hosts` 数组以连接到 Unix 套接字和 IP 地址，如下所示：

   ```json
   {
     "hosts": ["unix:///var/run/docker.sock", "tcp://127.0.0.1:2375"]
   }
   ```

2. 重启 Docker。

3. 验证更改是否已生效。

   ```console
   $ sudo netstat -lntp | grep dockerd
   tcp        0      0 127.0.0.1:2375          0.0.0.0:*               LISTEN      3758/dockerd
   ```

### 允许通过防火墙访问远程 API

如果您在运行 Docker 的同一台主机上运行防火墙，并且您想从另一台远程主机访问 Docker 远程 API，则必须配置防火墙以允许 Docker 端口上的入站连接。如果您使用的是 TLS 加密传输，则默认端口为 `2376`，否则为 `2375`。

两个常见的防火墙守护进程是：

- [Uncomplicated Firewall (ufw)](https://help.ubuntu.com/community/UFW)，常用于 Ubuntu 系统。
- [firewalld](https://firewalld.org)，常用于基于 RPM 的系统。

咨询您的操作系统和防火墙文档。以下信息可能有助于您入门。本说明中使用的设置是允许性的，您可能希望使用更严格锁定系统的不同配置。

- 对于 ufw，在您的配置中设置 `DEFAULT_FORWARD_POLICY="ACCEPT"`。

- 对于 firewalld，在您的策略中添加类似于以下的规则。一条用于入站请求，一条用于出站请求。

  ```xml
  <direct>
    [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -i zt0 -j ACCEPT </rule> ]
    [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -o zt0 -j ACCEPT </rule> ]
  </direct>
  ```

  确保接口名称和链名称正确。

## 附加信息

有关守护进程远程访问配置选项的更多详细信息，请参阅 [dockerd CLI 参考](/reference/cli/dockerd/#bind-docker-to-another-hostport-or-a-unix-socket)。
