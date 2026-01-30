---
description: 在内容信托沙箱中实践
keywords: trust, security, root, keys, repository, sandbox, 信任, 安全, 沙箱
title: 在内容信托沙箱中实践
aliases:
- /security/trust/trust_sandbox/
---

本页介绍了如何设置和使用沙箱来实验内容信托。沙箱允许您在本地配置和尝试内容信托操作，而不会影响您的生产镜像。

在开始使用此沙箱之前，您应该已经阅读过 [内容信托概览](index.md)。

## 前提条件

这些说明假设您正在运行 Linux 或 macOS。您可以在本地机器或虚拟机上运行此沙箱。您需要拥有在本地机器或虚拟机中运行 docker 命令的权限。

此沙箱要求您安装两个 Docker 工具：Docker Engine >= 1.10.0 和 Docker Compose >= 1.6.0。要安装 Docker Engine，请从 [受支持平台列表](../../install/_index.md) 中选择。要安装 Docker Compose，请参阅 [此处的详细说明](/manuals/compose/install/_index.md)。

## 沙箱中有什么？

如果您只是开箱即用地使用内容信托，您只需要 Docker Engine 客户端和对 Docker Hub 的访问权限。沙箱模拟了一个生产信任环境，并设置了以下额外组件：

| 容器            | 描述                                                                                                                                 |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| trustsandbox    | 一个包含最新版本 Docker Engine 且预配置了一些证书的容器。这是您的沙箱，您可以在其中使用 `docker` 客户端测试信任操作。 |
| Registry server | 本地注册表服务。                                                                                                                 |
| Notary server   | 处理管理信任所有重活的服务。                                                                               |

这意味着您运行着自己的内容信托 (Notary) 服务器和注册表。如果您只使用 Docker Hub，则不需要这些组件，因为 Docker Hub 已经为您内置了它们。然而，对于沙箱，您将构建自己完整的模拟生产环境。

在 `trustsandbox` 容器中，您将与本地注册表而不是 Docker Hub 交互。这意味着您日常使用的镜像仓库不会被用到，在您实践时它们是受保护的。

在沙箱中实践时，您还将创建根密钥和仓库密钥。沙箱配置为将所有密钥和文件存储在 `trustsandbox` 容器内部。由于您在沙箱中创建的密钥仅供实践使用，销毁容器也会同时销毁这些密钥。

通过为 `trustsandbox` 容器使用 docker-in-docker 镜像，您也不会因为推送和拉取的镜像而污染真实的 Docker 守护进程缓存。镜像存储在附加到此容器的匿名卷中，并可在销毁容器后一并销毁。

## 构建沙箱

在本节中，您使用 Docker Compose 来指定如何设置并将 `trustsandbox` 容器、Notary 服务器和 Registry 服务器连接在一起。


1. 创建一个新的 `trustsandbox` 目录并进入其中。

        $ mkdir trustsandbox
        $ cd trustsandbox

2. 使用您喜欢的编辑器创建一个名为 `compose.yaml` 的文件。例如，使用 vim：

        $ touch compose.yaml
        $ vim compose.yaml

3. 在新文件中添加以下内容：

        version: "2"
        services:
          notaryserver:
            image: dockersecurity/notary_autobuilds:server-v0.5.1
            volumes:
              - notarycerts:/var/lib/notary/fixtures
            networks:
              - sandbox
            environment:
              - NOTARY_SERVER_STORAGE_TYPE=memory
              - NOTARY_SERVER_TRUST_SERVICE_TYPE=local
          sandboxregistry:
            image: registry:2.4.1
            networks:
              - sandbox
            container_name: sandboxregistry
          trustsandbox:
            image: docker:dind
            networks:
              - sandbox
            volumes:
              - notarycerts:/notarycerts
            privileged: true
            container_name: trustsandbox
            entrypoint: ""
            command: |-
                sh -c '
                    cp /notarycerts/root-ca.crt /usr/local/share/ca-certificates/root-ca.crt &&
                    update-ca-certificates &&
                    dockerd-entrypoint.sh --insecure-registry sandboxregistry:5000'
        volumes:
          notarycerts:
            external: false
        networks:
          sandbox:
            external: false

