# PDF 目录提取指南

新课程初始化后，需要从教材 PDF 中提取目录结构来填充 `config.md`（章节总览）和 `curriculum.md`（教学计划）。

## 推荐工具: pypdfium2

`pypdfium2` 能可靠提取中文 PDF 的书签/目录（包括多级嵌套），而 `pdfplumber` 在扫描型 PDF 上经常失败。

### 安装

```bash
pip install pypdfium2
```

### ⚠️ 版本检测（必做）

pypdfium2 v4.x 和 v5.x 的 API 不同。**先检测版本再选择代码路径。**

```python
import pypdfium2 as pdfium
print(pdfium.__version__)  # 检查版本号
first = list(pdf.get_toc())[0]
print(dir(first))  # 检查是属性还是方法
```

| 特征 | v4.x（旧版） | v5.x（新版） |
|------|-------------|-------------|
| 访问标题 | `item.title` | `item.get_title()` |
| 访问页码 | `item.page_index` | `item.get_dest().page_index`（可能 None） |
| `.title` 报错 | 正常使用 | `AttributeError: 'PdfOutlineItem' has no attribute 'title'` |
| `.get_title()` 报错 | `AttributeError: 'PdfOutlineItem' object has no attribute 'get_title'` | 正常使用 |

**快速判断：** 先试 `.title`，如果有 → v4.x API。如果报错 → v5.x API。

### 提取完整目录

**注意：** `get_toc()` 返回的是 generator（生成器），不是 list。需要先 `list()` 化才能用 `len()`。

#### pypdfium2 v4.x API（属性访问）

```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("<教材路径>")
toc = list(pdf.get_toc())

if toc:
    for item in toc:
        level = item.level
        prefix = "  " * level
        title = item.title.strip() if item.title else "(no title)"
        page_num = item.page_index + 1 if item.page_index is not None else "?"
        print(f"{prefix}[L{level}] {title} (p.{page_num})")
else:
    print("No TOC/bookmarks found")

total_pages = len(pdf)
print(f"Total pages: {total_pages}")
```

#### pypdfium2 v5.x API（方法调用）

```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("<教材路径>")
toc = list(pdf.get_toc())

if toc:
    for item in toc:
        level = item.level
        prefix = "  " * level
        title = item.get_title()
        # get_dest() 可能返回 None，需防御
        try:
            dest = item.get_dest()
            page_num = dest.page_index + 1 if dest else "?"
        except:
            page_num = "?"
        print(f"{prefix}[L{level}] {title} (p.{page_num})")
else:
    print("No TOC/bookmarks found")

total_pages = len(pdf)
print(f"Total pages: {total_pages}")
```

### 提取文本内容

**注意：** 正确 API 是 `page.get_textpage().get_text_range()` 或 `page.get_textpage().get_text_bounded()`。

```python
# 扫描关键页面（目录页等）的文本
for page_idx in [2, 3, 4, 5]:  # 替换为目标页码（0-indexed）
    page = pdf[page_idx]
    text = page.get_textpage().get_text_range()
    if text and text.strip():
        print(f"=== P{page_idx+1} ===")
        print(text[:1000])
```

### 当 get_toc() 不返回 page_index 时的替代策略

部分 PDF 的书签（超链接标记的书签）没有 page destination，`get_dest()` 返回 None。此时无法从书签直接获得页码映射。

**替代方案：搜索文本中的章节标题来定位起始页**

```python
# 已知某篇章标题，扫描全文找到它在哪一页
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("教材.pdf")
total = len(pdf)

for i in range(total):
    try:
        page = pdf[i]
        tp = page.get_textpage()
        text = tp.get_text_bounded()
        if "德充符" in text and "鲁有兀者王骀" in text:
            print(f"德充符 正文开始于 PDF page index {i}")
            break
    except:
        pass
```

更好的做法：**先从目录页（通常是前几页）扫描文本版的目录**，获取章节名→页码的映射，然后搜索该页码附近的页面确认内容起始：

