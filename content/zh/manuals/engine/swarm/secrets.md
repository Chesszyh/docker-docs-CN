--- 
title: 使用 Docker 机密 (Secrets) 管理敏感数据
description: 了解如何使用 Docker 服务安全地存储、检索和使用敏感数据
keywords: swarm, secrets, credentials, sensitive strings, sensitive data, security, encryption, encryption at rest, 机密, 凭据, 加密, 敏感数据
tags: [Secrets]
---

## 关于机密 (Secrets)

就 Docker Swarm 服务而言，*机密 (secret)* 是指一类数据，如密码、SSH 私钥、SSL 证书，或其他不应通过网络传输、不应以未加密方式存储在 Dockerfile 或应用程序源代码中的敏感数据。您可以使用 Docker *机密 (secrets)* 来集中管理这些数据，并仅将其安全地传输到需要访问它们的容器中。机密在 Docker Swarm 中无论是传输过程还是静态存储时都是加密的。特定的机密仅对已被明确授予访问权限的服务可用，且仅在该服务任务运行时才可用。

您可以使用机密来管理容器在运行时需要的、但您不想存储在镜像或源码控制系统中的任何敏感数据，例如：

- 用户名和密码
- TLS 证书和密钥
- SSH 密钥
- 其他重要数据，如数据库名称或内部服务器名称
- 通用字符串或二进制内容 (大小最多 500 KB)

> [!NOTE]
> 
> Docker 机密仅对 Swarm 服务可用，对独立容器不可用。要使用此特性，请考虑将您的容器调整为以服务形式运行。有状态容器通常可以在不更改容器代码的情况下，以副本数为 1 的服务运行。

使用机密的另一个用例是在容器与一组凭据之间提供一层抽象。考虑这样一个场景：您的应用程序有独立的开发、测试和生产环境。每个环境都可以有不同的凭据，并以相同的机密名称存储在开发、测试和生产 Swarm 中。您的容器只需要知道机密的名称即可在所有三个环境中运行。

您也可以使用机密来管理非敏感数据，如配置文件。不过，Docker 支持使用 [Configs](configs.md) 来存储非敏感数据。Configs 直接挂载到容器的文件系统中，而不使用 RAM 磁盘。

### Windows 支持

Docker 包含对 Windows 容器上的机密的支持。在实现上存在差异的地方，下文的示例中会予以说明。请记住以下显著区别：

- Microsoft Windows 没有内置的 RAM 磁盘管理驱动程序，因此在运行中的 Windows 容器内，机密以明文形式持久化到容器的根磁盘中。然而，机密在容器停止时会被显式移除。此外，Windows 不支持使用 `docker commit` 或类似命令将运行中的容器持久化为镜像。

