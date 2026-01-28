---
title: "接口: Dialog"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/Dialog/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/Dialog/
---

允许打开原生对话框。

**`起始版本`**

0.2.3

## 方法

### showOpenDialog

▸ **showOpenDialog**(`dialogProperties`): `Promise`<[`OpenDialogResult`](OpenDialogResult.md)\>

显示原生打开对话框。允许您选择文件或文件夹。

```typescript
ddClient.desktopUI.dialog.showOpenDialog({properties: ['openFile']});
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `dialogProperties` | `any` | 用于指定打开对话框行为的属性，请参阅 https://www.electronjs.org/docs/latest/api/dialog#dialogshowopendialogbrowserwindow-options。 |

#### 返回值

`Promise`<[`OpenDialogResult`](OpenDialogResult.md)\>
