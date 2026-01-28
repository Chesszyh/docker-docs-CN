---
title: 扩展后端
description: Docker 扩展 API
keywords: Docker, extensions, sdk, API
aliases:
 - /desktop/extensions-sdk/dev/api/backend/
---

`ddClient.extension.vm` 对象可用于与扩展元数据 [vm 部分](../../architecture/metadata.md#vm-section)中定义的后端进行通信。

## get

▸ **get**(`url`): `Promise`<`unknown`\>

执行 HTTP GET 请求到后端服务。

```typescript
ddClient.extension.vm.service
 .get("/some/service")
 .then((value: any) => console.log(value)
```

有关其他方法（如 POST、UPDATE 和 DELETE），请参阅 [Service API 参考](/reference/api/extensions-sdk/HttpService.md)。

> 已弃用的扩展后端通信
>
> 下面使用 `window.ddClient.backend` 的方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

`window.ddClient.backend` 对象可用于与扩展元数据 [vm 部分](../../architecture/metadata.md#vm-section)中定义的后端进行通信。客户端已连接到后端。

使用示例：

```typescript
window.ddClient.backend
  .get("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .post("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .put("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .patch("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .delete("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .head("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .request({ url: "/url", method: "GET", headers: { 'header-key': 'header-value' }, data: { ... }})
  .then((value: any) => console.log(value));
```

## 在扩展后端容器中运行命令

例如，在后端容器内执行命令 `ls -l`：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"]);
```

流式输出在后端容器中执行的命令。例如，在后端容器内生成命令 `ls -l`：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
  stream: {
    onOutput(data) {
      if (data.stdout) {
        console.error(data.stdout);
      } else {
        console.log(data.stderr);
      }
    },
    onError(error) {
      console.error(error);
    },
    onClose(exitCode) {
      console.log("onClose with exit code " + exitCode);
    },
  },
});
```

有关更多详细信息，请参阅 [Extension VM API 参考](/reference/api/extensions-sdk/ExtensionVM.md)

> 已弃用的扩展后端命令执行
>
> 此方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

如果您的扩展附带了应在后端容器内运行的额外二进制文件，您可以使用 `execInVMExtension` 函数：

```typescript
const output = await window.ddClient.backend.execInVMExtension(
  `cliShippedInTheVm xxx`
);
console.log(output);
```

## 在主机上调用扩展二进制文件

您可以运行在扩展元数据 [host 部分](../../architecture/metadata.md#host-section)中定义的二进制文件。

例如，在主机上执行附带的二进制文件 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

只要 `kubectl` 二进制文件作为扩展的一部分被附带，您就可以在主机上生成 `kubectl -h` 命令并获取输出流：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"], {
  stream: {
    onOutput(data: { stdout: string } | { stderr: string }): void {
      if (data.stdout) {
        console.error(data.stdout);
      } else {
        console.log(data.stderr);
      }
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

您可以流式输出在后端容器或主机中执行的命令。

有关更多详细信息，请参阅 [Extension Host API 参考](/reference/api/extensions-sdk/ExtensionHost.md)

> 已弃用的扩展二进制文件调用
>
> 此方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

在主机上执行命令：

```typescript
window.ddClient.execHostCmd(`cliShippedOnHost xxx`).then((cmdResult: any) => {
  console.log(cmdResult);
});
```

流式输出在后端容器或主机中执行的命令：

```typescript
window.ddClient.spawnHostCmd(
  `cliShippedOnHost`,
  [`arg1`, `arg2`],
  (data: any, err: any) => {
    console.log(data.stdout, data.stderr);
    // Once the command exits we get the status code
    if (data.code) {
      console.log(data.code);
    }
  }
);
```

> [!NOTE]
>
>您不能在单个 `exec()` 调用中使用命令链（如 `cmd1 $(cmd2)` 或在命令之间使用管道）。
>
> 您需要为每个命令调用 `exec()`，并在需要时解析结果以将参数传递给下一个命令。
