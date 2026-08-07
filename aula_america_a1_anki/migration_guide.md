# migration_guide

## 从旧版 Builder 迁移

旧版音频文件名由以下内容的哈希决定：

- model
- voice
- speed
- tts instructions
- spanish text

新仓库保持了相同的 TTS 配置和哈希算法，因此旧版 `audio_cache` 可以直接复用。

操作：

1. 找到旧版 `Aula_Anki_Cedar_Builder`。
2. 打开旧版 `audio_cache`。
3. 复制其中所有 `.mp3`。
4. 粘贴到新仓库的 `audio_cache`。
5. 运行 `build_deck.command`。

当前 21 张卡使用的西语文本没有改变，因此音频齐全时不会重新调用 API。

## 导入 Anki

1. 先同步 Anki。
2. 导入 `release/aula_america_a1_v0_1_2.apkg`。
3. 允许更新已有笔记。
4. 不导入其他人的学习进度。

完成后检查：

- 总卡片数量没有异常翻倍
- 原有复习进度仍在
- 听问即答卡只显示 Anki 自带播放按钮
- 音频可以播放
