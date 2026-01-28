---
title: 使用 Docker Configs 存储配置数据
description: How to store configuration data separate from the runtime
keywords: swarm, configuration, configs
---

## 关于 configs

Docker swarm 服务的 configs 允许您将非敏感信息（如配置文件）存储在服务镜像或运行容器之外。这使您可以保持镜像尽可能通用，而无需将配置文件绑定挂载到容器中或使用环境变量。

Configs 的工作方式与 [secrets](secrets.md) 类似，只是它们不是静态加密的，并且直接挂载到容器的文件系统中，而不使用 RAM 磁盘。Configs 可以随时添加到服务或从服务中移除，服务可以共享 config。您甚至可以将 configs 与环境变量或标签结合使用，以获得最大的灵活性。Config 值可以是通用字符串或二进制内容（大小最多 500 kb）。

> [!NOTE]
>
> Docker configs 仅适用于 swarm 服务，不适用于独立容器。要使用此功能，请考虑将您的容器调整为以规模为 1 的服务运行。

Linux 和 Windows 服务都支持 Configs。

### Windows 支持

Docker 包含对 Windows 容器上 configs 的支持，但实现方面存在差异，这些差异在下面的示例中有所说明。请记住以下显著差异：

- 具有自定义目标的 Config 文件不会直接绑定挂载到 Windows 容器中，因为 Windows 不支持非目录文件绑定挂载。相反，容器的 configs 都挂载在容器内的 `C:\ProgramData\Docker\internal\configs`（这是一个不应被应用程序依赖的实现细节）中。符号链接用于从那里指向容器内 config 的所需目标。默认目标是 `C:\ProgramData\Docker\configs`。

- 当创建使用 Windows 容器的服务时，configs 不支持指定 UID、GID 和 mode 的选项。Configs 目前只能由容器内的管理员和具有 `system` 访问权限的用户访问。

