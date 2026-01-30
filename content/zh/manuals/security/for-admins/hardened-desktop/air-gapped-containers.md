---
title: 离线容器
description: 离线容器 - 是什么、优势以及如何配置。
keywords: air gapped, security, Docker Desktop, configuration, proxy, network
aliases:
 - /desktop/hardened-desktop/settings-management/air-gapped-containers/
 - /desktop/hardened-desktop/air-gapped-containers/
---

{{< summary-bar feature_name="Air-gapped containers" >}}

离线容器（Air-gapped containers）允许您限制容器访问网络资源，限制数据可以上传到或下载自哪些位置。

Docker Desktop 可以对来自容器的网络流量应用一组自定义代理规则。代理可以配置为：

- 接受网络连接
- 拒绝网络连接
- 通过 HTTP 或 SOCKS 代理进行隧道传输

您可以选择：

- 策略适用于哪些出站 TCP 端口。例如，仅某些端口 `80`、`443` 或使用 `*` 表示所有端口。
- 是转发到单个 HTTP 或 SOCKS 代理，还是通过代理自动配置（PAC）文件为每个目标设置策略。

## 配置

假设已启用[强制登录](/manuals/security/for-admins/enforce-sign-in/_index.md)和[设置管理](settings-management/_index.md)，请将新的代理配置添加到 `admin-settings.json` 文件中。例如：

```json
{
  "configurationFileVersion": 2,
  "containersProxy": {
    "locked": true,
    "mode": "manual",
    "http": "",
    "https": "",
    "exclude": [],
    "pac": "http://192.168.1.16:62039/proxy.pac",
    "transparentPorts": "*"
  }
}
```

`containersProxy` 设置描述了应用于容器流量的策略。有效字段包括：

- `locked`：如果为 true，开发人员无法覆盖这些设置。如果为 false，这些设置将被解释为开发人员可以更改的默认值。
- `mode`：与现有 `proxy` 设置含义相同。可能的值为 `system` 和 `manual`。
- `http`、`https`、`exclude`：与 `proxy` 设置含义相同。仅在 `mode` 设置为 `manual` 时生效。
- `pac`：PAC 文件的 URL。仅在 `mode` 为 `manual` 时生效，并且优先级高于 `http`、`https`、`exclude`。
- `transparentPorts`：以逗号分隔的端口列表（例如 `"80,443,8080"`）或通配符（`*`），指示应代理哪些端口。

> [!IMPORTANT]
>
> `admin-settings.json` 文件中任何现有的 `proxy` 设置将继续应用于主机上应用程序的流量。
> 如果 PAC 文件下载失败，容器将阻止对目标 URL 的请求。

## PAC 文件示例

有关 PAC 文件的一般信息，请参阅 [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Proxy_servers_and_tunneling/Proxy_Auto-Configuration_PAC_file)。

以下是一个 PAC 文件示例：

```javascript
function FindProxyForURL(url, host) {
	if (localHostOrDomainIs(host, 'internal.corp')) {
		return "PROXY 10.0.0.1:3128";
	}
	if (isInNet(host, "192.168.0.0", "255.255.255.0")) {
	    return "DIRECT";
	}
    return "PROXY reject.docker.internal:1234";
}
```

`url` 参数为 `http://host_or_ip:port` 或 `https://host_or_ip:port`。

主机名通常可用于端口 `80` 和 `443` 上的出站请求，但对于其他情况，只有 IP 地址可用。

`FindProxyForURL` 可以返回以下值：

- `PROXY host_or_ip:port`：通过 HTTP 代理 `host_or_ip:port` 隧道传输此请求
- `SOCKS5 host_or_ip:port`：通过 SOCKS 代理 `host_or_ip:port` 隧道传输此请求
- `DIRECT`：让此请求直接通过，不使用代理
- `PROXY reject.docker.internal:any_port`：拒绝此请求

在这个特定示例中，`internal.corp` 的 HTTP 和 HTTPS 请求通过 HTTP 代理 `10.0.0.1:3128` 发送。连接到子网 `192.168.0.0/24` 上 IP 的请求直接连接。所有其他请求都被阻止。

要限制连接到开发人员本地机器端口的流量，请[匹配特殊主机名 `host.docker.internal`](/manuals/desktop/features/networking.md#i-want-to-connect-from-a-container-to-a-service-on-the-host)。
