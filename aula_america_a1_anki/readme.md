# aula_america_a1_anki

这是长期维护的西班牙语 A1 Anki 牌组源仓库。技术上的 deck ID、Note Type model ID 和历史 deck 名称继续保持不变，以保证旧牌组可以累积更新。

当前正式版本：`0.9.5`

## Travel Prebuild Extension

本仓库在 `anki_v046` 的完整代码仓库基础上，加入旅行期间使用的
NVH U6-U9 预装内容。

源码保留：

- `travel_prebuild_readme.md`
- `travel_prebuild_manifest.json`
- `prebuilds/v047/*.tsv`
- `prebuilds/v048_v050/*.tsv`

历史 `.apkg`、manifest 和 bundle zip 属于生成产物，不再长期保存在源码仓库中。

旧旅行预装包的历史导入顺序为：

1. 现有 v0.4.6 累积牌组
2. `anki_v047_nvh_u6_prebuild.apkg`
3. `anki_v048_nvh_u7_prebuild.apkg`
4. `anki_v049_nvh_u8_mirador_review.apkg`
5. `anki_v050_nvh_u9_prebuild.apkg`

也可以在导入 v047 后，直接导入：

`anki_v048_v050_nvh_travel_pack.apkg`

不要同时导入 combined v048-v050 和单独的 v048/v049/v050 包。

## 当前课程来源

- 已完成并保留：Aula América 1，Unidad 1–3。
- 从本版开始：Nos vemos hoy 1 作为新的课程结构主线。
- Aula América 1 继续用于拉美西语校准、旅行实用表达补充和覆盖检查。
- Aula Internacional 1 教师用书继续作为教学设计参考。
- Aula Internacional 1 单词表继续用于词汇覆盖审计。

Nos vemos hoy U1–U5 已完成阶段性收口。v0.4.6 正式关闭 U5《Comer con gusto》：教材核心目标、Aula 拉美校准、`este/esta/estos/estas/esto` 桥接补遗、少量 Mexico Food Core I 与真实 Travel Core 均已进入同一累积牌组；低价值食谱词汇继续有意识地不做主动覆盖。

## 当前卡片统计

- 278 张 `chunk_production`
- 63 张 `dialogue_response`
- 483 张 `vocabulary`
- 94 张 `grammar_pattern`
- 99 张 `rule_concept`
- 81 张 `mistake_contrast`
- 4 张 `pronunciation`
- 7 张 `listening_dialogue`
- 共 1109 张卡

当前 active 内容包含 Aula U1-U3、NVH U3-U6（含一次教材核心词汇/搭配补遗审计），以及按新标准从零重制的 NVH U7 Phase 1–2。U7 Phase 2 已覆盖 pretérito perfecto、时间标记、muy/mucho、实用数量词和旅行准备，截止到投诉/道歉模块之前；旧 `inactive_content/unidad_nvh_07.json` 仅作为历史参考，不恢复、不迁移 UID。卡片按“基础词汇 → 规则理解 → 语法运用 → 高频句块 → 问答情景 → 易错综合 → 情景听力”组织，不拆成独立牌组。

## 核心原则

1. 牌组始终累积更新，不按每课拆成多个 deck。
2. 已发布 UID 永不改变，也不重新分配。
3. 已发布 Note Type 的 model ID、字段顺序和模板数量冻结；新增训练目标只能用新的 model ID 增加 Note Type，不修改旧契约。
4. 模板与内容分离。
5. 相同西语文本复用同一份音频缓存。
6. 文件名只使用英文小写字母、数字和下划线。
7. 版本号在文件名中写成 `v0_1_0`。
8. 每次生成前必须通过自动验证。
9. Anki 卡片按学习依赖组织：基础词汇 → 规则理解 → 语法运用 → 高频句块 → 问答情景 → 易错综合 → 情景听力。
10. 每张卡尽量只承担 1–3 个明确提取目标，不为凑数量合并无关知识。
11. 所有供学习者模仿的西语例句都应纳入 TTS；错误句不生成音频。

## Nos vemos U3 最终覆盖

### Bridge Lesson
- `probar`
- `Encantado/a`、`Igualmente`
- `Tenemos una reserva`
- `Estados Unidos / estadounidense`
- 西班牙 `vosotros` 的被动识别
- `coche / carro` 地区差异

### Familia y relaciones
- 核心家庭成员和亲属关系
- `mi/mis · tu/tus · su/sus`
- `nuestro/nuestra/nuestros/nuestras`
- `su` 的歧义与 `de + 人/代词`
- `pareja · esposo/a · novio/a · compañero/a de trabajo`

### Describir personas
- 高频外貌和性格形容词
- 形容词性数一致
- `muy / bastante / un poco`
- `tener el pelo... / tener los ojos...`
- `estar + estado civil`

### Gustos
- `me/te/le/nos/les + gusta(n)`
- `A Ana le...`
- `A mí me...`
- `también / tampoco / A mí sí / A mí no`
- `encantar`
- `interesar / interesa(n)`
- `un amigo mío / una amiga mía`
- `¿Con quién...?`
- `favorito/a`、`¿Qué tipo de música te gusta más?`
- 拉美 `bien + 形容词`（当前以识别为主，主动输出优先 `muy`）
- 高频音乐类型词汇

### Fechas
- 12 个月
- `¿Cuándo es tu cumpleaños?`
- `el + día + de + mes`
- 拉美优先的 `el primero de...`
- `Creo que...`

