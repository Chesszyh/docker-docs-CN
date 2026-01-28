---
description: How PKI works in swarm mode
keywords: swarm, security, tls, pki,
title: 使用公钥基础设施 (PKI) 管理 swarm 安全
---

Docker 内置的 Swarm 模式公钥基础设施（PKI）系统使得安全部署容器编排系统变得简单。swarm 中的节点使用双向传输层安全（TLS）来认证、授权和加密与 swarm 中其他节点的通信。

当你通过运行 `docker swarm init` 创建 swarm 时，Docker 会将自身指定为管理节点。默认情况下，管理节点会生成一个新的根证书颁发机构（CA）以及一个密钥对，用于保护与加入 swarm 的其他节点之间的通信。如果你愿意，可以使用 [docker swarm init](/reference/cli/docker/swarm/init.md) 命令的 `--external-ca` 标志指定你自己的外部生成的根 CA。

管理节点还会生成两个令牌，用于将其他节点加入 swarm：一个工作节点令牌和一个管理节点令牌。每个令牌都包含根 CA 证书的摘要和一个随机生成的密钥。当节点加入 swarm 时，加入的节点使用摘要来验证远程管理节点的根 CA 证书。远程管理节点使用密钥来确保加入的节点是经过批准的节点。

每当有新节点加入 swarm 时，管理节点都会向该节点颁发证书。该证书包含一个随机生成的节点 ID，用于在证书通用名称（CN）下标识该节点，以及在组织单位（OU）下标识角色。节点 ID 在当前 swarm 中作为该节点生命周期内的加密安全节点标识。

下图说明了管理节点和工作节点如何使用最低 TLS 1.2 加密通信。

![TLS diagram](/engine/swarm/images/tls.webp?w=600)

以下示例显示了来自工作节点证书的信息：

```none
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            3b:1c:06:91:73:fb:16:ff:69:c3:f7:a2:fe:96:c1:73:e2:80:97:3b
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: CN=swarm-ca
        Validity
            Not Before: Aug 30 02:39:00 2016 GMT
            Not After : Nov 28 03:39:00 2016 GMT
        Subject: O=ec2adilxf4ngv7ev8fwsi61i7, OU=swarm-worker, CN=dw02poa4vqvzxi5c10gm4pq2g
...snip...
```

默认情况下，swarm 中的每个节点每三个月更新一次证书。你可以通过运行 `docker swarm update --cert-expiry <TIME PERIOD>` 命令来配置此间隔。最小轮换值为 1 小时。详情请参阅 [docker swarm update](/reference/cli/docker/swarm/update.md) CLI 参考。

## 轮换 CA 证书

> [!NOTE]
>
> Mirantis Kubernetes Engine (MKE)，前身为 Docker UCP，为 swarm 提供外部证书管理器服务。如果你在 MKE 上运行 swarm，不应该手动轮换 CA 证书。如果需要轮换证书，请联系 Mirantis 支持。

如果集群 CA 密钥或管理节点被入侵，你可以轮换 swarm 根 CA，这样所有节点将不再信任由旧根 CA 签名的证书。

运行 `docker swarm ca --rotate` 来生成新的 CA 证书和密钥。如果你愿意，可以传递 `--ca-cert` 和 `--external-ca` 标志来指定根证书并使用 swarm 外部的根 CA。或者，你可以传递 `--ca-cert` 和 `--ca-key` 标志来指定你希望 swarm 使用的确切证书和密钥。

当你执行 `docker swarm ca --rotate` 命令时，会按顺序发生以下事情：

1.  Docker 生成一个交叉签名证书。这意味着新根 CA 证书的一个版本是由旧根 CA 证书签名的。这个交叉签名证书被用作所有新节点证书的中间证书。这确保了仍然信任旧根 CA 的节点仍然可以验证由新 CA 签名的证书。

2.  Docker 还会通知所有节点立即更新其 TLS 证书。这个过程可能需要几分钟，具体取决于 swarm 中的节点数量。

3.  在 swarm 中的每个节点都拥有由新 CA 签名的新 TLS 证书后，Docker 会忘记旧的 CA 证书和密钥材料，并通知所有节点仅信任新的 CA 证书。

    这也会导致 swarm 的加入令牌发生变化。之前的加入令牌不再有效。

从这一点开始，所有新颁发的节点证书都由新的根 CA 签名，并且不包含任何中间证书。

## 了解更多

* 阅读了解[节点](nodes.md)的工作原理。
* 了解 Swarm 模式[服务](services.md)的工作原理。
