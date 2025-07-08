---
title: "接口: ExecResultV0"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExecResultV0/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExecResultV0/
---

## 属性

### cmd

• `可选` `只读` **cmd**: `string`

___

### killed

• `可选` `只读` **killed**: `boolean`

___

### signal

• `可选` `只读` **signal**: `string`

___

### code

• `可选` `只读` **code**: `number`

___

### stdout

• `只读` **stdout**: `string`

___

### stderr

• `只读` **stderr**: `string`

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
