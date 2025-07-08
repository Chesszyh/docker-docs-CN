---
title: "接口: OpenDialogResult"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/OpenDialogResult/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/OpenDialogResult/
---

**`自`**

0.2.3

## 属性

### canceled

• `只读` **canceled**: `boolean`

对话框是否已取消。

___

### filePaths

• `只读` **filePaths**: `string`[]

用户选择的文件路径数组。如果对话框被取消，这将是一个空数组。

___

### bookmarks

• `可选` `只读` **bookmarks**: `string`[]

仅限 macOS。与 `filePaths` 数组匹配的 `base64` 编码字符串数组，其中包含安全范围的书签数据。必须启用 `securityScopedBookmarks` 才能填充此项。
