---
title: Bake 中的继承
linkTitle: 继承
weight: 30
description: 了解如何在 Bake 中从其他目标继承属性
keywords: buildx, buildkit, bake, inheritance, targets, attributes
---

目标可以使用 `inherits` 属性从其他目标继承属性。例如，假设您有一个为开发环境构建 Docker 镜像的目标：

```hcl {title=docker-bake.hcl}
target "app-dev" {
  args = {
    GO_VERSION = "{{% param example_go_version %}}"
  }
  tags = ["docker.io/username/myapp:dev"]
  labels = {
    "org.opencontainers.image.source" = "https://github.com/username/myapp"
    "org.opencontainers.image.author" = "moby.whale@example.com"
  }
}
```

您可以创建一个使用相同构建配置的新目标，但为生产构建使用略有不同的属性。在此示例中，`app-release` 目标继承 `app-dev` 目标，但覆盖 `tags` 属性并添加一个新的 `platforms` 属性：

```hcl {title=docker-bake.hcl}
target "app-release" {
  inherits = ["app-dev"]
  tags = ["docker.io/username/myapp:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

## 通用可重用目标

一种常见的继承模式是定义一个包含所有或大多数项目构建目标共享属性的通用目标。例如，以下 `_common` 目标定义了一组通用的构建参数：

```hcl {title=docker-bake.hcl}
target "_common" {
  args = {
    GO_VERSION = "{{% param example_go_version %}}"
    BUILDKIT_CONTEXT_KEEP_GIT_DIR = 1
  }
}
```

然后，您可以在其他目标中继承 `_common` 目标以应用共享属性：

```hcl {title=docker-bake.hcl}
target "lint" {
  inherits = ["_common"]
  dockerfile = "./dockerfiles/lint.Dockerfile"
  output = [{ type = "cacheonly" }]
}

target "docs" {
  inherits = ["_common"]
  dockerfile = "./dockerfiles/docs.Dockerfile"
  output = ["./docs/reference"]
}

target "test" {
  inherits = ["_common"]
  target = "test-output"
  output = ["./test"]
}

target "binaries" {
  inherits = ["_common"]
  target = "binaries"
  output = ["./build"]
  platforms = ["local"]
}
```

## 覆盖继承的属性

当一个目标继承另一个目标时，它可以覆盖任何继承的属性。例如，以下目标覆盖了继承目标的 `args` 属性：

```hcl {title=docker-bake.hcl}
target "app-dev" {
  inherits = ["_common"]
  args = {
    GO_VERSION = "1.17"
  }
  tags = ["docker.io/username/myapp:dev"]
}
```

`app-release` 中的 `GO_VERSION` 参数被设置为 `1.17`，覆盖了 `app-dev` 目标中的 `GO_VERSION` 参数。

有关覆盖属性的更多信息，请参阅[覆盖配置](./overrides.md)页面。

## 从多个目标继承

`inherits` 属性是一个列表，这意味着您可以重用多个其他目标的属性。在以下示例中，app-release 目标重用了 `app-dev` 和 `_common` 目标的属性。

```hcl {title=docker-bake.hcl}
target "_common" {
  args = {
    GO_VERSION = "{{% param example_go_version %}}"
    BUILDKIT_CONTEXT_KEEP_GIT_DIR = 1
  }
}

target "app-dev" {
  inherits = ["_common"]
  args = {
    BUILDKIT_CONTEXT_KEEP_GIT_DIR = 0
  }
  tags = ["docker.io/username/myapp:dev"]
  labels = {
    "org.opencontainers.image.source" = "https://github.com/username/myapp"
    "org.opencontainers.image.author" = "moby.whale@example.com"
  }
}

target "app-release" {
  inherits = ["app-dev", "_common"]
  tags = ["docker.io/username/myapp:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

当从多个目标继承属性并存在冲突时，出现在 inherits 列表中最后的目标优先。前面的示例在 `_common` 目标中定义了 `BUILDKIT_CONTEXT_KEEP_GIT_DIR`，并在 `app-dev` 目标中覆盖了它。

`app-release` 目标同时继承了 `app-dev` 目标和 `_common` 目标。`BUILDKIT_CONTEXT_KEEP_GIT_DIR` 参数在 `app-dev` 目标中被设置为 0，在 `_common` 目标中被设置为 1。`app-release` 目标中的 `BUILDKIT_CONTEXT_KEEP_GIT_DIR` 参数被设置为 1，而不是 0，因为 `_common` 目标出现在 inherits 列表的最后。

## 重用目标的单个属性

如果您只想从一个目标继承单个属性，可以使用点表示法引用另一个目标的属性。例如，在以下 Bake 文件中，`bar` 目标重用了 `foo` 目标的 `tags` 属性：

```hcl {title=docker-bake.hcl}
target "foo" {
  dockerfile = "foo.Dockerfile"
  tags       = ["myapp:latest"]
}
target "bar" {
  dockerfile = "bar.Dockerfile"
  tags       = target.foo.tags
}
```
