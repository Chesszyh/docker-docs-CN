---
title: Registry 认证
description: "指定 Docker Registry v2 认证规范"
keywords: registry, images, tags, repository, distribution, Bearer authentication, advanced, 注册中心, 镜像, 标签, 仓库, 分发, 承载认证, 高级
---

本文档概述了 registry 认证方案：

![v2 registry auth](./images/v2-registry-auth.png)

1. 尝试向 registry 发起推送（push）或拉取（pull）操作。
2. 如果 registry 需要授权，它将返回 `401 Unauthorized` HTTP 响应，并附带如何进行认证的信息。
3. registry 客户端向认证服务请求 Bearer 令牌。
4. 认证服务返回一个不透明的 Bearer 令牌，代表客户端的授权访问权限。
5. 客户端使用嵌入在请求的 `Authorization` 头部中的 Bearer 令牌重试原始请求。
6. Registry 通过验证 Bearer 令牌及其嵌入的声明集（claim set）来对客户端进行授权，并像往常一样开始推送/拉取会话。

## 要求

- 能够理解并响应资源服务器返回的令牌认证质询的 Registry 客户端。
- 能够管理由任何给定服务（例如 Docker Registry 中的仓库）托管的资源访问控制的授权服务器。
- 能够信任授权服务器签发的、供客户端用于授权的令牌的 Docker Registry，并具备验证这些令牌以便单次使用或在足够短的时间内使用的能力。

## 授权服务器端点说明

所描述的服务器旨在作为独立访问控制管理器，用于管理由其他服务托管的资源，这些服务希望使用独立的访问控制管理器进行认证和授权管理。

官方 Docker Registry 使用此类服务来认证客户端并验证其对 Docker 镜像仓库的授权。

自 Docker 1.6 起，Docker Engine 中的 registry 客户端已更新，以处理此类授权工作流程。

## 如何进行认证

Registry V1 客户端首先联系索引（index）以启动推送或拉取。在 Registry V2 工作流程下，客户端应首先联系 registry。如果 registry 服务器需要认证，它将返回 `401 Unauthorized` 响应，并带有 `WWW-Authenticate` 头部，详细说明如何向此 registry 进行认证。

例如，假设我（用户名 `jlhawn`）正尝试将镜像推送到仓库 `samalba/my-app`。为了让 registry 授权此操作，我需要对 `samalba/my-app` 仓库具有 `push` 权限。registry 将首先返回此响应：

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

注意指示认证质询的 HTTP 响应头：

```text
Www-Authenticate: Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"
```

