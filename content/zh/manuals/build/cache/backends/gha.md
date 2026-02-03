---
title: GitHub Actions 缓存 (GitHub Actions cache)
description: 使用 GitHub Actions 缓存管理您 CI 环境中的构建缓存
keywords: build, buildx, cache, backend, gha, github, actions, 缓存, 后端
alias:
  - /build/building/cache/backends/gha/
---

{{< summary-bar feature_name="GitHub Actions 缓存" >}}

GitHub Actions 缓存利用了 [GitHub 提供的 Actions 缓存](https://github.com/actions/cache) 或其他支持 GitHub Actions 缓存协议的缓存服务。只要您的用例符合 [GitHub 设置的大小和使用限制](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#usage-limits-and-eviction-policy)，这就是在 GitHub Actions 工作流中推荐使用的缓存方式。

默认的 `docker` 驱动不支持此缓存存储后端。要使用此特性，请使用其他驱动创建一个新构建器。更多信息请参见 [构建驱动](/manuals/build/builders/drivers/_index.md)。

## 语法

```console
$ docker buildx build --push -t <注册表>/<镜像名> \
  --cache-to type=gha[,参数...] \
  --cache-from type=gha[,参数...] .
```

下表描述了可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| 名称 | 选项 | 类型 | 默认值 | 说明 |
|----------------|-------------------------|-------------|------------------------------------------------|----------------------------------------------------------------------|
| `url` | `cache-to`,`cache-from` | 字符串 | `$ACTIONS_CACHE_URL` 或 `$ACTIONS_RESULTS_URL` | 缓存服务器 URL，参见 [身份验证][1]。 |
| `url_v2` | `cache-to`,`cache-from` | 字符串 | `$ACTIONS_RESULTS_URL` | 缓存 v2 服务器 URL，参见 [身份验证][1]。 |
| `token` | `cache-to`,`cache-from` | 字符串 | `$ACTIONS_RUNTIME_TOKEN` | 访问令牌，参见 [身份验证][1]。 |
| `scope` | `cache-to`,`cache-from` | 字符串 | `buildkit` | 缓存对象所属的作用域，参见 [作用域 (scope)][2] |
| `mode` | `cache-to` | `min`,`max` | `min` | 要导出的缓存层，参见 [缓存模式][3]。 |
| `ignore-error` | `cache-to` | 布尔值 | `false` | 忽略由于缓存导出失败而引起的错误。 |
| `timeout` | `cache-to`,`cache-from` | 字符串 | `10m` | 导入或导出缓存的超时时长。 |
| `repository` | `cache-to` | 字符串 | | 用于缓存存储的 GitHub 仓库。 |
| `ghtoken` | `cache-to` | 字符串 | | 访问 GitHub API 所需的 GitHub 令牌。 |

[1]: #身份验证
[2]: #作用域-scope
[3]: _index.md#缓存模式

## 身份验证

如果未指定 `url`、`url_v2` 或 `token` 参数，`gha` 缓存后端将回退到使用环境变量。如果您是从内联步骤手动调用 `docker buildx` 命令，则必须手动暴露这些变量。建议使用 [`crazy-max/ghaction-github-runtime`](https://github.com/crazy-max/ghaction-github-runtime) 这个 GitHub Action 来辅助暴露这些变量。

## 作用域 (Scope)

作用域是用于标识缓存对象的键。默认情况下，它被设置为 `buildkit`。如果您构建多个镜像，每个构建都会覆盖前一个构建的缓存，仅保留最后的缓存。

为了保留多个构建的缓存，您可以为 `scope` 属性指定一个唯一的名称。在以下示例中，缓存作用域被设置为镜像名称，以确保每个镜像都有自己的缓存：

```console
$ docker buildx build --push -t <注册表>/<镜像1> \
  --cache-to type=gha,url=...,token=...,scope=image \
  --cache-from type=gha,url=...,token=...,scope=image .
$ docker buildx build --push -t <注册表>/<镜像2> \
  --cache-to type=gha,url=...,token=...,scope=image2 \
  --cache-from type=gha,url=...,token=...,scope=image2 .
```

GitHub 的 [缓存访问限制](https://docs.github.com/en/actions/advanced-guides/caching-dependencies-to-speed-up-workflows#restrictions-for-accessing-a-cache) 仍然适用。工作流只能访问当前分支、基础分支和默认分支的缓存。

### 使用 `docker/build-push-action`

使用 [`docker/build-push-action`](https://github.com/docker/build-push-action) 时，`url` 和 `token` 参数会自动填充。无需手动指定它们，也不需要任何额外的变通方法。

例如：

```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: "<注册表>/<镜像名>:latest"
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## 避免 GitHub Actions 缓存 API 节流 (Throttling)

GitHub 的 [使用限制和驱逐策略](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#usage-limits-and-eviction-policy) 导致过时的缓存条目在一段时间后会被移除。默认情况下，`gha` 缓存后端使用 GitHub Actions 缓存 API 来检查缓存条目的状态。

如果您在短时间内发出过多请求，GitHub Actions 缓存 API 会受到速率限制（rate limiting），这可能会在使用 `gha` 缓存后端进行构建期间的缓存查找时发生。

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

为了缓解此问题，您可以向 BuildKit 提供一个 GitHub 令牌 (token)。这允许 BuildKit 利用标准的 GitHub API 来检查缓存键，从而减少对缓存 API 的请求次数。

要提供 GitHub 令牌，您可以使用 `ghtoken` 参数，并使用 `repository` 参数指定用于缓存存储的仓库。`ghtoken` 参数是一个具有 `repo` 作用域的 GitHub 令牌，这是访问 GitHub Actions 缓存 API 所需的。

当您使用 `docker/build-push-action` 进行构建时，`ghtoken` 参数会自动设置为 `secrets.GITHUB_TOKEN` 的值。您也可以通过 `github-token` 输入手动设置 `ghtoken` 参数，如下例所示：

```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: "<注册表>/<镜像名>:latest"
    cache-from: type=gha
    cache-to: type=gha,mode=max
    github-token: ${{ secrets.MY_CUSTOM_TOKEN }}
```

## 深入阅读

欲了解缓存简介，请参阅 [Docker 构建缓存](../_index.md)。

有关 `gha` 缓存后端的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit#github-actions-cache-experimental)。

有关在 Docker 中使用 GitHub Actions 的更多信息，请参阅 [GitHub Actions 简介](../../ci/github-actions/_index.md)。