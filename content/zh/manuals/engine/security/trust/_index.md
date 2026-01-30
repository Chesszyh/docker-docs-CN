---
description: 在 Docker 中启用内容信托 (Content Trust)
keywords: content, trust, security, docker, documentation, 内容信托, 安全
---

在联网系统之间传输数据时，信任是一个核心关注点。特别是在通过互联网等不可信介质进行通信时，确保系统操作的所有数据的完整性和发布者身份至关重要。您使用 Docker Engine 向公共或私有注册表推送和拉取镜像 (数据)。内容信托使您能够验证通过任何渠道从注册表接收的所有数据的完整性和发布者身份。

## 关于 Docker 内容信托 (DCT)

Docker 内容信托 (DCT) 提供了对发送到远程 Docker 注册表以及从其接收的数据使用数字签名的能力。这些签名允许客户端或运行时验证特定镜像标签的完整性和发布者。

通过 DCT，镜像发布者可以对镜像进行签名，而镜像消费者可以确保他们拉取的镜像是经过签名的。发布者可以是手动对其内容进行签名的个人或组织，也可以是在发布过程中自动对其内容进行签名的自动化软件供应链。

### 镜像标签与 DCT

单个镜像记录具有以下标识符：

```text
[REGISTRY_HOST[:REGISTRY_PORT]/]REPOSITORY[:TAG]
```

一个特定的镜像 `REPOSITORY` (仓库) 可以有多个标签。例如，`latest` 和 `3.1.2` 都是 `mongo` 镜像的标签。镜像发布者可以多次构建镜像和标签组合，在每次构建时更改镜像。

DCT 与镜像的 `TAG` 部分相关联。每个镜像仓库都有一组密钥，镜像发布者使用这些密钥对镜像标签进行签名。镜像发布者可以自行决定对哪些标签进行签名。

