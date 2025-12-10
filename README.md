# AutoGLM-GUI

AutoGLM 手机助手的现代化 Web 图形界面 - 让 AI 自动化操作 Android 设备变得简单

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)

## ✨ 特性

- **对话式任务管理** - 通过聊天界面控制 Android 设备
- **实时屏幕预览** - 随时查看设备正在执行的操作
- **零配置部署** - 支持任何 OpenAI 兼容的 LLM API
- **ADB 深度集成** - 通过 Android Debug Bridge 直接控制设备

## 🚀 快速开始

### 前置要求

- Python 3.10+
- 已开启 USB 调试的 Android 设备
- 已安装 ADB 并添加到系统 PATH
- 一个 OpenAI 兼容的 API 端点

### 快捷运行（推荐）

**无需安装，直接运行：**

```bash
# 使用 uvx 一键启动（无需提前安装包）
uvx autoglm-gui --base-url http://localhost:8080/v1
```

这是最简单的方式！`uvx` 会自动下载并运行最新版本，无需手动安装。

### 传统安装

如果你需要离线使用或想要固定版本：

```bash
# 方式 1: 通过 pip 安装
pip install autoglm-gui
autoglm-gui --base-url http://localhost:8080/v1

# 方式 2: 从源码安装
git clone https://github.com/your-repo/AutoGLM-GUI.git
cd AutoGLM-GUI
uv sync
uv run autoglm-gui --base-url http://localhost:8080/v1
```

启动后，在浏览器中打开 http://localhost:8000 即可开始使用！

## 📖 使用说明

1. **连接设备** - 启用 USB 调试并通过 ADB 连接设备
2. **初始化** - 点击 "Initialize Agent" 并配置 API 设置
3. **对话** - 描述你想要做什么（例如："打开微信，找到张三的聊天记录"）
4. **观察** - Agent 会逐步执行操作

## 🛠️ 开发指南

```bash
# 后端开发（自动重载）
uv run autoglm-gui --base-url http://localhost:8080/v1 --reload

# 前端开发服务器
cd frontend && pnpm dev

# 构建完整包
uv run python scripts/build.py --pack
```

## 📝 开源协议

Apache License 2.0

## 🙏 致谢

本项目基于 [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM) 构建，感谢 zai-org 团队在 AutoGLM 框架上的卓越工作。
