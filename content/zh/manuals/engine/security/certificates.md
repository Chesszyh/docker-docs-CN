---
description: 如何设置和使用证书与注册表配合以验证访问
keywords: Usage, registry, repository, client, root, certificate, docker, apache, ssl, tls, documentation, examples, articles, tutorials, 注册表, 仓库, 客户端, 根证书, 验证
title: 使用证书验证仓库客户端
---

在 [使用 HTTPS 运行 Docker](protect-access.md) 中，您了解到默认情况下 Docker 通过非网络 Unix 套接字运行，必须启用 TLS 才能使 Docker 客户端和守护进程通过 HTTPS 进行安全通信。TLS 确保了注册表 (registry) 端点的真实性，并确保往返注册表的流量是加密的。

本文演示了如何使用基于证书的客户端-服务器身份验证，确保 Docker 注册表服务器与 Docker 守护进程 (注册表服务器的客户端) 之间的流量已加密且经过正确身份验证。

我们将向您展示如何为注册表安装证书颁发机构 (CA) 根证书，以及如何设置客户端 TLS 证书以进行验证。

## 了解配置

通过在 `/etc/docker/certs.d` 下创建一个使用注册表主机名 (例如 `localhost`) 命名的目录来配置自定义证书。该目录下的所有 `*.crt` 文件都被添加为 CA 根证书。

> [!NOTE]
>
> 在 Linux 上，任何根证书颁发机构都会与系统默认值 (包括主机的根 CA 集) 合并。如果您在 Windows Server 上运行 Docker，或是在使用 Windows 容器的 Docker Desktop for Windows 上运行，则仅在未配置自定义根证书时才使用系统默认证书。

存在一个或多个 `<filename>.key/cert` 对，向 Docker 表明访问目标仓库需要自定义证书。

> [!NOTE]
>
> 如果存在多个证书，则按字母顺序依次尝试。如果出现 4xx 级别或 5xx 级别的身份验证错误，Docker 将继续尝试下一个证书。

以下展示了带有自定义证书的配置：

```text
    /etc/docker/certs.d/        <-- 证书目录
    └── localhost:5000          <-- 主机名:端口
       ├── client.cert          <-- 客户端证书
       ├── client.key           <-- 客户端密钥
       └── ca.crt               <-- 签署了注册表证书的根 CA (PEM 格式)
```

上述示例与操作系统相关，仅用于说明目的。您应咨询您的操作系统文档以创建操作系统提供的捆绑证书链。


## 创建客户端证书

使用 OpenSSL 的 `genrsa` 和 `req` 命令，先生成 RSA 密钥，然后使用该密钥创建证书。

```console
$ openssl genrsa -out client.key 4096
$ openssl req -new -x509 -text -key client.key -out client.cert
```

> [!NOTE]
>
> 这些 TLS 命令仅在 Linux 上生成一组可用的证书。macOS 中的 OpenSSL 版本与 Docker 所需的证书类型不兼容。

## 故障排查提示

Docker 守护进程将 `.crt` 文件解释为 CA 证书，将 `.cert` 文件解释为 客户端证书。如果 CA 证书被意外赋予了 `.cert` 扩展名而不是正确的 `.crt` 扩展名，Docker 守护进程会记录以下错误消息：

```text
Missing key KEY_NAME for client certificate CERT_NAME. CA certificates should use the extension .crt.
```

如果访问 Docker 注册表时没有端口号，请不要在目录名称中添加端口。以下显示了默认端口 443 上注册表的配置，该注册表通过 `docker login my-https.registry.example.com` 访问：

```text
    /etc/docker/certs.d/
    └── my-https.registry.example.com          <-- 不带端口的主机名
       ├── client.cert
       ├── client.key
       └── ca.crt
```

## 相关信息

* [使用受信任的镜像](trust/_index.md)
* [保护 Docker 守护进程套接字](protect-access.md)
