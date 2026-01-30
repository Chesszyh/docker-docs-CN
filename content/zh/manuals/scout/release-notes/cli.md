---
title: Docker Scout CLI 发布说明
linkTitle: CLI 发布说明
description: 了解 Docker Scout CLI 插件的最新功能
keywords: docker scout, 发布说明, 更新日志, cli, 功能, 变化, 增量, 新版本, 发布, github actions
---

本页包含有关 Docker Scout [CLI 插件](https://github.com/docker/scout-cli/) 和 `docker/scout-action` [GitHub Action](https://github.com/docker/scout-action) 的新功能、改进、已知问题和错误修复的信息。

## 1.15.0

{{< release-date date="2024-10-31" >}}

### 新功能

- 为 `docker scout sbom` 添加了新的 `--format=cyclonedx` 标志，以 CycloneDX 格式输出 SBOM。

### 改进

- 在 CVE 摘要中采用从高到低的排序顺序。
- 支持启用和禁用通过 `docker scout push` 或 `docker scout watch` 启用的仓库。

### 错误修复

- 改进了在没有证明的情况下分析 `oci` 目录时的消息提示。仅支持单平台镜像和*带有证明*的多平台镜像。不支持不带证明的多平台镜像。
- 改进了分类器和 SBOM 索引器：
  - 添加了 Liquibase `lpm` 的分类器。
  - 添加了 Rakudo Star/MoarVM 二进制分类器。
  - 添加了 silverpeas 实用工具的二进制分类器。
- 改进了使用 containerd 镜像存储时证明的读取和缓存。

## 1.14.0

{{< release-date date="2024-09-24" >}}

### 新功能

- 在 `docker scout cves` 命令中添加了 CVE 级别的抑制信息。

### 错误修复

- 修复了列出悬空镜像 (dangling images) CVE 的问题，例如：`local://sha256:...`
- 修复了分析文件系统输入时发生的崩溃 (panic)，例如使用 `docker scout cves fs://.`

## 1.13.0

{{< release-date date="2024-08-05" >}}

### 新功能

- 为 `docker scout quickview`、`docker scout policy` 和 `docker scout compare` 命令添加了 `--only-policy` 过滤选项。
- 为 `docker scout cves` 和 `docker scout quickview` 命令添加了 `--ignore-suppressed` 过滤选项，以过滤掉受 [例外](/scout/explore/exceptions/) 影响的 CVE。

### 错误修复与改进

- 在检查中使用条件策略名称。
- 增加了对使用链接器标志 (linker flags) 设置的 Go 项目版本的检测支持，例如：

  ```console
  $ go build -ldflags "-X main.Version=1.2.3"
  ```

## 1.12.0

{{< release-date date="2024-07-31" >}}

### 新功能

- 仅显示基础镜像中的漏洞：

  ```console {title="CLI"}
  $ docker scout cves --only-base IMAGE
  ```

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: cves
    image: [IMAGE]
    only-base: true
  ```

- 在 `quickview` 命令中考虑 VEX。

  ```console {title="CLI"}
  $ docker scout quickview IMAGE --only-vex-affected --vex-location ./path/to/my.vex.json
  ```

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: quickview
    image: [IMAGE]
    only-vex-affected: true
    vex-location: ./path/to/my.vex.json
  ```

- 在 `cves` 命令 (GitHub Actions) 中考虑 VEX。

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: cves
    image: [IMAGE]
    only-vex-affected: true
    vex-location: ./path/to/my.vex.json
  ```

### 错误修复与改进

- 将 `github.com/docker/docker` 更新为 `v26.1.5+incompatible` 以修复 CVE-2024-41110。
- 将 Syft 更新为 1.10.0。

## 1.11.0

{{< release-date date="2024-07-25" >}}

### 新功能

- 过滤 CISA 已知利用漏洞 (KEV) 目录中列出的 CVE。

  ```console {title="CLI"}
  $ docker scout cves [IMAGE] --only-cisa-kev

  ... (裁剪后的输出) ...
  ## Packages and Vulnerabilities

  0C     1H     0M     0L  io.netty/netty-codec-http2 4.1.97.Final
  pkg:maven/io.netty/netty-codec-http2@4.1.97.Final

  ✗ HIGH CVE-2023-44487  CISA KEV  [OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities]
    https://scout.docker.com/v/CVE-2023-44487
    Affected range  : <4.1.100
    Fixed version   : 4.1.100.Final
    CVSS Score      : 7.5
    CVSS Vector     : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H
  ... (裁剪后的输出) ...
  ```

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: cves
    image: [IMAGE]
    only-cisa-kev: true
  ```

- 添加了新的分类器：
  - `spiped`
  - `swift`
  - `eclipse-mosquitto`
  - `znc`

### 错误修复与改进

- 允许在没有子组件时进行 VEX 匹配。
- 修复了附加无效 VEX 文档时发生的崩溃。
- 修复了 SPDX 文档根。
- 修复了镜像使用 SCRATCH 作为基础镜像时的基础镜像检测。

## 1.10.0

{{< release-date date="2024-06-26" >}}

### 错误修复与改进

- 添加了新的分类器：
  - `irssi`
  - `Backdrop`
  - `CrateDB CLI (Crash)`
  - `monica`
  - `Openliberty`
  - `dumb-init`
  - `friendica`
  - `redmine`
- 修复了软件包上仅包含空格的制作者 (originator) 导致 BuildKit 导出器中断的问题。
- 修复了带摘要镜像的 SPDX 声明中镜像引用的解析问题。
- 为镜像比较支持 `sbom://` 前缀：

  ```console {title="CLI"}
  $ docker scout compare sbom://image1.json --to sbom://image2.json
  ```

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: compare
    image: sbom://image1.json
    to: sbom://image2.json
  ```

## 1.9.3

{{< release-date date="2024-05-28" >}}

### 错误修复

- 修复了检索缓存 SBOM 时发生的崩溃。

## 1.9.1

{{< release-date date="2024-05-27" >}}

### 新功能

- 在 `docker scout cves` 命令中通过 `--format gitlab` 增加了对 [GitLab 容器扫描文件格式](https://docs.gitlab.com/ee/development/integrations/secure.html#container-scanning) 的支持。

  以下是一个管道示例：

  ```yaml
     docker-build:
    # 使用官方 docker 镜像。
    image: docker:cli
    stage: build
    services:
      - docker:dind
    variables:
      DOCKER_IMAGE_NAME: $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
    before_script:
      - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY

      # 安装 curl 和 Docker Scout CLI
      - |
        apk add --update curl
        curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
        apk del curl
        rm -rf /var/cache/apk/*
      # 运行 Docker Scout CLI 需要登录 Docker Hub
      - echo "$DOCKER_HUB_PAT" | docker login --username "$DOCKER_HUB_USER" --password-stdin

    # 所有分支都使用 $DOCKER_IMAGE_NAME 打标签 (默认为 commit ref slug)
    # 默认分支还使用 `latest` 打标签
    script:
      - docker buildx b --pull -t "$DOCKER_IMAGE_NAME" .
      - docker scout cves "$DOCKER_IMAGE_NAME" --format gitlab --output gl-container-scanning-report.json
      - docker push "$DOCKER_IMAGE_NAME"
      - |
        if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
          docker tag "$DOCKER_IMAGE_NAME" "$CI_REGISTRY_IMAGE:latest"
          docker push "$CI_REGISTRY_IMAGE:latest"
        fi
    # 仅在存在 Dockerfile 的分支中运行此任务
    rules:
      - if: $CI_COMMIT_BRANCH
        exists:
          - Dockerfile
    artifacts:
      reports:
        container_scanning: gl-container-scanning-report.json
  ```

### 错误修复与改进

- `docker scout attest add` 命令支持单架构镜像。
- 在 `docker scout quickview` 和 `docker scout recommendations` 命令中指示镜像来源是否未使用 `mode=max` 创建。如果不使用 `mode=max`，基础镜像可能会被错误检测，导致结果准确性降低。

## 1.9.0

{{< release-date date="2024-05-24" >}}

已废弃，建议使用 [1.9.1](#191)。

## 1.8.0

{{< release-date date="2024-04-25" >}}

### 错误修复与改进

- 改进了 EPSS 评分和百分位数的格式。

  修改前：

  ```text
  EPSS Score      : 0.000440
  EPSS Percentile : 0.092510
  ```

  修改后：

  ```text
  EPSS Score      : 0.04%
  EPSS Percentile : 9th percentile
  ```

- 修复了分析本地文件系统时 `docker scout cves` 命令的 markdown 输出。 [docker/scout-cli#113](https://github.com/docker/scout-cli/issues/113)

## 1.7.0

{{< release-date date="2024-04-15" >}}

### 新功能

- [`docker scout push` 命令](/reference/cli/docker/scout/push/) 现在已正式发布：在本地分析镜像并将 SBOM 推送到 Docker Scout。

### 错误修复与改进

- 修复了使用 `docker scout attestation add` 为私有仓库中的镜像添加证明的问题。
- 修复了基于空 `scratch` 基础镜像的镜像处理。
- Docker Scout CLI 命令的新 `sbom://` 协议允许您从标准输入读取 Docker Scout SBOM。

  ```console
  $ docker scout sbom IMAGE | docker scout qv sbom://
  ```

- 添加了 Joomla 软件包的分类器。

## 1.6.4

{{< release-date date="2024-03-26" >}}

### 错误修复与改进

- 修复了基于 RPM 的 Linux 发行版的 epoch 处理。

## 1.6.3

{{< release-date date="2024-03-22" >}}

### 错误修复与改进

- 改进了软件包检测，以忽略已引用但未安装的软件包。

## 1.6.2

{{< release-date date="2024-03-22" >}}

### 错误修复与改进

- EPSS 数据现在通过后端获取，而不是通过 CLI 客户端获取。
- 修复了使用 `sbom://` 前缀渲染 markdown 输出时的一个问题。

### 移除

- 移除了 `docker scout cves --epss-date` 和 `docker scout cache prune --epss` 标志。

## 1.6.1

{{< release-date date="2024-03-20" >}}

> [!NOTE]
>
> 此版本仅影响 `docker/scout-action` GitHub Action。

### 新功能

- 增加了对传入 SDPX 或 in-toto SDPX 格式的 SBOM 文件的支持。

  ```yaml
  uses: docker/scout-action@v1
  with:
      command: cves
      image: sbom://alpine.spdx.json
  ```

- 增加了对 `syft-json` 格式 SBOM 文件的支持。

  ```yaml
  uses: docker/scout-action@v1
  with:
      command: cves
      image: sbom://alpine.syft.json
  ```

## 1.6.0

{{< release-date date="2024-03-19" >}}

> [!NOTE]
>
> 此版本仅影响 CLI 插件，不影响 GitHub Action。

### 新功能

- 增加了对传入 SDPX 或 in-toto SDPX 格式的 SBOM 文件的支持。

  ```console
  $ docker scout cves sbom://path/to/sbom.spdx.json
  ```

- 增加了对 `syft-json` 格式 SBOM 文件的支持。

  ```console
  $ docker scout cves sbom://path/to/sbom.syft.json
  ```

- 支持从标准输入读取 SBOM 文件。

  ```console
  $ syft -o json alpine | docker scout cves sbom://
  ```

- 根据 EPSS 评分确定 CVE 的优先级。

  - 使用 `--epss` 显示并划分 CVE 优先级。
  - 使用 `--epss-score` 和 `--epss-percentile` 根据评分和百分位数进行过滤。
  - 使用 `docker scout cache prune --epss` 清除缓存的 EPSS 文件。

### 错误修复与改进

- 从 WSL2 使用 Windows 缓存。

  在运行 Docker Desktop 的 WSL2 内部，Docker Scout CLI 插件现在会使用 Windows 的缓存。这样，如果镜像已被 Docker Desktop 索引，则无需在 WSL2 侧重新索引。
- 如果通过 [设置管理 (Settings Management)](/manuals/security/for-admins/hardened-desktop/settings-management/_index.md) 功能禁用了索引，则 CLI 中的索引操作现在会被阻止。

- 修复了分析单个镜像 `oci-dir` 输入时发生的崩溃。
- 改进了使用 containerd 镜像存储时对本地证明的支持。

## 早期版本

Docker Scout CLI 插件早期版本的发布说明可在 [GitHub](https://github.com/docker/scout-cli/releases) 上查看。