- 在 Windows 上，我们建议在主机上包含 Docker 根目录的卷上启用 [BitLocker](https://technet.microsoft.com/en-us/library/cc732774(v=ws.11).aspx)，以确保运行中容器的机密在磁盘上是加密存储的。

- 具有自定义目标的机密文件不会直接绑定挂载到 Windows 容器中，因为 Windows 不支持非目录文件的绑定挂载。相反，容器的所有机密都挂载在容器内的 `C:\ProgramData\Docker\internal\secrets` (这是一个实现细节，应用程序不应依赖它)。符号链接用于从该位置指向容器内机密的目标位置。默认目标是 `C:\ProgramData\Docker\secrets`。

- 创建使用 Windows 容器的服务时，机密不支持指定 UID、GID 和权限模式 (mode) 的选项。目前，机密仅供容器内的管理员和具有 `system` 访问权限的用户访问。

## Docker 如何管理机密

当您向 Swarm 添加机密时，Docker 会通过双向 TLS 连接将机密发送给 Swarm 管理节点。机密存储在经过加密的 Raft 日志中。整个 Raft 日志会在其他管理节点之间进行复制，从而确保机密与 Swarm 其他管理数据具有相同的高可用性保证。

当您授予新建或运行中的服务访问机密的权限时，解密后的机密会挂载到容器的内存文件系统中。在 Linux 容器中，挂载点在容器内的默认位置是 `/run/secrets/<secret_name>`，在 Windows 容器中是 `C:\ProgramData\Docker\secrets`。您也可以指定自定义位置。

您可以随时更新服务，以授予其访问额外机密的权限，或撤销其对给定机密的访问权限。

只有当节点是 Swarm 管理节点，或者节点正在运行已被授予访问机密权限的服务任务时，该节点才有权访问 (加密的) 机密。当容器任务停止运行时，共享给它的已解密机密会从该容器的内存文件系统中卸载，并从节点的内存中清除。

如果节点在运行具有机密访问权限的任务容器时失去了与 Swarm 的连接，该任务容器仍可访问其机密，但在节点重新连接到 Swarm 之前无法接收更新。

您可以随时添加或检查单个机密，或列出所有机密。您不能删除正在运行的服务正在使用的机密。参见 [轮换机密](secrets.md#example-rotate-a-secret)，了解在不中断运行中服务的情况下删除机密的方法。

为了更容易地更新或回滚机密，请考虑在机密名称中添加版本号或日期。由于可以控制机密在给定容器内的挂载点，这一点变得更加容易。

## 阅读更多关于 `docker secret` 命令的信息

使用以下链接阅读有关特定命令的信息，或者继续查看 [在服务中使用机密的示例](secrets.md#simple-example-get-started-with-secrets)。

- [`docker secret create`](/reference/cli/docker/secret/create.md)
- [`docker secret inspect`](/reference/cli/docker/secret/inspect.md)
- [`docker secret ls`](/reference/cli/docker/secret/ls.md)
- [`docker secret rm`](/reference/cli/docker/secret/rm.md)
- `docker service create` 的 [`--secret`](/reference/cli/docker/service/create.md#secret) 标志
- `docker service update` 的 [`--secret-add` 和 `--secret-rm`](/reference/cli/docker/service/update.md#secret-add) 标志

## 示例

本节包含三个由浅入深的示例，说明了如何使用 Docker 机密。这些示例中使用的镜像已经过更新，以便更容易地使用 Docker 机密。要了解如何以类似方式修改您自己的镜像，请参阅 [在您的镜像中构建对 Docker 机密的支持](#build-support-for-docker-secrets-into-your-images)。

> [!NOTE]
> 
> 为简单起见，这些示例使用单引擎 Swarm 和未进行扩展的服务。示例使用 Linux 容器，但 Windows 容器也支持机密。参见 [Windows 支持](#windows-support)。

### 在 Compose 文件中定义和使用机密 

`docker-compose` 和 `docker stack` 命令都支持在 Compose 文件中定义机密。详情请参阅 [Compose 文件参考](/reference/compose-file/legacy-versions.md)。

### 简单示例：机密入门

这个简单的示例展示了仅通过几个命令机密是如何工作的。有关更实际的示例，请继续查看 [中级示例：在 Nginx 服务中使用机密](#intermediate-example-use-secrets-with-a-nginx-service)。

1.  向 Docker 添加一个机密。`docker secret create` 命令读取标准输入，因为代表读取机密来源文件的最后一个参数被设置为 `-`。

    ```console
    $ printf "This is a secret" | docker secret create my_secret_data -
    ```

2.  创建一个 `redis` 服务并授予其访问该机密的权限。默认情况下，容器可以在 `/run/secrets/<secret_name>` 处访问该机密，但您可以使用 `target` 选项自定义容器上的文件名。

    ```console
    $ docker service create --name redis --secret my_secret_data redis:alpine
    ```

3.  使用 `docker service ps` 验证任务是否运行正常。如果一切正常，输出类似于以下内容：

    ```console
    $ docker service ps redis

    ID            NAME       IMAGE         NODE              DESIRED STATE  CURRENT STATE          ERROR  PORTS
    bkna6bpn8r1a  redis.1    redis:alpine  ip-172-31-46-109  Running        Running 8 seconds ago  
    ```

    如果出现错误，且任务失败并反复重启，您将看到类似于以下内容：

    ```console
    $ docker service ps redis

    NAME                      IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR                      PORTS
    redis.1.siftice35gla      redis:alpine  moby  Running        Running 4 seconds ago                             
     \_ redis.1.whum5b7gu13e  redis:alpine  moby  Shutdown       Failed 20 seconds ago      "task: non-zero exit (1)"  
     \_ redis.1.2s6yorvd9zow  redis:alpine  moby  Shutdown       Failed 56 seconds ago      "task: non-zero exit (1)"  
     \_ redis.1.ulfzrcyaf6pg  redis:alpine  moby  Shutdown       Failed about a minute ago  "task: non-zero exit (1)"  
     \_ redis.1.wrny5v4xyps6  redis:alpine  moby  Shutdown       Failed 2 minutes ago       "task: non-zero exit (1)"
    ```

4.  使用 `docker ps` 获取 `redis` 服务任务容器的 ID，以便您可以使用 `docker container exec` 连接到容器并读取机密数据文件的内容。该文件默认对所有人可读，且名称与机密名称相同。下面的第一个命令说明如何查找容器 ID，第二和第三个命令使用 shell 补全自动执行此操作。

    ```console
    $ docker ps --filter name=redis -q

    5cb1c2348a59

    $ docker container exec $(docker ps --filter name=redis -q) ls -l /run/secrets

    total 4
    -r--r--r--    1 root     root            17 Dec 13 22:48 my_secret_data

    $ docker container exec $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

    This is a secret
    ```

5.  验证如果您 commit (提交) 该容器，机密是否不可用。

    ```console
    $ docker commit $(docker ps --filter name=redis -q) committed_redis

    $ docker run --rm -it committed_redis cat /run/secrets/my_secret_data

    cat: can't open '/run/secrets/my_secret_data': No such file or directory
    ```

6.  尝试删除该机密。删除失败，因为 `redis` 服务正在运行且有权访问该机密。

    ```console
    $ docker secret ls

    ID                          NAME                CREATED             UPDATED
    wwwrxza8sxy025bas86593fqs   my_secret_data      4 hours ago         4 hours ago


    $ docker secret rm my_secret_data

    Error response from daemon: rpc error: code = 3 desc = secret
    'my_secret_data' is in use by the following service: redis
    ```

7.  通过更新服务，从运行中的 `redis` 服务中移除对该机密的访问权限。

    ```console
    $ docker service update --secret-rm my_secret_data redis
    ```

8.  再次重复步骤 3 和 4，验证服务不再具有对该机密的访问权限。容器 ID 会不同，因为 `service update` 命令会重新部署服务。

    ```console
    $ docker container exec -it $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

    cat: can't open '/run/secrets/my_secret_data': No such file or directory
    ```

9.  停止并移除该服务，并从 Docker 中删除该机密。

    ```console
    $ docker service rm redis

    $ docker secret rm my_secret_data
    ```

### 简单示例：在 Windows 服务中使用机密 

这是一个非常简单的示例，展示了如何在运行 Windows 容器的 Docker for Windows 上的 Microsoft IIS 服务中使用机密。这是一个简单的示例，它将网页存储在机密中。

此示例假设您已安装了 PowerShell。

1.  将以下内容保存到新文件 `index.html` 中。

    ```html
    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello Docker! You have deployed a HTML page.</p>
      </body>
    </html>
    ```

2.  如果您还没有这样做，请初始化或加入 Swarm。

    ```console
    > docker swarm init
    ```

3.  将 `index.html` 文件保存为名为 `homepage` 的 Swarm 机密。

    ```console
    > docker secret create homepage index.html
    ```

4.  创建一个 IIS 服务并授予其访问 `homepage` 机密的权限。

    ```console
    > docker service create \
        --name my-iis \
        --publish published=8000,target=8000 \
        --secret src=homepage,target="\inetpub\wwwroot\index.html" \
        microsoft/iis:nanoserver
    ```

    > [!NOTE]
    > 
    > 从技术上讲，本例没有理由使用机密；使用 [Configs](configs.md) 会更合适。本例仅用于说明目的。

5.  访问位于 `http://localhost:8000/` 的 IIS 服务。它应该提供第一步中的 HTML 内容。

6.  移除服务和机密。

    ```console
    > docker service rm my-iis
    > docker secret rm homepage
    > docker image remove secret-test
    ```

### 中级示例：在 Nginx 服务中使用机密

此示例分为两部分。[第一部分](#generate-the-site-certificate) 主要是关于生成站点证书，并不直接涉及 Docker 机密，但它为 [第二部分](#configure-the-nginx-container) 做了准备，在第二部分中，您将站点证书和 Nginx 配置作为机密进行存储和使用。

#### 生成站点证书

为您网站生成根 CA 以及 TLS 证书和密钥。对于生产站点，您可能希望使用 `Let’s Encrypt` 等服务来生成 TLS 证书和密钥，但此示例使用命令行工具。这一步有点复杂，但只是一个设置步骤，目的是为了让您有东西可以作为 Docker 机密存储。如果您想跳过这些子步骤，可以 [使用 Let's Encrypt](https://letsencrypt.org/getting-started/) 生成站点密钥和证书，将文件命名为 `site.key` 和 `site.crt`，然后直接跳到 [配置 Nginx 容器](#configure-the-nginx-container)。

1.  生成根密钥。

    ```console
    $ openssl genrsa -out "root-ca.key" 4096
    ```

2.  使用根密钥生成 CSR。

    ```console
    $ openssl req \
              -new -key "root-ca.key" \
              -out "root-ca.csr" -sha256 \
              -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA'
    ```

3.  配置根 CA。编辑一个名为 `root-ca.cnf` 的新文件并粘贴以下内容。这限制了根 CA 只能签署叶子证书，而不能签署中间 CA。

    ```ini
    [root_ca]
    basicConstraints = critical,CA:TRUE,pathlen:1
    keyUsage = critical, nonRepudiation, cRLSign, keyCertSign
    subjectKeyIdentifier=hash
    ```

4.  对证书进行签名。

    ```console
    $ openssl x509 -req  -days 3650  -in "root-ca.csr" \
                   -signkey "root-ca.key" -sha256 -out "root-ca.crt" \
                   -extfile "root-ca.cnf" -extensions \
                   root_ca
    ```

5.  生成站点密钥。

    ```console
    $ openssl genrsa -out "site.key" 4096
    ```

6.  生成站点证书并使用站点密钥进行签名。

    ```console
    $ openssl req -new -key "site.key" -out "site.csr" -sha256 \
              -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost'
    ```

7.  配置站点证书。编辑一个名为 `site.cnf` 的新文件并粘贴以下内容。这限制了站点证书只能用于验证服务器，而不能用于签署证书。

    ```ini
    [server]
    authorityKeyIdentifier=keyid,issuer
    basicConstraints = critical,CA:FALSE
    extendedKeyUsage=serverAuth
    keyUsage = critical, digitalSignature, keyEncipherment
    subjectAltName = DNS:localhost, IP:127.0.0.1
    subjectKeyIdentifier=hash
    ```

8.  对站点证书进行签名。

    ```console
    $ openssl x509 -req -days 750 -in "site.csr" -sha256 \
        -CA "root-ca.crt" -CAkey "root-ca.key"  -CAcreateserial \
        -out "site.crt" -extfile "site.cnf" -extensions server
    ```

9.  Nginx 服务不需要 `site.csr` 和 `site.cnf` 文件，但如果您想生成新的站点证书，则需要它们。请保护好 `root-ca.key` 文件。

#### 配置 Nginx 容器

1.  生成一个非常基础的 Nginx 配置，通过 HTTPS 提供静态文件。TLS 证书和密钥存储为 Docker 机密，以便于轮换。 

    在当前目录下，创建一个名为 `site.conf` 的新文件，内容如下：

    ```nginx
    server {
        listen                443 ssl;
        server_name           localhost;
        ssl_certificate       /run/secrets/site.crt;
        ssl_certificate_key   /run/secrets/site.key;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
    }
    ```

2.  创建三个机密，分别代表密钥、证书和 `site.conf`。只要文件小于 500 KB，您就可以将其存储为机密。这允许您将密钥、证书和配置从使用它们的服务中解耦。在这些命令中，最后一个参数代表在主机文件系统上读取机密的来源路径。在这些示例中，机密名称和文件名是相同的。

    ```console
    $ docker secret create site.key site.key

    $ docker secret create site.crt site.crt

    $ docker secret create site.conf site.conf
    ```

    ```console
    $ docker secret ls

    ID                          NAME                  CREATED             UPDATED
    2hvoi9mnnaof7olr3z5g3g7fp   site.key       58 seconds ago      58 seconds ago
    aya1dh363719pkiuoldpter4b   site.crt       24 seconds ago      24 seconds ago
    zoa5df26f7vpcoz42qf2csth8   site.conf      11 seconds ago      11 seconds ago
    ```

3.  创建一个运行 Nginx 的服务，并授予其访问三个机密的权限。`docker service create` 命令的最后部分创建了一个从机密 `site.conf` 的位置到 `/etc/nginx/conf.d/` 的符号链接，Nginx 在该目录下寻找额外的配置文件。这一步发生在 Nginx 实际启动之前，因此如果您更改了 Nginx 配置，无需重新构建镜像。

    > [!NOTE]
    > 
    > 通常情况下，您会创建一个 Dockerfile 将 `site.conf` 复制到指定位置，构建镜像，并使用自定义镜像运行容器。本例不需要自定义镜像。它一步完成了 `site.conf` 的部署和容器运行。

    默认情况下，机密位于容器内的 `/run/secrets/` 目录中，这可能需要容器内执行额外步骤才能在不同路径下使用机密。下例创建了一个指向 `site.conf` 文件真实位置的符号链接，以便 Nginx 可以读取它：

    ```console
    $ docker service create \
         --name nginx \
         --secret site.key \
         --secret site.crt \
         --secret site.conf \
         --publish published=3000,target=443 \
         nginx:latest \
         sh -c "ln -s /run/secrets/site.conf /etc/nginx/conf.d/site.conf && exec nginx -g 'daemon off;'"
    ```

    除了创建符号链接，机密还允许您使用 `target` 选项指定自定义位置。下例说明了如何让 `site.conf` 机密在容器内的 `/etc/nginx/conf.d/site.conf` 路径下可用，而无需使用符号链接：

    ```console
    $ docker service create \
         --name nginx \
         --secret site.key \
         --secret site.crt \
         --secret source=site.conf,target=/etc/nginx/conf.d/site.conf \
         --publish published=3000,target=443 \
         nginx:latest \
         sh -c "exec nginx -g 'daemon off;'"
    ```

    `site.key` 和 `site.crt` 机密使用了简写语法，没有设置自定义 `target` 位置。简写语法会将机密挂载在 `/run/secrets/` 下，名称与机密相同。在运行中的容器内，现在存在以下三个文件：

    - `/run/secrets/site.key`
    - `/run/secrets/site.crt`
    - `/etc/nginx/conf.d/site.conf`

4.  验证 Nginx 服务是否正在运行。

    ```console
    $ docker service ls

    ID            NAME   MODE        REPLICAS  IMAGE
    zeskcec62q24  nginx  replicated  1/1       nginx:latest

    $ docker service ps nginx

    NAME                  IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR  PORTS
    nginx.1.9ls3yo9ugcls  nginx:latest  moby  Running        Running 3 minutes ago
    ```

5.  验证服务是否正常运行：您可以访问 Nginx 服务器，并确认正在使用正确的 TLS 证书。

    ```console
    $ curl --cacert root-ca.crt https://localhost:3000

    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>

    <p>For online documentation and support. refer to
    <a href="https://nginx.org">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="https://www.nginx.com">www.nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```

    ```console
    $ openssl s_client -connect localhost:3000 -CAfile root-ca.crt

    CONNECTED(00000003)
    depth=1 /C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
    verify return:1
    depth=0 /C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
    verify return:1
    ---
    Certificate chain
     0 s:/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
       i:/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
    ---
    Server certificate
    -----BEGIN CERTIFICATE-----
    …
    -----END CERTIFICATE-----
    subject=/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
    issuer=/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
    ---
    No client certificate CA names sent
    ---
    SSL handshake has read 1663 bytes and written 712 bytes
    ---
    New, TLSv1/SSLv3, Cipher is AES256-SHA
    Server public key is 4096 bit
    Secure Renegotiation IS supported
    Compression: NONE
    Expansion: NONE
    SSL-Session:
        Protocol  : TLSv1
        Cipher    : AES256-SHA
        Session-ID: A1A8BF35549C5715648A12FD7B7E3D861539316B03440187D9DA6C2E48822853
        Session-ID-ctx: 
        Master-Key: F39D1B12274BA16D3A906F390A61438221E381952E9E1E05D3DD784F0135FB81353DA38C6D5C021CB926E844DFC49FC4
        Key-Arg   : None
        Start Time: 1481685096
        Timeout   : 300 (sec)
        Verify return code: 0 (ok)
    ```

6.  运行完此例后进行清理，移除 `nginx` 服务和存储的机密。

    ```console
    $ docker service rm nginx

    $ docker secret rm site.crt site.key site.conf
    ```

### 高级示例：在 WordPress 服务中使用机密

在此示例中，您将创建一个带有自定义 root 密码的单节点 MySQL 服务，将凭据添加为机密，并创建一个使用这些凭据连接到 MySQL 的单节点 WordPress 服务。 [下一个示例](#example-rotate-a-secret) 在本例基础上进行扩展，向您展示如何轮换 MySQL 密码并更新服务，以便 WordPress 服务仍能连接到 MySQL。

此示例说明了一些使用 Docker 机密的技巧，以避免在镜像中保存敏感凭据或在命令行中直接传递它们。

> [!NOTE]
> 
> 为简单起见，本例使用单引擎 Swarm，并使用单节点 MySQL 服务，因为单实例 MySQL 服务器无法通过简单的扩展服务来扩展，且设置 MySQL 集群超出了本例范围。
> 
> 此外，更改 MySQL 的 root 口令不像更改磁盘上的文件那么简单。您必须使用查询或 `mysqladmin` 命令在 MySQL 中更改密码。 

1.  为 MySQL 生成一个随机的字母数字密码，并使用 `docker secret create` 命令将其存储为名为 `mysql_password` 的 Docker 机密。要更改密码长度，请调整 `openssl` 命令的最后一个参数。这只是创建相对随机密码的一种方式。您可以根据需要选择其他命令来生成密码。

    > [!NOTE]
    > 
    > 机密创建后无法更新。您只能移除并重新创建它，且无法移除正在被服务使用的机密。但是，您可以使用 `docker service update` 授予或撤销运行中服务访问机密的权限。如果您需要更新机密的能力，请考虑在机密名称中添加版本组件，以便稍后添加新版本、更新服务以使用新版本，然后移除旧版本。

    最后一个参数设置为 `-`，表示从标准输入读取输入。

    ```console
    $ openssl rand -base64 20 | docker secret create mysql_password -

    l1vinzevzhj4goakjap5ya409
    ```

    返回的值不是密码，而是机密的 ID。在后续教程中，ID 输出将被省略。

    为 MySQL `root` 用户生成第二个机密。此机密不会共享给稍后创建的 WordPress 服务。它仅用于引导 `mysql` 服务。

    ```console
    $ openssl rand -base64 20 | docker secret create mysql_root_password -
    ```

    使用 `docker secret ls` 列出由 Docker 管理的机密：

    ```console
    $ docker secret ls

    ID                          NAME                  CREATED             UPDATED
    l1vinzevzhj4goakjap5ya409   mysql_password        41 seconds ago      41 seconds ago
    yvsczlx9votfw3l0nz5rlidig   mysql_root_password   12 seconds ago      12 seconds ago
    ```

    机密存储在 Swarm 加密的 Raft 日志中。

2.  创建一个用户定义的 overlay 网络，用于 MySQL 和 WordPress 服务之间的通信。无需将 MySQL 服务暴露给任何外部主机或容器。

    ```console
    $ docker network create -d overlay mysql_private
    ```

3.  创建 MySQL 服务。MySQL 服务具有以下特征：

    - 副本数设置为 `1`，因此只运行单个 MySQL 任务。
    - 仅在该 `mysql_private` 网络上的其他容器可访问。
    - 使用卷 `mydata` 存储 MySQL 数据，以便在 `mysql` 服务重启后数据仍能持久存在。
    - 机密各自挂载在 `/run/secrets/mysql_password` 和 `/run/secrets/mysql_root_password` 的 `tmpfs` 文件系统中。它们永远不会以环境变量的形式暴露，也不会在运行 `docker commit` 命令时提交到镜像中。`mysql_password` 机密是供非特权 WordPress 容器连接 MySQL 时使用的。
    - 设置环境变量 `MYSQL_PASSWORD_FILE` 和 `MYSQL_ROOT_PASSWORD_FILE` 以指向文件 `/run/secrets/mysql_password` 和 `/run/secrets/mysql_root_password`。`mysql` 镜像在首次初始化系统数据库时会从这些文件中读取密码字符串。之后，密码将存储在 MySQL 系统数据库本身中。
    - 设置环境变量 `MYSQL_USER` 和 `MYSQL_DATABASE`。当容器启动时，会创建一个名为 `wordpress` 的新数据库，且 `wordpress` 用户仅对此数据库拥有完整权限。该用户无法创建或删除数据库，也无法更改 MySQL 配置。

      ```console
      $ docker service create \
           --name mysql \
           --replicas 1 \
           --network mysql_private \
           --mount type=volume,source=mydata,destination=/var/lib/mysql \
           --secret source=mysql_root_password,target=mysql_root_password \
           --secret source=mysql_password,target=mysql_password \
           -e MYSQL_ROOT_PASSWORD_FILE="/run/secrets/mysql_root_password" \
           -e MYSQL_PASSWORD_FILE="/run/secrets/mysql_password" \
           -e MYSQL_USER="wordpress" \
           -e MYSQL_DATABASE="wordpress" \
           mysql:latest
      ```

4.  使用 `docker service ls` 命令验证 `mysql` 容器是否正在运行。

    ```console
    $ docker service ls

    ID            NAME   MODE        REPLICAS  IMAGE
    wvnh0siktqr3  mysql  replicated  1/1       mysql:latest
    ```

5.  MySQL 设置好后，创建一个连接到 MySQL 服务的 WordPress 服务。WordPress 服务具有以下特征：

    - 副本数设置为 `1`，因此只运行单个 WordPress 任务。由于在容器文件系统中存储 WordPress 会话数据的限制，负载均衡 WordPress 的练习留给读者。
    - 在主机机器的 30000 端口上暴露 WordPress，以便您可以从外部主机访问它。如果您的主机机器 80 端口上没有运行 Web 服务器，您可以改为暴露 80 端口。
    - 连接到 `mysql_private` 网络以便与 `mysql` 容器通信，同时在所有 Swarm 节点上将 80 端口发布到 30000 端口。
    - 有权访问 `mysql_password` 机密，但指定了容器内的不同目标文件名。WordPress 容器使用挂载点 `/run/secrets/wp_db_password`。
    - 设置环境变量 `WORDPRESS_DB_PASSWORD_FILE` 指向机密挂载的文件路径。WordPress 服务将从该文件中读取 MySQL 密码字符串并将其添加到 `wp-config.php` 配置文件中。
    - 使用用户名 `wordpress` 和 `/run/secrets/wp_db_password` 中的密码连接到 MySQL 容器，并在 `wordpress` 数据库不存在时创建它。
    - 将其数据 (如主题和插件) 存储在名为 `wpdata` 的卷中，以便这些文件在服务重启时持久存在。

    ```console
    $ docker service create \
         --name wordpress \
         --replicas 1 \
         --network mysql_private \
         --publish published=30000,target=80 \
         --mount type=volume,source=wpdata,destination=/var/www/html \
         --secret source=mysql_password,target=wp_db_password \
         -e WORDPRESS_DB_USER="wordpress" \
         -e WORDPRESS_DB_PASSWORD_FILE="/run/secrets/wp_db_password" \
         -e WORDPRESS_DB_HOST="mysql:3306" \
         -e WORDPRESS_DB_NAME="wordpress" \
         wordpress:latest
    ```

6.  使用 `docker service ls` 和 `docker service ps` 命令验证服务是否正在运行。

    ```console
    $ docker service ls

    ID            NAME       MODE        REPLICAS  IMAGE
    wvnh0siktqr3  mysql      replicated  1/1       mysql:latest
    nzt5xzae4n62  wordpress  replicated  1/1       wordpress:latest
    ```

    ```console
    $ docker service ps wordpress

    ID            NAME         IMAGE             NODE  DESIRED STATE  CURRENT STATE           ERROR  PORTS
    aukx6hgs9gwc  wordpress.1  wordpress:latest  moby  Running        Running 52 seconds ago   
    ```

    此时，您实际上可以撤销 WordPress 服务对 `mysql_password` 机密的访问权限，因为 WordPress 已将该机密复制到了其配置文件 `wp-config.php` 中。目前暂不执行此操作，因为我们稍后会用到它来辅助轮换 MySQL 密码。

7.  从任何 Swarm 节点访问 `http://localhost:30000/` 并使用基于 Web 的向导设置 WordPress。所有这些设置都存储在 MySQL 的 `wordpress` 数据库中。WordPress 会自动为您的 WordPress 用户生成一个密码，这与 WordPress 用来访问 MySQL 的密码完全不同。请妥善保存此密码 (例如保存在密码管理器中)。在 [轮换机密](#example-rotate-a-secret) 后，您需要用它登录 WordPress。

    可以尝试撰写一两篇博文，并安装 WordPress 插件或主题，以验证 WordPress 是否正常运行及其状态是否在服务重启后得以保存。

8.  如果您打算继续执行下一个示例 (演示如何轮换 MySQL root 密码)，请不要清理任何服务或机密。

### 示例：轮换机密 (Rotate a secret)

本示例建立在前一个示例的基础上。在这种情况下，您创建一个带有新 MySQL 密码的新机密，更新 `mysql` 和 `wordpress` 服务以使用该机密，然后移除旧机密。

> [!NOTE]
> 
> 更改 MySQL 数据库的密码涉及运行额外的查询或命令，而不只是更改单个环境变量或文件，因为该镜像仅在数据库尚不存在时才会设置 MySQL 密码，且 MySQL 默认在数据库内部存储密码。轮换密码或其他机密可能涉及 Docker 之外的额外步骤。

1.  创建新密码并将其存储为名为 `mysql_password_v2` 的机密。

    ```console
    $ openssl rand -base64 20 | docker secret create mysql_password_v2 -
    ```

2.  更新 MySQL 服务，使其同时拥有对旧机密和新机密的访问权限。请记住，您无法更新或重命名机密，但可以撤销机密并使用新的目标文件名重新授予访问权限。

    ```console
    $ docker service update \
         --secret-rm mysql_password mysql

    $ docker service update \
         --secret-add source=mysql_password,target=old_mysql_password \
         --secret-add source=mysql_password_v2,target=mysql_password \
         mysql
    ```

    更新服务会导致其重启，当 MySQL 服务第二次重启时，它可以访问 `/run/secrets/old_mysql_password` 下的旧机密和 `/run/secrets/mysql_password` 下的新机密。

    尽管 MySQL 服务现在已经有了旧机密和新机密，但 `wordpress` 用户的 MySQL 密码尚未更改。

    > [!NOTE]
    > 
    > 本例不轮换 MySQL 的 `root` 密码。

3.  现在，使用 `mysqladmin` CLI 更改 `wordpress` 用户的 MySQL 密码。此命令从 `/run/secrets` 中的文件读取旧密码和新密码，但不会在命令行中暴露它们，也不会将其保存在 shell 历史记录中。

    请迅速执行此操作并进入下一步，因为此时 WordPress 将失去连接 MySQL 的能力。

    首先，找到 `mysql` 容器任务的 ID。

    ```console
    $ docker ps --filter name=mysql -q

    c7705cf6176f
    ```

    在下面的命令中替换 ID，或者使用第二种变体，它利用 shell 扩展一步完成。

    ```console
    $ docker container exec <CONTAINER_ID> \
        bash -c 'mysqladmin --user=wordpress --password="$(< /run/secrets/old_mysql_password)" password "$(< /run/secrets/mysql_password)"'
    ```

    或者：

    ```console
    $ docker container exec $(docker ps --filter name=mysql -q) \
        bash -c 'mysqladmin --user=wordpress --password="$(< /run/secrets/old_mysql_password)" password "$(< /run/secrets/mysql_password)"'
    ```

4.  更新 `wordpress` 服务以使用新密码，同时保持目标路径为 `/run/secrets/wp_db_password`。这将触发 WordPress 服务的滚动重启，并开始使用新机密。

    ```console
    $ docker service update \
         --secret-rm mysql_password \
         --secret-add source=mysql_password_v2,target=wp_db_password \
         wordpress    
    ```

5.  再次通过任何 Swarm 节点浏览 http://localhost:30000/ 来验证 WordPress 是否正常工作。使用您在之前任务中通过 WordPress 向导设置的用户名和密码。

    验证您撰写的博文是否仍然存在，如果您更改了任何配置值，也请验证它们是否仍保持更改后的状态。

6.  从 MySQL 服务中撤销对旧机密的访问权限，并从 Docker 中删除该旧机密。

    ```console
    $ docker service update \
         --secret-rm mysql_password \
         mysql

    $ docker secret rm mysql_password
    ```


7.  运行以下命令移除 WordPress 服务、MySQL 容器、`mydata` 和 `wpdata` 卷以及 Docker 机密：

    ```console
    $ docker service rm wordpress mysql

    $ docker volume rm mydata wpdata

    $ docker secret rm mysql_password_v2 mysql_root_password
    ```

## 在您的镜像中构建对 Docker 机密的支持

如果您开发的容器可以作为服务部署，且需要将敏感数据 (如凭据) 作为环境变量，请考虑调整您的镜像以利用 Docker 机密。实现此目标的一种方法是确保您在创建容器时传递给镜像的每个参数也可以从文件中读取。

许多 [Docker 官方镜像](https://github.com/docker-library/) 已通过这种方式进行了更新，例如上述示例中使用的 [wordpress](https://github.com/docker-library/wordpress/) 镜像。

当您启动 WordPress 容器时，您通过将参数设置为环境变量来提供其所需的参数。WordPress 镜像已更新，因此包含 WordPress 重要数据的环境变量 (如 `WORDPRESS_DB_PASSWORD`) 也具有可以从文件读取其值的变体 (`WORDPRESS_DB_PASSWORD_FILE`)。此策略确保了向后兼容性，同时允许您的容器从 Docker 管理的机密中读取信息，而不是直接传递。

> [!NOTE]
> 
> Docker 机密不会直接设置环境变量。这是一个刻意的决定，因为环境变量可能会在容器之间无意中泄露 (例如，如果您使用 `--link`)。

## 在 Compose 中使用机密

```yaml

services:
   db:
     image: mysql:latest
     volumes:
       - db_data:/var/lib/mysql
     environment:
       MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_root_password
       - db_password

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_password


secrets:
   db_password:
     file: db_password.txt
   db_root_password:
     file: db_root_password.txt

volumes:
    db_data:
```

此示例使用 Compose 文件中的两个机密创建了一个简单的 WordPress 站点。

顶级元素 `secrets` 定义了两个机密：`db_password` 和 `db_root_password`。

部署时，Docker 会创建这两个机密，并使用 Compose 文件中指定的文件内容对其进行填充。

`db` 服务使用了两个机密，而 `wordpress` 使用了一个。

当您部署时，Docker 会在服务中的 `/run/secrets/<secret_name>` 下挂载一个文件。这些文件永远不会持久化在磁盘上，而是在内存中管理的。

每个服务都使用环境变量来指定服务应该去哪里寻找这些机密数据。

有关机密简写和详写语法的更多信息，可以在 [Compose 规范](/reference/compose-file/secrets.md) 中找到。

```
