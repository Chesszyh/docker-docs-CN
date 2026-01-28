--- 
title: 容器化 Ruby on Rails 应用程序
linkTitle: 容器化你的应用
weight: 10
keywords: ruby, flask, containerize, initialize
description: 了解如何容器化 Ruby on Rails 应用程序。
alias:
  - /language/ruby/build-images/
  - /language/ruby/run-containers/
  - /language/ruby/containerize/
  - /guides/language/ruby/containerize/
---

## 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例显示 Git CLI，但你可以使用任何客户端。

## 概述

本节将带你完成容器化并运行 [Ruby on Rails](https://rubyonrails.org/) 应用程序。

从 Rails 7.1 开始，[开箱即支持 Docker](https://guides.rubyonrails.org/7_1_release_notes.html#generate-dockerfiles-for-new-rails-applications)。这意味着当你创建一个新的 Rails 应用程序时，你会得到为你生成的 `Dockerfile`、`.dockerignore` 和 `bin/docker-entrypoint` 文件。

如果你有一个现有的 Rails 应用程序，你将需要手动创建 Docker 资产。遗憾的是，`docker init` 命令尚不支持 Rails。这意味着如果你正在使用 Rails，你需要从下面的示例中手动复制 Dockerfile 和其他相关配置。

## 1. 初始化 Docker 资产

Rails 7.1 开箱即生成多阶段 Dockerfile，下面是从 Rails 模板生成的此类文件的示例。

> 多阶段 Dockerfile 通过分离构建和运行时依赖项，确保最终镜像中仅包含必要的组件，从而帮助创建更小、更高效的镜像。在 [多阶段构建指南](/get-started/docker-concepts/building-images/multi-stage-builds/) 中阅读更多内容。

虽然 Dockerfile 是自动生成的，但了解其用途和功能很重要。强烈建议查看以下示例。


```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
# check=error=true

# This Dockerfile is designed for production, not development.
# docker build -t app . 
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<value from config/master.key> --name app app

# For a containerized dev environment, see Dev Containers: https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# Make sure RUBY_VERSION matches the Ruby version in .ruby-version
ARG RUBY_VERSION=3.3.6
FROM docker.io/library/ruby:$RUBY_VERSION-slim AS base

# Rails app lives here
WORKDIR /rails

# Install base packages
# Replace libpq-dev with sqlite3 if using SQLite, or libmysqlclient-dev if using MySQL
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Set production environment
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# Throw-away build stage to reduce size of final image
FROM base AS build

# Install packages needed to build gems
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Install JavaScript dependencies and Node.js for asset compilation
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# Install application gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# Install node modules
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# Copy application code
COPY . .

# Precompile bootsnap code for faster boot times
RUN bundle exec bootsnap precompile app/ lib/

# Precompiling assets for production without requiring secret RAILS_MASTER_KEY
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# Final stage for app image
FROM base

# Copy built artifacts: gems, application
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# Run and own only the runtime files as a non-root user for security
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# Entrypoint prepares the database.
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# Start server via Thruster by default, this can be overwritten at runtime
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```

上面的 Dockerfile 假设你正在使用 Thruster 与 Puma 一起作为应用程序服务器。如果你使用任何其他服务器，你可以将最后三行替换为以下内容：

```dockerfile
# Start the application server
EXPOSE 3000
CMD ["./bin/rails", "server"]
```

此 Dockerfile 使用位于 `./bin/docker-entrypoint` 的脚本作为容器的入口点。此脚本准备数据库并运行应用程序服务器。下面是此类脚本的一个示例。

```bash {title=docker-entrypoint}
#!/bin/bash -e

# Enable jemalloc for reduced memory usage and latency.
if [ -z "${LD_PRELOAD+x}" ]; then
    LD_PRELOAD=$(find /usr/lib -name libjemalloc.so.2 -print -quit)
    export LD_PRELOAD
fi

# If running the rails server then create or migrate existing database
if [ "${@: -2:1}" == "./bin/rails" ] && [ "${@: -1:1}" == "server" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
```

除了上面的两个文件之外，你还需要一个 `.dockerignore` 文件。此文件用于从构建上下文中排除文件和目录。下面是 `.dockerignore` 文件的一个示例。

```text {collapse=true,title=".dockerignore"}
# See https://docs.docker.com/engine/reference/builder/#dockerignore-file for more about ignoring files.

# Ignore git directory.
/.git/
/.gitignore

# Ignore bundler config.
/.bundle

# Ignore all environment files.
/.env*

# Ignore all default key files.
/config/master.key
/config/credentials/*.key

# Ignore all logfiles and tempfiles.
/log/*
/tmp/*
!/log/.keep
!/tmp/.keep

# Ignore pidfiles, but keep the directory.
/tmp/pids/*
!/tmp/pids/.keep

# Ignore storage (uploaded files in development and any SQLite databases).
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/.keep

# Ignore assets.
/node_modules/
/app/assets/builds/*
!/app/assets/builds/.keep
/public/assets

# Ignore CI service files.
/.github

# Ignore development files
/.devcontainer

# Ignore Docker-related files
/.dockerignore
/Dockerfile*
```

你可能需要的最后一个可选文件是 `compose.yaml` 文件，Docker Compose 使用它来定义构成应用程序的服务。由于使用 SQLite 作为数据库，因此不需要为数据库定义单独的服务。唯一需要的服务是 Rails 应用程序本身。

```yaml {title=compose.yaml}
services:
  web:
    build: .
    environment:
      - RAILS_MASTER_KEY
    ports:
      - "3000:80"
```

你现在的应用程序文件夹中应该有以下文件：

- `.dockerignore`
- `compose.yaml`
- `Dockerfile`
- `bin/docker-entrypoint`

要了解有关文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile)
- [.dockerignore](/reference/dockerfile#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)
- [docker-entrypoint](/reference/dockerfile/#entrypoint)

## 2. 运行应用程序

要运行应用程序，请在应用程序目录内的终端中运行以下命令。

```console
$ RAILS_MASTER_KEY=<master_key_value> docker compose up --build
```

打开浏览器并在 [http://localhost:3000](http://localhost:3000) 查看应用程序。你应该会看到一个简单的 Ruby on Rails 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

## 3. 在后台运行应用程序

你可以通过添加 `-d` 选项使应用程序与终端分离运行。在 `docker-ruby-on-rails` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:3000](http://localhost:3000) 查看应用程序。

你应该会看到一个简单的 Ruby on Rails 应用程序。

在终端中，运行以下命令来停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，你学习了如何使用 Docker 容器化并运行你的 Ruby 应用程序。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，你将了解如何使用 GitHub Actions 设置 CI/CD 管道。

