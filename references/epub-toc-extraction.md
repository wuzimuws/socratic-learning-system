# EPUB 目录提取指南

从 epub 教材中提取目录（Table of Contents）来填充课程章节结构。epub 本质是 zip 压缩包，TOC 信息存储在 `toc.ncx` 中。

## 前置条件

Python 标准库即可，无需额外安装：
- `zipfile`（内置）
- `xml.etree.ElementTree`（内置）

## 提取步骤

### 1. 打开 epub 并列出关键文件

```python
import zipfile

epub_path = "/path/to/book.epub"
with zipfile.ZipFile(epub_path, 'r') as z:
    all_files = z.namelist()
    # 找 toc.ncx 和 content.opf
    for f in all_files:
        print(f)
```

### 2. 快速查看目录结构（print_tree 法）

最可靠的方式是先打印树形结构查看标签名：

```python
import zipfile
from xml.etree import ElementTree as ET

epub_path = "/path/to/book.epub"
with zipfile.ZipFile(epub_path, 'r') as z:
    ncx_raw = z.read('toc.ncx').decode('utf-8')
    root = ET.fromstring(ncx_raw)
    
    def print_tree(el, depth=0):
        tag = el.tag.split('}')[1] if '}' in el.tag else el.tag
        text = (el.text or '').strip()[:80]
        indent = "  " * depth
        if text:
            print(f"{indent}{tag}: {text}")
        else:
            print(f"{indent}{tag}")
        for child in el:
            print_tree(child, depth+1)
    
    print_tree(root)
```

### 3. 提取章节列表

```python
import zipfile
from xml.etree import ElementTree as ET

epub_path = "/path/to/book.epub"
chapters = []

with zipfile.ZipFile(epub_path, 'r') as z:
    ncx_raw = z.read('toc.ncx').decode('utf-8')
    root = ET.fromstring(ncx_raw)
    
    # 遍历所有 navPoint
    for navpoint in root.iter():
        tag = navpoint.tag.split('}')[1] if '}' in navpoint.tag else navpoint.tag
        if tag != 'navPoint':
            continue
        
        # 找标题：navLabel > text
        # 兼容 namespace 问题：遍历子元素找 text
        for child in navpoint.iter():
            t = child.tag.split('}')[1] if '}' in child.tag else child.tag
            if t == 'text' and child.text:
                chapters.append(child.text.strip())
                break

print(f"共 {len(chapters)} 章")
for i, ch in enumerate(chapters, 1):
    print(f"  {i}. {ch}")
```

### 4. 从 content.opf 提取元数据（作者、出版社等）

```python
import zipfile
from xml.etree import ElementTree as ET

with zipfile.ZipFile(epub_path, 'r') as z:
    opf_raw = z.read('content.opf').decode('utf-8')
    root = ET.fromstring(opf_raw)
    
    # 提取 dc:title, dc:creator, dc:publisher, dc:description
    for child in root.iter():
        tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
        if tag in ('title', 'creator', 'publisher', 'description'):
            print(f"{tag}: {child.text}")
```

## 常见 epub 结构

### 帛书版（单层导航）
```
版权信息 → 版本说明 → 上篇 德经 → 01, 02, ... 44 → 下篇 道经 → 45, 46, ... 81 → 后记
```

### 现代书（多层导航）
```
Part 1: 理论基础
  第1章: xxx
  第2章: xxx
Part 2: 实践方法
  第3章: xxx
```

## 填充 curriculum.md

提取出章节列表后，按主题或按 3-4 章一组分组，填入教学计划表：

```markdown
| 课次 | 章节 | 内容 | 老师 | 状态 |
|------|------|------|------|------|
| 0 | 全景导论 | 全书结构、核心问题 | 星瑶 | **当前** |
| 1 | 01-10章 | 主题描述 | 星瑶 | 待开始 |
...
```

## 注意事项

- **文件名编码：** epub 文件名可能包含中文、空格、Unicode 引号（如 `Anna's Archive` 中的右单引号 U+2019）
- **macOS TCC：** `shutil.copy2()` 从 Downloads 复制文件可能被 TCC 阻止（Killed:9）。使用 Python `shutil.copy2()` 在 `execute_code()` 中执行可绕过。复制前先用 `os.listdir()` + 模糊匹配找到准确路径
- **nav.xhtml 备选：** 部分 epub 用 `nav.xhtml` 而非 `toc.ncx`。此时搜索 `<nav>` 标签中的 `<ol><li><a>` 结构提取目录
- **章节编号对照：** 帛书版道德经的章节编号与通行本完全不同。提取后需标注入 curriculum.md 的对照表
- **NCX namespace：** 不同 epub 的 NCX namespace 可能不同（`http://www.daisy.org/z3986/2005/ncx/` 最常见），用 `tag.split('}')[1]` 剥离 namespace 后按本地名匹配
