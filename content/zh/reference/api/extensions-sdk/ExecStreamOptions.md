---
title: "接口: ExecStreamOptions"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExecStreamOptions/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExecStreamOptions/
---

**`起始版本`**

0.2.2

## 属性

### onOutput

• `Optional` **onOutput**: (`data`: { `stdout`: `string` ; `stderr?`: `undefined`  } \| { `stdout?`: `undefined` ; `stderr`: `string`  }) => `void`

#### 类型声明

▸ (`data`): `void`

在接收命令执行输出时调用。
默认情况下，输出在任意边界处分割成块。
如果您希望输出按完整行分割，请将 `splitOutputLines` 设置为 true。然后每行调用一次回调。

**`起始版本`**

0.2.0

##### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `data` | `{ stdout: string; stderr?: undefined } \| { stdout?: undefined; stderr: string }` | 输出内容。可以包含 stdout 字符串或 stderr 字符串，每次一个。 |

##### 返回值

`void`

___

### onError

• `Optional` **onError**: (`error`: `any`) => `void`

#### 类型声明

▸ (`error`): `void`

如果执行的命令出错，则调用此方法报告错误。

##### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `error` | `any` | 执行命令时发生的错误 |

##### 返回值

`void`

___

### onClose

• `Optional` **onClose**: (`exitCode`: `number`) => `void`

#### 类型声明

▸ (`exitCode`): `void`

在进程退出时调用。

##### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `exitCode` | `number` | 进程退出码 |

##### 返回值

`void`

___

### splitOutputLines

• `Optional` `Readonly` **splitOutputLines**: `boolean`

指定调用 `onOutput(data)` 的行为。默认为原始输出，在任意位置分割输出。如果设置为 true，每行调用一次 `onOutput`。
