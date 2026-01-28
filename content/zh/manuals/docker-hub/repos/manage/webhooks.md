---
description: Docker Hub Webhooks
keywords: Docker, webhooks, hub, builds
title: Webhooks
weight: 80
aliases:
- /docker-hub/webhooks/
---

您可以使用 webhooks 在仓库中发生推送事件时触发另一个服务中的操作。Webhooks 是发送到您在 Docker Hub 中定义的 URL 的 POST 请求。

## 创建 webhook

要创建 webhook：
1. 在您选择的仓库中，选择 **Webhooks** 标签。
2. 为 webhook 提供一个名称。
3. 提供目标 webhook URL。这是 webhook POST 请求发送的目的地。
4. 选择 **Create**。

## 查看 webhook 传递历史

要查看 webhook 的历史记录：
1. 将鼠标悬停在 **Current Webhooks section** 下的 webhook 上。
2. 选择 **Menu options** 图标。
3. 选择 **View History**。

然后您可以查看传递历史，以及 POST 请求传递是否成功。

## 示例 webhook 负载

Webhook 负载具有以下 JSON 格式：

```json
{
  "callback_url": "https://registry.hub.docker.com/u/svendowideit/testhook/hook/2141b5bi5i5b02bec211i4eeih0242eg11000a/",
  "push_data": {
    "pushed_at": 1417566161,
    "pusher": "trustedbuilder",
    "tag": "latest"
  },
  "repository": {
    "comment_count": 0,
    "date_created": 1417494799,
    "description": "",
    "dockerfile": "#\n# BUILD\u0009\u0009docker build -t svendowideit/apt-cacher .\n# RUN\u0009\u0009docker run -d -p 3142:3142 -name apt-cacher-run apt-cacher\n#\n# and then you can run containers with:\n# \u0009\u0009docker run -t -i -rm -e http_proxy http://192.168.1.2:3142/ debian bash\n#\nFROM\u0009\u0009ubuntu\n\n\nVOLUME\u0009\u0009[/var/cache/apt-cacher-ng]\nRUN\u0009\u0009apt-get update ; apt-get install -yq apt-cacher-ng\n\nEXPOSE \u0009\u00093142\nCMD\u0009\u0009chmod 777 /var/cache/apt-cacher-ng ; /etc/init.d/apt-cacher-ng start ; tail -f /var/log/apt-cacher-ng/*\n",
    "full_description": "Docker Hub based automated build from a GitHub repo",
    "is_official": false,
    "is_private": true,
    "is_trusted": true,
    "name": "testhook",
    "namespace": "svendowideit",
    "owner": "svendowideit",
    "repo_name": "svendowideit/testhook",
    "repo_url": "https://registry.hub.docker.com/u/svendowideit/testhook/",
    "star_count": 0,
    "status": "Active"
  }
}
```