此格式记录在 [RFC 6750 第 3 节：The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://tools.ietf.org/html/rfc6750#section-3) 中。

此质询表明 registry 需要由指定的令牌服务器签发的令牌，并且客户端尝试的请求需要在其声明集中包含足够的访问条目。为了响应此质询，客户端需要使用 `WWW-Authenticate` 头部中的 `service` 和 `scope` 值对 URL `https://auth.docker.io/token` 发起 `GET` 请求。

## 请求令牌

定义了使用令牌端点获取 bearer 令牌和 refresh 令牌。

### 查询参数

#### `service`

托管资源的服务的名称。

#### `offline_token`

是否随 bearer 令牌一起返回 refresh 令牌。refresh 令牌能够为同一主体获取具有不同范围的其他 bearer 令牌。refresh 令牌没有过期时间，客户端应将其视为完全不透明。

#### `client_id`

标识客户端的字符串。此 `client_id` 不需要向授权服务器注册，但应设置为有意义的值，以便对未注册客户端创建的密钥进行审计。接受的语法定义在 [RFC6749 附录 A.1](https://tools.ietf.org/html/rfc6749#appendix-A.1) 中。

#### `scope`

所涉及的资源，格式为前面显示的 `WWW-Authenticate` 头部中 `scope` 参数中由空格分隔的条目之一。如果 `WWW-Authenticate` 头部中有多个 `scope` 条目，则应多次指定此查询参数。前面的示例将指定为：`scope=repository:samalba/my-app:push`。scope 字段可以为空，以请求 refresh 令牌而不向返回的 bearer 令牌提供任何资源权限。

### 令牌响应字段

#### `token`

客户端在随后的请求中应在 `Authorization` 头部提供的、不透明的 `Bearer` 令牌。

#### `access_token`

为了与 OAuth 2.0 兼容，也接受名为 `access_token` 的 `token`。必须至少指定其中一个字段，但两者也可能同时出现（为了与旧版本客户端兼容）。当两者都指定时，它们应该是等效的；如果不同，客户端的选择是未定义的。

#### `expires_in`

（可选）令牌自签发以来的有效时长（以秒为单位）。如果省略，默认为 60 秒。为了与旧版本客户端兼容，返回的令牌有效期不应少于 60 秒。

#### `issued_at`

（可选）签发给定令牌的 [RFC3339](https://www.ietf.org/rfc/rfc3339.txt) 序列化 UTC 标准时间。如果省略 `issued_at`，则过期时间从令牌交换完成时算起。

#### `refresh_token`

（可选）可用于为同一主体获取具有不同范围的其他访问令牌的令牌。此令牌应由客户端安全保管，并且仅发送给签发 bearer 令牌的授权服务器。仅当请求中提供了 `offline_token=true` 时，才会设置此字段。

### 示例

在此示例中，客户端向以下 URL 发起 HTTP GET 请求：

```text
https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull,push
```

令牌服务器应首先尝试使用请求中提供的任何认证凭据来认证客户端。从 Docker 1.11 开始，Docker Engine 同时支持 Basic Authentication 和 OAuth2 来获取令牌。Docker 1.10 及以前版本中，Docker Engine 中的 registry 客户端仅支持 Basic Authentication。如果向令牌服务器进行的认证尝试失败，令牌服务器应返回 `401 Unauthorized` 响应，表明提供的凭据无效。

令牌服务器是否需要认证取决于该访问控制提供商的策略。某些请求可能需要认证来确定访问权限（例如推送或拉取私有仓库），而其他请求则可能不需要（例如从公共仓库拉取）。

在认证客户端之后（如果没有尝试认证，则可能仅仅是匿名客户端），令牌服务器接下来必须查询其访问控制列表，以确定客户端是否具有请求的范围（scope）。在此示例请求中，如果我已认证为用户 `jlhawn`，令牌服务器将确定我对实体 `registry.docker.io` 托管的仓库 `samalba/my-app` 具有何种访问权限。

一旦令牌服务器确定了客户端对 `scope` 参数中请求的资源具有何种访问权限，它将获取每个资源上请求的操作集与客户端实际被授予的操作集的交集。如果客户端仅具有所请求访问权限的子集，**绝不能将其视为错误**，因为在这种工作流中，指示授权错误并非令牌服务器的责任。

继续示例请求，令牌服务器将发现客户端被授予的仓库访问权限集为 `[pull, push]`，当与请求的访问权限集 `[pull, push]` 求交集时，得到一个相等的集合。如果发现被授予的访问权限集仅为 `[pull]`，那么求交集后的集合将仅为 `[pull]`。如果客户端对仓库没有访问权限，那么求交集后的集合将为空 `[]`。

正是这个求交集后的访问权限集被放置在返回的令牌中。

然后，服务器使用此求交集后的访问权限集构造一个特定于实现的令牌，并将其返回给 Docker 客户端，供其用于向受众服务进行认证（在指示的时间窗口内）：

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IlBZWU86VEVXVTpWN0pIOjI2SlY6QVFUWjpMSkMzOlNYVko6WEdIQTozNEYyOjJMQVE6WlJNSzpaN1E2In0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJqbGhhd24iLCJhdWQiOiJyZWdpc3RyeS5kb2NrZXIuY29tIiwiZXhwIjoxNDE1Mzg3MzE1LCJuYmYiOjE0MTUzODcwMTUsImlhdCI6MTQxNTM4NzAxNSwianRpIjoidFlKQ08xYzZjbnl5N2tBbjBjN3JLUGdiVjFIMWJGd3MiLCJhY2Nlc3MiOlt7InR5cGUiOiJyZXBvc2l0b3J5IiwibmFtZSI6InNhbWFsYmEvbXktYXBwIiwiYWN0aW9ucyI6WyJwdXNoIl19XX0.QhflHPfbd6eVF4lM9bwYpFZIV0PfikbyXuLx959ykRTBpe3CYnzs6YBK8FToVb5R47920PVLrh8zuLzdCr9t3w", "expires_in": 3600,"issued_at": "2009-11-10T23:00:00Z"}
```

## 使用 Bearer 令牌

一旦客户端获得令牌，它将再次尝试 registry 请求，并将令牌放置在 HTTP `Authorization` 头部中，如下所示：

```text
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IkJWM0Q6MkFWWjpVQjVaOktJQVA6SU5QTDo1RU42Ok40SjQ6Nk1XTzpEUktFOkJWUUs6M0ZKTDpQT1RMIn0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJCQ0NZOk9VNlo6UUVKNTpXTjJDOjJBVkM6WTdZRDpBM0xZOjQ1VVc6NE9HRDpLQUxMOkNOSjU6NUlVTCIsImF1ZCI6InJlZ2lzdHJ5LmRvY2tlci5jb20iLCJleHAiOjE0MTUzODczMTUsIm5iZiI6MTQxNTM4NzAxNSwiaWF0IjoxNDE1Mzg3MDE1LCJqdGkiOiJ0WUpDTzFjNmNueXk3a0FuMGM3cktQZ2JWMUgxYkZ3cyIsInNjb3BlIjoiamxoYXduOnJlcG9zaXRvcnk6c2FtYWxiYS9teS1hcHA6cHVzaCxwdWxsIGpsaGF3bjpuYW1lc3BhY2U6c2FtYWxiYTpwdWxsIn0.Y3zZSwaZPqy4y9oRBVRImZyv3m_S9XDHF1tWwN7mL52C_IiA73SJkWVNsvNqpJIn5h7A2F8biv_S2ppQ1lgkbw
```

这也描述在 [RFC 6750 第 2.1 节：The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://tools.ietf.org/html/rfc6750#section-2.1) 中。
