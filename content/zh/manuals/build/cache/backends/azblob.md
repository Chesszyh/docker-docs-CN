---
title: Azure Blob 存储缓存
description: 使用 Azure blob 存储管理构建缓存
keywords: build, buildx, cache, backend, azblob, azure
aliases:
  - /build/building/cache/backends/azblob/
---

{{< summary-bar feature_name="Azure blob" >}}

`azblob` 缓存存储将你的构建缓存结果上传到
[Azure 的 blob 存储服务](https://azure.microsoft.com/en-us/services/storage/blobs/)。

此缓存存储后端不支持默认的 `docker` 驱动程序。要使用此功能，请使用不同的驱动程序创建一个新的构建器。有关更多信息，请参阅[构建驱动程序](/manuals/build/builders/drivers/_index.md)。

## 概要

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=azblob,name=<cache-image>[,parameters...] \
  --cache-from type=azblob,name=<cache-image>[,parameters...] .
```

下表描述了可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| 名称                | 选项                    | 类型        | 默认值  | 描述                                         |
| ------------------- | ----------------------- | ----------- | ------- | -------------------------------------------- |
| `name`              | `cache-to`,`cache-from` | String      |         | 必需。缓存镜像的名称。                         |
| `account_url`       | `cache-to`,`cache-from` | String      |         | 存储账户的基础 URL。                           |
| `secret_access_key` | `cache-to`,`cache-from` | String      |         | Blob 存储账户密钥，参见[身份验证][1]。         |
| `mode`              | `cache-to`              | `min`,`max` | `min`   | 要导出的缓存层，参见[缓存模式][2]。            |
| `ignore-error`      | `cache-to`              | Boolean     | `false` | 忽略由缓存导出失败引起的错误。                 |

[1]: #authentication
[2]: _index.md#cache-mode

## 身份验证

如果未指定 `secret_access_key`，则会按照
[Azure Go SDK](https://docs.microsoft.com/en-us/azure/developer/go/azure-sdk-authentication)
的方案从 BuildKit 服务器上的环境变量中读取。环境变量是从服务器读取的，而不是从 Buildx 客户端读取。

## 延伸阅读

有关缓存的介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `azblob` 缓存后端的更多信息，请参阅
[BuildKit README](https://github.com/moby/buildkit#azure-blob-storage-cache-experimental)。
