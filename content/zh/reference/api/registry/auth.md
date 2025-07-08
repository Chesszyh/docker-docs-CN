---
title: 注册表认证
description: "指定 Docker Registry v2 认证"
keywords: 注册表, 镜像, 标签, 仓库, 分发, Bearer 认证, 高级
---

本文档概述了注册表认证方案：

![v2 registry auth](./images/v2-registry-auth.png)

1. 尝试与注册表开始推送/拉取操作。
2. 如果注册表需要授权，它将返回 `401 Unauthorized` HTTP 响应，其中包含如何认证的信息。
3. 注册表客户端向授权服务请求 Bearer 令牌。
4. 授权服务返回一个不透明的 Bearer 令牌，表示客户端的授权访问。
5. 客户端使用嵌入在请求的 Authorization 头中的 Bearer 令牌重试原始请求。
6. 注册表通过验证 Bearer 令牌及其嵌入的声明集来授权客户端，并像往常一样开始推送/拉取会话。

## 要求

- 能够理解并响应资源服务器返回的令牌认证挑战的注册表客户端。
- 能够管理由任何给定服务（例如 Docker Registry 中的仓库）托管的资源的访问控制的授权服务器。
- 能够信任授权服务器签署令牌的 Docker Registry，客户端可以使用这些令牌进行授权，并能够在单次使用或足够短的时间内验证这些令牌。

## 授权服务器端点描述

所描述的服务器旨在作为独立访问控制管理器，用于托管在其他服务中的资源，这些服务希望使用单独的访问控制管理器进行认证和管理授权。

官方 Docker Registry 使用此类服务来认证客户端并验证其对 Docker 镜像仓库的授权。

截至 Docker 1.6，Docker Engine 中的注册表客户端已更新，以处理此类授权工作流。

## 如何认证

Registry V1 客户端首先联系索引以启动推送或拉取。在 Registry V2 工作流下，客户端应首先联系注册表。如果注册表服务器需要认证，它将返回 `401 Unauthorized` 响应，其中包含 `WWW-Authenticate` 头，详细说明如何向此注册表进行认证。

例如，假设我（用户名 `jlhawn`）正在尝试将镜像推送到仓库 `samalba/my-app`。为了让注册表授权此操作，我需要对 `samalba/my-app` 仓库具有 `push` 访问权限。注册表将首先返回此响应：

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

请注意指示认证挑战的 HTTP 响应头：

```text
Www-Authenticate: Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"
```

