--- 
description: 如何设置和运行带有 SSH 或 HTTPS 的 Docker
keywords: docker, docs, article, example, ssh, https, daemon, tls, ca, certificate, 安全, 守护进程, 证书
title: 保护 Docker 守护进程套接字
---

默认情况下，Docker 通过非网络 UNIX 套接字运行。它也可以选择使用 SSH 或 TLS (HTTPS) 套接字进行通信。

## 使用 SSH 保护 Docker 守护进程套接字

> [!NOTE]
> 
> 指定的 `USERNAME` 必须具有访问远程机器上 Docker 套接字的权限。参考 [以非 root 用户管理 Docker](../install/linux-postinstall.md#manage-docker-as-a-non-root-user) 了解如何授予非 root 用户对 Docker 套接字的访问权限。

以下示例创建一个 [`docker context`](/manuals/engine/manage-resources/contexts.md)，以便使用 SSH 作为远程机器上的 `docker-user` 用户连接到 `host1.example.com` 上的远程 `dockerd` 守护进程：

```console
$ docker context create \
    --docker host=ssh://docker-user@host1.example.com \
    --description="Remote engine" \
    my-remote-engine

my-remote-engine
Successfully created context "my-remote-engine"
```

创建上下文后，使用 `docker context use` 将 `docker` CLI 切换到该上下文，并连接到远程引擎：

```console
$ docker context use my-remote-engine
my-remote-engine
Current context is now "my-remote-engine"

$ docker info
<打印远程引擎的输出>
```

使用 `default` 上下文切回默认 (本地) 守护进程：

```console
$ docker context use default
default
Current context is now "default"
```

或者，使用 `DOCKER_HOST` 环境变量临时切换 `docker` CLI，通过 SSH 连接到远程主机。这不需要创建上下文，对于与不同引擎建立临时连接很有用：

```console
$ export DOCKER_HOST=ssh://docker-user@host1.example.com
$ docker info
<打印远程引擎的输出>
```

### SSH 提示

为了获得最佳的 SSH 使用体验，请按如下方式配置 `~/.ssh/config`，以允许在多次调用 `docker` CLI 时重用 SSH 连接：

```text
ControlMaster     auto
ControlPath       ~/.ssh/control-%C
ControlPersist    yes
```

## 使用 TLS (HTTPS) 保护 Docker 守护进程套接字

如果您需要 Docker 能够以安全的方式通过 HTTP 而不是 SSH 访问，可以通过指定 `tlsverify` 标志并将 Docker 的 `tlscacert` 标志指向受信任的 CA 证书来启用 TLS (HTTPS)。

在守护进程模式下，它仅允许通过由该 CA 签名的证书进行身份验证的客户端连接。在客户端模式下，它仅连接到具有由该 CA 签名的证书的服务器。

> [!IMPORTANT]
> 
> 使用 TLS 和管理 CA 是一个高级话题。在生产环境中使用之前，请先熟悉 OpenSSL、x509 和 TLS。

### 使用 OpenSSL 创建 CA、服务器和客户端密钥

> [!NOTE]
> 
> 在以下示例中，将所有 `$HOST` 实例替换为您 Docker 守护进程主机的 DNS 名称。

首先，在 Docker 守护进程的主机上生成 CA 私钥和公钥：

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
Common Name (e.g. server FQDN or YOUR name) [*.example.com]:$HOST
Email Address []:Sven@home.org.au
```

现在您有了 CA，可以创建服务器密钥和证书签名请求 (CSR)。确保“Common Name”与您连接 Docker 时使用的主机名匹配：

> [!NOTE]
> 
> 将以下示例中所有的 `$HOST` 替换为您 Docker 守护进程主机的 DNS 名称。

```console
$ openssl genrsa -out server-key.pem 4096
Generating RSA private key, 4096 bit long modulus
.....................................................................++
.................................................................................................++
e is 65537 (0x10001)

$ openssl req -subj "/CN=$HOST" -sha256 -new -key server-key.pem -out server.csr
```

接下来，我们将使用 CA 签署公钥：

由于 TLS 连接可以通过 IP 地址以及 DNS 名称建立，因此在创建证书时需要指定 IP 地址。例如，要允许使用 `10.10.10.20` 和 `127.0.0.1` 进行连接：

```console
$ echo subjectAltName = DNS:$HOST,IP:10.10.10.20,IP:127.0.0.1 >> extfile.cnf
```

将 Docker 守护进程密钥的扩展用途属性设置为仅用于服务器身份验证：

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

[授权插件](/engine/extend/plugins_authorization/) 提供了更精细的控制，以补充双向 TLS 的身份验证。除了上述文档中描述的其他信息外，运行在 Docker 守护进程上的授权插件还会接收到连接 Docker 客户端的证书信息。

对于客户端身份验证，创建客户端密钥和证书签名请求：

> [!NOTE]
> 
> 为简化接下来的几个步骤，您也可以在 Docker 守护进程的主机上执行此步骤。

```console
$ openssl genrsa -out key.pem 4096
Generating RSA private key, 4096 bit long modulus
.........................................................++
................++
e is 65537 (0x10001)

$ openssl req -subj '/CN=client' -new -key key.pem -out client.csr
```

要使该密钥适用于客户端身份验证，请创建一个新的扩展配置文件：

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

生成 `cert.pem` 和 `server-cert.pem` 后，您可以安全地删除两个证书签名请求和扩展配置文件：

```console
$ rm -v client.csr server.csr extfile.cnf extfile-client.cnf
```

在默认 `umask` 为 022 的情况下，您的密钥是 *所有人可读* 的，并且对您和您的组是可写的。

为了防止密钥被意外损坏，请移除它们的写权限。要使它们仅对您自己可读，请按如下方式更改文件模式：

```console
$ chmod -v 0400 ca-key.pem key.pem server-key.pem
```

证书可以是所有人可读的，但您可能希望移除写访问权限以防止意外损坏：

```console
$ chmod -v 0444 ca.pem server-cert.pem cert.pem
```

现在您可以使 Docker 守护进程仅接受来自提供由您的 CA 信任的证书的客户端连接：

```console
$ dockerd \
    --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=server-cert.pem \
    --tlskey=server-key.pem \
    -H=0.0.0.0:2376
```

要连接到 Docker 并验证其证书，请提供您的客户端密钥、证书和受信任的 CA：

> [!TIP]
> 
> 此步骤应在您的 Docker 客户端机器上运行。因此，您需要将 CA 证书、服务器证书和客户端证书复制到该机器上。

> [!NOTE]
> 
> 在以下示例中，将所有 `$HOST` 实例替换为您 Docker 守护进程主机的 DNS 名称。

```console
$ docker --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=cert.pem \
    --tlskey=key.pem \
    -H=$HOST:2376 version
```

> [!NOTE]
> 
> 基于 TLS 的 Docker 应运行在 TCP 端口 2376 上。

> [!WARNING]
> 
> 如上例所示，使用证书身份验证时，您不需要通过 `sudo` 或 `docker` 组运行 `docker` 客户端。这意味着任何拥有密钥的人都可以向您的 Docker 守护进程发送任何指令，从而获得对托管守护进程的机器的 root 访问权限。请像保管 root 密码一样保管这些密钥！

### 默认安全

如果您希望默认保护您的 Docker 客户端连接，可以将文件移动到主目录中的 `.docker` 目录中 —— 并且同时设置 `DOCKER_HOST` 和 `DOCKER_TLS_VERIFY` 变量 (而不是在每次调用时都传递 `-H=tcp://$HOST:2376` 和 `--tlsverify`)。

```console
$ mkdir -pv ~/.docker
$ cp -v {ca,cert,key}.pem ~/.docker

$ export DOCKER_HOST=tcp://$HOST:2376 DOCKER_TLS_VERIFY=1
```

Docker 现在默认进行安全连接：

    $ docker ps

### 其他模式

如果您不想要完全的双向身份验证，可以通过混合标志以其他各种模式运行 Docker。

#### 守护进程模式

 - 设置 `tlsverify`、`tlscacert`、`tlscert`、`tlskey`: 验证客户端
 - 设置 `tls`、`tlscert`、`tlskey`: 不验证客户端

#### 客户端模式

 - `tls`: 根据公共/默认 CA 池验证服务器
 - `tlsverify`、`tlscacert`: 根据给定的 CA 验证服务器
 - `tls`、`tlscert`、`tlskey`: 使用客户端证书进行身份验证，不根据给定的 CA 验证服务器
 - `tlsverify`、`tlscacert`、`tlscert`、`tlskey`: 使用客户端证书进行身份验证，并根据给定的 CA 验证服务器

如果找到了，客户端会发送其客户端证书，因此您只需将密钥放入 `~/.docker/{ca,cert,key}.pem` 即可。或者，如果您想将密钥存储在其他位置，可以使用环境变量 `DOCKER_CERT_PATH` 指定该位置。

```console
$ export DOCKER_CERT_PATH=~/.docker/zone1/
$ docker --tlsverify ps
```

#### 使用 `curl` 连接到安全的 Docker 端口

要使用 `curl` 发出测试 API 请求，您需要使用三个额外的命令行标志：

```console
$ curl https://$HOST:2376/images/json \
  --cert ~/.docker/cert.pem \
  --key ~/.docker/key.pem \
  --cacert ~/.docker/ca.pem
```

## 相关信息

* [使用证书验证仓库客户端](certificates.md)
* [使用受信任的镜像](trust/_index.md)