4. 保存并关闭文件。

5. 在本地系统上运行容器。

        $ docker compose up -d

    第一次运行此命令时，docker-in-docker、Notary 服务器和注册表镜像会从 Docker Hub 下载。


## 在沙箱中实践

现在一切都已设置好，您可以进入 `trustsandbox` 容器并开始测试 Docker 内容信托。在您的宿主机上，获取 `trustsandbox` 容器的一个 shell：

    $ docker container exec -it trustsandbox sh
    / #

### 测试一些内容信托操作

现在，从 `trustsandbox` 容器内部拉取一些镜像。

1. 下载一个 `docker` 镜像进行测试。

        / # docker pull docker/trusttest
        docker pull docker/trusttest
        Using default tag: latest
        latest: Pulling from docker/trusttest

        b3dbab3810fc: Pull complete
        a9539b34a6ab: Pull complete
        Digest: sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a
        Status: Downloaded newer image for docker/trusttest:latest

2. 给它打上标签，以便推送到我们的沙箱注册表：

        / # docker tag docker/trusttest sandboxregistry:5000/test/trusttest:latest

3. 启用内容信托。

        / # export DOCKER_CONTENT_TRUST=1

4. 指定信任服务器。

        / # export DOCKER_CONTENT_TRUST_SERVER=https://notaryserver:4443

    这一步是必要的，因为沙箱使用的是它自己的服务器。通常如果您使用 Docker Public Hub，则不需要此步骤。

5. 拉取测试镜像。

        / # docker pull sandboxregistry:5000/test/trusttest
        Using default tag: latest
        Error: remote trust data does not exist for sandboxregistry:5000/test/trusttest: notaryserver:4443 does not have trust data for sandboxregistry:5000/test/trusttest

      您会看到一个错误，因为此内容尚未存在于 `notaryserver` 上。

6. 推送并签署受信任镜像。

        / # docker push sandboxregistry:5000/test/trusttest:latest
        The push refers to repository [sandboxregistry:5000/test/trusttest]
        5f70bf18a086: Pushed
        c22f7bc058a9: Pushed
        latest: digest: sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926 size: 734
        Signing and pushing trust metadata
        You are about to create a new root signing key passphrase. This passphrase
        will be used to protect the most sensitive key in your signing system. Please
        choose a long, complex passphrase and be careful to keep the password and the
        key file itself secure and backed up. It is highly recommended that you use a
        password manager to generate the passphrase and keep it safe. There will be no
        way to recover this key. You can find the key in your config directory.
        Enter passphrase for new root key with ID 27ec255:
        Repeat passphrase for new root key with ID 27ec255:
        Enter passphrase for new repository key with ID 58233f9 (sandboxregistry:5000/test/trusttest):
        Repeat passphrase for new repository key with ID 58233f9 (sandboxregistry:5000/test/trusttest):
        Finished initializing "sandboxregistry:5000/test/trusttest"
        Successfully signed "sandboxregistry:5000/test/trusttest":latest

    由于这是您第一次推送该仓库，Docker 会创建新的根密钥和仓库密钥，并要求您提供用于加密它们的密码。如果在此之后再次推送，它只会要求您提供仓库密码，以便解密密钥并再次签名。

7. 尝试拉取您刚刚推送的镜像：

        / # docker pull sandboxregistry:5000/test/trusttest
        Using default tag: latest
        Pull (1 of 1): sandboxregistry:5000/test/trusttest:latest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
        sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926: Pulling from test/trusttest
        Digest: sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
        Status: Downloaded newer image for sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
        Tagging sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926 as sandboxregistry:5000/test/trusttest:latest


