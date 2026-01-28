---
title: "接口: OpenDialogResult"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/OpenDialogResult/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/OpenDialogResult/
---

**`起始版本`**

0.2.3

## 属性

### canceled

• `Readonly` **canceled**: `boolean`

对话框是否被取消。

___

### filePaths

• `Readonly` **filePaths**: `string`[]

用户选择的文件路径数组。如果对话框被取消，这将是一个空数组。

___

### bookmarks

• `Optional` `Readonly` **bookmarks**: `string`[]

仅适用于 macOS。与 `filePaths` 数组匹配的 `base64` 编码字符串数组，包含安全作用域书签数据。必须启用 `securityScopedBookmarks` 才能填充此属性。
