---
description: 内容信托的授权
keywords: trust, security, delegations, keys, repository, 信任, 安全, 授权, 密钥, 仓库
title: 内容信托的授权 (Delegations)
aliases:
- /ee/dtr/user/access-dtr/configure-your-notary-client/
---

Docker 内容信托 (DCT) 中的授权 (Delegations) 允许您控制谁可以以及谁不能签署镜像标签。授权会拥有一对私有和公有的授权密钥。一个授权可能包含多对密钥和贡献者，以便：a) 允许多个用户成为授权的一部分，以及 b) 支持密钥轮换。

Docker 内容信托中最关键的授权是 `targets/releases`。这被视为受信任镜像标签的规范来源，如果没有贡献者的密钥属于此授权，他们将无法签署标签。

幸运的是，当使用 `$ docker trust` 命令时，我们会自动初始化仓库、管理仓库密钥，并通过 `docker trust signer add` 将协作者的密钥添加到 `targets/releases` 授权中。

## 配置 Docker 客户端

默认情况下，`$ docker trust` 命令期望 notary 服务器的 URL 与镜像标签中指定的注册表 URL 相同 (遵循与 `$ docker push` 类似的逻辑)。使用 Docker Hub 或 DTR 时，notary 服务器的 URL 与注册表 URL 相同。然而，对于自托管环境或第三方注册表，您需要指定 notary 服务器的替代 URL。这可以通过以下方式完成：

```console
$ export DOCKER_CONTENT_TRUST_SERVER=https://<URL>:<PORT>
```

如果在自托管环境中未导出此变量，您可能会看到如下错误：

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
<...>
Error: trust data missing for remote repository registry.example.com/admin/demo or remote repository not found: timestamp key trust data unavailable.  Has a notary repository been initialized?

$ docker trust inspect registry.example.com/admin/demo --pretty
WARN[0000] Error while downloading remote metadata, using cached timestamp - this might not be the latest version available remotely
<...>
```

如果您已为 notary 服务器启用了身份验证，或正在使用 DTR，则在向 notary 服务器推送数据之前需要先登录。

```console
$ docker login registry.example.com/user/repo
Username: admin
Password:

Login Succeeded

$ docker trust signer add --key cert.pem jeff registry.example.com/user/repo
Adding signer "jeff" to registry.example.com/user/repo...
Initializing signed repository for registry.example.com/user/repo...
Successfully initialized "registry.example.com/user/repo"
Successfully added signer: jeff to registry.example.com/user/repo
```

如果您未登录，您将看到：

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/user/repo
Adding signer "jeff" to registry.example.com/user/repo...
Initializing signed repository for registry.example.com/user/repo...
you are not authorized to perform this operation: server returned 401.

Failed to add signer to: registry.example.com/user/repo
```

## 配置 Notary 客户端

DCT 的某些高级特性需要使用 Notary CLI。要安装和配置 Notary CLI：

