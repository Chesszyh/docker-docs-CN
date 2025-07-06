---
title: 在测试中使用 Dex 模拟 OAuth 服务
description: &desc 在测试中使用 Dex 模拟 OAuth 服务
keywords: Dex, 容器支持的开发
linktitle: 使用 Dex 模拟 OAuth 服务
summary: *desc
tags: [app-dev, distributed-systems]
languages: []
params:
  time: 10 分钟
---

Dex 是一个开源的 OpenID Connect (OIDC) 和 OAuth 2.0 身份提供程序，可以配置为针对各种后端身份提供程序（例如 LDAP、SAML 和 OAuth）进行身份验证。在 Docker 容器中运行 Dex 允许开发人员模拟 OAuth 2.0 服务器以进行测试和开发。本指南将引导您使用 Docker 容器将 Dex 设置为 OAuth 模拟服务器。

如今，OAuth 是 Web 服务中身份验证的首选，其中大部分都提供了使用 GitHub、Google 或 Apple 等流行 OAuth 服务进行访问的可能性。使用 OAuth 可确保更高级别的安全性和简化性，因为无需为每个服务创建新的配置文件。这意味着，通过允许应用程序代表用户访问资源而无需共享密码，OAuth 最大限度地降低了凭据泄露的风险。

在本指南中，您将学习如何：

- 使用 Docker 启动 Dex 容器。
- 在 GitHub Action (GHA) 中使用模拟 OAuth，而无需依赖外部 OAuth 提供程序。

## 将 Dex 与 Docker 结合使用

[Dex 的官方 Docker 镜像](https://hub.docker.com/r/dexidp/dex/) 提供了一种方便的方式来部署和管理 Dex 实例。Dex 适用于各种 CPU 架构，包括 amd64、armv7 和 arm64，确保与不同设备和平台的兼容性。您可以在 [Dex 文档站点](https://dexidp.io/docs/getting-started/) 上了解有关 Dex 独立的更多信息。

### 先决条件

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
`config.yaml` 文件定义了 Dex 的设置，包括连接器、客户端和存储。对于模拟服务器设置，您可以使用以下最小配置：

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
- `issuer`：Dex 的公共 URL。

- `storage`：为简单起见，使用内存存储。

- `web`：Dex 将在端口 5556 上侦听。

- `staticClients`：定义一个客户端应用程序 (`example-app`) 及其重定向 URI 和密钥。

- `enablePasswordDB`：启用静态密码身份验证。

- `staticPasswords`：定义一个用于身份验证的静态用户。哈希是密码的 bcrypt 哈希。

> [!NOTE]
>
> 确保哈希是您所需密码的有效 bcrypt 哈希。您可以使用 [bcrypt-generator.com](https://bcrypt-generator.com/) 等工具生成此哈希。
或使用像 [htpasswd](https://httpd.apache.org/docs/2.4/programs/htpasswd.html) 这样的 CLI 工具，如以下示例所示：`echo password | htpasswd -BinC 10 admin | cut -d: -f2`

配置 Docker Compose 后，启动 Dex：
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

此命令将下载 Dex Docker 镜像（如果尚不可用）并以分离模式启动容器。


要验证 Dex 是否正在运行，请检查日志以确保 Dex 已成功启动：
```bash
docker compose logs -f dex
```
您应该会看到指示 Dex 正在指定端口上侦听的输出。

### 在 GHA 中使用 Dex OAuth 测试

要测试 OAuth 流程，您需要一个配置为针对 Dex 进行身份验证的客户端应用程序。最典型的用例之一是在 GitHub Actions 中使用它。由于 Dex 支持模拟身份验证，因此您可以按照[文档](https://dexidp.io/docs)中的建议预定义测试用户。`config.yaml` 文件应如下所示：

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
# mockCallback 连接器始终返回用户“kilgore@kilgore.trout”。
- type: mockCallback
  id: mock
  name: Mock
```
现在，您可以将 Dex 服务插入到您的 `~/.github/workflows/ci.yaml` 文件中：

```yaml
[...]
jobs:
  test-oauth:
    runs-on: ubuntu-latest
    steps:
      - name: 安装 Dex
        run: |
          curl -L https://github.com/dexidp/dex/releases/download/v2.37.0/dex_linux_amd64 -o dex
          chmod +x dex

      - name: 启动 Dex 服务器
        run: |
          nohup ./dex serve config.yaml > dex.log 2>&1 &
          sleep 5  # 给 Dex 一点时间启动
[...]
```


### 结论

通过遵循本指南，您已使用 Docker 将 Dex 设置为 OAuth 模拟服务器。此设置对于测试和开发非常宝贵，可让您模拟 OAuth 流程，而无需依赖外部身份提供程序。有关更高级的配置和集成，请参阅 [Dex 文档](https://dexidp.io/docs/)。
