---
title: Local 和 tar 导出器
keywords: build, buildx, buildkit, exporter, local, tar
description: >
  local 和 tar 导出器将构建结果保存到本地文件系统
aliases:
  - /build/building/exporters/local-tar/
---

`local` 和 `tar` 导出器将构建结果的根文件系统输出到本地目录。它们对于生成非容器镜像的产物很有用。

- `local` 导出文件和目录。
- `tar` 导出相同的内容，但将导出打包为 tarball。

## 概要

使用 `local` 导出器构建容器镜像：

```console
$ docker buildx build --output type=local[,parameters] .
$ docker buildx build --output type=tar[,parameters] .
```

下表描述了可用的参数：

| 参数        | 类型    | 默认值 | 描述                                                                                                                                                                                                                            |
|------------------|---------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dest`           | String  |         | 复制文件的路径                                                                                                                                                                                                                  |
| `platform-split` | Boolean | `true`  | 当使用 local 导出器进行多平台构建时，默认情况下会在目标目录中创建与每个目标平台匹配的子文件夹。设置为 `false` 可将所有平台的文件合并到同一目录中。 |

## 进一步阅读

有关 `local` 或 `tar` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#local-directory)。
