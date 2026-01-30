---
description: 如何将 Docker Scout 与 Jenkins 集成
keywords: 供应链, 安全, ci, 持续集成, jenkins
title: 将 Docker Scout 与 Jenkins 集成
linkTitle: Jenkins
---

您可以将以下阶段和步骤定义添加到 `Jenkinsfile` 中，以将 Docker Scout 作为 Jenkins 管道的一部分运行。管道需要一个名为 `DOCKER_HUB` 的凭据，其中包含用于对 Docker Hub 进行身份验证的用户名和密码。它还需要为镜像和标签定义一个环境变量。

```groovy
pipeline {
    agent {
        // Agent 详情
    }

    environment {
        DOCKER_HUB = credentials('jenkins-docker-hub-credentials')
        IMAGE_TAG  = 'myorg/scout-demo-service:latest'
    }

    stages {
        stage('Analyze image') {
            steps {
                // 安装 Docker Scout
                sh 'curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /usr/local/bin'

                // 登录 Docker Hub
                sh 'echo $DOCKER_HUB_PSW | docker login -u $DOCKER_HUB_USR --password-stdin'

                // 分析并在发现危急 (critical) 或高危 (high) 漏洞时失败
                sh 'docker-scout cves $IMAGE_TAG --exit-code --only-severity critical,high'
            }
        }
    }
}
```

这将安装 Docker Scout，登录 Docker Hub，然后运行 Docker Scout 为某个镜像和标签生成 CVE 报告。它仅显示危急或高危漏洞。

> [!NOTE]
>
> 如果您看到与镜像缓存相关的 `permission denied` (权限被拒绝) 错误，请尝试将 [`DOCKER_SCOUT_CACHE_DIR`](/manuals/scout/how-tos/configure-cli.md) 环境变量设置为可写目录。或者，使用 `DOCKER_SCOUT_NO_CACHE=true` 完全禁用本地缓存。
