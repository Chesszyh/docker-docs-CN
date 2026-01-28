---
description: How to setup and run Docker with SSH or HTTPS
keywords: docker, docs, article, example, ssh, https, daemon, tls, ca,  certificate
title: 保护 Docker 守护进程套接字
aliases:
- /articles/https/
- /engine/articles/https/
- /engine/security/https/
---

默认情况下，Docker 通过非网络化的 UNIX 套接字运行。它也可以选择使用 SSH 或 TLS（HTTPS）套接字进行通信。

## 使用 SSH 保护 Docker 守护进程套接字

> [!NOTE]
>
> 给定的 `USERNAME` 必须具有访问远程机器上 docker 套接字的权限。请参阅[以非 root 用户身份管理 Docker](../install/linux-postinstall.md#manage-docker-as-a-non-root-user) 了解如何授予非 root 用户访问 docker 套接字的权限。

以下示例创建一个 [`docker context`](/manuals/engine/manage-resources/contexts.md) 以使用 SSH 连接到 `host1.example.com` 上的远程 `dockerd` 守护进程，并作为远程机器上的 `docker-user` 用户：

```console
$ docker context create \
    --docker host=ssh://docker-user@host1.example.com \
    --description="Remote engine" \
    my-remote-engine

my-remote-engine
Successfully created context "my-remote-engine"
```

创建上下文后，使用 `docker context use` 切换 `docker` CLI 以使用它，并连接到远程引擎：

```console
$ docker context use my-remote-engine
my-remote-engine
Current context is now "my-remote-engine"

$ docker info
<prints output of the remote engine>
```

使用 `default` 上下文切换回默认（本地）守护进程：

```console
$ docker context use default
default
Current context is now "default"
```

或者，使用 `DOCKER_HOST` 环境变量临时切换 `docker` CLI 以使用 SSH 连接到远程主机。这不需要创建上下文，对于与不同引擎创建临时连接很有用：

```console
$ export DOCKER_HOST=ssh://docker-user@host1.example.com
$ docker info
<prints output of the remote engine>
```

### SSH 技巧

为了获得最佳的 SSH 用户体验，请按以下方式配置 `~/.ssh/config`，以允许为 `docker` CLI 的多次调用重用 SSH 连接：

```text
 ControlMaster     auto
 ControlPath       ~/.ssh/control-%C
 ControlPersist    yes
```

## 使用 TLS（HTTPS）保护 Docker 守护进程套接字

如果你需要以安全的方式通过 HTTP 而不是 SSH 访问 Docker，你可以通过指定 `tlsverify` 标志并将 Docker 的 `tlscacert` 标志指向受信任的 CA 证书来启用 TLS（HTTPS）。

在守护进程模式下，它只允许来自由该 CA 签名的证书认证的客户端的连接。在客户端模式下，它只连接到由该 CA 签名的证书的服务器。

> [!IMPORTANT]
>
> 使用 TLS 和管理 CA 是一个高级话题。在生产环境中使用之前，请熟悉 OpenSSL、x509 和 TLS。

### 使用 OpenSSL 创建 CA、服务器和客户端密钥

> [!NOTE]
>
> 在以下示例中，将所有 `$HOST` 实例替换为你的 Docker 守护进程主机的 DNS 名称。

首先，在 Docker 守护进程的主机上，生成 CA 私钥和公钥：

```console
$ openssl genrsa -aes256 -out ca-key.pem 4096
Generating RSA private key, 4096 bit long modulus
..............................................................................++
........++
e is 65537 (0x10001)
Enter pass phrase for ca-key.pem:
Verifying - Enter pass phrase for ca-key.pem:

$ openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
Enter pass phrase for ca-key.pem:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:Queensland
Locality Name (eg, city) []:Brisbane
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Docker Inc
Organizational Unit Name (eg, section) []:Sales
Common Name (e.g. server FQDN or YOUR name) []:$HOST
Email Address []:Sven@home.org.au
```

现在你有了 CA，你可以创建服务器密钥和证书签名请求（CSR）。确保"Common Name"与你用于连接 Docker 的主机名匹配：

> [!NOTE]
>
> 在以下示例中，将所有 `$HOST` 实例替换为你的 Docker 守护进程主机的 DNS 名称。

```console
$ openssl genrsa -out server-key.pem 4096
Generating RSA private key, 4096 bit long modulus
.....................................................................++
.................................................................................................++
e is 65537 (0x10001)

$ openssl req -subj "/CN=$HOST" -sha256 -new -key server-key.pem -out server.csr
```

接下来，我们将使用我们的 CA 签署公钥：

由于 TLS 连接可以通过 IP 地址和 DNS 名称建立，因此在创建证书时需要指定 IP 地址。例如，要允许使用 `10.10.10.20` 和 `127.0.0.1` 进行连接：

```console
$ echo subjectAltName = DNS:$HOST,IP:10.10.10.20,IP:127.0.0.1 >> extfile.cnf
```

将 Docker 守护进程密钥的扩展用法属性设置为仅用于服务器身份验证：

```console
$ echo extendedKeyUsage = serverAuth >> extfile.cnf
```

现在，生成签名证书：

```console
$ openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out server-cert.pem -extfile extfile.cnf
Signature ok
subject=/CN=your.host.com
Getting CA Private Key
Enter pass phrase for ca-key.pem:
```

[授权插件](/engine/extend/plugins_authorization/)提供了更细粒度的控制来补充来自双向 TLS 的身份验证。除了上述文档中描述的其他信息外，在 Docker 守护进程上运行的授权插件会接收连接 Docker 客户端的证书信息。

对于客户端身份验证，创建客户端密钥和证书签名请求：

> [!NOTE]
>
> 为了简化接下来的几个步骤，你也可以在 Docker 守护进程的主机上执行此步骤。

```console
$ openssl genrsa -out key.pem 4096
Generating RSA private key, 4096 bit long modulus
.........................................................++
................++
e is 65537 (0x10001)

$ openssl req -subj '/CN=client' -new -key key.pem -out client.csr
```

要使密钥适合客户端身份验证，请创建一个新的扩展配置文件：

```console
$ echo extendedKeyUsage = clientAuth > extfile-client.cnf
```

现在，生成签名证书：

```console
$ openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out cert.pem -extfile extfile-client.cnf
Signature ok
subject=/CN=client
Getting CA Private Key
Enter pass phrase for ca-key.pem:
```

生成 `cert.pem` 和 `server-cert.pem` 后，你可以安全地删除两个证书签名请求和扩展配置文件：

```console
$ rm -v client.csr server.csr extfile.cnf extfile-client.cnf
```

使用默认的 `umask` 022，你的密钥是*全局可读*的，并且对你和你的组可写。

为了保护你的密钥免受意外损坏，请删除它们的写权限。要使它们只对你可读，请按以下方式更改文件模式：

```console
$ chmod -v 0400 ca-key.pem key.pem server-key.pem
```

证书可以是全局可读的，但你可能希望删除写访问权限以防止意外损坏：

```console
$ chmod -v 0444 ca.pem server-cert.pem cert.pem
```

现在你可以使 Docker 守护进程只接受来自提供由你的 CA 信任的证书的客户端的连接：

```console
$ dockerd \
    --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=server-cert.pem \
    --tlskey=server-key.pem \
    -H=0.0.0.0:2376
```

要连接到 Docker 并验证其证书，请提供你的客户端密钥、证书和受信任的 CA：

> [!TIP]
>
> 此步骤应在你的 Docker 客户端机器上运行。因此，你需要将你的 CA 证书、服务器证书和客户端证书复制到该机器。

> [!NOTE]
>
> 在以下示例中，将所有 `$HOST` 实例替换为你的 Docker 守护进程主机的 DNS 名称。

```console
$ docker --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=cert.pem \
    --tlskey=key.pem \
    -H=$HOST:2376 version
```

> [!NOTE]
>
> 基于 TLS 的 Docker 应该在 TCP 端口 2376 上运行。

> [!WARNING]
>
> 如上例所示，当你使用证书身份验证时，不需要使用 `sudo` 或 `docker` 组运行 `docker` 客户端。这意味着任何拥有密钥的人都可以向你的 Docker 守护进程发出任何指令，从而获得托管守护进程的机器的 root 访问权限。像保护 root 密码一样保护这些密钥！

### 默认安全

如果你想默认保护你的 Docker 客户端连接，你可以将文件移动到你的主目录中的 `.docker` 目录——同时设置 `DOCKER_HOST` 和 `DOCKER_TLS_VERIFY` 变量（而不是在每次调用时传递 `-H=tcp://$HOST:2376` 和 `--tlsverify`）。

```console
$ mkdir -pv ~/.docker
$ cp -v {ca,cert,key}.pem ~/.docker

$ export DOCKER_HOST=tcp://$HOST:2376 DOCKER_TLS_VERIFY=1
```

Docker 现在默认安全连接：

    $ docker ps

### 其他模式

如果你不想进行完整的双向身份验证，你可以通过混合标志以各种其他模式运行 Docker。

#### 守护进程模式

 - `tlsverify`、`tlscacert`、`tlscert`、`tlskey` 设置：验证客户端
 - `tls`、`tlscert`、`tlskey`：不验证客户端

#### 客户端模式

 - `tls`：基于公共/默认 CA 池验证服务器
 - `tlsverify`、`tlscacert`：基于给定的 CA 验证服务器
 - `tls`、`tlscert`、`tlskey`：使用客户端证书进行身份验证，不基于给定的 CA 验证服务器
 - `tlsverify`、`tlscacert`、`tlscert`、`tlskey`：使用客户端证书进行身份验证，并基于给定的 CA 验证服务器

如果找到，客户端会发送其客户端证书，所以你只需要将你的密钥放入 `~/.docker/{ca,cert,key}.pem`。或者，如果你想将密钥存储在其他位置，你可以使用环境变量 `DOCKER_CERT_PATH` 指定该位置。

```console
$ export DOCKER_CERT_PATH=~/.docker/zone1/
$ docker --tlsverify ps
```

#### 使用 `curl` 连接到安全的 Docker 端口

要使用 `curl` 进行测试 API 请求，你需要使用三个额外的命令行标志：

```console
$ curl https://$HOST:2376/images/json \
  --cert ~/.docker/cert.pem \
  --key ~/.docker/key.pem \
  --cacert ~/.docker/ca.pem
```

## 相关信息

* [使用证书进行仓库客户端验证](certificates.md)
* [使用受信任的镜像](trust/_index.md)
