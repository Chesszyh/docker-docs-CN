---
description: 了解 Docker Desktop 的网络工作原理并查看已知限制
keywords: networking, 网络, docker desktop, proxy, 代理, vpn, Linux, Mac, Windows
title: 探索 Docker Desktop 的网络特性
linkTitle: 网络 (Networking)
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

Docker Desktop 包含内置的网络功能，可帮助您将容器与宿主机上的服务、容器之间、或通过代理和 VPN 进行连接。

## 适用于所有平台的网络特性

### VPN 穿透 (VPN Passthrough)

当连接到 VPN 时，Docker Desktop 的网络仍可正常工作。为此，Docker Desktop 会拦截来自容器的流量，并将其注入到宿主机中，就好像该流量起源于 Docker 应用程序一样。

### 端口映射 (Port mapping)

当您使用 `-p` 参数运行容器时，例如：

```console
$ docker run -p 80:80 -d nginx
```

Docker Desktop 会将容器中运行在 `80` 端口上的任何内容（在本例中为 `nginx`）映射到 `localhost` 的 `80` 端口上。在这个例子中，宿主机和容器的端口是相同的。

为了避免与宿主机上已经使用 `80` 端口的服务发生冲突，可以这样做：

```console
$ docker run -p 8000:80 -d nginx
```

现在，对 `localhost:8000` 的连接将被发送到容器的 `80` 端口。

> [!TIP]
>
> `-p` 的语法是 `宿主机端口:容器端口`。

### HTTP/HTTPS 代理支持

