---
title: 运行你的 Java 测试
linkTitle: 运行测试
weight: 30
keywords: Java, build, test
description: 如何构建和运行你的 Java 测试
alias:
  - /language/java/run-tests/
  - /guides/language/java/run-tests/
---

## 先决条件

完成本指南的所有前面部分，从 [容器化 Java 应用程序](containerize.md) 开始。

## 概览

测试是现代软件开发的重要组成部分。测试对不同的开发团队来说可能意味着很多事情。有单元测试、集成测试和端到端测试。在本指南中，你将了解如何在 Docker 中运行单元测试。

### 用于测试的多阶段 Dockerfile

在以下示例中，你将把测试命令拉入你的 Dockerfile。
将你的 Dockerfile 的内容替换为以下内容。

```dockerfile {hl_lines="3-19"}
# syntax=docker/dockerfile:1

FROM eclipse-temurin:21-jdk-jammy as base
WORKDIR /build
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/

FROM base as test
WORKDIR /build
COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw test

FROM base as deps
WORKDIR /build
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw dependency:go-offline -DskipTests

FROM deps as package
WORKDIR /build
COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

FROM package as extract
WORKDIR /build
RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

FROM extract as development
WORKDIR /build
RUN cp -r /build/target/extracted/dependencies/. ./ 
RUN cp -r /build/target/extracted/spring-boot-loader/. ./ 
RUN cp -r /build/target/extracted/snapshot-dependencies/. ./ 
RUN cp -r /build/target/extracted/application/. ./ 
ENV JAVA_TOOL_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8000"
CMD [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]

FROM eclipse-temurin:21-jre-jammy AS final
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
COPY --from=extract build/target/extracted/dependencies/ ./ 
COPY --from=extract build/target/extracted/spring-boot-loader/ ./ 
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./ 
COPY --from=extract build/target/extracted/application/ ./ 
EXPOSE 8080
ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

首先，你添加了一个新的 base 阶段。在 base 阶段，你添加了 test 和 deps 阶段都需要的通用指令。

接下来，你基于 base 阶段添加了一个名为 `test` 的新测试阶段。
在此阶段，你复制了必要的源文件，然后指定 `RUN` 来运行 `./mvnw test`。
你使用 `RUN` 而不是 `CMD` 来运行测试。
原因是 `CMD` 指令在容器运行时运行，而 `RUN` 指令在构建镜像时运行。
使用 `RUN` 时，如果测试失败，构建将失败。

最后，你将 deps 阶段更新为基于 base 阶段，并删除了现在位于 base 阶段的指令。

运行以下命令以使用测试阶段作为目标构建新镜像并查看测试结果。包括 `--progress=plain` 以查看构建输出，`--no-cache` 以确保测试始终运行，以及 `--target test` 以针对测试阶段。

现在，构建你的镜像并运行你的测试。你将运行 `docker build` 命令并添加 `--target test` 标志，以便专门运行测试构建阶段。

```console
$ docker build -t java-docker-image-test --progress=plain --no-cache --target=test .
```

你应该看到包含以下内容的输出

```console
... 

#15 101.3 [WARNING] Tests run: 45, Failures: 0, Errors: 0, Skipped: 2
#15 101.3 [INFO] 
#15 101.3 [INFO] ------------------------------------------------------------------------
#15 101.3 [INFO] BUILD SUCCESS
#15 101.3 [INFO] ------------------------------------------------------------------------
#15 101.3 [INFO] Total time:  01:39 min
#15 101.3 [INFO] Finished at: 2024-02-01T23:24:48Z
#15 101.3 [INFO] ------------------------------------------------------------------------
#15 DONE 101.4s
```

## 后续步骤

在下一节中，你将了解如何使用 GitHub Actions 设置 CI/CD 管道。

```