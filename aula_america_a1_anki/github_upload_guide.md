# github_upload_guide

1. 本地运行 `build_deck.command`。
2. 确认 `release` 中已经有最新 `.apkg`。
3. 运行 `prepare_github_upload.command`。
4. 打开生成的 `github_upload` 文件夹。
5. 把其中全部内容上传到 GitHub 仓库根目录。

建议仓库名称：

`aula_america_a1_anki`

以后常规发布主要替换：

- `release/aula_america_a1_vX_X_X.apkg`
- `release/release_manifest.json`
- `release/content_summary.tsv`
- `changelog.md`
- 有变化的 `content/unidad_XX.json`

模板和生成器通常不再改变。
