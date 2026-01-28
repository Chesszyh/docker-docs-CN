---
title: GitHub Actions 缓存
description: 在 CI 中使用 GitHub Actions 缓存管理构建缓存
keywords: build, buildx, cache, backend, gha, github, actions
aliases:
  - /build/building/cache/backends/gha/
---

{{< summary-bar feature_name="GitHub Actions cache" >}}

GitHub Actions 缓存利用
[GitHub 提供的 Action 缓存](https://github.com/actions/cache)或其他支持 GitHub Actions 缓存协议的缓存服务。只要你的用例符合
[GitHub 设置的大小和使用限制](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#usage-limits-and-eviction-policy)，这是在 GitHub Actions 工作流中推荐使用的缓存。

此缓存存储后端不支持默认的 `docker` 驱动程序。要使用此功能，请使用不同的驱动程序创建一个新的构建器。有关更多信息，请参阅[构建驱动程序](/manuals/build/builders/drivers/_index.md)。

## 概要

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=gha[,parameters...] \
  --cache-from type=gha[,parameters...] .
```

下表描述了可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| 名称           | 选项                    | 类型        | 默认值                                          | 描述                                                          |
|----------------|-------------------------|-------------|-------------------------------------------------|---------------------------------------------------------------|
| `url`          | `cache-to`,`cache-from` | String      | `$ACTIONS_CACHE_URL` 或 `$ACTIONS_RESULTS_URL`  | 缓存服务器 URL，参见[身份验证][1]。                             |
| `url_v2`       | `cache-to`,`cache-from` | String      | `$ACTIONS_RESULTS_URL`                          | 缓存 v2 服务器 URL，参见[身份验证][1]。                         |
| `token`        | `cache-to`,`cache-from` | String      | `$ACTIONS_RUNTIME_TOKEN`                        | 访问令牌，参见[身份验证][1]。                                   |
| `scope`        | `cache-to`,`cache-from` | String      | `buildkit`                                      | 缓存对象所属的作用域，参见[作用域][2]                           |
| `mode`         | `cache-to`              | `min`,`max` | `min`                                           | 要导出的缓存层，参见[缓存模式][3]。                             |
| `ignore-error` | `cache-to`              | Boolean     | `false`                                         | 忽略由缓存导出失败引起的错误。                                  |
| `timeout`      | `cache-to`,`cache-from` | String      | `10m`                                           | 导入或导出缓存超时前的最大持续时间。                            |
| `repository`   | `cache-to`              | String      |                                                 | 用于缓存存储的 GitHub 仓库。                                    |
| `ghtoken`      | `cache-to`              | String      |                                                 | 访问 GitHub API 所需的 GitHub 令牌。                            |

[1]: #authentication
[2]: #scope
[3]: _index.md#cache-mode

## 身份验证

如果 `url`、`url_v2` 或 `token` 参数未指定，`gha` 缓存后端将回退使用环境变量。如果你从内联步骤手动调用 `docker buildx` 命令，则必须手动暴露这些变量。考虑使用
[`crazy-max/ghaction-github-runtime`](https://github.com/crazy-max/ghaction-github-runtime)
GitHub Action 作为暴露变量的辅助工具。

## 作用域

作用域是用于标识缓存对象的键。默认情况下，它设置为 `buildkit`。如果你构建多个镜像，每个构建都会覆盖前一个的缓存，只留下最终的缓存。

要为多个构建保留缓存，你可以使用特定名称指定此作用域属性。在以下示例中，缓存设置为镜像名称，以确保每个镜像都有自己的缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=gha,url=...,token=...,scope=image \
  --cache-from type=gha,url=...,token=...,scope=image .
$ docker buildx build --push -t <registry>/<image2> \
  --cache-to type=gha,url=...,token=...,scope=image2 \
  --cache-from type=gha,url=...,token=...,scope=image2 .
```

GitHub 的[缓存访问限制](https://docs.github.com/en/actions/advanced-guides/caching-dependencies-to-speed-up-workflows#restrictions-for-accessing-a-cache)仍然适用。工作流只能访问当前分支、基础分支和默认分支的缓存。

### 使用 `docker/build-push-action`

使用
[`docker/build-push-action`](https://github.com/docker/build-push-action) 时，`url` 和 `token` 参数会自动填充。无需手动指定它们或包含任何额外的解决方法。

例如：

```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: "<registry>/<image>:latest"
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## 避免 GitHub Actions 缓存 API 限流

GitHub 的[使用限制和驱逐策略](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#usage-limits-and-eviction-policy)会导致过期的缓存条目在一定时间后被删除。默认情况下，`gha` 缓存后端使用 GitHub Actions 缓存 API 来检查缓存条目的状态。

如果你在短时间内发出太多请求，GitHub Actions 缓存 API 会受到速率限制，这可能是由于使用 `gha` 缓存后端进行构建时缓存查找导致的。

```text
#31 exporting to GitHub Actions Cache
#31 preparing build cache for export
#31 preparing build cache for export 600.3s done
#31 ERROR: maximum timeout reached
------
 > exporting to GitHub Actions Cache:
------
ERROR: failed to solve: maximum timeout reached
make: *** [Makefile:35: release] Error 1
Error: Process completed with exit code 2.
```

要缓解此问题，你可以向 BuildKit 提供 GitHub 令牌。这使 BuildKit 能够利用标准 GitHub API 来检查缓存键，从而减少对缓存 API 的请求次数。

要提供 GitHub 令牌，你可以使用 `ghtoken` 参数，以及 `repository` 参数来指定用于缓存存储的仓库。`ghtoken` 参数是具有 `repo` 作用域的 GitHub 令牌，这是访问 GitHub Actions 缓存 API 所必需的。

当你使用 `docker/build-push-action` action 构建时，`ghtoken` 参数会自动设置为 `secrets.GITHUB_TOKEN` 的值。你也可以使用 `github-token` 输入手动设置 `ghtoken` 参数，如以下示例所示：

```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: "<registry>/<image>:latest"
    cache-from: type=gha
    cache-to: type=gha,mode=max
    github-token: ${{ secrets.MY_CUSTOM_TOKEN }}
```

## 延伸阅读

有关缓存的介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `gha` 缓存后端的更多信息，请参阅
[BuildKit README](https://github.com/moby/buildkit#github-actions-cache-experimental)。

有关将 GitHub Actions 与 Docker 一起使用的更多信息，请参阅
[GitHub Actions 简介](../../ci/github-actions/_index.md)