### Cultura y comprensión
- Chocolates Valor：`exportar / producto`、`más de + 数字`、`trabajar con...`
- Guatemala：`naturaleza fascinante`、`idioma oficial`、`limitar con`
- `el español`（语言名作名词）vs `hablar español`（高频零冠词句块）


### Travel Core III
- `el avión`
- `la terminal`
- `el asiento`
- `el cajero automático`
- `la propina`
- `la tarjeta de embarque`
- `el equipaje de mano`
- `la aduana`
- `el retraso`
- `el barrio`
- `la contraseña`
- `picante`

这 12 项来自对当前累计卡组的去重后缺口审计；已有的 `la entrada / la salida / la puerta / el metro / la parada / el mapa / la dirección / la tarjeta / el efectivo / abierto/a / cerrado/a` 等不重复创建。

### Errores reales de cierre
- `¿Cuándo tu cumpleaños?` → `¿Cuándo es tu cumpleaños?`
- `¿Dónde es tu hotel?` → `¿Dónde está tu hotel?`
- `Tiene treinta y siete años.` → `Tengo treinta y siete años.`
- `Tengo los padres viven...` → `Mis padres viven...`
- 语言名称小写：`español`
- `Me gusta el pop más.` → `Me gusta más el pop.`

## 第一次迁移

如果你已经使用过旧版 Builder：

1. 解压本仓库。
2. 把旧文件夹中 `audio_cache` 里的 MP3 全部复制到本仓库的 `audio_cache`。
3. 不要复制旧的 `build_deck.py`、模板或 output。
4. 运行 `validate_content.command`。
5. 运行 `build_deck.command`。

本版保留了既有 Note Type 的 model ID、字段顺序和全部历史 UID，因此重新导入生成的牌组时，Anki 应把旧笔记识别为更新，而新增的 NVH 卡片作为新笔记加入。

## 生成牌组

运行：

`build_deck.command`

程序会先验证内容，并运行卡片设计审计。卡片原则见
`docs/card_design_principles.md`。

手动检查可运行：

`python3 scripts/validate_content.py`

`python3 scripts/audit_card_design.py`

如果 `audio_cache` 中已经包含所有需要的音频，它不会询问 API key，也不会调用 TTS。

仅当有新西语文本缺少音频时，才会提示输入 OpenAI API key。

生成结果：

`release/aula_america_a1_v0_9_0_u7_phase2.apkg`

同时生成：

- `release/release_manifest.json`
- `release/content_summary.tsv`

## 强制重新生成音频

只有更换声音、语速、模型或口音指令时才运行：

`refresh_audio.command`

普通新增卡片不要运行这个命令。

当前 `config/tts_config.json` 的全局指令以接近墨西哥的中性拉美西语为目标：语速应接近真实日常对话，但仍保持 A1 学习者可理解；问路、交通、餐厅和服务场景要有自然、友好的互动语气，不按单词慢读，也不使用明显西班牙本土特征。常见组合如 `por aquí`、`está abierto`、`dónde está`、`quién es`、`en el centro`、`va al centro` 应按意群自然连起来，不要逐词切开。

从 v0.8.0 起，`listening_dialogue` 使用独立 `listening_dialogue` TTS profile：整段 3–6 轮对话一次合成，速度为真实拉美日常会话级别，不因 A1 身份主动降速；禁止教学式停顿、逐词强调和语义块之间的人为切分。允许自然连读、功能词弱化、sinalefa/resilabificación 和真实问答语调。换轮只保留正常对话所需的短停顿，不把每一句单独生成后拼接。

如果某条音频仍然听起来逐词断开，把完整西语文本加入 `text_instruction_overrides`，单独说明应连读的词组。U6 高频旅行句目前已经为 `¿Hay una farmacia por aquí?`、`¿Dónde está la oficina de turismo?`、`¿Puedo ir en metro?`、`¿Este autobús va al centro?`、`Tiene que tomar la línea 3 en dirección al centro histórico.`、`¿Cuánto se tarda?` 等句子加了精确 override。

个别文本可在 `config/tts_config.json` 的 `text_instruction_overrides` 中加入额外提示。键必须与实际朗读文本完全一致。构建脚本会把单条提示计入缓存哈希，因此以后只修改某一条覆盖提示时，只会为受影响的文本创建新的缓存文件。

## GitHub 上传

完成本地生成后，运行：

`prepare_github_upload.command`

它会创建：

`github_upload`

该目录会包含源代码、配置、内容、模板和文档；不会包含 `audio_cache`、`output`、`release`、`github_upload`、`venv` 或 API key。

## 未来更新流程

每完成一段课程：

1. 更新对应的 `content/unidad_*.json`
2. 提升版本号
3. 更新 `changelog.md`
4. 运行验证
5. 只为新文本生成缺失音频
6. 生成新的累积 `.apkg`
7. 把 release 中的新牌组上传到 GitHub

Nos vemos U3 使用 `content/unidad_nvh_03.json`，现已标记为 complete；这样既保留 Aula U3 的历史内容，也能明确区分新的主线教材。

## 七种 Note Type

### chunk_production
中文或场景提示，主动说出完整西语句块。

### dialogue_response
播放西语问题或对方的话，直接用西语回应。

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

## 例句音频规则

所有供学习者模仿的西班牙语例句都应纳入 TTS：主动表达、对话问题与回答、词汇例句、语法答案与正确对比例句、规则例句、发音目标等均有音频。易错辨析中的错误句不生成音频，只给正确句发音，避免强化错误输入。
