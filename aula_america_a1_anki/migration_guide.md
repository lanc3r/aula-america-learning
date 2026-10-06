# migration_guide

## 从旧版 Builder / 旧版本仓库迁移

音频缓存文件名由以下内容的哈希决定：

- model
- voice
- speed
- TTS instructions
- Spanish text

当前仓库继续保持既有 Cedar TTS 配置和缓存规则，因此旧版本的 `audio_cache` 可以直接复用。

操作：

1. 解压当前版本仓库。
2. 找到你上一版本中的 `audio_cache`。
3. 把其中所有 `.mp3` 复制到当前版本的 `audio_cache`。
4. 运行 `validate_content.command`。
5. 运行 `build_deck.command`。
6. 程序只会为当前版本新增且缓存中缺失的西语文本请求生成音频。

如果你不想在某台机器上调用 TTS，就不要运行构建；源内容和验证都不需要 API key。

## 导入 Anki

1. 先同步 Anki。
2. 在本地生成并导入当前版本 `release/aula_america_a1_v0_3_2.apkg`。
3. 允许 Anki 更新已有笔记。
4. 不导入其他人的学习进度。

本项目保持既有 deck ID、Note Type model ID、字段顺序和已发布 UID，因此正常升级时应更新原笔记，并保留既有复习进度。

完成后检查：

- 总卡片数量没有异常翻倍
- 原有复习进度仍在
- 新增卡片正常出现
- 听问即答卡只显示 Anki 自带播放按钮
- 新旧音频都可以播放
