---
title: 使用环境变量配置 Docker Scout
linkTitle: Docker Scout 环境变量
description: 使用这些环境变量配置 Docker Scout CLI 命令的行为
keywords: scout, supply chain, cli, environment, variables, env, vars, configure
aliases:
  - /scout/env-vars/
---

以下环境变量可用于配置 Docker Scout CLI 命令以及相应的 `docker/scout-cli` 容器镜像：

| 名称                                    | 格式    | 描述                                                                                        |
| :-------------------------------------- | ------- | :------------------------------------------------------------------------------------------ |
| DOCKER_SCOUT_CACHE_FORMAT               | String  | 本地镜像缓存的格式；可以是 `oci` 或 `tar`（默认值：`oci`）                                  |
| DOCKER_SCOUT_CACHE_DIR                  | String  | 存储本地 SBOM 缓存的目录（默认值：`$HOME/.docker/scout`）                                   |
| DOCKER_SCOUT_NO_CACHE                   | Boolean | 设置为 `true` 时，禁用本地 SBOM 缓存的使用                                                  |
| DOCKER_SCOUT_OFFLINE                    | Boolean | 在索引 SBOM 时使用[离线模式](#offline-mode)                                                 |
| DOCKER_SCOUT_REGISTRY_TOKEN             | String  | 拉取镜像时用于镜像仓库身份验证的令牌                                                        |
| DOCKER_SCOUT_REGISTRY_USER              | String  | 拉取镜像时用于镜像仓库身份验证的用户名                                                      |
| DOCKER_SCOUT_REGISTRY_PASSWORD          | String  | 拉取镜像时用于镜像仓库身份验证的密码或个人访问令牌                                          |
| DOCKER_SCOUT_HUB_USER                   | String  | 用于 Docker Scout 后端身份验证的 Docker Hub 用户名                                          |
| DOCKER_SCOUT_HUB_PASSWORD               | String  | 用于 Docker Scout 后端身份验证的 Docker Hub 密码或个人访问令牌                              |
| DOCKER_SCOUT_NEW_VERSION_WARN           | Boolean | 当有新版本的 Docker Scout CLI 可用时发出警告                                                |
| DOCKER_SCOUT_EXPERIMENTAL_WARN          | Boolean | 对实验性功能发出警告                                                                        |
| DOCKER_SCOUT_EXPERIMENTAL_POLICY_OUTPUT | Boolean | 禁用策略评估的实验性输出                                                                    |

## 离线模式

在正常操作下，Docker Scout 会交叉引用外部系统（如 npm、NuGet 或 proxy.golang.org）来检索镜像中发现的软件包的额外信息。

当 `DOCKER_SCOUT_OFFLINE` 设置为 `true` 时，Docker Scout 镜像分析将以离线模式运行。离线模式意味着 Docker Scout 不会向外部系统发出出站请求。

要使用离线模式：

```console
$ export DOCKER_SCOUT_OFFLINE=true
```
