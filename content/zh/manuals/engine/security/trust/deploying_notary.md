---
description: 部署 Notary
keywords: trust, security, notary, deployment, 信任, 安全, 部署
title: 使用 Compose 部署 Notary 服务器
---

部署 Notary 服务器最简单的方法是使用 Docker Compose。要执行本页中的步骤，您必须已经 [安装了 Docker Compose](/manuals/compose/install/_index.md)。

1. 克隆 Notary 仓库。
   
   ```console
   $ git clone https://github.com/theupdateframework/notary.git
   ```

2. 使用示例证书构建并启动 Notary 服务器。

   ```console
   $ docker compose up -d 
   ```

   有关如何部署 Notary 服务器的更详细文档，请参阅 [运行 Notary 服务的说明](https://github.com/theupdateframework/notary/blob/master/docs/running_a_service.md) 以及 [Notary 仓库](https://github.com/theupdateframework/notary) 以获取更多信息。

3. 在尝试与 Notary 服务器交互之前，确保您的 Docker 或 Notary 客户端信任 Notary 服务器的证书。

根据您使用的客户端，请参阅 [Docker](/reference/cli/docker/#notary) 或 [Notary](https://github.com/docker/notary#using-notary) 的说明。

## 如果您想在生产环境中使用 Notary

在 Notary 服务器发布官方稳定版本后，请返回此处查看说明。要提前了解在生产环境中部署 Notary 的信息，请参阅 [Notary 仓库](https://github.com/theupdateframework/notary)。
