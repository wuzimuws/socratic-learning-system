# OmniFocus AppleScript 查询模板

> 用于 socratic-learning-system 实操书教学（GTD《搞定》）中的系统诊断。
> 在 macOS 上通过 `osascript -e '...'` 调用。

## 基础模板

### 1. 获取所有文件夹和项目

```applescript
tell application "OmniFocus"
    set output to ""
    try
        tell front document
            set folderList to folders
            repeat with f in folderList
                set output to output & "📁 " & name of f & ":" & return
                try
                    set projList to projects of f
                    repeat with p in projList
                        set output to output & "  📄 " & name of p & return
                    end repeat
                end try
                set output to output & return
            end repeat
        end tell
    end try
    return output
end tell
```

### 2. 获取所有标签

```applescript
tell application "OmniFocus"
    set output to ""
    try
        tell front document
            set tagList to tags
            repeat with t in tagList
                set output to output & "  #" & name of t & return
            end repeat
        end tell
    end try
    return output
end tell
```

### 3. 获取收件箱任务数

```applescript
tell application "OmniFocus"
    try
        tell front document
            set inboxTasks to every inbox task
            return count of inboxTasks
        end tell
    end try
end tell
```

### 4. 获取收件箱任务详情（含持续时间）

```applescript
tell application "OmniFocus"
    set output to ""
    try
        tell front document
            set inboxTasks to every inbox task
            repeat with t in inboxTasks
                set taskName to name of t
                try
                    set taskEstimate to estimated minutes of t
                on error
                    set taskEstimate to "未设"
                end try
                set output to output & "- " & taskName & " (" & taskEstimate & "分钟)" & return
            end repeat
        end tell
    end try
    return output
end tell
```

### 5. 查询所有透视（Perspectives）

```applescript
tell application "OmniFocus"
    set output to ""
    try
        tell front document
            set perspList to perspectives
            repeat with p in perspList
                set output to output & "  👁️ " & name of p & return
            end repeat
        end tell
    end try
    return output
end tell
```

### 6. 获取所有带某个标签的任务

```applescript
-- 将 "#等待" 替换为要查询的标签名称
tell application "OmniFocus"
    set tagName to "等待"
    set output to ""
    try
        tell front document
            set targetTag to first tag whose name is tagName
            set taggedTasks to tasks of targetTag
            repeat with t in taggedTasks
                set output to output & "- " & name of t & return
            end repeat
        end tell
    end try
    return output
end tell
```

### 7. 获取所有项目总数和已完成/未完成统计

```applescript
tell application "OmniFocus"
    try
        tell front document
            set allProjects to every project
            set totalCount to count of allProjects
            set activeCount to 0
            repeat with p in allProjects
                if status of p is active then
                    set activeCount to activeCount + 1
                end if
            end repeat
            return "总项目: " & totalCount & ", 活跃: " & activeCount & ", 已完成/搁置: " & (totalCount - activeCount)
        end tell
    end try
end tell
```

## 教学注意事项

- AppleScript 通过 `osascript` 从 macOS 终端调用，无需任何安装
- 查询前需确认 OmniFocus 正在运行
- 首次运行时可能需要授权辅助功能（系统偏好设置 → 隐私与安全性 → 辅助功能 → 添加终端）
- 中文标签名在 AppleScript 中可直接使用（无需转义）
- 查询结果在 terminal 中通过 `\r` 换行，需用 `return` 替代 `\n` 在 AppleScript 中拼接
- 标签的 `estimated minutes` 字段可能未设，需用 `try...on error...end try` 包裹

## 支持的 OmniFocus 版本

- OmniFocus 3: ✅ 已验证
- OmniFocus 4: 未验证，但 AppleScript API 大概率未变