```python
# 1. 扫描目录页文本
dir_page = pdf[1]  # 目录页通常在 p.1~3
dir_text = dir_page.get_textpage().get_text_range()
# 找到类似 "德充符  66" 的文本行 → 知道德充符在 PDF 页码 66
# 2. 但 PDF index 和印刷页码不一定一致 → 需要实际搜索文本确认
for i in range(60, 75):
    text = pdf[i].get_textpage().get_text_bounded()
    if "鲁有兀者王骀" in text:
        print(f"实际起始 PDF index = {i}")
        break
```

### 从目录生成 curriculum.md 章节表

提取出目录后，按以下结构填入 `curriculum.md`：

```markdown
## 教学计划

| 课次 | 章节 | 内容 | 老师 | 状态 |
|------|------|------|------|------|
| 1 | 导论 | 全书全景介绍 | 星瑶 | 待开始 |
| 2 | 第1章 | 章节标题 | | 待开始 |
| 3 | 第2章 | 章节标题 | | 待开始 |
...
```

## 替代方案

### pdfplumber（适用于文本型 PDF）

```python
import pdfplumber

with pdfplumber.open(path) as pdf:
    for i, page in enumerate(pdf.pages[:30]):
        text = page.extract_text()
        if text and text.strip():
            print(f"=== P{i+1} ===")
            print(text[:500])
```

局限性：可能产生大量 CropBox 警告，无法提取书签目录，仅适合逐页扫读。

## 常见问题

| 问题 | 解决 |
|------|------|
| PDF 是扫描版（图片） | pypdfium2 仍可提取 TOC（如果 PDF 内嵌了书签）。内容提取需 OCR（参考 `ocr-and-documents` skill） |
| PDF 有密码 | 在命令行解码：`qpdf --password=<密码> --decrypt input.pdf output.pdf` |
| 中文路径报错 | 从 `execute_code` 调用 Python 写入文件时用相对路径或英文路径变量。在 `terminal()` 内嵌 Python 时注意 shell 引号嵌套 |
| 书签（TOC）只有顶层结构，没有详细章节 | 这是常见情况。PDF 的书签可能只包含"扉页/目录/正文/版权页"6-7条。此时应该**扫描目录页的文本**来获取完整章节结构。目录页通常在正文前几页（p.3-6 左右），用 `page.get_textpage().get_text_range()` 提取文本，手动解析章节标题和层级。详见上方"提取文本内容" |

## 执行环境坑

- **不要用 execute_code() 运行 pypdfium2** — execute_code 在隔离的 sandbox 环境中运行，可能没有安装 pypdfium2。始终用 `terminal()` + 内联 python3 调用来提取 PDF。
- **API 版本混淆（最常见坑）：** pypdfium2 v4.x 用属性访问（`item.title`），v5.x 用方法调用（`item.get_title()`）。**先检测版本（见上方版本检测表），不要硬编码。** 用错 API 会报 `AttributeError`，而且报错名并不直接告诉你是版本问题（v4 上调用 `.get_title()` 报 "no attribute"；v5 上访问 `.title` 也报 "no attribute"）。
- **`item.get_dest()` 返回 None** — v5.x 中部分 PDF 的书签没有页内链接，无法获取页码。此时改用"搜索章节标题文本"的策略寻找章节起始页（见上方"当 get_toc() 不返回 page_index 时的替代策略"）。
- **运行时提示 `get_text_bounded()` 不存在** — 新版本 pypdfium2 的 API 变了。使用 `page.get_textpage().get_text_range()` 替代。
- **`len(toc)` 报错 `TypeError: object of type 'generator' has no len()`** — `get_toc()` 返回 generator，先 `list()` 化。

## 填充 config.md 的章节总览

```markdown
## 章节总览

全书分为X编共X章：

### 第一编：编名（第1-X章）
- 第1章 章名 — 小节主题1、小节主题2
- 第2章 章名 — 小节主题1、小节主题2
...
```