此格式在 [RFC 6750 第 3 节：OAuth 2.0 授权框架：Bearer 令牌使用](https://tools.ietf.org/html/rfc6750#section-3) 中有详细说明。

此挑战表明注册表需要由指定令牌服务器颁发的令牌，并且客户端正在尝试的请求需要在其声明集中包含足够的访问条目。为了响应此挑战，客户端需要使用 `WWW-Authenticate` 头中的 `service` 和 `scope` 值向 URL `https://auth.docker.io/token` 发出 `GET` 请求。

## 请求令牌

定义使用令牌端点获取 Bearer 和刷新令牌。

### 查询参数

#### `service`

托管资源的服务的名称。

#### `offline_token`

是否与 Bearer 令牌一起返回刷新令牌。刷新令牌能够为具有不同范围的同一主体获取额外的 Bearer 令牌。刷新令牌没有过期时间，应被客户端视为完全不透明。

#### `client_id`

标识客户端的字符串。此 `client_id` 不需要向授权服务器注册，但应设置为有意义的值，以便允许审计由未注册客户端创建的密钥。接受的语法在 [RFC6749 附录 A.1](https://tools.ietf.org/html/rfc6749#appendix-A.1) 中定义。

#### `scope`

所讨论的资源，格式为前面所示的 `WWW-Authenticate` 头中 `scope` 参数的空格分隔条目之一。如果 `WWW-Authenticate` 头中有多个 `scope` 条目，则应多次指定此查询参数。前面的示例将指定为：`scope=repository:samalba/my-app:push`。`scope` 字段可以为空，以请求刷新令牌，而不向返回的 Bearer 令牌提供任何资源权限。

### 令牌响应字段

#### `token`

一个不透明的 `Bearer` 令牌，客户端应在后续请求中在 `Authorization` 头中提供该令牌。

#### `access_token`

为了与 OAuth 2.0 兼容，也接受名为 `access_token` 的 `token`。必须指定这些字段中的至少一个，但也可以同时出现（为了与旧客户端兼容）。当两者都指定时，它们应该等效；如果它们不同，则客户端的选择未定义。

#### `expires_in`

（可选）自令牌颁发以来，令牌将保持有效的持续时间（以秒为单位）。如果省略，则默认为 60 秒。为了与旧客户端兼容，令牌的有效期不应少于 60 秒。

#### `issued_at`

（可选）给定令牌颁发时的 [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) 序列化 UTC 标准时间。如果省略 `issued_at`，则过期时间从令牌交换完成时开始计算。

#### `refresh_token`

（可选）可用于为具有不同范围的同一主体获取额外访问令牌的令牌。此令牌应由客户端安全保存，并且只能发送给颁发 Bearer 令牌的授权服务器。此字段仅在请求中提供 `offline_token=true` 时设置。

### 示例

在此示例中，客户端向以下 URL 发出 HTTP GET 请求：

```text
https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull,push
```

令牌服务器应首先尝试使用请求中提供的任何认证凭据来认证客户端。从 Docker 1.11 开始，Docker Engine 支持 Basic Authentication 和 OAuth2 来获取令牌。Docker 1.10 及更早版本中，Docker Engine 中的注册表客户端仅支持 Basic Authentication。如果尝试向令牌服务器进行认证失败，令牌服务器应返回 `401 Unauthorized` 响应，表明提供的凭据无效。

令牌服务器是否需要认证取决于该访问控制提供商的策略。某些请求可能需要认证才能确定访问权限（例如推送或拉取私有仓库），而其他请求可能不需要（例如从公共仓库拉取）。

认证客户端后（如果未尝试认证，则可能只是匿名客户端），令牌服务器接下来必须查询其访问控制列表，以确定客户端是否具有请求的范围。在此示例请求中，如果我已认证为用户 `jlhawn`，则令牌服务器将确定我对实体 `registry.docker.io` 托管的仓库 `samalba/my-app` 具有哪些访问权限。

一旦令牌服务器确定客户端对 `scope` 参数中请求的资源具有哪些访问权限，它将获取每个资源上请求的操作集与客户端实际被授予的操作集的交集。如果客户端只拥有请求访问权限的子集，**则不应将其视为错误**，因为在此工作流中，令牌服务器没有责任指示授权错误。

继续示例请求，令牌服务器将发现客户端对仓库的授予访问权限集为 `[pull, push]`，当与请求的访问权限 `[pull, push]` 相交时，会产生一个相等的集合。如果发现授予的访问权限集仅为 `[pull]`，则交集集将仅为 `[pull]`。如果客户端对仓库没有访问权限，则交集集将为空，即 `[]`。

正是这个访问权限的交集集被放置在返回的令牌中。

然后，服务器使用此交集访问权限集构建一个特定于实现的令牌，并将其返回给 Docker 客户端，以便在指定的时间窗口内用于向受众服务进行认证：

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IlBZWU86VEVXVTpWN0pIOjI2SlY6QVFUWjpMSkMzOlNYVko6WEdIQTozNEYyOjJMQVE6WlJNSzpaN1E2In0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJqbGhhd24iLCJhdWQiOiJyZWdpc3RyeS5kb2NrZXIuY29tIiwiZXhwIjoxNDE1Mzg3MzE1LCJuYmYiOjE0MTUzODcwMTUsImlhdCI6MTQxNTM4NzAxNSwianRpIjoidFJKQ08xYzZjbnl5N2tBbjBjN3JLUGdiVjFIMWJGd3MiLCJhY2Nlc3MiOlt7InR5cGUiOiJyZXBvc2l0b3J5IiwibmFtZSI6InNhbWFsYmEvbXktYXBwIiwiYWN0aW9ucyI6WyJwdXNoIl19XX0.QhflHPfbd6eVF4lM9bwYpFZIV0PfikbyXuLx959ykRTBpe3CYnzs6YBK8FToVb5R47920PVLrh8zuLzdCr9t3w", "expires_in": 3600,"issued_at": "2009-11-10T23:00:00Z"}
```

## 使用 Bearer 令牌

客户端获得令牌后，它将再次尝试注册表请求，并将令牌放置在 HTTP `Authorization` 头中，如下所示：

```text
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IkJWM0Q6MkFWWjpVQjVaOktJQVA6SU5QTDo1RU42Ok40SjQ6Nk1XTzpEUktFOkJWUUs6M0ZKTDpQT1RMIn0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJCQ0NZOk9VNlo6UUVKNTpXTjJDOjJBVkM6WTdZRDpBM0xZOjQ1VVc6NE9HRDpLQUxMOkNOSjU6NUlVTCIsImF1ZCI6InJlZ2lzdHJ5LmRvY2tlci5jb20iLCJleHAiOjE0MTUzODczMTUsIm5iZiI6MTQxNTM4NzAxNSwiaWF0IjoxNDE1Mzg3MDE1LCJqdGkiOiJ0WUpDTzFjNmNueXk3a0FuMGM3cktQZ2JWMUgxYkZ3cyIsInNjb3BlIjoiamxoYXduOnJlcG9zaXRvcnk6c2FtYWxiYS9teS1hcHA6cHVzaCxwdWxsIGpsaGF3bjpuYW1lc3BhY2U6c2FtYWxiYTpwdWxsIn0.Y3zZSwaZPqy4y9oRBVRImZyv3m_S9XDHF1tWwN7mL52C_IiA73SJkWVNsvNqpJIn5h7A2F8biv_S2ppQ1lgkbw
```

这也在 [RFC 6750 第 2.1 节：OAuth 2.0 授权框架：Bearer 令牌使用](https://tools.ietf.org/html/rfc6750#section-2.1) 中有所描述。