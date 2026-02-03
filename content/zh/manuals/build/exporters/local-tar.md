---
title: 本地与 Tar 导出器 (Local and tar exporters)
keywords: build, buildx, buildkit, exporter, local, tar, 导出器, 本地
description: >
  本地与 Tar 导出器用于将构建结果保存到本地文件系统中
aliases:
  - /build/building/exporters/local-tar/
---

`local` 和 `tar` 导出器将构建结果的根文件系统输出到本地目录中。当您想要生成非容器镜像的产物时，它们非常有用。

- `local` 导出文件和目录。
- `tar` 导出相同的内容，但会将导出的内容打包成一个 tar 包。

## 语法

使用 `local` 导出器构建容器镜像：

```console
$ docker buildx build --output type=local[,参数] .
$ docker buildx build --output type=tar[,参数] .
```

下表描述了可用参数：

| 参数 | 类型 | 默认值 | 说明 |
|------------------|---------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dest` | 字符串 | | 文件复制的目标路径。 |
| `platform-split` | 布尔值 | `true` | 在多平台构建中使用本地导出器时，默认情况下会在目标目录中为每个目标平台创建一个匹配的子文件夹。将其设置为 `false` 可将所有平台的文件合并到同一个目录中。 |

## 深入阅读

有关 `local` 或 `tar` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#local-directory)。