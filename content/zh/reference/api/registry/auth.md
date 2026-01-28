---
title: Registry 认证
description: "指定 Docker Registry v2 认证"
keywords: registry, images, tags, repository, distribution, Bearer authentication, advanced
---

本文档概述了 registry 认证方案：

![v2 registry 认证](./images/v2-registry-auth.png)

1. 尝试与 registry 开始推/拉操作。
2. 如果 registry 需要授权，它将返回包含如何进行身份验证信息的 `401 Unauthorized` HTTP 响应。
3. registry 客户端向授权服务请求 Bearer 令牌。
4. 授权服务返回一个不透明的 Bearer 令牌，代表客户端的授权访问。
5. 客户端使用嵌入在请求 Authorization 标头中的 Bearer 令牌重试原始请求。
6. Registry 通过验证 Bearer 令牌及其嵌入的声明集来授权客户端，并像往常一样开始推/拉会话。

## 要求

- 能够理解并响应资源服务器返回的令牌认证挑战的 Registry 客户端。
- 能够管理其托管在任何给定服务（例如 Docker Registry 中的仓库）上的资源的访问控制的授权服务器。
- 一个 Docker Registry，能够信任授权服务器签名的令牌，客户端可以使用该令牌进行授权，并能够在一次性使用或在足够短的时间内验证这些令牌。

## 授权服务器端点描述

所描述的服务器旨在充当由其他服务托管的资源的独立访问控制管理器，这些服务希望使用单独的访问控制管理器进行身份验证和管理授权。

官方 Docker Registry 使用此类服务来对客户端进行身份验证，并验证其对 Docker 镜像仓库的授权。

从 Docker 1.6 开始，Docker 引擎中的 registry 客户端已更新为处理此类授权工作流。

## 如何进行身份验证

Registry V1 客户端首先联系索引以发起推送或拉取。在 Registry V2 工作流下，客户端应首先联系 registry。如果 registry 服务器需要身份验证，它将返回带有 `WWW-Authenticate` 标头的 `401 Unauthorized` 响应，详细说明如何向此 registry 进行身份验证。

例如，假设我（用户名 `jlhawn`）正试图将镜像推送到仓库 `samalba/my-app`。为了让 registry 授权此操作，我需要对 `samalba/my-app` 仓库拥有 `push` 访问权限。registry 将首先返回此响应：

```text
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Docker-Distribution-Api-Version: registry/2.0
Www-Authenticate: Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"
Date: Thu, 10 Sep 2015 19:32:31 GMT
Content-Length: 235
Strict-Transport-Security: max-age=31536000

{"errors":[{"code":"UNAUTHORIZED","message":"access to the requested resource is not authorized","detail":[{"Type":"repository","Name":"samalba/my-app","Action":"pull"},{"Type":"repository","Name":"samalba/my-app","Action":"push"}]}]}
```

请注意指示认证挑战的 HTTP 响应标头：

```text
Www-Authenticate: Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"
```