- 在 Windows 上，使用 `config://<config-name>` 格式的 `--credential-spec` 创建或更新服务。这会在容器启动前直接将 gMSA 凭据文件传递给节点。工作节点上不会将 gMSA 凭据写入磁盘。有关更多信息，请参阅[将服务部署到 swarm](services.md#gmsa-for-swarm)。

## Docker 如何管理 configs

当您向 swarm 添加 config 时，Docker 通过双向 TLS 连接将 config 发送到 swarm 管理节点。Config 存储在加密的 Raft 日志中。整个 Raft 日志在其他管理节点之间复制，确保 configs 与 swarm 管理数据的其余部分具有相同的高可用性保证。

当您授予新创建或正在运行的服务对 config 的访问权限时，config 将作为文件挂载到容器中。Linux 容器中挂载点的位置默认为 `/<config-name>`。在 Windows 容器中，configs 都挂载到 `C:\ProgramData\Docker\configs`，并创建符号链接到所需位置，默认为 `C:\<config-name>`。

您可以使用数字 ID 或用户或组的名称设置 config 的所有权（`uid` 和 `gid`）。您还可以指定文件权限（`mode`）。对于 Windows 容器，这些设置会被忽略。

- 如果未设置，config 由运行容器命令的用户（通常是 `root`）和该用户的默认组（通常也是 `root`）拥有。
- 如果未设置，config 具有全局可读权限（mode `0444`），除非在容器内设置了 `umask`，在这种情况下 mode 会受到该 `umask` 值的影响。

您可以随时更新服务以授予其对额外 configs 的访问权限或撤销其对给定 config 的访问权限。

只有当节点是 swarm 管理节点或正在运行已被授予对 config 访问权限的服务任务时，节点才能访问 configs。当容器任务停止运行时，共享给它的 configs 会从该容器的内存文件系统中卸载并从节点的内存中刷新。

如果节点在运行具有 config 访问权限的任务容器时失去与 swarm 的连接，任务容器仍然可以访问其 configs，但在节点重新连接到 swarm 之前无法接收更新。

您可以随时添加或检查单个 config，或列出所有 configs。您无法移除正在运行的服务正在使用的 config。请参阅[轮换 config](configs.md#example-rotate-a-config) 了解如何在不中断正在运行的服务的情况下移除 config。

为了更轻松地更新或回滚 configs，请考虑在 config 名称中添加版本号或日期。通过控制 config 在给定容器内的挂载点，这变得更加容易。

要更新堆栈，请对 Compose 文件进行更改，然后重新运行 `docker stack deploy -c <new-compose-file> <stack-name>`。如果您在该文件中使用新的 config，您的服务将开始使用它们。请记住，配置是不可变的，因此您无法更改现有服务的文件。相反，您创建一个新的 config 来使用不同的文件。

您可以运行 `docker stack rm` 来停止应用并删除堆栈。这会移除由具有相同堆栈名称的 `docker stack deploy` 创建的任何 config。这会移除_所有_ configs，包括那些未被服务引用的以及在 `docker service update --config-rm` 之后保留的。

## 阅读更多关于 `docker config` 命令的信息

使用这些链接阅读特定命令，或继续查看[关于将 configs 与服务一起使用的示例](#advanced-example-use-configs-with-a-nginx-service)。

- [`docker config create`](/reference/cli/docker/config/create.md)
- [`docker config inspect`](/reference/cli/docker/config/inspect.md)
- [`docker config ls`](/reference/cli/docker/config/ls.md)
- [`docker config rm`](/reference/cli/docker/config/rm.md)

## 示例

本节包含逐步深入的示例，说明如何使用 Docker configs。

> [!NOTE]
>
> 这些示例为了简单起见使用单引擎 swarm 和未扩展的服务。示例使用 Linux 容器，但 Windows 容器也支持 configs。

### 在 compose 文件中定义和使用 configs

`docker stack` 命令支持在 Compose 文件中定义 configs。但是，`docker compose` 不支持 `configs` 键。有关详细信息，请参阅 [Compose 文件参考](/reference/compose-file/legacy-versions.md)。

### 简单示例：开始使用 configs

这个简单的示例展示了 configs 如何仅用几个命令就能工作。有关实际示例，请继续查看[高级示例：将 configs 与 Nginx 服务一起使用](#advanced-example-use-configs-with-a-nginx-service)。

1.  向 Docker 添加一个 config。`docker config create` 命令读取标准输入，因为最后一个参数（表示要从中读取 config 的文件）设置为 `-`。

    ```console
    $ echo "This is a config" | docker config create my-config -
    ```

2.  创建一个 `redis` 服务并授予其对 config 的访问权限。默认情况下，容器可以在 `/my-config` 访问 config，但您可以使用 `target` 选项自定义容器上的文件名。

    ```console
    $ docker service create --name redis --config my-config redis:alpine
    ```

3.  使用 `docker service ps` 验证任务正在运行且没有问题。如果一切正常，输出类似于：

    ```console
    $ docker service ps redis

    ID            NAME     IMAGE         NODE              DESIRED STATE  CURRENT STATE          ERROR  PORTS
    bkna6bpn8r1a  redis.1  redis:alpine  ip-172-31-46-109  Running        Running 8 seconds ago
    ```

4.  使用 `docker ps` 获取 `redis` 服务任务容器的 ID，以便您可以使用 `docker container exec` 连接到容器并读取 config 数据文件的内容，该文件默认对所有人可读，并且与 config 的名称相同。下面的第一个命令说明了如何找到容器 ID，第二个和第三个命令使用 shell 自动补全来完成此操作。

    ```console
    $ docker ps --filter name=redis -q

    5cb1c2348a59

    $ docker container exec $(docker ps --filter name=redis -q) ls -l /my-config

    -r--r--r--    1 root     root            12 Jun  5 20:49 my-config

    $ docker container exec $(docker ps --filter name=redis -q) cat /my-config

    This is a config
    ```

5.  尝试移除 config。移除失败，因为 `redis` 服务正在运行并且可以访问该 config。

    ```console

    $ docker config ls

    ID                          NAME                CREATED             UPDATED
    fzwcfuqjkvo5foqu7ts7ls578   hello               31 minutes ago      31 minutes ago


    $ docker config rm my-config

    Error response from daemon: rpc error: code = 3 desc = config 'my-config' is
    in use by the following service: redis
    ```

6.  通过更新服务从正在运行的 `redis` 服务中移除对 config 的访问权限。

    ```console
    $ docker service update --config-rm my-config redis
    ```

7.  再次重复步骤 3 和 4，验证服务不再可以访问该 config。容器 ID 不同，因为 `service update` 命令重新部署了服务。

    ```none
    $ docker container exec -it $(docker ps --filter name=redis -q) cat /my-config

    cat: can't open '/my-config': No such file or directory
    ```

8.  停止并移除服务，并从 Docker 中移除 config。

    ```console
    $ docker service rm redis

    $ docker config rm my-config
    ```

### 简单示例：在 Windows 服务中使用 configs

这是一个非常简单的示例，展示了如何在 Docker for Windows 上运行 Windows 容器的 Microsoft IIS 服务中使用 configs。这是一个将网页存储在 config 中的简单示例。

此示例假设您已安装 PowerShell。

1.  将以下内容保存到名为 `index.html` 的新文件中。

    ```html
    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello Docker! You have deployed a HTML page.</p>
      </body>
    </html>
    ```

2.  如果您还没有这样做，请初始化或加入 swarm。

    ```powershell
    docker swarm init
    ```

3.  将 `index.html` 文件保存为名为 `homepage` 的 swarm config。

    ```powershell
    docker config create homepage index.html
    ```

4.  创建一个 IIS 服务并授予其对 `homepage` config 的访问权限。

    ```powershell
    docker service create
        --name my-iis
        --publish published=8000,target=8000
        --config src=homepage,target="\inetpub\wwwroot\index.html"
        microsoft/iis:nanoserver
    ```

5.  在 `http://localhost:8000/` 访问 IIS 服务。它应该提供第一步中的 HTML 内容。

6.  移除服务和 config。

    ```powershell
    docker service rm my-iis

    docker config rm homepage
    ```

### 示例：使用模板化 config

要创建内容将使用模板引擎生成的配置，请使用 `--template-driver` 参数并将引擎名称指定为其参数。模板将在创建容器时渲染。

1.  将以下内容保存到名为 `index.html.tmpl` 的新文件中。

    ```html
    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello {{ env "HELLO" }}! I'm service {{ .Service.Name }}.</p>
      </body>
    </html>
    ```

2.  将 `index.html.tmpl` 文件保存为名为 `homepage` 的 swarm config。提供参数 `--template-driver` 并指定 `golang` 作为模板引擎。

    ```console
    $ docker config create --template-driver golang homepage index.html.tmpl
    ```

3.  创建一个运行 Nginx 的服务，该服务可以访问环境变量 HELLO 和 config。

    ```console
    $ docker service create \
         --name hello-template \
         --env HELLO="Docker" \
         --config source=homepage,target=/usr/share/nginx/html/index.html \
         --publish published=3000,target=80 \
         nginx:alpine
    ```

4.  验证服务是否正常运行：您可以访问 Nginx 服务器，并且正在提供正确的输出。

    ```console
    $ curl http://0.0.0.0:3000

    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello Docker! I'm service hello-template.</p>
      </body>
    </html>
    ```

### 高级示例：将 configs 与 Nginx 服务一起使用

此示例分为两部分。[第一部分](#generate-the-site-certificate)完全关于生成站点证书，并不直接涉及 Docker configs，但它为[第二部分](#configure-the-nginx-container)做好准备，在第二部分中，您将站点证书和 Nginx 配置作为一系列 secrets 和 config 存储和使用。该示例展示了如何设置 config 的选项，例如容器内的目标位置和文件权限（`mode`）。

#### 生成站点证书

为您的站点生成根 CA 和 TLS 证书及密钥。对于生产站点，您可能需要使用 `Let's Encrypt` 等服务来生成 TLS 证书和密钥，但此示例使用命令行工具。此步骤有点复杂，但只是一个设置步骤，以便您有东西存储为 Docker secret。如果您想跳过这些子步骤，您可以[使用 Let's Encrypt](https://letsencrypt.org/getting-started/) 生成站点密钥和证书，将文件命名为 `site.key` 和 `site.crt`，然后跳到[配置 Nginx 容器](#configure-the-nginx-container)。

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

3.  配置根 CA。编辑一个名为 `root-ca.cnf` 的新文件，并将以下内容粘贴到其中。这会限制根 CA 只能签署叶证书，而不能签署中间 CA。

    ```none
    [root_ca]
    basicConstraints = critical,CA:TRUE,pathlen:1
    keyUsage = critical, nonRepudiation, cRLSign, keyCertSign
    subjectKeyIdentifier=hash
    ```

4.  签署证书。

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

6.  生成站点证书并使用站点密钥签名。

    ```console
    $ openssl req -new -key "site.key" -out "site.csr" -sha256 \
              -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost'
    ```

7.  配置站点证书。编辑一个名为 `site.cnf` 的新文件，并将以下内容粘贴到其中。这会限制站点证书，使其只能用于验证服务器，而不能用于签署证书。

    ```none
    [server]
    authorityKeyIdentifier=keyid,issuer
    basicConstraints = critical,CA:FALSE
    extendedKeyUsage=serverAuth
    keyUsage = critical, digitalSignature, keyEncipherment
    subjectAltName = DNS:localhost, IP:127.0.0.1
    subjectKeyIdentifier=hash
    ```

8.  签署站点证书。

    ```console
    $ openssl x509 -req -days 750 -in "site.csr" -sha256 \
        -CA "root-ca.crt" -CAkey "root-ca.key" -CAcreateserial \
        -out "site.crt" -extfile "site.cnf" -extensions server
    ```

9.  `site.csr` 和 `site.cnf` 文件不是 Nginx 服务所需的，但如果您想生成新的站点证书，则需要它们。保护好 `root-ca.key` 文件。

#### 配置 Nginx 容器

1.  创建一个非常基本的 Nginx 配置，通过 HTTPS 提供静态文件。TLS 证书和密钥存储为 Docker secrets，以便可以轻松轮换。

    在当前目录中，创建一个名为 `site.conf` 的新文件，内容如下：

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

2.  创建两个 secrets，分别代表密钥和证书。您可以将任何小于 500 KB 的文件存储为 secret。这允许您将密钥和证书与使用它们的服务解耦。在这些示例中，secret 名称和文件名相同。

    ```console
    $ docker secret create site.key site.key

    $ docker secret create site.crt site.crt
    ```

3.  将 `site.conf` 文件保存在 Docker config 中。第一个参数是 config 的名称，第二个参数是要从中读取的文件。

    ```console
    $ docker config create site.conf site.conf
    ```

    列出 configs：

    ```console
    $ docker config ls

    ID                          NAME                CREATED             UPDATED
    4ory233120ccg7biwvy11gl5z   site.conf           4 seconds ago       4 seconds ago
    ```


4.  创建一个运行 Nginx 的服务，该服务可以访问两个 secrets 和 config。将 mode 设置为 `0440`，以便文件只能由其所有者和该所有者的组读取，而不是全局可读。

    ```console
    $ docker service create \
         --name nginx \
         --secret site.key \
         --secret site.crt \
         --config source=site.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
         --publish published=3000,target=443 \
         nginx:latest \
         sh -c "exec nginx -g 'daemon off;'"
    ```

    在运行的容器中，现在存在以下三个文件：

    - `/run/secrets/site.key`
    - `/run/secrets/site.crt`
    - `/etc/nginx/conf.d/site.conf`

5.  验证 Nginx 服务正在运行。

    ```console
    $ docker service ls

    ID            NAME   MODE        REPLICAS  IMAGE
    zeskcec62q24  nginx  replicated  1/1       nginx:latest

    $ docker service ps nginx

    NAME                  IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR  PORTS
    nginx.1.9ls3yo9ugcls  nginx:latest  moby  Running        Running 3 minutes ago
    ```

6.  验证服务是否正常运行：您可以访问 Nginx 服务器，并且正在使用正确的 TLS 证书。

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

7.  除非您要继续下一个示例，否则在运行此示例后通过移除 `nginx` 服务以及存储的 secrets 和 config 进行清理。

    ```console
    $ docker service rm nginx

    $ docker secret rm site.crt site.key

    $ docker config rm site.conf
    ```

您现在已经配置了一个 Nginx 服务，其配置与其镜像解耦。您可以使用完全相同的镜像但使用不同的配置来运行多个站点，而无需构建自定义镜像。

### 示例：轮换 config

要轮换 config，首先保存一个与当前使用的 config 名称不同的新 config。然后重新部署服务，移除旧 config 并在容器内的相同挂载点添加新 config。此示例基于前面的示例，通过轮换 `site.conf` 配置文件来说明。

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

2.  使用新的 `site.conf` 创建一个名为 `site-v2.conf` 的新 Docker config。

    ```bah
    $ docker config create site-v2.conf site.conf
    ```

3.  更新 `nginx` 服务以使用新 config 而不是旧 config。

    ```console
    $ docker service update \
      --config-rm site.conf \
      --config-add source=site-v2.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
      nginx
    ```

4.  使用 `docker service ps nginx` 验证 `nginx` 服务是否已完全重新部署。完成后，您可以移除旧的 `site.conf` config。

    ```console
    $ docker config rm site.conf
    ```

5.  要清理，您可以移除 `nginx` 服务，以及 secrets 和 configs。

    ```console
    $ docker service rm nginx

    $ docker secret rm site.crt site.key

    $ docker config rm site-v2.conf
    ```

您现在已经更新了 `nginx` 服务的配置，而无需重建其镜像。
