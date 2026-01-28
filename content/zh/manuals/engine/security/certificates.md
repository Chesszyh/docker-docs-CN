---
description: How to set up and use certificates with a registry to verify access
keywords: Usage, registry, repository, client, root, certificate, docker, apache,
  ssl, tls, documentation, examples, articles, tutorials
title: 使用证书验证仓库客户端
aliases:
- /articles/certificates/
- /engine/articles/certificates/
---

在[使用 HTTPS 运行 Docker](protect-access.md) 中，你了解到默认情况下，Docker 通过非网络化的 Unix 套接字运行，必须启用 TLS 才能使 Docker 客户端和守护进程通过 HTTPS 安全通信。TLS 确保仓库端点的真实性，并确保往返仓库的流量是加密的。

本文演示如何使用基于证书的客户端-服务器身份验证来确保 Docker 仓库服务器和 Docker 守护进程（仓库服务器的客户端）之间的流量是加密的并经过正确的身份验证。

我们将向你展示如何为仓库安装证书颁发机构（CA）根证书以及如何设置客户端 TLS 证书进行验证。

## 理解配置

通过在 `/etc/docker/certs.d` 下创建一个与仓库主机名相同的目录来配置自定义证书，例如 `localhost`。所有 `*.crt` 文件都作为 CA 根证书添加到此目录。

> [!NOTE]
>
> 在 Linux 上，任何根证书颁发机构都会与系统默认值合并，包括主机的根 CA 集。如果你在 Windows Server 上运行 Docker，或在 Windows 容器上运行 Docker Desktop for Windows，则只有在未配置自定义根证书时才使用系统默认证书。

一个或多个 `<filename>.key/cert` 对的存在向 Docker 表明需要自定义证书才能访问所需的仓库。

> [!NOTE]
>
> 如果存在多个证书，则按字母顺序尝试每个证书。如果出现 4xx 级或 5xx 级身份验证错误，Docker 会继续尝试下一个证书。

以下说明了使用自定义证书的配置：

```text
    /etc/docker/certs.d/        <-- Certificate directory
    └── localhost:5000          <-- Hostname:port
       ├── client.cert          <-- Client certificate
       ├── client.key           <-- Client key
       └── ca.crt               <-- Root CA that signed
                                    the registry certificate, in PEM
```

前面的示例是特定于操作系统的，仅用于说明目的。你应该查阅操作系统文档以创建操作系统提供的捆绑证书链。


## 创建客户端证书

使用 OpenSSL 的 `genrsa` 和 `req` 命令首先生成一个 RSA 密钥，然后使用该密钥创建证书。

```console
$ openssl genrsa -out client.key 4096
$ openssl req -new -x509 -text -key client.key -out client.cert
```

> [!NOTE]
>
> 这些 TLS 命令仅在 Linux 上生成有效的证书集。macOS 中的 OpenSSL 版本与 Docker 所需的证书类型不兼容。

## 故障排除技巧

Docker 守护进程将 `.crt` 文件解释为 CA 证书，将 `.cert` 文件解释为客户端证书。如果 CA 证书意外地被赋予了 `.cert` 扩展名而不是正确的 `.crt` 扩展名，Docker 守护进程会记录以下错误消息：

```text
Missing key KEY_NAME for client certificate CERT_NAME. CA certificates should use the extension .crt.
```

如果在没有端口号的情况下访问 Docker 仓库，则不要在目录名称中添加端口。以下显示了默认端口 443 上仓库的配置，该仓库通过 `docker login my-https.registry.example.com` 访问：

```text
    /etc/docker/certs.d/
    └── my-https.registry.example.com          <-- Hostname without port
       ├── client.cert
       ├── client.key
       └── ca.crt
```

## 相关信息

* [使用受信任的镜像](trust/_index.md)
* [保护 Docker 守护进程套接字](protect-access.md)
