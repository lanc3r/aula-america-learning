# aula_america_a1_anki

这是长期维护的 Aula América A1 Anki 牌组源仓库。

当前正式版本：`0.1.2`

当前牌组内容以 Unidad 1 已完成的课程为基础，包含：

- 14 张 `chunk_production`
- 4 张 `dialogue_response`
- 3 张 `mistake_contrast`
- 共 21 张卡

另外四种类型已经完成设计并冻结，但当前没有为了占位而制造无意义卡片：

- `vocabulary`
- `grammar_pattern`
- `rule_concept`
- `pronunciation`

## 核心原则

1. 牌组始终累积更新，不按每课拆成多个 deck。
2. 已发布 UID 永不改变，也不重新分配。
3. Note Type 的 model ID、字段顺序和模板数量已经冻结。
4. 模板与内容分离。
5. 相同西语文本复用同一份音频缓存。
6. 文件名只使用英文小写字母、数字和下划线。
7. 版本号在文件名中写成 `v0_1_0`。
8. 每次生成前必须通过自动验证。

## 第一次迁移

你已经使用过旧版 Builder 时：

1. 解压本仓库。
2. 把旧文件夹中 `audio_cache` 里的 MP3 全部复制到本仓库的 `audio_cache`。
3. 不要复制旧的 `build_deck.py`、模板或 output。
4. 运行 `validate_content.command`。
5. 运行 `build_deck.command`。

本版保留了旧版三个 Note Type 的 model ID、字段顺序和卡片 UID，因此重新导入生成的牌组时，Anki 应把它识别为原有笔记的更新，而不是创建重复笔记。

## 生成牌组

运行：

`build_deck.command`

程序会先验证内容。

如果 `audio_cache` 中已经包含所有需要的音频，它不会询问 API key，也不会调用 TTS。

仅当有新西语文本缺少音频时，才会提示输入 OpenAI API key。

生成结果：

`release/aula_america_a1_v0_1_2.apkg`

同时生成：

- `release/release_manifest.json`
- `release/content_summary.tsv`

## 强制重新生成音频

只有更换声音、语速、模型或口音指令时才运行：

`refresh_audio.command`

普通新增卡片不要运行这个命令。

## GitHub 上传

完成本地生成后，运行：

`prepare_github_upload.command`

它会创建：

`github_upload`

该目录会包含：

- 源代码
- 配置
- 内容
- 模板
- 文档
- release 中的最新牌组

它不会包含：

- `audio_cache`
- `output`
- `venv`
- API key

把 `github_upload` 目录中的内容上传到 GitHub 即可。

## 未来更新流程

每完成一课：

1. 更新对应的 `content/unidad_XX.json`
2. 提升版本号
3. 更新 `changelog.md`
4. 运行验证
5. 只为新文本生成缺失音频
6. 生成新的累积 `.apkg`
7. 把 release 中的新牌组上传到 GitHub

正常情况下，模板、Note Type 和生成器不再变化。

## 七种 Note Type

### chunk_production

中文或场景提示，主动说出完整西语句块。

### dialogue_response

播放西语问题，直接用西语回答。

### vocabulary

词汇卡。名词保存冠词、性别和复数，并配真实例句。

### grammar_pattern

训练语法结构的实际使用，而不是背定义。

### rule_concept

保存有长期解释力的规律和母规则。

### mistake_contrast

保存真实错误、自然度辨析和负迁移。

### pronunciation

训练发音、听辨、舌位、气流和常见错误。

## 安全

程序不会把 API key 写入任何文件。

不要在仓库中手动创建保存 API key 的文件。
