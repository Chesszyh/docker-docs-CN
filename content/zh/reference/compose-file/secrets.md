---
title: 秘密顶级元素
description: 探索秘密顶级元素可以拥有的所有属性。
keywords: compose, compose 规范, 秘密, compose 文件参考
aliases: 
 - /compose/compose-file/09-secrets/
weight: 60
---

秘密是 [Configs](configs.md) 的一种，专注于敏感数据，并为此用途设置了特定约束。

服务只有在 `services` 顶级元素中的 [`secrets` 属性](services.md#secrets) 明确授予时才能访问秘密。

顶级 `secrets` 声明定义或引用授予 Compose 应用程序中服务的敏感数据。
秘密的来源可以是 `file` 或 `environment`。

- `file`：秘密是使用指定路径文件的内容创建的。
- `environment`：秘密是使用主机上环境变量的值创建的。

## 示例 1

`server-certificate` 秘密在应用程序部署时创建为 `<project_name>_server-certificate`，通过将 `server.cert` 的内容注册为平台秘密。

```yml
secrets:
  server-certificate:
    file: ./server.cert
```

## 示例 2

`token` 秘密在应用程序部署时创建为 `<project_name>_token`，通过将 `OAUTH_TOKEN` 环境变量的内容注册为平台秘密。

```yml
secrets:
  token:
    environment: "OAUTH_TOKEN"
```

## 附加资源

有关更多信息，请参阅 [如何在 Compose 中使用秘密](/manuals/compose/how-tos/use-secrets.md)。