一个镜像仓库可以包含一个已签名的标签和另一个未签名的标签。例如，考虑 [Mongo 镜像仓库](https://hub.docker.com/r/library/mongo/tags/)。`latest` 标签可能是未签名的，而 `3.1.6` 标签可能是已签名的。镜像发布者负责决定是否对某个镜像标签进行签名。在这种表示中，一些镜像标签已签名，另一些则未签名：

![已签名的标签](images/tag_signing.png)

发布者可以选择是否签署特定标签。因此，未签名标签的内容与具有相同名称的已签名标签的内容可能不匹配。例如，发布者可以推送一个带标签的镜像 `someimage:latest` 并对其进行签名。稍后，同一个发布者可以推送一个未签名的 `someimage:latest` 镜像。第二次推送会替换上一个未签名的 `latest` 标签，但不会影响已签名的 `latest` 版本。能够选择签署哪些标签，允许发布者在正式签署之前对镜像的未签名版本进行迭代。

镜像消费者可以启用 DCT 以确保他们使用的镜像是经过签名的。如果消费者启用了 DCT，他们只能拉取、运行或构建受信任的镜像。启用 DCT 有点像为您的注册表应用一个“过滤器”。消费者只能“看到”已签名的镜像标签，而不太理想的未签名镜像标签对他们来说是“不可见”的。

![信任视图](images/trust_view.png)

对于未启用 DCT 的消费者，他们使用 Docker 镜像的方式没有任何变化。每个镜像都是可见的，无论它是否已签名。

### Docker 内容信托密钥

镜像标签的信任是通过使用签名密钥来管理的。当首次调用使用 DCT 的操作时，会创建一组密钥。一组密钥由以下几类密钥组成：

- 离线密钥 (offline key)，它是镜像标签 DCT 的根
- 仓库或标签密钥 (repository or tagging keys)，用于签署标签
- 服务端管理密钥 (server-managed keys)，如时间戳密钥，它为您的仓库提供新鲜度安全保证

下图描绘了各种签名密钥及其关系：

![内容信托组件](images/trust_components.png)

> [!WARNING]
>
> 根密钥一旦丢失便无法恢复。如果您丢失了任何其他密钥，请发送电子邮件至 [Docker Hub 支持](mailto:hub-support@docker.com)。此损失还要求之前使用过该仓库已签名标签的每个消费者进行手动干预。

您应该将根密钥备份到安全的地方。鉴于只有创建新仓库时才需要它，建议将其离线存储在硬件中。有关保护和备份密钥的详情，请务必阅读如何 [管理 DCT 密钥](trust_key_mng.md)。

## 使用 Docker 内容信托签署镜像

在 Docker CLI 中，我们可以使用 `$ docker trust` 命令语法来签署并推送容器镜像。这是构建在 Notary 功能集之上的。有关更多信息，请参阅 [Notary GitHub 仓库](https://github.com/theupdateframework/notary)。

签署镜像的前提条件是拥有一个附带有 Notary 服务器的 Docker 注册表 (例如 Docker Hub)。建立自托管环境的说明可以在 [这里](/engine/security/trust/deploying_notary/) 找到。

要签署 Docker 镜像，您需要一个授权密钥对。这些密钥可以使用 `$ docker trust key generate` 在本地生成，也可以由证书颁发机构生成。

首先，我们将授权私钥添加到本地 Docker 信任仓库中。(默认情况下存储在 `~/.docker/trust/` 中)。如果您使用 `$ docker trust key generate` 生成授权密钥，私钥会自动添加到本地信任库中。如果您是导入独立的密钥，则需要使用 `$ docker trust key load` 命令。

```console
$ docker trust key generate jeff
Generating key for jeff...
Enter passphrase for new jeff key with ID 9deed25:
Repeat passphrase for new jeff key with ID 9deed25:
Successfully generated and loaded private key. Corresponding public key available: /home/ubuntu/Documents/mytrustdir/jeff.pub
```

或者，如果您已有现成的密钥：

```console
$ docker trust key load key.pem --name jeff
Loading key from "key.pem"...
Enter passphrase for new jeff key with ID 8ae710e:
Repeat passphrase for new jeff key with ID 8ae710e:
Successfully imported key from key.pem
```

接下来，我们需要将授权公钥添加到 Notary 服务器；这针对 Notary 中特定的镜像仓库，称为全局唯一名称 (GUN)。如果这是您第一次向该仓库添加授权，此命令还会使用本地 Notary 规范根密钥初始化该仓库。要详细了解初始化仓库以及授权的作用，请参阅 [内容信托的授权](trust_delegation.md)。

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
Enter passphrase for new repository key with ID 10b5e94:
```

最后，我们将使用授权私钥对特定标签进行签名并将其推送到注册表。

```console
$ docker trust sign registry.example.com/admin/demo:1
Signing and pushing trust data for local image registry.example.com/admin/demo:1, may overwrite remote trust data
The push refers to repository [registry.example.com/admin/demo]
7bff100f35cb: Pushed
1: digest: sha256:3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e size: 528
Signing and pushing trust metadata
Enter passphrase for signer key with ID 8ae710e:
Successfully signed registry.example.com/admin/demo:1
```

或者，一旦导入密钥，就可以通过导出 DCT 环境变量并使用 `$ docker push` 命令推送镜像。

```console
$ export DOCKER_CONTENT_TRUST=1

$ docker push registry.example.com/admin/demo:1
The push refers to repository [registry.example.com/admin/demo:1]
7bff100f35cb: Pushed
1: digest: sha256:3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e size: 528
Signing and pushing trust metadata
Enter passphrase for signer key with ID 8ae710e:
Successfully signed registry.example.com/admin/demo:1
```

可以使用 `$ docker trust inspect` 命令查看标签或仓库的远程信任数据：

```console
$ docker trust inspect --pretty registry.example.com/admin/demo:1

Signatures for registry.example.com/admin/demo:1

SIGNED TAG          DIGEST                                                             SIGNERS
1                   3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e   jeff

List of signers and their keys for registry.example.com/admin/demo:1

SIGNER              KEYS
jeff                8ae710e3ba82

Administrative keys for registry.example.com/admin/demo:1

  Repository Key:	10b5e94c916a0977471cc08fa56c1a5679819b2005ba6a257aa78ce76d3a1e27
  Root Key:	84ca6e4416416d78c4597e754f38517bea95ab427e5f95871f90d460573071fc
```

可以使用 `$ docker trust revoke` 命令删除标签的远程信任数据：

```console
$ docker trust revoke registry.example.com/admin/demo:1
Enter passphrase for signer key with ID 8ae710e:
Successfully deleted signature for registry.example.com/admin/demo:1
```

## Docker 内容信托的客户端强制执行

Docker 客户端默认禁用内容信托。要启用它，请将 `DOCKER_CONTENT_TRUST` 环境变量设置为 `1`。这会阻止用户使用不包含签名的带标签镜像。

当 Docker 客户端启用 DCT 时，对带标签镜像进行操作的 `docker` CLI 命令必须具有内容签名或显式的内容哈希。使用 DCT 的命令包括：

* `push`
* `build`
* `create`
* `pull`
* `run`

例如，在启用 DCT 的情况下，`docker pull someimage:latest` 仅在 `someimage:latest` 已签名时才会成功。但是，只要哈希存在，使用显式内容哈希的操作总是会成功：

```console
$ docker pull registry.example.com/user/image:1
Error: remote trust data does not exist for registry.example.com/user/image: registry.example.com does not have trust data for registry.example.com/user/image

$ docker pull registry.example.com/user/image@sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a
sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1: Pulling from user/image
ff3a5c916c92: Pull complete
a59a168caba3: Pull complete
Digest: sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1
Status: Downloaded newer image for registry.example.com/user/image@sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1
```

## 相关信息

* [内容信托的授权](trust_delegation.md)
* [内容信托自动化](trust_automation.md)
* [管理内容信托密钥](trust_key_mng.md)
* [在内容信托沙箱中实践](trust_sandbox.md)
