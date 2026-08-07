# changelog

## 0.1.2

### fixed

- 验证器忽略 `venv`、`audio_cache`、`output`、`release` 和其他生成目录
- 构建时不再检查第三方 Python 包的文件名
- 验证失败时显示简洁提示，不再抛出 `CalledProcessError` traceback

## 0.1.1

### fixed

- 验证器忽略 `.DS_Store`、`.keep` 以及其他隐藏文件
- 隐藏的操作系统元数据不再导致验证失败
- 文件命名规则仍适用于所有正式项目文件


## 0.1.0

### added

- 建立长期维护的仓库结构
- 冻结七种 Note Type
- 加入 Note Type 契约哈希
- 加入 UID、字段、问号、文件名自动验证
- 加入 GitHub 安全上传目录生成器
- 加入累积 release 目录
- 加入所有七种卡片类型的样式预览

### preserved

- 保留原有 deck ID
- 保留三种已有 Note Type 的 model ID
- 保留三种已有 Note Type 的字段顺序
- 保留 21 张现有卡的 UID
- 保留 cedar、中性拉美西语和当前语速
- 保留旧音频缓存哈希规则

### content

- chunk_production: 14
- dialogue_response: 4
- mistake_contrast: 3
- total: 21
