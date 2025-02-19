# **文件分类工具**  
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 一款基于Python的文件分类工具,支持根据文件类型自动整理文件夹中的内容。灵感来源于IDM下载器提示是否希望分类文件,使你凌乱的文件变整洁!

---

## **目录**
1. [简介](#简介)
2. [功能特性](#功能特性)
3. [安装指南](#安装指南)
4. [使用方法](#使用方法)
5. [配置文件说明](#配置文件说明)
6. [打包为可执行文件](#打包为可执行文件)
7. [常见问题](#常见问题)
8. [贡献指南](#贡献指南)
9. [许可证](#许可证)

---

## **简介**

文件分类工具是一款轻量级的 Python 程序，旨在帮助用户快速整理文件夹中的文件。它可以根据文件扩展名将文件归类到不同的子文件夹中，并提供友好的中文提示和日志记录功能。程序支持多线程处理、进度条显示以及自定义配置，适合日常文件管理需求。

---

## **功能特性**

- **文件分类**：根据文件扩展名将文件归类到指定的文件夹(如压缩包、文档、图片等)
- **多线程加速**：使用多线程技术提高文件处理效率
- **冲突解决**：自动重命名同名文件，避免覆盖
- **日志记录**：详细记录操作过程，方便排查问题
- **跨平台支持**：适用于 Windows、macOS和Linux
- **可扩展性**：通过外部配置文件轻松自定义分类规则

---

## **安装指南**

### **依赖环境**
- Python 3.6 或更高版本
- 需要安装以下 Python 库：
  - `tqdm`（用于进度条显示）

你可以通过以下命令安装依赖：
```bash
pip install tqdm
```

### **克隆项目**
将项目克隆到本地：
```bash
git clone https://github.com/your_username/file-classifier.git
cd file-classifier
```

---

## **使用方法**

### **1、你可以直接运行脚本**
直接运行 Python 脚本：
```bash
python classify_files.py
```
程序会提示你输入目标目录路径和其他选项

### **命令行参数**
目前不支持命令行参数，所有交互通过程序内提示完成

---

## **配置文件说明**

程序依赖 `config.json` 文件来定义分类规则和受保护项,以下是配置文件的示例：

```json
{
    "categories": {
        "Compress": [".zip", ".7z", ".rar", ".tar", ".gz", ".bz2", ".xz"],
        "Program": [".exe", ".apk", ".msi", ".bat", ".sh"],
        "Photo": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
        "Documents": [".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".rtf", ".csv"]
    },
    "protected_items": [".git", "venv", "__pycache__", ".idea", ".vscode", "node_modules"],
    "script_extensions": [".py", ".pyw"]
}
```

- **`categories`**：定义文件分类规则,键为分类名称,值为对应的文件扩展名列表。
- **`protected_items`**：定义需要跳过的受保护项(如隐藏文件夹或开发工具文件夹)
- **`script_extensions`**：定义需要跳过的脚本文件扩展名

---

## **2、你也打包为可执行文件**

如果你希望将程序打包为独立的 `.exe` 文件,可以使用 `PyInstaller`：

1. 安装 `PyInstaller`：
   ```bash
   pip install pyinstaller
   ```

2. 打包脚本：
   ```bash
   pyinstaller --onefile classify_files.py
   ```

3. 打包完成后,生成的可执行文件位于 `dist` 文件夹中。

> **注意**：确保 `config.json` 文件与生成的 `.exe` 文件位于同一目录下

---

## **常见问题**

### **1. 运行时提示找不到 `config.json` 文件**
确保 `config.json` 文件与脚本或 `.exe` 文件位于同一目录下

---

## **贡献指南**

欢迎为本项目贡献代码或提出建议！请遵循以下步骤：

1. Fork 本仓库。
2. 创建一个新的分支 (`git checkout -b feature/your-feature`)。
3. 提交你的更改 (`git commit -m "Add some feature"`)。
4. 推送到远程分支 (`git push origin feature/your-feature`)。
5. 提交 Pull Request。

---

## **许可证**

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