此格式记录在 [RFC 6750 第 3 节：OAuth 2.0 授权框架：Bearer 令牌使用](https://tools.ietf.org/html/rfc6750#section-3) 中。

此挑战表明 registry 需要由指定令牌服务器颁发的令牌，并且客户端尝试的请求将需要在其声明集中包含足够的访问条目。为了响应此挑战，客户端需要使用来自 `WWW-Authenticate` 标头的 `service` 和 `scope` 值向 URL `https://auth.docker.io/token` 发出 `GET` 请求。

## 请求令牌

定义使用令牌端点获取 bearer 和刷新令牌。

### 查询参数

#### `service`

托管资源的服务名称。

#### `offline_token`

是否连同 bearer 令牌一起返回刷新令牌。刷新令牌能够为具有不同作用域的同一主体获取额外的 bearer 令牌。刷新令牌没有过期时间，对客户端来说应被视为完全不透明。

#### `client_id`

标识客户端的字符串。此 `client_id` 不需要向授权服务器注册，但应设置为有意义的值，以便允许审计由未注册客户端创建的密钥。接受的语法定义在 [RFC6749 附录 A.1](https://tools.ietf.org/html/rfc6749#appendix-A.1) 中。

#### `scope`

有问题的资源，格式化为前面显示的 `WWW-Authenticate` 标头中的 `scope` 参数的空格分隔条目之一。如果 `WWW-Authenticate` 标头中有多个 `scope` 条目，则应多次指定此查询参数。前面的示例将指定为：`scope=repository:samalba/my-app:push`。scope 字段可以为空，以请求刷新令牌，而不向返回的 bearer 令牌提供任何资源权限。

### 令牌响应字段

#### `token`

客户端应在 `Authorization` 标头中的后续请求中提供的不透明 `Bearer` 令牌。

#### `access_token`

为了与 OAuth 2.0 兼容，也接受名称 `access_token` 下的 `token`。必须指定这些字段中的至少一个，但也可以同时出现（为了与旧客户端兼容）。当同时指定时，它们应该是等效的；如果它们不同，则客户端的选择未定义。

#### `expires_in`

（可选）自令牌颁发以来保持有效的持续时间（以秒为单位）。省略时，默认为 60 秒。为了与旧客户端兼容，返回的令牌寿命不应少于 60 秒。

#### `issued_at`

（可选）给定令牌颁发时的 [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) 序列化 UTC 标准时间。如果省略 `issued_at`，则过期时间从令牌交换完成时开始计算。

#### `refresh_token`

（可选）可用于为具有不同作用域的同一主体获取额外访问令牌的令牌。此令牌应由客户端保持安全，并且仅发送到颁发 bearer 令牌的授权服务器。只有在请求中提供了 `offline_token=true` 时，才会设置此字段。

### 示例

对于此示例，客户端向以下 URL 发出 HTTP GET 请求：

```text
https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull,push
```

令牌服务器应首先尝试使用请求提供的任何身份验证凭据对客户端进行身份验证。从 Docker 1.11 开始，Docker 引擎支持基本身份验证和 OAuth2 获取令牌。Docker 1.10 及之前版本，Docker 引擎中的 registry 客户端仅支持基本身份验证。如果尝试向令牌服务器进行身份验证失败，令牌服务器应返回 `401 Unauthorized` 响应，指示提供的凭据无效。

令牌服务器是否需要身份验证取决于该访问控制提供者的策略。某些请求可能需要身份验证才能确定访问权限（例如推送或拉取私有仓库），而其他请求则可能不需要（例如从公共仓库拉取）。

在对客户端进行身份验证（如果未尝试进行身份验证，则可能只是匿名客户端）之后，令牌服务器接下来必须查询其访问控制列表以确定客户端是否具有请求的作用域。在这个示例请求中，如果我已作为用户 `jlhawn` 进行身份验证，令牌服务器将确定我对实体 `registry.docker.io` 托管的仓库 `samalba/my-app` 拥有什么访问权限。

一旦令牌服务器确定了客户端对 `scope` 参数中请求的资源的访问权限，它将取每个资源上请求的操作集与客户端实际上已被授予的操作集的交集。如果客户端仅拥有请求访问权限的子集，**这一定不被视为错误**，因为在工作流的这一部分指示授权错误不是令牌服务器的责任。

继续示例请求，令牌服务器将发现客户端对仓库的授予访问权限集为 `[pull, push]`，当与请求的访问权限 `[pull, push]` 相交时，产生相等的集合。如果发现授予的访问权限集仅为 `[pull]`，则相交集将仅为 `[pull]`。如果客户端对仓库没有访问权限，则相交集将为空 `[]`。

正是这个相交的访问权限集被放置在返回的令牌中。

然后，服务器构造一个包含此相交访问权限集的特定于实现的令牌，并将其返回给 Docker 客户端，以用于向受众服务进行身份验证（在指示的时间窗口内）：

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IlBZWU86VEVXVTpWN0pIOjI2SlY6QVFUWjpMSkMzOlNYVko6WEdIQTozNEYyOjJMQVE6WlJNSzpaN1E2In0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJqbGhhd24iLCJhdWQiOiJyZWdpc3RyeS5kb2NrZXIuY29tIiwiZXhwIjoxNDE1Mzg3MzE1LCJuYmYiOjE0MTUzODcwMTUsImlhdCI6MTQxNTM4NzAxNSwianRpIjoidFlKQ08xYzZjbnl5N2tBbjBjN3JLUGdiVjFIMWJGd3MiLCJhY2Nlc3MiOlt7InR5cGUiOiJyZXBvc2l0b3J5IiwibmFtZSI6InNhbWFsYmEvbXktYXBwIiwiYWN0aW9ucyI6WyJwdXNoIl19XX0.QhflHPfbd6eVF4lM9bwYpFZIV0PfikbyXuLx959ykRTBpe3CYnzs6YBK8FToVb5R47920PVLrh8zuLzdCr9t3w", "expires_in": 3600,"issued_at": "2009-11-10T23:00:00Z"}
```

## 使用 Bearer 令牌

一旦客户端有了令牌，它将再次尝试 registry 请求，并将令牌放置在 HTTP `Authorization` 标头中，如下所示：

```text
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IkJWM0Q6MkFWWjpVQjVaOktJQVA6SU5QTDo1RU42Ok40SjQ6Nk1XTzpEUktFOkJWUUs6M0ZKTDpQT1RMIn0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJCQ0NZOk9VNlo6UUVKNTpXTjJDOjJBVkM6WTdZRDpBM0xZOjQ1VVc6NE9HRDpLQUxMOkNOSjU6NUlVTCIsImF1ZCI6InJlZ2lzdHJ5LmRvY2tlci5jb20iLCJleHAiOjE0MTUzODczMTUsIm5iZiI6MTQxNTM4NzAxNSwiaWF0IjoxNDE1Mzg3MDE1LCJqdGkiOiJ0WUpDTzFjNmNueXk3a0FuMGM3cktQZ2JWMUgxYkZ3cyIsInNjb3BlIjoiamxoYXduOnJlcG9zaXRvcnk6c2FtYWxiYS9teS1hcHA6cHVzaCxwdWxsIGpsaGF3bjpuYW1lc3BhY2U6c2FtYWxiYTpwdWxsIn0.Y3zZSwaZPqy4y9oRBVRImZyv3m_S9XDHF1tWwN7mL52C_IiA73SJkWVNsvNqpJIn5h7A2F8biv_S2ppQ1lgkbw
```

这也描述在 [RFC 6750 第 2.1 节：OAuth 2.0 授权框架：Bearer 令牌使用](https://tools.ietf.org/html/rfc6750#section-2.1) 中
