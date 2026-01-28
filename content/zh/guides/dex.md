---
title: 使用 Dex 在测试中模拟 OAuth 服务
description: &desc 使用 Dex 在测试中模拟 OAuth 服务
keywords: Dex, container-supported development
linktitle: 使用 Dex 模拟 OAuth 服务
summary: *desc
tags: [app-dev, distributed-systems]
languages: []
params:
  time: 10 minutes
---

Dex 是一个开源的 OpenID Connect（OIDC）和 OAuth 2.0 身份提供者，可以配置为针对各种后端身份提供者进行身份认证，如 LDAP、SAML 和 OAuth。在 Docker 容器中运行 Dex 允许开发人员模拟 OAuth 2.0 服务器以用于测试和开发目的。本指南将引导您使用 Docker 容器设置 Dex 作为 OAuth 模拟服务器。

如今 OAuth 是 Web 服务中首选的身份认证方式，大多数服务都提供使用流行的 OAuth 服务（如 GitHub、Google 或 Apple）进行访问的可能性。使用 OAuth 可以保证更高的安全性和简化性，因为无需为每个服务创建新的配置文件。这意味着，通过允许应用程序代表用户访问资源而无需共享密码，OAuth 最大限度地降低了凭据暴露的风险。

在本指南中，您将学习如何：

- 使用 Docker 启动 Dex 容器。
- 在 GitHub Action（GHA）中使用模拟 OAuth，而无需依赖外部 OAuth 提供者。

## 在 Docker 中使用 Dex

[Dex 的官方 Docker 镜像](https://hub.docker.com/r/dexidp/dex/)提供了一种便捷的方式来部署和管理 Dex 实例。Dex 可用于各种 CPU 架构，包括 amd64、armv7 和 arm64，确保与不同设备和平台的兼容性。您可以在 [Dex 文档网站](https://dexidp.io/docs/getting-started/)上了解更多关于 Dex 独立运行的信息。

### 前提条件

[Docker Compose](/compose/)：推荐用于管理多容器 Docker 应用程序。

### 使用 Docker 设置 Dex

首先为您的 Dex 项目创建一个目录：

```bash
mkdir dex-mock-server
cd dex-mock-server
```
使用以下结构组织您的项目：

```bash
dex-mock-server/
├── config.yaml
└── compose.yaml
```

创建 Dex 配置文件：
config.yaml 文件定义了 Dex 的设置，包括连接器、客户端和存储。对于模拟服务器设置，您可以使用以下最小配置：

```yaml
# config.yaml
issuer: http://localhost:5556/dex
storage:
  type: memory
web:
  http: 0.0.0.0:5556
staticClients:
  - id: example-app
    redirectURIs:
      - 'http://localhost:5555/callback'
    name: 'Example App'
    secret: ZXhhbXBsZS1hcHAtc2VjcmV0
enablePasswordDB: true
staticPasswords:
  - email: "admin@example.com"
    hash: "$2a$10$2b2cU8CPhOTaGrs1HRQuAueS7JTT5ZHsHSzYiFPm1leZck7Mc8T4W"
    username: "admin"
    userID: "1234"
```

说明：
- issuer：Dex 的公共 URL。

- storage：为简单起见使用内存存储。

- web：Dex 将在端口 5556 上监听。

- staticClients：定义一个客户端应用程序（example-app）及其重定向 URI 和密钥。

- enablePasswordDB：启用静态密码身份认证。

- staticPasswords：定义用于身份认证的静态用户。hash 是密码的 bcrypt 哈希值。

> [!NOTE]
>
> 确保 hash 是您所需密码的有效 bcrypt 哈希值。您可以使用 [bcrypt-generator.com](https://bcrypt-generator.com/) 等工具生成此值。
或使用 CLI 工具如 [htpasswd](https://httpd.apache.org/docs/2.4/programs/htpasswd.html)，如以下示例：`echo password | htpasswd -BinC 10 admin | cut -d: -f2`

配置好 Docker Compose 后，启动 Dex：
```yaml
# docker-compose.yaml

services:
  dex:
    image: dexidp/dex:latest
    container_name: dex
    ports:
      - "5556:5556"
    volumes:
      - ./config.yaml:/etc/dex/config.yaml
    command: ["dex", "serve", "/etc/dex/config.yaml"]
```

现在可以使用 `docker compose` 命令运行容器。
```bash
docker compose up -d
```

此命令将下载 Dex Docker 镜像（如果尚不可用）并在分离模式下启动容器。


要验证 Dex 正在运行，请检查日志以确保 Dex 成功启动：
```bash
docker compose logs -f dex
```
您应该看到指示 Dex 正在指定端口上监听的输出。

### 在 GHA 中使用 Dex OAuth 测试

要测试 OAuth 流程，您需要一个配置为针对 Dex 进行身份认证的客户端应用程序。最典型的用例之一是在 GitHub Actions 中使用它。由于 Dex 支持模拟身份认证，您可以按照[文档](https://dexidp.io/docs)中的建议预定义测试用户。`config.yaml` 文件应如下所示：

```yaml
issuer: http://127.0.0.1:5556/dex

storage:
  type: memory

web:
  http: 0.0.0.0:5556

oauth2:
  skipApprovalScreen: true

staticClients:
  - name: TestClient
    id: client_test_id
    secret: client_test_secret
    redirectURIs:
      - http://{ip-your-app}/path/to/callback/ # 示例：http://localhost:5555/callback

connectors:
# mockCallback 连接器始终返回用户 'kilgore@kilgore.trout'。
- type: mockCallback
  id: mock
  name: Mock
```
现在您可以在 `~/.github/workflows/ci.yaml` 文件中插入 Dex 服务：

```yaml
[...]
jobs:
  test-oauth:
    runs-on: ubuntu-latest
    steps:
      - name: Install Dex
        run: |
          curl -L https://github.com/dexidp/dex/releases/download/v2.37.0/dex_linux_amd64 -o dex
          chmod +x dex

      - name: Start Dex Server
        run: |
          nohup ./dex serve config.yaml > dex.log 2>&1 &
          sleep 5  # 给 Dex 一些启动时间
[...]
```


### 结论

通过遵循本指南，您已经使用 Docker 设置了 Dex 作为 OAuth 模拟服务器。此设置对于测试和开发非常有价值，允许您在不依赖外部身份提供者的情况下模拟 OAuth 流程。有关更高级的配置和集成，请参阅 [Dex 文档](https://dexidp.io/docs/)。
