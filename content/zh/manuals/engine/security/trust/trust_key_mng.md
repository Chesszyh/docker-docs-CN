---
description: 管理内容信托密钥
keywords: trust, security, root, keys, repository, 信任, 安全, 根密钥, 仓库
title: 管理内容信托密钥
---

镜像标签的信任是通过使用密钥来管理的。Docker 的内容信托使用五种不同类型的密钥：

| 密钥       | 描述 |                                                                                                                                                                                                                         
|:-----------|:----------- |
| 根密钥 (root key)   | 镜像标签内容信托的根。启用内容信托时，只需创建一次根密钥。也称为离线密钥 (offline key)，因为它应该被离线保存。 |
| 目标密钥 (targets)    | 此密钥允许您签署镜像标签，管理授权 (包括授权密钥或允许的授权路径)。也称为仓库密钥 (repository key)，因为此密钥决定了哪些标签可以被签署到镜像仓库中。 |
| 快照密钥 (snapshot)   | 此密钥签署当前镜像标签的集合，防止混合和匹配攻击。 |                                                                                                                                         
| 时间戳密钥 (timestamp)  | 此密钥允许 Docker 镜像仓库拥有新鲜度安全保证，而不需要客户端定期刷新内容。 |
| 授权密钥 (delegation) | 授权密钥是可选的标记密钥，允许您将签署镜像标签的权限委托给其他发布者，而无需共享您的目标密钥。 |

首次在启用内容信托的情况下执行 `docker push` 时，系统会自动为镜像仓库生成根密钥、目标密钥、快照密钥和时间戳密钥：

- 根密钥和目标密钥在客户端本地生成并存储。

- 时间戳密钥和快照密钥在与 Docker 注册表一同部署的签名服务器中安全地生成并存储。这些密钥在一个不直接暴露于互联网的后端服务中生成，并以加密方式存储。使用 Notary CLI 可以 [在本地管理您的快照密钥](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#rotate-keys)。

授权密钥是可选的，不会作为正常 `docker` 工作流的一部分生成。它们需要 [手动生成并添加到仓库中](trust_delegation.md#creating-delegation-keys)。

## 选择密码

您为根密钥和仓库密钥选择的密码应随机生成并存储在密码管理器中。拥有仓库密钥允许用户在仓库上签署镜像标签。密码用于加密存储中的密钥，并确保丢失笔记本电脑或意外备份不会使私钥素材面临风险。

## 备份您的密钥

所有 Docker 信任密钥在创建时都会使用您提供的密码进行加密存储。即便如此，您仍应注意备份它们的位置。良好的做法是创建两个加密的 USB 密钥。

> [!WARNING]
>
> 将您的密钥备份到安全、稳妥的位置非常重要。仓库密钥丢失是可以恢复的，但根密钥丢失则无法恢复。

Docker 客户端将密钥存储在 `~/.docker/trust/private` 目录中。在备份之前，您应该将它们 `tar` 成一个存档文件：

```console
$ umask 077; tar -zcvf private_keys_backup.tar.gz ~/.docker/trust/private; umask 022
```

## 硬件存储与签名

Docker 内容信托可以存储并使用来自 Yubikey 4 的根密钥进行签名。Yubikey 的优先级高于存储在文件系统中的密钥。当您初始化一个带有内容信托的新仓库时，Docker Engine 会在本地寻找根密钥。如果未找到密钥且存在 Yubikey 4，Docker Engine 会在 Yubikey 4 中创建一个根密钥。有关更多详情，请参阅 [Notary 文档](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#use-a-yubikey)。

在 Docker Engine 1.11 之前，此功能仅在实验性分支中提供。

## 密钥丢失

> [!WARNING]
>
> 如果发布者丢失了密钥，意味着失去了为相关仓库签署镜像的能力。如果您丢失了密钥，请发送电子邮件至 [Docker Hub 支持](mailto:hub-support@docker.com)。再次提醒，根密钥的丢失是不可恢复的。

这种丢失还要求在丢失前使用过该仓库中已签署标签的每个消费者进行手动干预。
镜像消费者对于之前从受影响仓库下载的内容会收到以下错误：

```console
Warning: potential malicious behavior - trust data has insufficient signatures for remote repository docker.io/my/image: valid signatures did not meet threshold
```

要纠正此问题，他们需要下载一个使用新密钥签署的新镜像标签。

## 相关信息

* [Docker 中的内容信托](index.md)
* [内容信托自动化](trust_automation.md)
* [内容信托的授权](trust_delegation.md)
* [在内容信托沙箱中实践](trust_sandbox.md)
