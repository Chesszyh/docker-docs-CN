---
description: Docker Desktop 在组织内正常运行所需的域名 URL 列表。
keywords: Docker Desktop, 允许列表, allowlist, 防火墙, 身份验证 URL, 分析
title: Docker Desktop 允许列表 (Allowlist)
tags: [管理]
linkTitle: 允许列表
weight: 100
aliases:
  - /desktop/allow-list/
---

{{< summary-bar feature_name="允许列表" >}}

本页包含您需要添加到防火墙允许列表中的域名 URL，以确保 Docker Desktop 在您的组织内正常运行。

## 需要允许的域名 URL

| 域名 | 描述 |
| ------------------------------------------------------------------------------------ | -------------------------------------------- |
| https://api.segment.io                                                               | 数据分析                                    |
| https://cdn.segment.com                                                              | 数据分析                                    |
| https://notify.bugsnag.com                                                           | 错误报告                                |
| https://sessions.bugsnag.com                                                         | 错误报告                                |
| https://auth.docker.io                                                               | 身份验证                               |
| https://cdn.auth0.com                                                                | 身份验证                               |
| https://login.docker.com                                                             | 身份验证                               |
| https://auth.docker.com                                                              | 身份验证                               |
| https://desktop.docker.com                                                           | 更新                                       |
| https://hub.docker.com                                                               | Docker Hub                                   |
| https://registry-1.docker.io                                                         | Docker 拉取/推送                             |
| https://production.cloudflare.docker.com                                             | Docker 拉取/推送 (付费计划)                |
| https://docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com | Docker 拉取/推送 (个人计划 / 匿名) |
| https://docker-pinata-support.s3.amazonaws.com                                       | 故障排除                              |
| https://api.dso.docker.com                                                           | Docker Scout 服务                         |
| https://api.docker.com                                                               | 新 API                                      |
