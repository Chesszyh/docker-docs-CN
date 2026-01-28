---
title: 扩展 UI API
description: Docker 扩展开发概述
keywords: Docker, extensions, sdk, development
aliases:
 - /desktop/extensions-sdk/dev/api/overview/
---

扩展 UI 运行在沙盒环境中，无法访问任何 electron 或 nodejs API。

扩展 UI API 提供了一种方式，让前端可以执行不同的操作，并与 Docker Desktop 仪表板或底层系统进行通信。

提供带有 Typescript 支持的 JavaScript API 库，以便在您的扩展代码中获取所有 API 定义。

- [@docker/extension-api-client](https://www.npmjs.com/package/@docker/extension-api-client) 提供对扩展 API 入口点 `DockerDesktopClient` 的访问。
- [@docker/extension-api-client-types](https://www.npmjs.com/package/@docker/extension-api-client-types) 可以作为开发依赖项添加，以便在您的 IDE 中获得类型自动补全。

```Typescript
import { createDockerDesktopClient } from '@docker/extension-api-client';

export function App() {
  // obtain Docker Desktop client
  const ddClient = createDockerDesktopClient();
  // use ddClient to perform extension actions
}
```

`ddClient` 对象提供对各种 API 的访问：

- [扩展后端](backend.md)
- [Docker](docker.md)
- [仪表板](dashboard.md)
- [导航](dashboard-routes-navigation.md)

在[此处](reference/api/extensions-sdk/_index.md)查找扩展 API 参考。
