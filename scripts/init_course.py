#!/usr/bin/env python3
"""
init_course.py — 从 socratic-learning-system 模板创建新课

用法:
    python3 init_course.py <项目目录> <课程名> [--book <教材路径>]

示例:
<<<<<<< HEAD
    python3 init_course.py /Users/wangle/ai-learning-system 工作-消费主义和新穷人 --book book.epub
=======
    python3 init_course.py /path/to/your/project 工作-消费主义和新穷人 --book book.epub
>>>>>>> Update socratic-learning-system

执行后会在 courses/<课程名>/ 下创建:
    material/       — 教材文件
    config.md       — 该书特有配置（学科背景、作者、章节概览）
    curriculum.md   — 课程大纲（章节表+教学计划）
    book_notes.md   — 教材改进记录
    progress.md     — 本课程详细进度日志
"""

import sys, os, shutil
from datetime import datetime


def init_course(project_dir, course_name, book_path=None):
    project_dir = os.path.abspath(project_dir)
    course_dir = os.path.join(project_dir, 'courses', course_name)
    base_dir = os.path.join(project_dir, 'base')
    material_dir = os.path.join(course_dir, 'material')

    # 检查项目目录是否存在
    if not os.path.exists(project_dir):
        print(f"❌ 项目目录不存在: {project_dir}")
        print("   请先创建项目，确保 base/ 目录已就绪")
        return False

    # 检查 base/ 是否存在
    if not os.path.exists(base_dir):
        print(f"⚠️  base/ 目录不存在，请先创建 base/ 目录")
        print(f"   从 skill 模板复制: cp -r <skill_dir>/templates/socratic {base_dir}")
        return False

    # 检查是否已存在
    if os.path.exists(course_dir):
        print(f"⚠️  课程目录已存在: {course_dir}")
        return False

    # 创建课程目录
    os.makedirs(material_dir, exist_ok=True)

    # 创建 config.md（该书特有配置）
    config_path = os.path.join(course_dir, 'config.md')
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(f"# 课程配置: {course_name}\n\n")
        f.write(f"- 课程名: {course_name}\n")
        if book_path:
            f.write(f"- 教材: {os.path.basename(book_path)}\n")
        f.write(f"- 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## 学科背景\n\n（请补充该书的学科领域和核心问题）\n\n")
        f.write("## 章节总览\n\n请参考教材结构补充章节信息\n")

    # 如果有教材，复制到 material/
    if book_path and os.path.exists(book_path):
        dst = os.path.join(material_dir, os.path.basename(book_path))
        shutil.copy2(book_path, dst)
        book_size = os.path.getsize(dst)
        print(f"📖 教材已导入: {dst} ({book_size:,} bytes)")

    # 创建 curriculum.md（课程大纲）
    curriculum_path = os.path.join(course_dir, 'curriculum.md')
    with open(curriculum_path, 'w', encoding='utf-8') as f:
        f.write(f"# 课程大纲: {course_name}\n\n")
        f.write("> 按教材章节拆分，每节课对应一个教学单元。\n\n")
        f.write("## 课程信息\n")
        f.write(f"- **课程名:** {course_name}\n")
        if book_path:
            f.write(f"- **教材:** {os.path.basename(book_path)}\n")
        f.write(f"- **创建时间:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## 教学计划\n\n")
        f.write("| 课次 | 章节 | 内容 | 老师 | 状态 |\n")
        f.write("|------|------|------|------|------|\n")
        f.write("| 1 | | | | 待开始 |\n\n")
        f.write("---\n")
        f.write("> 根据教材结构补充章节内容后，就可以开始上课了！\n")

    # 创建 book_notes.md（教材改进记录）
    notes_path = os.path.join(course_dir, 'book_notes.md')
    with open(notes_path, 'w', encoding='utf-8') as f:
        f.write(f"# 教材改进记录 — {course_name}\n\n")
        f.write("> 教学过程中发现的教材可改进点。\n\n")
        f.write("| 章节 | 类型 | 说明 |\n")
        f.write("|------|------|------|\n")
        f.write("| | | |\n")

    # 创建 courses/<书>/progress.md（本课详细进度）
    prog_path = os.path.join(course_dir, 'progress.md')
    with open(prog_path, 'w', encoding='utf-8') as f:
        f.write(f"# 课程进度: {course_name}\n\n")
        f.write(f"> 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## 教学计划\n\n")
        f.write("| 课次 | 章节 | 老师 | 状态 |\n")
        f.write("|------|------|------|------|\n")
        f.write("| | | | 待开始 |\n\n")
        f.write("---\n\n")
        f.write("## 详细记录\n\n（每次课后在此追加）\n")

    print(f"""
✅ 课程创建成功!

  课程目录: {course_dir}/
  ├── material/         教材文件
  ├── config.md         课程配置信息
  ├── curriculum.md     课程大纲（编辑此处填写章节）
  ├── book_notes.md     教材改进记录
  └── progress.md       本课详细进度

📌 开课准备:
  1. 编辑 curriculum.md 补充章节内容
  2. 编辑 config.md 补充学科背景
  3. 开始上课（AI 会自动读取 base/ 配置 + 本目录配置）

📌 结构说明:
  base/ 中的 learner_profile.md 有明确的"跨书/按书"分区
  开新课前需手动把 learner_profile.md 中"当前课程"段归档到"历史课程"段
""")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python3 init_course.py <项目目录> <课程名> [--book <教材路径>]")
        sys.exit(1)

    project_dir = sys.argv[1]
    course_name = sys.argv[2]
    book_path = None

    if '--book' in sys.argv:
        idx = sys.argv.index('--book')
        if idx + 1 < len(sys.argv):
            book_path = sys.argv[idx + 1]

    success = init_course(project_dir, course_name, book_path)
    sys.exit(0 if success else 1)
