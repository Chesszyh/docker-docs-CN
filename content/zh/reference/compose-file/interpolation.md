---
title: 变量插值
description: 了解变量插值
keywords: compose, compose specification, interpolation, compose file reference
aliases:
 - /compose/compose-file/12-interpolation/
weight: 90
---

{{% include "compose/interpolation.md" %}}

对于花括号表达式，支持以下格式：
- 直接替换
  - `${VAR}` -> `VAR` 的值
- 默认值
  - `${VAR:-default}` -> 如果 `VAR` 已设置且非空则为其值，否则为 `default`
  - `${VAR-default}` -> 如果 `VAR` 已设置则为其值，否则为 `default`
- 必需值
  - `${VAR:?error}` -> 如果 `VAR` 已设置且非空则为其值，否则退出并显示错误
  - `${VAR?error}` -> 如果 `VAR` 已设置则为其值，否则退出并显示错误
- 替代值
  - `${VAR:+replacement}` -> 如果 `VAR` 已设置且非空则为 `replacement`，否则为空
  - `${VAR+replacement}` -> 如果 `VAR` 已设置则为 `replacement`，否则为空

变量插值也可以嵌套：

- `${VARIABLE:-${FOO}}`
- `${VARIABLE?$FOO}`
- `${VARIABLE:-${FOO:-default}}`

其他扩展的 shell 风格特性，如 `${VARIABLE/foo/bar}`，Compose 不支持。

只要字符串形成有效的变量定义，Compose 就会处理 `$` 符号后面的任何字符串——可以是字母数字名称（`[_a-zA-Z][_a-zA-Z0-9]*`）或以 `${` 开头的花括号字符串。在其他情况下，它将被保留而不尝试插入值。

当你的配置需要字面美元符号时，可以使用 `$$`（双美元符号）。这也防止 Compose 插入值，因此 `$$` 允许你引用不想被 Compose 处理的环境变量。

```yml
web:
  build: .
  command: "$$VAR_NOT_INTERPOLATED_BY_COMPOSE"
```

如果 Compose 无法解析替换的变量且未定义默认值，它会显示警告并用空字符串替换该变量。

由于 Compose 文件中的任何值都可以通过变量替换进行插值，包括复杂元素的紧凑字符串表示法，因此插值在合并之前按每个文件进行。

插值仅适用于 YAML 值，不适用于键。对于键实际上是任意用户定义字符串的少数地方，如 [labels](services.md#labels) 或 [environment](services.md#environment)，必须使用替代的等号语法才能应用插值。例如：

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
