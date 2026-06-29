# Skill 导出与分享工作流

当用户要求将 socratic-learning-system skill 导出为可分享的压缩包时执行。

## 目的

生成一个干净、不包含个人学习数据的 skill 副本，供他人安装使用。

## 步骤

### 1. 复制到桌面

```python
shutil.copytree(skill_dir, "/Users/<user>/Desktop/socratic-learning-system")
```

### 2. 移除所有案例文件

所有 `references/case-study-*.md` 文件包含具体学习者的对话记录和个人数据，必须全部移除：

```python
for f in os.listdir(ref_dir):
    if f.startswith("case-study-"):
        os.remove(f)
```

保留 pure-method references（socratic-method.md, teaching-patterns.md, live-text-reading, panoramic-overview, pdf/epub-toc-extraction 等）。

### 3. 清洗个人路径

在 SKILL.md 和 scripts/init_course.py 中：
- 将 `/Users/<真实用户名>/<项目名>` 替换为 `/path/to/your/project`
- 将任何硬编码的用户名替换为占位符

### 4. 验证清洁度

遍历所有剩余文件，检查是否残留以下字符串：
- 学习者姓名（如"星原"）
- 真实用户名（如"wangle"）
- 项目路径（如"ai-learning-system"）
- 特定 profile 名（如"socrates"）

### 5. 创建使用说明

在根目录创建 `使用说明.txt`，包含：
- 功能概述（一句话）
- 核心优势（3-5条）
- 使用方式（步骤 + 命令示例）
- 使用要点（推荐节奏、文本类型对应的教学法）
- 文件结构说明
- 权利声明

### 6. 打包

```bash
cd /Users/<user>/Desktop
zip -r socratic-learning-system-vX.Y.Z.zip socratic-learning-system/ -x "*.DS_Store"
```

### 重要注意事项

- **不要动源 skill** — 只操作副本
- **模板文件保持原样** — 模板本来就是初始化用的，不需要清洗
- **教学法参考文件通常不包含个人数据** — 但用搜索验证
- **readme 的权利声明格式**：`本 skill 由 [权利人] 原创开发。保留所有权利。`
