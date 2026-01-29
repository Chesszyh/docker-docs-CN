---
title: 本地和 tar 导出器
keywords: build, buildx, buildkit, 导出器, 本地, tar
description: >
  本地和 tar 导出器将构建结果保存到本地文件系统
---

`local` 和 `tar` 导出器将构建结果的根文件系统输出到本地目录中。它们对于生成非容器镜像的构件非常有用。

- `local` 导出文件和目录。
- `tar` 导出相同的内容，但会将导出内容打包成一个 tar 包。

## 概要

使用 `local` 导出器构建容器镜像：

```console
$ docker buildx build --output type=local[,parameters] .
$ docker buildx build --output type=tar[,parameters] .
```

下表描述了可用参数：

| 参数 | 类型 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- |
| `dest`           | 字符串  |         | 复制文件的目标路径                                                                                                                                                                                                                  |
| `platform-split` | 布尔值 | `true`  | 在多平台构建中使用本地导出器时，默认会在目标目录中创建一个与每个目标平台相对应的子文件夹。将其设置为 `false` 可将所有平台的文件合并到同一个目录中。 |

## 延伸阅读

有关 `local` 或 `tar` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#local-directory)。
