---
title: Azure Blob 存储缓存
description: 使用 Azure Blob 存储管理构建缓存
keywords: build, buildx, cache, backend, azblob, azure, 缓存, 后端
alias:
  - /build/building/cache/backends/azblob/
---

{{< summary-bar feature_name="Azure blob" >}}

`azblob` 缓存存储后端将构建生成的缓存上传到 [Azure 的 Blob 存储服务](https://azure.microsoft.com/en-us/services/storage/blobs/)。

默认的 `docker` 驱动不支持此缓存存储后端。要使用此特性，请使用其他驱动创建一个新构建器。更多信息请参见 [构建驱动](/manuals/build/builders/drivers/_index.md)。

## 语法

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=azblob,name=<缓存镜像名>[,参数...] \
  --cache-from type=azblob,name=<缓存镜像名>[,参数...] .
```

下表描述了可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| 名称 | 选项 | 类型 | 默认值 | 说明 |
| ------------------- | ----------------------- | ----------- | ------- | -------------------------------------------------- |
| `name`              | `cache-to`,`cache-from` | 字符串 | | 必填。缓存镜像的名称。 |
| `account_url`       | `cache-to`,`cache-from` | 字符串 | | 存储账户的基础 URL。 |
| `secret_access_key` | `cache-to`,`cache-from` | 字符串 | | Blob 存储账户密钥，参见 [身份验证][1]。 |
| `mode`              | `cache-to`              | `min`,`max` | `min` | 要导出的缓存层，参见 [缓存模式][2]。 |
| `ignore-error`      | `cache-to`              | 布尔值 | `false` | 忽略由于缓存导出失败而引起的错误。 |

[1]: #身份验证
[2]: _index.md#缓存模式

## 身份验证

如果未指定 `secret_access_key`，系统将按照 [Azure Go SDK](https://docs.microsoft.com/en-us/azure/developer/go/azure-sdk-authentication) 的方案从 BuildKit 服务器上的环境变量中读取。请注意，环境变量是从服务器端读取的，而不是从 Buildx 客户端读取。

## 深入阅读

欲了解缓存简介，请参阅 [Docker 构建缓存](../_index.md)。

有关 `azblob` 缓存后端的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit#azure-blob-storage-cache-experimental)。