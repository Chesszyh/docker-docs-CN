---
title: "接口: ExtensionHost"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExtensionHost/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExtensionHost/
---

**`起始版本`**

0.2.0

## 属性

### cli

• `Readonly` **cli**: [`ExtensionCli`](ExtensionCli.md)

在主机上执行命令。

例如，在主机上执行附带的二进制文件 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

---

以流的形式输出在后端容器或主机上执行的命令的输出。

假设 `kubectl` 二进制文件作为扩展的一部分附带，您可以在主机上生成 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"], {
           stream: {
             onOutput(data): void {
                 // 由于我们可以同时收到 `stdout` 和 `stderr`，我们将它们包装在 JSON 对象中
                 JSON.stringify(
                   {
                     stdout: data.stdout,
                     stderr: data.stderr,
                   },
                   null,
                   "  "
                 );
             },
             onError(error: any): void {
               console.error(error);
             },
             onClose(exitCode: number): void {
               console.log("onClose with exit code " + exitCode);
             },
           },
         });
```
