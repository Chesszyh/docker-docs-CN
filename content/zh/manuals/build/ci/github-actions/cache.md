---
title: 使用 GitHub Actions 进行缓存管理
linkTitle: 缓存管理
keywords: ci, github actions, gha, buildkit, buildx, cache, 缓存
---

本页包含在 GitHub Actions 中使用缓存存储后端的示例。

> [!NOTE]
>
> 有关缓存存储后端的更多详情，请参阅 [缓存存储后端](../../cache/backends/_index.md)。

## 内联缓存 (Inline cache)

在大多数情况下，您会希望使用 [内联缓存导出器](../../cache/backends/inline.md)。但请注意，`inline` 缓存导出器仅支持 `min` 缓存模式。要使用 `max` 模式，请使用带 `cache-to` 选项的注册表缓存导出器，将镜像和缓存分开推送，如 [注册表缓存示例](#注册表缓存) 所示。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:latest
          cache-to: type=inline
```

## 注册表缓存 (Registry cache)

您可以使用 [注册表缓存导出器](../../cache/backends/registry.md) 从注册表上的缓存清单或（特殊的）镜像配置中导入/导出缓存。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

## GitHub 缓存

### 缓存后端 API

{{< summary-bar feature_name="缓存后端 API" >}}

[GitHub Actions 缓存导出器](../../cache/backends/gha.md) 后端使用 [GitHub 缓存服务 API](https://github.com/tonistiigi/go-actions-cache) 来获取和上传缓存 blob。这就是为什么您应该仅在 GitHub Action 工作流中使用此缓存后端，因为 `url` (`$ACTIONS_RESULTS_URL`) 和 `token` (`$ACTIONS_RUNTIME_TOKEN`) 属性仅在工作流上下文中才会被填充。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

> [!IMPORTANT]
>
> 自 [2025 年 4 月 15 日起，仅支持 GitHub 缓存服务 API v2](https://gh.io/gha-cache-sunset)。
> 
> 如果您在构建过程中遇到以下错误：
> 
> ```console
> ERROR: failed to solve: This legacy service is shutting down, effective April 15, 2025. Migrate to the new service ASAP. For more information: https://gh.io/gha-cache-sunset
> ```
> 
> 说明您可能正在使用仅支持旧版 GitHub 缓存服务 API v1 的过时工具。取决于您的使用场景，以下是您需要升级到的最低版本：
> * Docker Buildx >= v0.21.0
> * BuildKit >= v0.20.0
> * Docker Compose >= v2.33.1
> * Docker Engine >= v28.0.0（如果您在启用 containerd 镜像存储的情况下使用 Docker 驱动进行构建）
> 
> 如果您在 GitHub 托管的运行器（runners）上使用 `docker/build-push-action` 或 `docker/bake-action`，Docker Buildx 和 BuildKit 已经是最新的。但在自托管运行器上，您可能需要手动更新它们。或者，您可以使用 `docker/setup-buildx-action` 安装最新版本的 Docker Buildx：
> 
> ```yaml
> - name: Set up Docker Buildx
>   uses: docker/setup-buildx-action@v3
>   with:
>    version: latest
> ```
> 
> 如果您使用 Docker Compose 进行构建，可以使用 `docker/setup-compose-action`：
> 
> ```yaml
> - name: Set up Docker Compose
>   uses: docker/setup-compose-action@v1
>   with:
>    version: latest
> ```
> 
> 如果您在启用 containerd 镜像存储的情况下使用 Docker Engine 进行构建，可以使用 `docker/setup-docker-action`：
> 
> ```yaml
> -
>   name: Set up Docker
>   uses: docker/setup-docker-action@v4
>   with:
>     version: latest
>     daemon-config: |
>       {
>         "features": {
>           "containerd-snapshotter": true
>         }
>       }
> ```

### 缓存挂载 (Cache mounts)

默认情况下，BuildKit 不会在 GitHub Actions 缓存中保留缓存挂载。如果您希望将缓存挂载存入 GitHub Actions 缓存并在构建之间复用，可以使用由 [`reproducible-containers/buildkit-cache-dance`](https://github.com/reproducible-containers/buildkit-cache-dance) 提供的变通方案。

这个 GitHub Action 会创建临时容器，将缓存挂载数据提取并注入到您的 Docker 构建步骤中。

以下示例展示了如何在 Go 项目中使用此变通方案。

示例 Dockerfile 位于 `build/package/Dockerfile`：

```Dockerfile
FROM golang:1.21.1-alpine as base-build

WORKDIR /build
RUN go env -w GOMODCACHE=/root/.cache/go-build

COPY go.mod go.sum ./
RUN --mount=type=cache,target=/root/.cache/go-build go mod download

COPY ./src ./
RUN --mount=type=cache,target=/root/.cache/go-build go build -o /bin/app /build/src
...
```

示例 CI Action：

```yaml
name: ci

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: user/app
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Go Build Cache for Docker
        uses: actions/cache@v4
        with:
          path: go-build-cache
          key: ${{ runner.os }}-go-build-cache-${{ hashFiles('**/go.sum') }}

      - name: Inject go-build-cache
        uses: reproducible-containers/buildkit-cache-dance@4b2444fec0c0fb9dbf175a96c094720a692ef810 # v2.1.4
        with:
          cache-source: go-build-cache

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          cache-from: type=gha
          cache-to: type=gha,mode=max
          file: build/package/Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          platforms: linux/amd64,linux/arm64
```

有关此变通方案的更多信息，请参考 [GitHub 仓库](https://github.com/reproducible-containers/buildkit-cache-dance)。

### 本地缓存 (Local cache)

> [!WARNING]
>
> 目前旧的缓存条目不会被删除，因此缓存大小会 [持续增长](https://github.com/docker/build-push-action/issues/252)。以下示例使用 `Move cache` 步骤作为一种变通方法（更多信息请参见 [`moby/buildkit#1896`](https://github.com/moby/buildkit/issues/1896)）。

您还可以通过使用 [actions/cache](https://github.com/actions/cache) 以及 [本地缓存导出器](../../cache/backends/local.md) 来利用 [GitHub 缓存](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: ${{ runner.temp }}/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=local,src=${{ runner.temp }}/.buildx-cache
          cache-to: type=local,dest=${{ runner.temp }}/.buildx-cache-new,mode=max

      - # 临时修复
        # https://github.com/docker/build-push-action/issues/252
        # https://github.com/moby/buildkit/issues/1896
        name: Move cache
        run: |
          rm -rf ${{ runner.temp }}/.buildx-cache
          mv ${{ runner.temp }}/.buildx-cache-new ${{ runner.temp }}/.buildx-cache
```