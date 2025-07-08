---
title: "接口: Docker"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/Docker/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/Docker/
---

**`自`**

0.2.0

## 属性

### cli

• `只读` **cli**: [`DockerCommand`](DockerCommand.md)

您也可以直接执行 Docker 二进制文件。

```typescript
const output = await ddClient.docker.cli.exec("volume", [
  "ls",
  "--filter",
  "dangling=true"
]);
```

输出：

```json
{
  "stderr": "...",
  "stdout": "..."
}
```

为方便起见，命令结果对象还具有根据输出格式轻松解析它的方法。请参阅 [ExecResult](ExecResult.md)。

---

流式传输 Docker 命令执行的输出。
当命令输出过长或需要以流形式获取输出时，这很有用。

```typescript
await ddClient.docker.cli.exec("logs", ["-f", "..."], {
  stream: {
    onOutput(data): void {
        // 由于我们可以同时接收 `stdout` 和 `stderr`，因此我们将它们包装在 JSON 对象中
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

## 方法

### listContainers

▸ **listContainers**(`options?`): `Promise`<`unknown`\>

获取正在运行的容器列表（与 `docker ps` 相同）。

默认情况下，这不会列出已停止的容器。
您可以使用选项 `{"all": true}` 列出所有正在运行和已停止的容器。

```typescript
const containers = await ddClient.docker.listContainers();
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `options?` | `any` | （可选）。一个 JSON 对象，例如 `{ "all": true, "limit": 10, "size": true, "filters": JSON.stringify({ status: ["exited"] }), }`。有关不同属性的更多信息，请参阅 [Docker API 端点文档](https://docs.docker.com/engine/api/v1.41/#operation/ContainerList)。 |

#### 返回值

`Promise`<`unknown`\>

---

### listImages

▸ **listImages**(`options?`): `Promise`<`unknown`\>

获取本地容器镜像列表

```typescript
const images = await ddClient.docker.listImages();
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `options?` | `any` | （可选）。一个 JSON 对象，例如 `{ "all": true, "filters": JSON.stringify({ dangling: ["true"] }), "digests": true * }`。有关不同属性的更多信息，请参阅 [Docker API 端点文档](https://docs.docker.com/engine/api/v1.41/#tag/Image)。 |

#### 返回值

`Promise`<`unknown`\>
