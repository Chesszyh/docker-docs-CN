--- 
title: 使用 Docker Configs 存储配置数据
description: 了解如何将配置数据与运行时分离存储
keywords: swarm, configuration, configs, 配置
---

## 关于 Configs

Docker Swarm 服务配置 (Configs) 允许您在服务镜像或运行中的容器之外存储非敏感信息，如配置文件。这使您能够保持镜像尽可能通用，而无需将配置文件绑定挂载到容器中或使用环境变量。

Configs 的操作方式与 [机密 (Secrets)](secrets.md) 类似，不同之处在于它们在静态存储时不加密，并且直接挂载到容器的文件系统中，而不使用 RAM 磁盘。可以随时在服务中添加或删除 Configs，且多个服务可以共享同一个 Config。您甚至可以将 Configs 与环境变量或标签结合使用，以获得最大的灵活性。Config 的值可以是通用字符串或二进制内容 (大小最多 500 KB)。

> [!NOTE]
> 
> Docker Configs 仅对 Swarm 服务可用，对独立容器不可用。要使用此特性，请考虑将您的容器调整为以副本数为 1 的服务运行。

Configs 在 Linux 和 Windows 服务上均受支持。

### Windows 支持

Docker 包含对 Windows 容器上的 Configs 的支持，但在实现上存在一些差异，下文的示例中会有所说明。请记住以下显著区别：

- 具有自定义目标的配置文件不会直接绑定挂载到 Windows 容器中，因为 Windows 不支持非目录文件的绑定挂载。相反，容器的所有 Configs 都挂载在容器内的 `C:\ProgramData\Docker\internal\configs` (这是一个实现细节，应用程序不应依赖它)。符号链接用于从该位置指向容器内 Config 的目标位置。默认目标是 `C:\ProgramData\Docker\configs`。

- 创建使用 Windows 容器的服务时，Configs 不支持指定 UID、GID 和权限模式 (mode) 的选项。目前，Configs 仅供容器内的管理员和具有 `system` 访问权限的用户访问。