### 使用恶意镜像进行测试

当数据损坏且您在启用内容信托的情况下尝试拉取时会发生什么？在本节中，您将进入 `sandboxregistry` 并篡改一些数据。然后，尝试拉取它。

1.  保持 `trustsandbox` shell 和容器运行。

2.  从宿主机打开一个新的交互式终端，并获取 `sandboxregistry` 容器的一个 shell。

        $ docker container exec -it sandboxregistry bash
        root@65084fc6f047:/#

3.  列出您推送的 `test/trusttest` 镜像的层：

    ```console
    root@65084fc6f047:/# ls -l /var/lib/registry/docker/registry/v2/repositories/test/trusttest/_layers/sha256
    total 12
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 aac0c133338db2b18ff054943cee3267fe50c75cdee969aed88b1992539ed042
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 cc7629d1331a7362b5e5126beb5bf15ca0bf67eb41eab994c719a45de53255cd
    ```

4.  进入其中一个层的注册表存储目录 (这在不同的目录中)：

        root@65084fc6f047:/# cd /var/lib/registry/docker/registry/v2/blobs/sha256/aa/aac0c133338db2b18ff054943cee3267fe50c75cdee969aed88b1992539ed042

5.  向其中一个 `trusttest` 层添加恶意数据：

        root@65084fc6f047:/# echo "Malicious data" > data

6.  返回您的 `trustsandbox` 终端。

7.  列出 `trusttest` 镜像。

        / # docker image ls | grep trusttest
        REPOSITORY                            TAG                 IMAGE ID            CREATED             SIZE
        docker/trusttest                      latest              cc7629d1331a        11 months ago       5.025 MB
        sandboxregistry:5000/test/trusttest   latest              cc7629d1331a        11 months ago       5.025 MB
        sandboxregistry:5000/test/trusttest   <none>              cc7629d1331a        11 months ago       5.025 MB

8.  从本地缓存中删除 `trusttest:latest` 镜像。

        / # docker image rm -f cc7629d1331a
        Untagged: docker/trusttest:latest
        Untagged: sandboxregistry:5000/test/trusttest:latest
        Untagged: sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
        Deleted: sha256:cc7629d1331a7362b5e5126beb5bf15ca0bf67eb41eab994c719a45de53255cd
        Deleted: sha256:2a1f6535dc6816ffadcdbe20590045e6cbf048d63fd4cc753a684c9bc01abeea
        Deleted: sha256:c22f7bc058a9a8ffeb32989b5d3338787e73855bf224af7aa162823da015d44c

    Docker 不会重新下载它已经缓存的镜像，但我们希望 Docker 尝试从注册表下载被篡改的镜像，并由于其无效而拒绝它。

9.  再次拉取镜像。由于没有缓存，这将从注册表下载镜像。

        / # docker pull sandboxregistry:5000/test/trusttest
        Using default tag: latest
        Pull (1 of 1): sandboxregistry:5000/test/trusttest:latest@sha256:35d5bc26fd358da8320c137784fe590d8fcf9417263ef261653e8e1c7f15672e
        sha256:35d5bc26fd358da8320c137784fe590d8fcf9417263ef261653e8e1c7f15672e: Pulling from test/trusttest

        aac0c133338d: Retrying in 5 seconds
        a3ed95caeb02: Download complete
        error pulling image configuration: unexpected EOF

      由于信任系统无法验证镜像，拉取未能完成。

## 更多沙箱实践

现在，您的本地系统上已有一个完整的 Docker 内容信托沙箱，请随意实践并观察其行为。如果您发现任何有关 Docker 的安全问题，请随时发送邮件至 <security@docker.com>。


## 清理沙箱

完成后，如果您想清理所有已启动的服务以及创建的任何匿名卷，只需在创建 Docker Compose 文件的目录中运行以下命令：

        $ docker compose down -v
