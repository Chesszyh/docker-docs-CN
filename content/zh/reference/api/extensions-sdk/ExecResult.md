---
title: "接口: ExecResult"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExecResult/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExecResult/
---

**`自`**

0.2.0

## 继承

- [`RawExecResult`](RawExecResult.md)

  ↳ **`ExecResult`**

## 方法

### lines

▸ **lines**(): `string`[]

分割输出行。

#### 返回值

`string`[]

行列表。

___

### parseJsonLines

▸ **parseJsonLines**(): `any`[]

将每行输出解析为 JSON 对象。

#### 返回值

`any`[]

每行都是 JSON 对象的行列表。

___

### parseJsonObject

▸ **parseJsonObject**(): `any`

解析格式良好的 JSON 输出。

#### 返回值

`any`

JSON 对象。

## 属性

### cmd

• `可选` `只读` **cmd**: `string`

#### 继承自

[RawExecResult](RawExecResult.md).[cmd](RawExecResult.md#cmd)

___

### killed

• `可选` `只读` **killed**: `boolean`

#### 继承自

[RawExecResult](RawExecResult.md).[killed](RawExecResult.md#killed)

___

### signal

• `可选` `只读` **signal**: `string`

#### 继承自

[RawExecResult](RawExecResult.md).[signal](RawExecResult.md#signal)

___

### code

• `可选` `只读` **code**: `number`

#### 继承自

[RawExecResult](RawExecResult.md).[code](RawExecResult.md#code)

___

### stdout

• `只读` **stdout**: `string`

#### 继承自

[RawExecResult](RawExecResult.md).[stdout](RawExecResult.md#stdout)

___

### stderr

• `只读` **stderr**: `string`

#### 继承自

[RawExecResult](RawExecResult.md).[stderr](RawExecResult.md#stderr)
