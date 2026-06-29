# 苏格拉底学习系统 (Socratic Learning System) 使用说明

> 通用架构的 AI 学习系统，支持任意学科/教材，通过虚拟角色 + 苏格拉底教学法驱动学习。

---

## 快速开始

### 1. 首次使用：初始化项目

```bash
# 从 skill 模板复制 base 目录
cp -r <skill_dir>/templates/socratic /path/to/your/project/base

# 创建新课（需先有教材文件）
python3 <skill_dir>/scripts/init_course.py /path/to/your/project 课程名 --book 教材.epub
```

### 2. 在 Hermes 中加载 skill

```bash
hermes -s socratic-learning-system
```

或在会话中输入：

```
/skill socratic-learning-system
```

### 3. 开始上课

告诉 AI 你想学什么，AI 会引导你完成：
- 选择已有课程或开新课
- 提供教材路径
- 开始苏格拉底式教学

---

## 文件结构

```
project/                          # 项目根目录
├── base/                         # 跨书基础配置（活的，持续演化）
│   ├── system.md                 #   通用系统架构
│   ├── system_detail.md          #   通用背景设定
│   ├── learner_profile.md        #   学习者档案（跨书累积）
│   ├── chars/                    #   角色设定
│   │   ├── char_01.md            #   星瑶 — 活泼型
│   │   ├── char_02.md            #   月涵 — 温柔型
│   │   └── char_03.md            #   霜凝 — 严格型
│   ├── wechat_group.md           #   群聊记录
│   ├── wechat_unread.md          #   未读消息
│   ├── diary.md                  #   学习日记
│   └── session_archive.md        #   存档
│
└── courses/                      # 按书实例化
    └── <课程名>/
        ├── material/             #   教材文件
        ├── config.md             #   该书特有配置
        ├── curriculum.md         #   课程大纲
        ├── book_notes.md         #   教材改进记录
        └── progress.md           #   进度日志
```

---

## 三位老师

| 角色 | 风格 | 适合场景 |
|------|------|---------|
| 星瑶 | 活泼可爱，生动比喻 | 入门开篇，把抽象讲得接地气 |
| 月涵 | 温柔耐心，逐步引导 | 深入理解，厘清逻辑 |
| 霜凝 | 严格高效，高强度追问 | 巩固检验，查漏补缺 |

**推荐节奏：** 星瑶开篇 → 月涵深化 → 霜凝检验

---

## 教学模式

- **苏格拉底教学法：** 反问代替陈述，追问暴露矛盾
- **全景介绍优先：** 每本书第一次课先给整本书的逻辑主线
- **教材驱动：** 所有教学以教材为锚，不脱缰
- **课后更新：** 每次课后自动更新进度、日记、角色关系

---

## 安装

```bash
# 将 skill 放入 Hermes
cp -r socratic-learning-system ~/.hermes/skills/

# 或在 Hermes 中直接安装
hermes skills install https://raw.githubusercontent.com/wuzimuws/socratic-learning-system/main/SKILL.md
```

---

## 依赖

- Python 3.8+
- 如需 PDF 教材：`pip install pypdfium2`
- 如需 EPUB 教材：`pip install ebooklib`（Python 内置 zipfile 也可）

---

## GitHub

https://github.com/wuzimuws/socratic-learning-system
