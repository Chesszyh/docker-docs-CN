---
title: 插值
description: 了解插值
keywords: compose, compose 规范, 插值, compose 文件参考
aliases: 
 - /compose/compose-file/12-interpolation/
weight: 90
---

{{% include "compose/interpolation.md" %}}

对于大括号表达式，支持以下格式：
- 直接替换
  - `${VAR}` -> `VAR` 的值
- 默认值
  - `${VAR:-default}` -> 如果 `VAR` 已设置且非空，则为 `VAR` 的值，否则为 `default`
  - `${VAR-default}` -> 如果 `VAR` 已设置，则为 `VAR` 的值，否则为 `default`
- 必需值
  - `${VAR:?error}` -> 如果 `VAR` 已设置且非空，则为 `VAR` 的值，否则以错误退出
  - `${VAR?error}` -> 如果 `VAR` 已设置，则为 `VAR` 的值，否则以错误退出
- 替代值
  - `${VAR:+replacement}` -> 如果 `VAR` 已设置且非空，则为 `replacement`，否则为空
  - `${VAR+replacement}` -> 如果 `VAR` 已设置，则为 `replacement`，否则为空

插值也可以嵌套：

- `${VARIABLE:-${FOO}}`
- `${VARIABLE?$FOO}`
- `${VARIABLE:-${FOO:-default}}`

Compose 不支持其他扩展的 shell 样式功能，例如 `${VARIABLE/foo/bar}`。

只要它构成有效的变量定义（字母数字名称 `[_a-zA-Z][_a-zA-Z0-9]*` 或以 `${` 开头的大括号字符串），Compose 就会处理 `$` 符号后面的任何字符串。在其他情况下，它将保留而不尝试插值。

当您的配置需要文字美元符号时，可以使用 `$$`（双美元符号）。这也会阻止 Compose 插值，因此 `$$` 允许您引用您不希望由 Compose 处理的环境变量。

```yml
web:
  build: .
  command: "$$VAR_NOT_INTERPOLATED_BY_COMPOSE"
```

如果 Compose 无法解析替换的变量并且未定义默认值，它会显示警告并将变量替换为空字符串。

由于 Compose 文件中的任何值都可以通过变量替换进行插值，包括复杂元素的紧凑字符串表示法，因此插值在每个文件合并之前应用。

插值仅适用于 YAML 值，不适用于键。对于少数键实际上是任意用户定义字符串的地方，例如 [labels](services.md#labels) 或 [environment](services.md#environment)，必须使用备用等号语法才能应用插值。例如：

```yml
services:
  foo:
    labels:
      "$VAR_NOT_INTERPOLATED_BY_COMPOSE": "BAR"
```

```yml
services:
  foo:
    labels:
      - "$VAR_INTERPOLATED_BY_COMPOSE=BAR"
```
