---
description: 确保 Docker Desktop 在组织内正常运行所需的域名 URL 列表。
keywords: Docker Desktop, 允许列表, allowlist, allow list, 白名单, 防火墙, 身份验证 URL, 分析
title: Docker Desktop 允许列表
tags: [admin]
linkTitle: 允许列表
weight: 100
aliases:
  - /desktop/allow-list/
---

{{< summary-bar feature_name="允许列表" >}}

本页列出了您需要添加到防火墙允许列表（白名单）中的域名 URL，以确保 Docker Desktop 在您的组织内正常运行。

## 需要允许的域名 URL

| 域名                                                                              | 说明                                  |
| ------------------------------------------------------------------------------------ | -------------------------------------------- |
| https://api.segment.io                                                               | 分析 (Analytics)                                    |
| https://cdn.segment.com                                                              | 分析 (Analytics)                                    |
| https://notify.bugsnag.com                                                           | 错误报告 (Error reports)                                |
| https://sessions.bugsnag.com                                                         | 错误报告 (Error reports)                                |
| https://auth.docker.io                                                               | 身份验证 (Authentication)                               |
| https://cdn.auth0.com                                                                | 身份验证 (Authentication)                               |
| https://login.docker.com                                                             | 身份验证 (Authentication)                               |
| https://auth.docker.com                                                              | 身份验证 (Authentication)                               |
| https://desktop.docker.com                                                           | 更新 (Update)                                       |
| https://hub.docker.com                                                               | Docker Hub                                   |
| https://registry-1.docker.io                                                         | Docker 拉取/推送 (Docker Pull/Push)                             |
| https://production.cloudflare.docker.com                                             | Docker 拉取/推送 (Paid plans，付费方案)                |
| https://docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com | Docker 拉取/推送 (Personal plan / Anonymous，个人方案/匿名) |
| https://docker-pinata-support.s3.amazonaws.com                                       | 故障排除 (Troubleshooting)                              |
| https://api.dso.docker.com                                                           | Docker Scout 服务                         |
| https://api.docker.com                                                               | 新版 API                                      |