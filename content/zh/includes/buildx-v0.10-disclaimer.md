> [!NOTE]
>
> Buildx v0.10 启用了对最小 [SLSA Provenance](https://slsa.dev/provenance/)
> 证明的支持，这需要支持 [OCI 兼容的](https://github.com/opencontainers/image-spec)
> 多平台镜像。这可能会导致注册表和运行时支持方面的问题
> （例如 [Google Cloud Run 和 AWS Lambda](https://github.com/docker/buildx/issues/1533)）。
> 您可以选择使用 `--provenance=false` 禁用默认的 provenance 证明功能。
