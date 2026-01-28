---
title: 在容器中运行 Angular 测试
linkTitle: 运行您的测试
weight: 40
keywords: angular, test, jasmine
description: 了解如何在容器中运行 Angular 测试。

---

## 前提条件

完成本指南的所有前面章节，从[容器化 Angular 应用程序](containerize.md)开始。

## 概述

测试是开发过程中的关键部分。在本节中，您将学习如何：

- 在 Docker 容器内使用 Angular CLI 运行 Jasmine 单元测试。
- 使用 Docker Compose 隔离您的测试环境。
- 确保本地测试和基于容器的测试之间的一致性。


`docker-angular-sample` 项目预配置了 Jasmine，因此您无需额外设置即可快速开始。

---

## 在开发期间运行测试

`docker-angular-sample` 应用程序在以下位置包含一个示例测试文件：

```console
$ src/app/app.component.spec.ts
```

此测试使用 Jasmine 验证 AppComponent 逻辑。

### 步骤 1：更新 compose.yaml

向 `compose.yaml` 文件添加一个名为 `angular-test` 的新服务。此服务允许您在隔离的容器化环境中运行测试套件。

```yaml {hl_lines="22-26",linenos=true}
services:
  angular-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    develop:
      watch:
        - action: sync
          path: .
          target: /app

  angular-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-angular-sample
    ports:
      - "8080:8080"

  angular-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["npm", "run", "test"]

```

angular-test 服务重用与[开发](develop.md)相同的 `Dockerfile.dev`，并覆盖默认命令以使用 `npm run test` 运行测试。此设置确保测试环境与本地开发配置一致。


完成前面的步骤后，您的项目目录应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 步骤 2：运行测试

要在容器内执行测试套件，请从项目根目录运行以下命令：

```console
$ docker compose run --rm angular-test
```

此命令将：
- 启动 `compose.yaml` 文件中定义的 `angular-test` 服务。
- 使用与开发相同的环境执行 `npm run test` 脚本。
- 测试完成后使用 [`docker compose run --rm`](/engine/reference/commandline/compose_run) 命令自动删除容器。

您应该看到类似以下的输出：

```shell
Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        1.529 s
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI
> 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本节中，您学习了如何使用 Jasmine 和 Docker Compose 在 Docker 容器内运行 Angular 应用程序的单元测试。

您完成的内容：
- 在 `compose.yaml` 中创建了 `angular-test` 服务以隔离测试执行。
- 重用开发 `Dockerfile.dev` 以确保开发和测试环境之间的一致性。
- 使用 `docker compose run --rm angular-test` 在容器内运行测试。
- 确保了跨环境可靠、可重复的测试，而不依赖于本地机器设置。

---

## 相关资源

探索官方参考和最佳实践以优化您的 Docker 测试工作流程：

- [Dockerfile 参考](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 了解在 `compose.yaml` 中配置服务的完整语法和选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。
---

## 下一步

接下来，您将学习如何使用 GitHub Actions 设置 CI/CD 流水线，以便在容器化环境中自动构建和测试 Angular 应用程序。这确保您的代码在每次推送或拉取请求时都经过验证，保持开发工作流程的一致性和可靠性。
