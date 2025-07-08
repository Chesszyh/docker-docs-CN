---
title: "接口: ExecStreamOptions"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases: 
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExecStreamOptions/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExecStreamOptions/
---

**`自`**

0.2.2

## 属性

### onOutput

• `可选` **onOutput**: (`data`: { `stdout`: `string` ; `stderr?`: `undefined`  } \| { `stdout?`: `undefined` ; `stderr`: `string`  }) => `void`

#### 类型声明

▸ (`data`): `void`

接收到命令输出时调用。
默认情况下，输出在任意边界处分块。如果您希望输出按完整的行分割，请将 `splitOutputLines` 设置为 true。然后，每行调用一次回调。

**`自`**

0.2.0

##### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `data` | `{ stdout: string; stderr?: undefined } \| { stdout?: undefined; stderr: string }` | 输出内容。可以包含 stdout 字符串或 stderr 字符串，一次一个。 |

##### 返回值

`void`

___

### onError

• `可选` **onError**: (`error`: `any`) => `void`

#### 类型声明

▸ (`error`): `void`

如果执行的命令出错，则调用以报告错误。

##### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `error` | `any` | 执行命令中发生的错误 |

##### 返回值

`void`

___

### onClose

• `可选` **onClose**: (`exitCode`: `number`) => `void`

#### 类型声明

▸ (`exitCode`): `void`

进程退出时调用。

##### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `exitCode` | `number` | 进程退出代码 |

##### 返回值

`void`

___

### splitOutputLines

• `可选` `只读` **splitOutputLines**: `boolean`

指定调用 `onOutput(data)` 的行为。默认情况下为原始输出，在任何位置分割输出。如果设置为 true，则 `onOutput` 将为每行调用一次。