- 在 Windows 上，使用 `--credential-spec` 配合 `config://<config-name>` 格式来创建或更新服务。这会在容器启动前将 gMSA 凭据文件直接传递给节点。工作节点上不会将任何 gMSA 凭据写入磁盘。更多信息请参考 [将服务部署到 Swarm](services.md#gmsa-for-swarm)。

## Docker 如何管理 Configs

当您向 Swarm 添加 Config 时，Docker 会通过双向 TLS 连接将 Config 发送给 Swarm 管理节点。Config 存储在经过加密的 Raft 日志中。整个 Raft 日志会在其他管理节点之间进行复制，从而确保 Configs 与 Swarm 其他管理数据具有相同的高可用性保证。

当您授予新建或运行中的服务访问 Config 的权限时，该 Config 会以文件形式挂载到容器中。在 Linux 容器中，挂载点在容器内的默认位置是 `/<config-name>`。在 Windows 容器中，Configs 全部挂载到 `C:\ProgramData\Docker\configs` 中，并会为所需位置创建符号链接，默认位置为 `C:\<config-name>`。

您可以使用数字 ID 或用户/组的名称来设置 Config 的所有权 (`uid` 和 `gid`)。您还可以指定文件权限 (`mode`)。这些设置在 Windows 容器中会被忽略。

- 如果未设置，Config 归运行容器命令的用户 (通常是 `root`) 及其默认组 (通常也是 `root`) 所有。
- 如果未设置，Config 具有所有人可读的权限 (模式 `0444`)，除非容器内设置了 `umask`，在这种情况下，模式会受到该 `umask` 值的影响。

您可以随时更新服务，以授予其访问额外 Configs 的权限，或撤销其对给定 Config 的访问权限。

只有当节点是 Swarm 管理节点，或者节点正在运行已被授予访问 Config 权限的服务任务时，该节点才有权访问该 Config。当容器任务停止运行时，共享给它的 Configs 会从该容器的内存文件系统中卸载，并从节点的内存中清除。

如果节点在运行具有 Config 访问权限的任务容器时失去了与 Swarm 的连接，该任务容器仍可访问其 Configs，但在节点重新连接到 Swarm 之前无法接收更新。

您可以随时添加或检查单个 Config，或列出所有 Configs。您不能删除正在运行的服务正在使用的 Config。参见 [轮换 Config](configs.md#example-rotate-a-config)，了解在不中断运行中服务的情况下删除 Config 的方法。

为了更容易地更新或回滚 Configs，请考虑在 Config 名称中添加版本号或日期。由于可以控制 Config 在给定容器内的挂载点，这一点变得更加容易。

要更新 stack (栈)，请更改 Compose 文件，然后重新运行 `docker stack deploy -c <new-compose-file> <stack-name>`。如果您在该文件中使用了新的 Config，您的服务就会开始使用它。请记住，配置是不可变的，因此您不能更改现有服务的文件。相反，您需要创建一个新 Config 以使用不同的文件。

您可以运行 `docker stack rm` 来停止应用并撤销整个 stack。这将删除所有由 `docker stack deploy` 使用该 stack 名称创建的 Config。这将删除 *所有* Configs，包括那些未被服务引用的 Configs，以及在执行 `docker service update --config-rm` 后剩余的 Configs。

## 阅读更多关于 `docker config` 命令的信息

使用以下链接阅读有关特定命令的信息，或者继续查看 [在服务中使用 Configs 的示例](#advanced-example-use-configs-with-a-nginx-service)。

- [`docker config create`](/reference/cli/docker/config/create.md)
- [`docker config inspect`](/reference/cli/docker/config/inspect.md)
- [`docker config ls`](/reference/cli/docker/config/ls.md)
- [`docker config rm`](/reference/cli/docker/config/rm.md)

## 示例

本节包含一些由浅入深的示例，说明了如何使用 Docker Configs。

> [!NOTE]
> 
> 为简单起见，这些示例使用单引擎 Swarm 和未进行扩展的服务。示例使用 Linux 容器，但 Windows 容器也支持 Configs。

### 在 Compose 文件中定义和使用 Configs

`docker stack` 命令支持在 Compose 文件中定义 Configs。然而，`docker compose` 不支持 `configs` 键。详情请参阅 [Compose 文件参考](/reference/compose-file/legacy-versions.md)。

### 简单示例：Config 入门

这个简单的示例展示了仅通过几个命令 Configs 是如何工作的。有关更实际的示例，请继续查看 [高级示例：在 Nginx 服务中使用 Configs](#advanced-example-use-configs-with-a-nginx-service)。

1.  向 Docker 添加一个 Config。`docker config create` 命令读取标准输入，因为代表读取 Config 来源文件的最后一个参数被设置为 `-`。

    ```console
    $ echo "This is a config" | docker config create my-config -
    ```

2.  创建一个 `redis` 服务并授予其访问该 Config 的权限。默认情况下，容器可以在 `/my-config` 处访问该 Config，但您可以使用 `target` 选项自定义容器上的文件名。

    ```console
    $ docker service create --name redis --config my-config redis:alpine
    ```

3.  使用 `docker service ps` 验证任务是否运行正常。如果一切正常，输出类似于以下内容：

    ```console
    $ docker service ps redis

    ID            NAME       IMAGE         NODE              DESIRED STATE  CURRENT STATE          ERROR  PORTS
    bkna6bpn8r1a  redis.1    redis:alpine  ip-172-31-46-109  Running        Running 8 seconds ago
    ```

4.  使用 `docker ps` 获取 `redis` 服务任务容器的 ID，以便您可以使用 `docker container exec` 连接到容器并读取 Config 数据文件的内容。该文件默认对所有人可读，且名称与 Config 名称相同。下面的第一个命令说明如何查找容器 ID，第二和第三个命令使用 shell 补全自动执行此操作。

    ```console
    $ docker ps --filter name=redis -q

    5cb1c2348a59

    $ docker container exec $(docker ps --filter name=redis -q) ls -l /my-config

    -r--r--r--    1 root     root            12 Jun  5 20:49 my-config

    $ docker container exec $(docker ps --filter name=redis -q) cat /my-config

    This is a config
    ```

5.  尝试删除该 Config。删除失败，因为 `redis` 服务正在运行且有权访问该 Config。

    ```console

    $ docker config ls

    ID                          NAME                CREATED             UPDATED
    fzwcfuqjkvo5foqu7ts7ls578   hello               31 minutes ago      31 minutes ago


    $ docker config rm my-config

    Error response from daemon: rpc error: code = 3 desc = config 'my-config' is
    in use by the following service: redis
    ```

6.  通过更新服务，从运行中的 `redis` 服务中移除对该 Config 的访问权限。

    ```console
    $ docker service update --config-rm my-config redis
    ```

7.  再次重复步骤 3 和 4，验证服务不再具有对该 Config 的访问权限。容器 ID 会不同，因为 `service update` 命令会重新部署服务。

    ```none
    $ docker container exec -it $(docker ps --filter name=redis -q) cat /my-config

    cat: can't open '/my-config': No such file or directory
    ```

8.  停止并移除该服务，并从 Docker 中删除该 Config。

    ```console
    $ docker service rm redis

    $ docker config rm my-config
    ```

### 简单示例：在 Windows 服务中使用 Configs

这是一个非常简单的示例，展示了如何在运行 Windows 容器的 Docker for Windows 上的 Microsoft IIS 服务中使用 Configs。这是一个简单的示例，它将网页存储在 Config 中。

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

    ```powershell
    docker swarm init
    ```

3.  将 `index.html` 文件保存为名为 `homepage` 的 Swarm Config。

    ```powershell
    docker config create homepage index.html
    ```

4.  创建一个 IIS 服务并授予其访问 `homepage` Config 的权限。

    ```powershell
    docker service create
        --name my-iis
        --publish published=8000,target=8000
        --config src=homepage,target="\inetpub\wwwroot\index.html"
        microsoft/iis:nanoserver
    ```

5.  访问位于 `http://localhost:8000/` 的 IIS 服务。它应该提供第一步中的 HTML 内容。

6.  移除服务和 Config。

    ```powershell
    docker service rm my-iis

    docker config rm homepage
    ```

### 示例：使用模板化 Config

要创建一个内容将使用模板引擎生成的配置，请使用 `--template-driver` 参数并指定引擎名称作为其参数。模板将在创建容器时进行渲染。

1.  将以下内容保存到新文件 `index.html.tmpl` 中。

    ```html
    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello {{ env "HELLO" }}! I'm service {{ .Service.Name }}.</p>
      </body>
    </html>
    ```

2.  将 `index.html.tmpl` 文件保存为名为 `homepage` 的 Swarm Config。提供参数 `--template-driver` 并指定 `golang` 作为模板引擎。

    ```console
    $ docker config create --template-driver golang homepage index.html.tmpl
    ```

3.  创建一个运行 Nginx 的服务，该服务可以访问环境变量 HELLO 且有权访问该 Config。

    ```console
    $ docker service create \
         --name hello-template \
         --env HELLO="Docker" \
         --config source=homepage,target=/usr/share/nginx/html/index.html \
         --publish published=3000,target=80 \
         nginx:alpine
    ```

4.  验证服务是否正常运行：您可以访问 Nginx 服务器，并确认提供了正确的输出。

    ```console
    $ curl http://0.0.0.0:3000

    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello Docker! I'm service hello-template.</p>
      </body>
    </html>
    ```

### 高级示例：在 Nginx 服务中使用 Configs

此示例分为两部分。[第一部分](#generate-the-site-certificate) 主要是关于生成站点证书，并不直接涉及 Docker Configs，但它为 [第二部分](#configure-the-nginx-container) 做了准备，在第二部分中，您将站点证书作为一系列机密 (Secrets) 进行存储和使用，并将 Nginx 配置作为 Config 进行存储。该示例展示了如何在 Config 上设置选项，例如容器内的目标位置和文件权限 (`mode`)。

#### 生成站点证书

为您网站生成根 CA 以及 TLS 证书和密钥。对于生产站点，您可能希望使用 `Let’s Encrypt` 等服务来生成 TLS 证书和密钥，但此示例使用命令行工具。这一步有点复杂，但只是一个设置步骤，目的是为了让您有东西可以作为 Docker Secret 存储。如果您想跳过这些子步骤，可以 [使用 Let's Encrypt](https://letsencrypt.org/getting-started/) 生成站点密钥和证书，将文件命名为 `site.key` 和 `site.crt`，然后直接跳到 [配置 Nginx 容器](#configure-the-nginx-container)。

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

    ```none
    [root_ca]
    basicConstraints = critical,CA:TRUE,pathlen:1
    keyUsage = critical, nonRepudiation, cRLSign, keyCertSign
    subjectKeyIdentifier=hash
    ```

4.  对证书进行签名。

    ```console
    $ openssl x509 -req -days 3650 -in "root-ca.csr" \
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

    ```none
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
        -CA "root-ca.crt" -CAkey "root-ca.key" -CAcreateserial \
        -out "site.crt" -extfile "site.cnf" -extensions server
    ```

9.  Nginx 服务不需要 `site.csr` 和 `site.cnf` 文件，但如果您想生成新的站点证书，则需要它们。请保护好 `root-ca.key` 文件。

#### 配置 Nginx 容器

1.  生成一个非常基础的 Nginx 配置，通过 HTTPS 提供静态文件。TLS 证书和密钥存储为 Docker Secrets，以便于轮换。

    在当前目录下，创建一个名为 `site.conf` 的新文件，内容如下：

    ```none
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

2.  创建两个机密 (Secrets)，分别代表密钥和证书。只要文件小于 500 KB，您就可以将其存储为 Secret。这允许您将密钥和证书与使用它们的服务解耦。在这些示例中，Secret 名称和文件名是相同的。

    ```console
    $ docker secret create site.key site.key

    $ docker secret create site.crt site.crt
    ```

3.  将 `site.conf` 文件保存到 Docker Config 中。第一个参数是 Config 的名称，第二个参数是读取它的来源文件。

    ```console
    $ docker config create site.conf site.conf
    ```

    列出 Configs：

    ```console
    $ docker config ls

    ID                          NAME                CREATED             UPDATED
    4ory233120ccg7biwvy11gl5z   site.conf           4 seconds ago       4 seconds ago
    ```


4.  创建一个运行 Nginx 的服务，并授予其访问两个机密和一个配置的权限。将模式设置为 `0440`，以便该文件仅对其所有者和该所有者的组可读，而不是所有人可读。

    ```console
    $ docker service create \
         --name nginx \
         --secret site.key \
         --secret site.crt \
         --config source=site.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
         nginx:latest \
         sh -c "exec nginx -g 'daemon off;'"
    ```

    在运行中的容器内，现在存在以下三个文件：

    - `/run/secrets/site.key`
    - `/run/secrets/site.crt`
    - `/etc/nginx/conf.d/site.conf`

5.  验证 Nginx 服务是否正在运行。

    ```console
    $ docker service ls

    ID            NAME   MODE        REPLICAS  IMAGE
    zeskcec62q24  nginx  replicated  1/1       nginx:latest

    $ docker service ps nginx

    NAME                  IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR  PORTS
    nginx.1.9ls3yo9ugcls  nginx:latest  moby  Running        Running 3 minutes ago
    ```

6.  验证服务是否正常运行：您可以访问 Nginx 服务器，并确认正在使用正确的 TLS 证书。

    ```console
    $ curl --cacert root-ca.crt https://0.0.0.0:3000

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

    <p>For online documentation and support, refer to
    <a href="https://nginx.org">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="https://www.nginx.com">www.nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```

    ```console
    $ openssl s_client -connect 0.0.0.0:3000 -CAfile root-ca.crt

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
    ...
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

7.  除非您打算继续下一个示例，否则在运行此示例后进行清理：移除 `nginx` 服务以及存储的机密和配置。

    ```console
    $ docker service rm nginx

    $ docker secret rm site.crt site.key

    $ docker config rm site.conf
    ```

现在您已经配置了一个 Nginx 服务，其配置与其镜像解耦。您可以运行具有完全相同镜像但配置不同的多个站点，而完全不需要构建自定义镜像。

### 示例：轮换 Config

要轮换 Config，首先保存一个与当前正在使用的 Config 名称不同的新 Config。然后重新部署该服务，移除旧 Config 并将新 Config 添加到容器内的同一个挂载点。本示例在前面的基础上，通过轮换 `site.conf` 配置文件进行演示。

1.  在本地编辑 `site.conf` 文件。在 `index` 行添加 `index.php`，然后保存文件。

    ```none
    server {
        listen                443 ssl;
        server_name           localhost;
        ssl_certificate       /run/secrets/site.crt;
        ssl_certificate_key   /run/secrets/site.key;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm index.php;
        }
    }
    ```

2.  使用新的 `site.conf` 创建一个新的 Docker Config，命名为 `site-v2.conf`。

    ```bah
    $ docker config create site-v2.conf site.conf
    ```

3.  更新 `nginx` 服务以使用新配置而不是旧配置。

    ```console
    $ docker service update \
      --config-rm site.conf \
      --config-add source=site-v2.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
      nginx
    ```

4.  使用 `docker service ps nginx` 验证 `nginx` 服务是否已完全重新部署。完成后，您可以删除旧的 `site.conf` 配置。

    ```console
    $ docker config rm site.conf
    ```

5.  要进行清理，您可以移除 `nginx` 服务，以及相关的机密和配置。

    ```console
    $ docker service rm nginx

    $ docker secret rm site.crt site.key

    $ docker config rm site-v2.conf
    ```

现在您已经更新了 `nginx` 服务的配置，而无需重新构建其镜像。
