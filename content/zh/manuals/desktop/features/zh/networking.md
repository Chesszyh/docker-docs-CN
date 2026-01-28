---
description: 了解 Docker Desktop 上的网络工作原理并查看已知限制
keywords: networking, docker desktop, proxy, vpn, Linux, Mac, Windows
title: 探索 Docker Desktop 的网络功能
linkTitle: 网络
aliases:
- /desktop/linux/networking/
- /docker-for-mac/networking/
- /mackit/networking/
- /desktop/mac/networking/
- /docker-for-win/networking/
- /docker-for-windows/networking/
- /desktop/windows/networking/
- /desktop/networking/
weight: 30
---

Docker Desktop 包含内置网络功能，帮助您将容器与主机上的服务、跨容器或通过代理和 VPN 进行连接。

## 所有平台的网络功能

### VPN 穿透

Docker Desktop 网络可以在连接到 VPN 时工作。为此，Docker Desktop 拦截来自容器的流量并将其注入主机，就像它来自 Docker 应用程序一样。

### 端口映射

当您使用 `-p` 参数运行容器时，例如：

```console
$ docker run -p 80:80 -d nginx
```

Docker Desktop 使容器中端口 `80` 上运行的内容（在本例中为 `nginx`）在 `localhost` 的端口 `80` 上可用。在此示例中，主机和容器端口相同。

为避免与主机上已使用端口 `80` 的服务冲突：

```console
$ docker run -p 8000:80 -d nginx
```

现在，到 `localhost:8000` 的连接将发送到容器中的端口 `80`。

> [!TIP]
>
> `-p` 的语法是 `HOST_PORT:CLIENT_PORT`。

### HTTP/HTTPS 代理支持