请参阅 [代理 (Proxies)](/manuals/desktop/settings-and-maintenance/settings.md#proxies)

### SOCKS5 代理支持

{{< summary-bar feature_name="SOCKS5 代理支持" >}}

SOCKS (Socket Secure) 是一种协议，通过代理服务器促进客户端和服务器之间的网络数据包路由。它为用户和应用程序提供了一种增强隐私、安全性和网络性能的方法。

您可以启用 SOCKS 代理支持，以允许发出请求（如拉取镜像），并从宿主机访问 Linux 容器后端的 IP。

要启用并设置 SOCKS 代理支持：

1. 导航到 **Settings（设置）** 中的 **Resources（资源）** 选项卡。
2. 从下拉菜单中选择 **Proxies（代理）**。
3. 开启 **Manual proxy configuration（手动代理配置）** 开关。
4. 在 **Secure Web Server HTTPS** 框中，粘贴您的 `socks5://host:port` 格式的 URL。

## Mac 和 Windows 的网络模式及 DNS 行为

在 Docker Desktop 4.42 及更高版本中，您可以自定义 Docker 处理容器网络和 DNS 解析的方式，以更好地支持从仅 IPv4 到双栈以及仅 IPv6 的各种环境。这些设置有助于防止因宿主机网络不兼容或配置错误而导致的超时和连接问题。

> [!NOTE]
>
> 这些设置可以在单个网络级别使用 CLI 标志或 Compose 文件选项进行覆盖。

### 默认网络模式 (Default networking mode)

选择 Docker 创建新网络时使用的默认 IP 协议。这允许您使 Docker 与宿主机的网络能力或组织的合规要求（如强制仅 IPv6 访问）保持一致。

可用选项包括：

- **Dual IPv4/IPv6** (默认)：同时支持 IPv4 和 IPv6。最灵活，是双栈网络环境的理想选择。
- **IPv4 only**：仅使用 IPv4 地址。如果您的宿主机或网络不支持 IPv6，请使用此选项。
- **IPv6 only**：仅使用 IPv6 地址。最适合正在过渡到或强制执行仅 IPv6 连接的环境。

> [!NOTE]
>
> 此设置可以在单个网络级别使用 CLI 标志或 Compose 文件选项进行覆盖。

### DNS 解析行为 (DNS resolution behavior)

控制 Docker 如何过滤返回给容器的 DNS 记录，从而在仅支持 IPv4 或 IPv6 的环境中提高可靠性。此设置对于防止应用尝试使用实际不可用的 IP 协议族进行连接特别有用，否则可能会导致不必要的延迟或失败。

根据您选择的网络模式，可用选项如下：

- **Auto (推荐)**：Docker 会检测宿主机的网络栈，并自动过滤掉不支持的 DNS 记录类型（IPv4 为 A 记录，IPv6 为 AAAA 记录）。
- **Filter IPv4 (A 记录)**：阻止容器解析 IPv4 地址。仅在双栈模式下可用。
- **Filter IPv6 (AAAA 记录)**：阻止容器解析 IPv6 地址。仅在双栈模式下可用。
- **No filtering**：Docker 返回所有 DNS 记录（A 和 AAAA），无论宿主机是否支持。

> [!IMPORTANT]
>
> 切换默认网络模式会将 DNS 过滤器重置为 Auto。

### 使用设置管理 (Settings Management)

如果您是管理员，可以使用[设置管理](/manuals/security/for-admins/hardened-desktop/settings-management/configure-json-file.md#networking)在开发人员的机器上强制执行这些 Docker Desktop 设置。请从以下代码片段中选择并将其添加到您的 `admin-settings.json` 文件中。

{{< tabs >}}
{{< tab name="网络模式" >}}

双栈 IPv4/IPv6：

```json
{
  "defaultNetworkingMode": {
    "locked": true,
    "value": "dual-stack"
  }
}
```

仅 IPv4：

```json
{
  "defaultNetworkingMode": {
    "locked": true,
    "value": "ipv4only"
  }
}
```

仅 IPv6：

```json
{
  "defaultNetworkingMode": {
    "locked": true,
    "value": "ipv6only"
  }
}
```

{{< /tab >}}
{{< tab name="DNS 解析" >}}

自动过滤：

```json
{
  "dnsInhibition": {
    "locked": true,
    "value": "auto"
  }
}
```

过滤 IPv4：

```json
{
  "dnsInhibition": {
    "locked": true,
    "value": "ipv4"
  }
}
```

过滤 IPv6：

```json
{
  "dnsInhibition": {
    "locked": true,
    "value": "ipv6"
  }
}
```

不进行过滤：

```json
{
  "dnsInhibition": {
    "locked": true,
    "value": "none"
  }
}
```

{{< /tab >}}
{{< /tabs >}}

## Mac 和 Linux 的网络特性

### SSH 代理转发 (SSH agent forwarding)

Mac 和 Linux 版 Docker Desktop 允许您在容器内部使用宿主机的 SSH 代理。操作步骤如下：

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

Docker 使用的内部 IP 地址可以在 **Settings（设置）** 中更改。更改 IP 后，您需要重置 Kubernetes 集群并退出任何活动的 Swarm。

### 宿主机上没有 `docker0` 网桥

由于 Docker Desktop 实现网络的方式，您在宿主机上看不到 `docker0` 接口。该接口实际上位于虚拟机内部。

### 无法 ping 我的容器

Docker Desktop 无法将流量路由到 Linux 容器。但如果您是 Windows 用户，您可以 ping 通 Windows 容器。

### 无法实现基于每个容器的 IP 寻址

这是因为 Docker 的 `bridge`（网桥）网络无法从宿主机直接访问。但如果您是 Windows 用户，使用 Windows 容器时可以实现基于每个容器的 IP 寻址。

## 使用场景与变通方法

### 我想从容器连接到宿主机上的服务

宿主机的 IP 地址会变，或者如果没有网络连接，则没有 IP。Docker 建议您连接到特殊的 DNS 名称 `host.docker.internal`，它会被解析为宿主机使用的内部 IP 地址。

您也可以使用 `gateway.docker.internal` 访问网关。

如果您的机器上安装了 Python，可以使用以下步骤作为从容器连接到宿主机服务的示例：

1. 运行以下命令在 8000 端口启动一个简单的 HTTP 服务器。

    `python -m http.server 8000`

    如果您安装的是 Python 2.x，请运行 `python -m SimpleHTTPServer 8000`。

2. 现在，运行一个容器，安装 `curl`，并尝试使用以下命令连接到宿主机：

    ```console
    $ docker run --rm -it alpine sh
    # apk add curl
    # curl http://host.docker.internal:8000
    # exit
    ```

### 我想从宿主机连接到容器

端口转发适用于 `localhost`。`--publish`、`-p` 或 `-P` 都有效。从 Linux 暴露的端口会被转发到宿主机。

Docker 建议您发布端口，或从另一个容器连接。即使在 Linux 上，如果容器在 overlay 网络而不是 bridge 网络上，您也需要这样做，因为这些网络是不路由的。

例如，运行一个 `nginx` Web 服务器：

```console
$ docker run -d -p 80:80 --name webserver nginx
```

为了澄清语法，以下两个命令都将容器的 `80` 端口发布到宿主机的 `8000` 端口：

```console
$ docker run --publish 8000:80 --name webserver nginx

$ docker run -p 8000:80 --name webserver nginx
```

要发布所有端口，请使用 `-P` 标志。例如，以下命令（以分离模式）启动一个容器，`-P` 标志将容器所有暴露的端口发布到宿主机的随机端口上。

```console
$ docker run -d -P --name webserver nginx
```

或者，您也可以使用 [host 网络模式](/manuals/engine/network/drivers/host.md#docker-desktop) 让容器直接访问宿主机的网络栈。

有关与 `docker run` 配合使用的发布选项的更多详情，请参阅 [run 命令](/reference/cli/docker/container/run.md)。