1. 下载 [客户端](https://github.com/theupdateframework/notary/releases) 并确保它在您的路径 (PATH) 中可用。

2. 在 `~/.notary/config.json` 创建一个包含以下内容的配置文件：

```json
{
  "trust_dir" : "~/.docker/trust",
  "remote_server": {
    "url": "https://registry.example.com",
    "root_ca": "../.docker/ca.pem"
  }
}
```

新创建的配置文件包含有关本地 Docker 信任数据位置和 notary 服务器 URL 的信息。

有关如何在 Docker 内容信托用例之外使用 notary 的更详细信息，请参阅 [此处的](https://github.com/theupdateframework/notary/blob/master/docs/command_reference.md) Notary CLI 文档。

## 创建授权密钥

添加第一个贡献者的前提条件是一对授权密钥。这些密钥可以在本地使用 `$ docker trust` 生成，也可以由证书颁发机构生成。

### 使用 Docker Trust 生成密钥

Docker trust 有一个内置的授权密钥对生成器，`$ docker trust key generate <name>`。运行此命令将自动把授权私钥加载到本地 Docker 信任库中。

```console
$ docker trust key generate jeff

Generating key for jeff...
Enter passphrase for new jeff key with ID 9deed25: 
Repeat passphrase for new jeff key with ID 9deed25: 
Successfully generated and loaded private key. Corresponding public key available: /home/ubuntu/Documents/mytrustdir/jeff.pub
```

### 手动生成密钥

如果您需要手动生成私钥 (RSA 或 ECDSA) 和包含公钥的 X.509 证书，您可以使用本地工具 (如 openssl 或 cfssl) 以及本地或公司范围的证书颁发机构 (CA)。

以下是如何生成 2048 位 RSA 密钥部分的示例 (所有 RSA 密钥必须至少为 2048 位)：

```console
$ openssl genrsa -out delegation.key 2048

Generating RSA private key, 2048 bit long modulus
....................................................+++
............+++
e is 65537 (0x10001)
```

他们应保持 `delegation.key` 的私密性，因为它用于签署标签。

然后他们需要生成一个包含公钥的 x509 证书，这就是您需要从他们那里得到的东西。以下是生成 CSR (证书签名请求) 的命令：

```console
$ openssl req -new -sha256 -key delegation.key -out delegation.csr
```

然后他们可以将其发送到您信任的任何 CA 进行签名，或者他们也可以自签名该证书 (在本例中，创建一个有效期为 1 年的证书)：

```console
$ openssl x509 -req -sha256 -days 365 -in delegation.csr -signkey delegation.key -out delegation.crt
```

然后他们需要给您 `delegation.crt`，无论是自签名的还是由 CA 签署的。

最后，您需要将私钥添加到本地 Docker 信任库中。

```console
$ docker trust key load delegation.key --name jeff

Loading key from "delegation.key"...
Enter passphrase for new jeff key with ID 8ae710e: 
Repeat passphrase for new jeff key with ID 8ae710e: 
Successfully imported key from delegation.key
```

### 查看本地授权密钥

要列出已导入本地 Docker 信任库的密钥，我们可以使用 Notary CLI。

```console
$ notary key list

ROLE       GUN                          KEY ID                                                              LOCATION
----       ---                          ------                                                              --------
root                                    f6c6a4b00fefd8751f86194c7d87a3bede444540eb3378c4a11ce10852ab1f96    /home/ubuntu/.docker/trust/private
jeff                                    9deed251daa1aa6f9d5f9b752847647cf8d705da0763aa5467650d0987ed5306    /home/ubuntu/.docker/trust/private
```

## 在 Notary 服务器中管理授权

当使用 `$ docker trust` 向 Notary 服务器添加第一个授权时，我们会自动初始化仓库的信任数据。这包括创建 notary 目标 (target) 和快照 (snapshot) 密钥，并轮换快照密钥以由 notary 服务器管理。有关这些密钥的更多信息可以在 [这里](trust_key_mng.md) 找到。

在初始化仓库时，您需要本地 Notary 规范根密钥的密钥和密码。如果您以前从未初始化过仓库，因此没有 Notary 根密钥，`$ docker trust` 将为您创建一个。

> [!IMPORTANT]
>
> 务必保护并备份您的 [Notary 规范根密钥](trust_key_mng.md)。

### 初始化仓库

要将第一个密钥上传到授权，并同时初始化仓库，您可以使用 `$ docker trust signer add` 命令。这会将贡献者的公钥添加到 `targets/releases` 授权中，并创建第二个 `targets/<name>` 授权。

对于 DCT，第二个授权的名称 (在下面的示例中为 `jeff`) 是为了帮助您跟踪密钥的所有者。在 Notary 更高级的用例中，额外的授权被用于层级结构。

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/admin/demo

Adding signer "jeff" to registry.example.com/admin/demo...
Initializing signed repository for registry.example.com/admin/demo...
Enter passphrase for root key with ID f6c6a4b: 
Enter passphrase for new repository key with ID b0014f8: 
Repeat passphrase for new repository key with ID b0014f8: 
Successfully initialized "registry.example.com/admin/demo"
Successfully added signer: jeff to registry.example.com/admin/demo
```

您可以使用 `$ docker trust inspect` 命令查看为每个仓库推送到 Notary 服务器的密钥。

```console
$ docker trust inspect --pretty registry.example.com/admin/demo

No signatures for registry.example.com/admin/demo


List of signers and their keys for registry.example.com/admin/demo

SIGNER              KEYS
jeff                1091060d7bfd

Administrative keys for registry.example.com/admin/demo

  Repository Key:	b0014f8e4863df2d028095b74efcb05d872c3591de0af06652944e310d96598d
  Root Key:	64d147e59e44870311dd2d80b9f7840039115ef3dfa5008127d769a5f657a5d7
```

您也可以使用 Notary CLI 来列出授权和密钥。在这里您可以清楚地看到密钥已附加到 `targets/releases` 和 `targets/jeff`。

```console
$ notary delegation list registry.example.com/admin/demo

ROLE                PATHS             KEY IDS                                                             THRESHOLD
----                -----             -------                                                             ---------
targets/jeff        "" <all paths>    1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    1
                                          
targets/releases    "" <all paths>    1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    1 
```

### 添加额外的签署者

Docker Trust 允许您为每个仓库配置多个授权，从而允许您管理授权的生命周期。当使用 `$ docker trust` 添加额外的授权时，协作者的密钥会再次被添加到 `targets/release` 角色中。

> 请注意，您需要仓库密钥的密码；该密码应在您第一次初始化仓库时配置好。

```console
$ docker trust signer add --key ben.pub ben registry.example.com/admin/demo

Adding signer "ben" to registry.example.com/admin/demo...
Enter passphrase for repository key with ID b0014f8: 
Successfully added signer: ben to registry.example.com/admin/demo
```

检查以证明现在有 2 个授权 (签署者)。

```console
$ docker trust inspect --pretty registry.example.com/admin/demo

No signatures for registry.example.com/admin/demo

List of signers and their keys for registry.example.com/admin/demo

SIGNER              KEYS
ben                 afa404703b25
jeff                1091060d7bfd

Administrative keys for registry.example.com/admin/demo

  Repository Key:	b0014f8e4863df2d028095b74efcb05d872c3591de0af06652944e310d96598d
  Root Key:	64d147e59e44870311dd2d80b9f7840039115ef3dfa5008127d769a5f657a5d7
```

### 向现有授权添加密钥

为了支持诸如密钥轮换和密钥过期/退役之类的事情，您可以为每个授权发布多个贡献者密钥。这里的唯一前提条件是确保使用相同的授权名称，在本例中为 `jeff`。Docker trust 将自动处理将此新密钥添加到 `targets/releases` 的过程。

> [!NOTE]
>
> 您需要仓库密钥的密码；该密码应在您第一次初始化仓库时配置。

```console
$ docker trust signer add --key cert2.pem jeff registry.example.com/admin/demo

Adding signer "jeff" to registry.example.com/admin/demo...
Enter passphrase for repository key with ID b0014f8: 
Successfully added signer: jeff to registry.example.com/admin/demo
```

检查以证明该授权 (签署者) 现在包含多个密钥 ID。

```console
$ docker trust inspect --pretty registry.example.com/admin/demo

No signatures for registry.example.com/admin/demo


List of signers and their keys for registry.example.com/admin/demo

SIGNER              KEYS
jeff                1091060d7bfd, 5570b88df073

Administrative keys for registry.example.com/admin/demo

  Repository Key:	b0014f8e4863df2d028095b74efcb05d872c3591de0af06652944e310d96598d
  Root Key:	64d147e59e44870311dd2d80b9f7840039115ef3dfa5008127d769a5f657a5d7
```

### 移除授权

如果您需要移除一个授权，包括附加到 `targets/releases` 角色的贡献者密钥，可以使用 `$ docker trust signer remove` 命令。

> [!NOTE]
>
> 由已移除的授权签署的标签将需要由活动的授权重新签署。

```console
$ docker trust signer remove ben registry.example.com/admin/demo
Removing signer "ben" from registry.example.com/admin/demo...
Enter passphrase for repository key with ID b0014f8: 
Successfully removed ben from registry.example.com/admin/demo
```

#### 故障排查

1) 如果您看到 `targets/releases` 中没有可用密钥的错误，您需要在重新签署镜像之前使用 `docker trust signer add` 添加额外的授权。

   ```text
   WARN[0000] role targets/releases has fewer keys than its threshold of 1; it will not be usable until keys are added to it
   ```

2) 如果您已经添加了额外的授权，但仍然看到 `targets/releases` 中没有有效签名的错误消息，您需要使用 Notary CLI 重新签署 `targets/releases` 授权文件。

   ```text
   WARN[0000] Error getting targets/releases: valid signatures did not meet threshold for targets/releases 
   ```

   重新签署授权文件是使用 `$ notary witness` 命令完成的：

   ```console
   $ notary witness registry.example.com/admin/demo targets/releases --publish
   ```

   有关 `$ notary witness` 命令的更多信息可以在 [这里](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#recovering-a-delegation) 找到。

### 从授权中移除贡献者的密钥

作为授权密钥轮换的一部分，您可能希望移除单个密钥但保留该授权。这可以使用 Notary CLI 完成。

请记住，您必须同时从 `targets/releases` 角色和特定于该签署者的 `targets/<name>` 角色中移除该密钥。

1) 我们需要从 Notary 服务器获取密钥 ID：

   ```console
   $ notary delegation list registry.example.com/admin/demo

   ROLE                PATHS             KEY IDS                                                             THRESHOLD
   ----                -----             -------                                                             ---------
   targets/jeff        "" <all paths>    8fb597cbaf196f0781628b2f52bff6b3912e4e8075720378fda60d17232bbcf9    1
                                         1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    
   targets/releases    "" <all paths>    8fb597cbaf196f0781628b2f52bff6b3912e4e8075720378fda60d17232bbcf9    1
                                         1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    
   ```

2) 从 `targets/releases` 授权中移除：

   ```console
   $ notary delegation remove registry.example.com/admin/demo targets/releases 1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1 --publish
   
   Auto-publishing changes to registry.example.com/admin/demo
   Enter username: admin
   Enter password: 
   Enter passphrase for targets key with ID b0014f8: 
   Successfully published changes for repository registry.example.com/admin/demo
   ```

3) 从 `targets/<name>` 授权中移除：

   ```console
   $ notary delegation remove registry.example.com/admin/demo targets/jeff 1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1 --publish
   
   Removal of delegation role targets/jeff with keys [5570b88df0736c468493247a07e235e35cf3641270c944d0e9e8899922fc6f99], to repository "registry.example.com/admin/demo" staged for next publish.
   
   Auto-publishing changes to registry.example.com/admin/demo
   Enter username: admin    
   Enter password: 
   Enter passphrase for targets key with ID b0014f8: 
   Successfully published changes for repository registry.example.com/admin/demo
   ```

4) 检查剩余的授权列表：

   ```console
   $ notary delegation list registry.example.com/admin/demo
   
   ROLE                PATHS             KEY IDS                                                             THRESHOLD
   ----                -----             -------                                                             ---------
   targets/jeff        "" <all paths>    8fb597cbaf196f0781628b2f52bff6b3912e4e8075720378fda60d17232bbcf9    1    
   targets/releases    "" <all paths>    8fb597cbaf196f0781628b2f52bff6b3912e4e8075720378fda60d17232bbcf9    1    
   ```

### 移除本地授权私钥

作为轮换授权密钥的一部分，您可能需要从本地 Docker 信任库中移除本地授权密钥。这可以使用 Notary CLI，通过 `$ notary key remove` 命令完成。

1) 我们需要从本地 Docker 信任库中获取密钥 ID：

   ```console
   $ notary key list
   
   ROLE       GUN                          KEY ID                                                              LOCATION
   ----       ---                          ------                                                              --------
   root                                    f6c6a4b00fefd8751f86194c7d87a3bede444540eb3378c4a11ce10852ab1f96    /home/ubuntu/.docker/trust/private
   admin                                   8fb597cbaf196f0781628b2f52bff6b3912e4e8075720378fda60d17232bbcf9    /home/ubuntu/.docker/trust/private
   jeff                                    1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    /home/ubuntu/.docker/trust/private
   targets    ...example.com/admin/demo    c819f2eda8fba2810ec6a7f95f051c90276c87fddfc3039058856fad061c009d    /home/ubuntu/.docker/trust/private
   ```

2) 从本地 Docker 信任库中移除密钥：

   ```console
   $ notary key remove 1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1
   
   Are you sure you want to remove 1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1 (role jeff) from /home/ubuntu/.docker/trust/private?  (yes/no)  y
   
   Deleted 1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1 (role jeff) from /home/ubuntu/.docker/trust/private.
   ```

## 移除仓库中的所有信任数据

您可以使用 Notary CLI 移除仓库中的所有信任数据，包括仓库密钥、目标密钥、快照密钥和所有授权密钥。

这通常是容器注册表在删除特定仓库之前的要求。

```console
$ notary delete registry.example.com/admin/demo --remote

Deleting trust data for repository registry.example.com/admin/demo
Enter username: admin
Enter password: 
Successfully deleted local and remote trust data for repository registry.example.com/admin/demo

$ docker trust inspect --pretty registry.example.com/admin/demo

No signatures or cannot access registry.example.com/admin/demo
```

## 相关信息

* [Docker 中的内容信托](index.md)
* [管理内容信托密钥](trust_key_mng.md)
* [内容信托自动化](trust_automation.md)
* [在内容信托沙箱中实践](trust_sandbox.md)
