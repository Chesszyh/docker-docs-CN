---
title: "接口: RawExecResult"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/RawExecResult/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/RawExecResult/
---

**`起始版本`**

0.2.0

## 继承层次

- **`RawExecResult`**

  ↳ [`ExecResult`](ExecResult.md)

## 属性

### cmd

• `Optional` `Readonly` **cmd**: `string`

___

### killed

• `Optional` `Readonly` **killed**: `boolean`

___

### signal

• `Optional` `Readonly` **signal**: `string`

___

### code

• `Optional` `Readonly` **code**: `number`

___

### stdout

• `Readonly` **stdout**: `string`

___

### stderr

• `Readonly` **stderr**: `string`