请参阅[代理](/manuals/desktop/settings-and-maintenance/settings.md#proxies)

### SOCKS5 代理支持

{{< summary-bar feature_name="SOCKS5 proxy support" >}}

SOCKS（Socket Secure）是一种协议，它通过代理服务器促进客户端和服务器之间的网络数据包路由。它为用户和应用程序提供了一种增强隐私、安全性和网络性能的方法。

您可以启用 SOCKS 代理支持以允许出站请求（例如拉取镜像）并从主机访问 Linux 容器后端 IP。

要启用和设置 SOCKS 代理支持：

1. 导航到 **Settings** 中的 **Resources** 选项卡。
2. 从下拉菜单中选择 **Proxies**。
3. 开启 **Manual proxy configuration** 开关。
4. 在 **Secure Web Server HTTPS** 框中，粘贴您的 `socks5://host:port` URL。

## Mac 和 Windows 的网络模式和 DNS 行为

使用 Docker Desktop 4.42 及更高版本，您可以自定义 Docker 处理容器网络和 DNS 解析的方式，以更好地支持各种环境——从仅 IPv4 到双栈和仅 IPv6 系统。这些设置有助于防止由不兼容或配置错误的主机网络引起的超时和连接问题。

> [!NOTE]
>
> 这些设置可以使用 CLI 标志或 Compose 文件选项按网络覆盖。

### 默认网络模式

选择 Docker 创建新网络时使用的默认 IP 协议。这允许您将 Docker 与主机的网络功能或组织要求对齐，例如强制仅 IPv6 访问。

可用选项有：

- **Dual IPv4/IPv6**（默认）：同时支持 IPv4 和 IPv6。最灵活，适用于具有双栈网络的环境。
- **IPv4 only**：仅使用 IPv4 地址。如果您的主机或网络不支持 IPv6，请使用此选项。
- **IPv6 only**：仅使用 IPv6 地址。最适合正在过渡到或强制仅 IPv6 连接的环境。

> [!NOTE]
>
> 此设置可以使用 CLI 标志或 Compose 文件选项按网络覆盖。

### DNS 解析行为

控制 Docker 如何过滤返回给容器的 DNS 记录，提高仅支持 IPv4 或 IPv6 环境的可靠性。此设置对于防止应用程序尝试使用实际上不可用的 IP 系列进行连接特别有用，这可能会导致可避免的延迟或失败。

根据您选择的网络模式，可用选项有：

- **Auto (recommended)**：Docker 检测主机的网络栈并自动过滤不支持的 DNS 记录类型（A 代表 IPv4，AAAA 代表 IPv6）。
- **Filter IPv4 (A records)**：阻止容器解析 IPv4 地址。仅在双栈模式下可用。
- **Filter IPv6 (AAAA records)**：阻止容器解析 IPv6 地址。仅在双栈模式下可用。
- **No filtering**：Docker 返回所有 DNS 记录（A 和 AAAA），无论主机是否支持。

> [!IMPORTANT]
>
> 切换默认网络模式会将 DNS 过滤器重置为 Auto。

### 使用设置管理

如果您是管理员，可以使用[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md#networking)在开发人员的机器上强制执行此 Docker Desktop 设置。从以下代码片段中选择并将其添加到您的 `admin-settings.json` 文件中。

{{< tabs >}}
{{< tab name="Networking mode" >}}

Dual IPv4/IPv6：

```json
{
  "defaultNetworkingMode": {
    "locked": true
    "value": "dual-stack"
  }
}
```

IPv4 only：

```json
{
  "defaultNetworkingMode": {
    "locked": true
    "value": "ipv4only"
  }
}
```

IPv6 only：

```json
{
  "defaultNetworkingMode": {
    "locked": true
    "value": "ipv6only"
  }
}
```

{{< /tab >}}
{{< tab name="DNS resolution" >}}

Auto filter：

```json
{
  "dnsInhibition": {
    "locked": true
    "value": "auto"
  }
}
```

Filter IPv4：

```json
{
  "dnsInhibition": {
    "locked": true
    "value": "ipv4"
  }
}
```

Filter IPv6：

```json
{
  "dnsInhibition": {
    "locked": true
    "value": "ipv6"
  }
}
```

No filter：

```json
{
  "dnsInhibition": {
    "locked": true
    "value": "none"
  }
}
```

{{< /tab >}}
{{< /tabs >}}

## Mac 和 Linux 的网络功能

### SSH 代理转发

Mac 和 Linux 版 Docker Desktop 允许您在容器内使用主机的 SSH 代理。要执行此操作：

1. 通过在 `docker run` 命令中添加以下参数来绑定挂载 SSH 代理套接字：

   ```console
   $--mount type=bind,src=/run/host-services/ssh-auth.sock,target=/run/host-services/ssh-auth.sock
   ```

2. 在容器中添加 `SSH_AUTH_SOCK` 环境变量：

    ```console
    $ -e SSH_AUTH_SOCK="/run/host-services/ssh-auth.sock"
    ```

要在 Docker Compose 中启用 SSH 代理，请在您的服务中添加以下标志：

 ```yaml
services:
  web:
    image: nginx:alpine
    volumes:
      - type: bind
        source: /run/host-services/ssh-auth.sock
        target: /run/host-services/ssh-auth.sock
    environment:
      - SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock
 ```

## 已知限制

### 更改内部 IP 地址

Docker 使用的内部 IP 地址可以从 **Settings** 更改。更改 IP 后，您需要重置 Kubernetes 集群并离开任何活动的 Swarm。

### 主机上没有 `docker0` 网桥

由于 Docker Desktop 中网络的实现方式，您无法在主机上看到 `docker0` 接口。此接口实际上在虚拟机内部。

### 我无法 ping 我的容器

Docker Desktop 无法将流量路由到 Linux 容器。但是，如果您是 Windows 用户，可以 ping Windows 容器。

### 无法实现每容器 IP 寻址

这是因为 Docker `bridge` 网络无法从主机访问。但是，如果您是 Windows 用户，Windows 容器可以实现每容器 IP 寻址。

## 用例和解决方法

### 我想从容器连接到主机上的服务

主机具有变化的 IP 地址，或者如果您没有网络访问权限，则没有 IP 地址。Docker 建议您连接到特殊的 DNS 名称 `host.docker.internal`，它解析为主机使用的内部 IP 地址。

您还可以使用 `gateway.docker.internal` 访问网关。

如果您的机器上安装了 Python，请使用以下说明作为示例，从容器连接到主机上的服务：

1. 运行以下命令在端口 8000 上启动一个简单的 HTTP 服务器。

    `python -m http.server 8000`

    如果您安装了 Python 2.x，请运行 `python -m SimpleHTTPServer 8000`。

2. 现在，运行一个容器，安装 `curl`，并尝试使用以下命令连接到主机：

    ```console
    $ docker run --rm -it alpine sh
    # apk add curl
    # curl http://host.docker.internal:8000
    # exit
    ```

### 我想从主机连接到容器

端口转发适用于 `localhost`。`--publish`、`-p` 或 `-P` 都有效。从 Linux 暴露的端口会转发到主机。

Docker 建议您发布端口，或从另一个容器连接。即使在 Linux 上，如果容器在覆盖网络（overlay network）而不是桥接网络（bridge network）上，也需要这样做，因为它们不会被路由。

例如，要运行 `nginx` Web 服务器：

```console
$ docker run -d -p 80:80 --name webserver nginx
```

为了澄清语法，以下两个命令都将容器的端口 `80` 发布到主机的端口 `8000`：

```console
$ docker run --publish 8000:80 --name webserver nginx

$ docker run -p 8000:80 --name webserver nginx
```

要发布所有端口，请使用 `-P` 标志。例如，以下命令启动一个容器（在分离模式下），`-P` 标志将容器的所有暴露端口发布到主机上的随机端口。

```console
$ docker run -d -P --name webserver nginx
```

或者，您也可以使用[主机网络](/manuals/engine/network/drivers/host.md#docker-desktop)使容器直接访问主机的网络栈。

有关与 `docker run` 一起使用的发布选项的更多详细信息，请参阅 [run 命令](/reference/cli/docker/container/run.md)。
