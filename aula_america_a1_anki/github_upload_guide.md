# github_upload_guide

1. 本地运行 `build_deck.command`。
2. 运行 `prepare_github_upload.command`。
3. 打开生成的 `github_upload` 文件夹。
4. 把其中全部内容上传到 GitHub 仓库根目录。

建议仓库名称：

`aula_america_a1_anki`

GitHub 仓库保留源码，不长期保存本地生成产物。`audio_cache/`、
`output/`、`release/` 和 `github_upload/` 都应保持在本地构建环境中。

以后常规更新主要替换：

- `changelog.md`
- 有变化的 `content/unidad_XX.json`
- 有变化的 `config/*.json`
- 有变化的 `docs/`、`scripts/` 或 `templates/`

模板和生成器通常不再改变。
