---
description: Docker Hub API v1（已弃用）
keywords: kitematic, deprecated
title: Docker Hub API v1（已弃用）
weight: 3
aliases:
  - /docker-hub/api/deprecated/
---

> **Deprecated**
>
> Docker Hub API v1 已弃用。请改用 Docker Hub API v2。

v1 路径中的以下 API 路由将不再工作，并返回 410 状态码：
* `/v1/repositories/{name}/images`
* `/v1/repositories/{name}/tags`
* `/v1/repositories/{name}/tags/{tag_name}`
* `/v1/repositories/{namespace}/{name}/images`
* `/v1/repositories/{namespace}/{name}/tags`
* `/v1/repositories/{namespace}/{name}/tags/{tag_name}`

如果你想在当前的应用程序中继续使用 Docker Hub API，请更新你的客户端以使用 v2 端点。

| **旧**                                                                                                                                                              | **新**                                                                                                                                                                                                              |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [/v1/repositories/{name}/images](https://github.com/moby/moby/blob/v1.3.0/docs/sources/reference/api/docker-io_api.md#list-user-repository-images)                   | [/v2/namespaces/{namespace}/repositories/{repository}/images](/reference/api/hub/latest.md#tag/images/operation/GetNamespacesRepositoriesImages)                                                              |
| [/v1/repositories/{namespace}/{name}/images](https://github.com/moby/moby/blob/v1.3.0/docs/sources/reference/api/docker-io_api.md#list-user-repository-images)       | [/v2/namespaces/{namespace}/repositories/{repository}/images](/reference/api/hub/latest.md#tag/images/operation/GetNamespacesRepositoriesImages)                                                              |
| [/v1/repositories/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#list-repository-tags)                                     | [/v2/namespaces/{namespace}/repositories/{repository}/tags](/reference/api/hub/latest.md#tag/repositories/paths/~1v2~1namespaces~1%7Bnamespace%7D~1repositories~1%7Brepository%7D~1tags/get)                  |
| [/v1/repositories/{namespace}/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#list-repository-tags)                         | [/v2/namespaces/{namespace}/repositories/{repository}/tags](/reference/api/hub/latest.md#tag/repositories/paths/~1v2~1namespaces~1%7Bnamespace%7D~1repositories~1%7Brepository%7D~1tags/get)                  |
| [/v1/repositories/{namespace}/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#get-image-id-for-a-particular-tag)            | [/v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}](/reference/api/hub/latest.md#tag/repositories/paths/~1v2~1namespaces~1%7Bnamespace%7D~1repositories~1%7Brepository%7D~1tags~1%7Btag%7D/get) |
| [/v1/repositories/{namespace}/{name}/tags/{tag_name}](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#get-image-id-for-a-particular-tag) | [/v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}](/reference/api/hub/latest.md#tag/repositories/paths/~1v2~1namespaces~1%7Bnamespace%7D~1repositories~1%7Brepository%7D~1tags~1%7Btag%7D/get) |
