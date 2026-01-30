---
description: Swarm 模式下的 PKI 工作原理
keywords: swarm, security, tls, pki, 安全
title: 使用公钥基础设施 (PKI) 管理 Swarm 安全
---

Docker 内置的 Swarm 模式公钥基础设施 (PKI) 系统使得安全部署容器编排系统变得简单。Swarm 中的节点使用双向传输层安全 (mutual TLS) 来对 Swarm 中的其他节点进行身份验证、授权和加密通信。

当您通过运行 `docker swarm init` 创建 Swarm 时，Docker 会将自身指定为管理节点。默认情况下，管理节点会生成一个新的根证书颁发机构 (CA) 以及一对密钥，用于保护与加入 Swarm 的其他节点的通信。如果您愿意，可以使用 [docker swarm init](/reference/cli/docker/swarm/init.md) 命令的 `--external-ca` 标志来指定您自己的外部生成的根 CA。

管理节点还会生成两个令牌，用于在向 Swarm 加入额外节点时使用：一个工作节点令牌和一个管理节点令牌。每个令牌都包含根 CA 证书的摘要和一个随机生成的机密。当一个节点加入 Swarm 时，加入节点使用该摘要来验证来自远程管理节点的根 CA 证书。远程管理节点使用该机密来确保加入节点是经过批准的节点。

每当有新节点加入 Swarm 时，管理节点都会为该节点颁发证书。该证书包含一个随机生成的节点 ID，用于在证书公用名 (CN) 下标识节点，并在组织单位 (OU) 下标识其角色。节点 ID 作为节点在当前 Swarm 生命周期内的加密安全节点身份。

下图说明了管理节点和工作节点如何使用最低 TLS 1.2 版本来加密通信。

![TLS 图示](/engine/swarm/images/tls.webp?w=600)

以下示例显示了来自工作节点的证书信息：

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

默认情况下，Swarm 中的每个节点每三个月更新一次其证书。您可以通过运行 `docker swarm update --cert-expiry <TIME PERIOD>` 命令来配置此间隔。最小轮换值为 1 小时。详情请参考 [docker swarm update](/reference/cli/docker/swarm/update.md) CLI 参考。

## 轮换 CA 证书

> [!NOTE]
>
> Mirantis Kubernetes Engine (MKE)，前身为 Docker UCP，为 Swarm 提供外部证书管理器服务。如果您在 MKE 上运行 Swarm，则不应手动轮换 CA 证书。相反，如果需要轮换证书，请联系 Mirantis 支持。

如果集群 CA 密钥或管理节点遭到破坏，您可以轮换 Swarm 根 CA，这样所有节点都不再信任由旧根 CA 签署的证书。

运行 `docker swarm ca --rotate` 以生成新的 CA 证书和密钥。如果您愿意，可以传递 `--ca-cert` 和 `--external-ca` 标志来指定根证书，并使用 Swarm 外部的根 CA。或者，您可以传递 `--ca-cert` 和 `--ca-key` 标志来指定您希望 Swarm 使用的确切证书和密钥。

当您执行 `docker swarm ca --rotate` 命令时，按顺序会发生以下情况：

1.  Docker 生成一个交叉签署的证书。这意味着新根 CA 证书的一个版本是由旧根 CA 证书签署的。这个交叉签署的证书被用作所有新节点证书的中间证书。这确保了仍然信任旧根 CA 的节点仍然可以验证由新 CA 签署的证书。

2.  Docker 还会通知所有节点立即更新其 TLS 证书。此过程可能需要几分钟，具体取决于 Swarm 中的节点数量。

3.  在 Swarm 中的每个节点都拥有由新 CA 签署的新 TLS 证书后，Docker 会丢弃旧的 CA 证书和密钥材料，并通知所有节点仅信任新的 CA 证书。

    这也导致 Swarm 的 join 令牌发生变化。之前的 join 令牌将不再有效。

从此以后，颁发的所有新节点证书都由新根 CA 签署，且不包含任何中间证书。

## 了解更多

* 阅读关于 [节点 (nodes)](nodes.md) 如何工作的信息。
* 了解 Swarm 模式 [服务 (services)](services.md) 如何工作。
