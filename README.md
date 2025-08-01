# FFmpeg 多媒体处理工具集

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)

一个基于Streamlit的图形化工具集，帮助用户轻松完成视频字幕处理、音频提取与合并等多媒体任务，无需记忆复杂的FFmpeg命令行参数。

## ✨ 功能特性

- 🖥️ 直观的图形用户界面，无需命令行经验
- 🔤 **字幕处理工具**：
  - 将字幕烧录到视频（硬字幕）
  - 从视频中提取软字幕（支持SRT、ASS、SSA等格式）
  - 支持多轨道字幕选择与自定义字符编码
- 🔊 **音频处理工具**：
  - 从视频中提取音频（支持MP3、AAC、WAV等格式）
  - 合并音视频文件
  - 音频质量与编码参数自定义
- 🎞️ 自定义输出文件名与格式
- 🔄 实时预览生成的FFmpeg命令
- 📋 一键复制命令到剪贴板

## 🚀 快速开始

### 前置要求
- Python 3.8+
- FFmpeg（已添加到系统PATH）

### 使用方法
1. 下载项目到本地
2. 双击运行 **启动.bat** 文件
3. 在浏览器中打开显示的本地地址（通常是 http://localhost:8501）

## 🖥️ 界面预览

| 主界面 | 字幕处理 |
|-------|----------|
| ![主界面](https://youke1.picui.cn/s1/2025/08/01/688ca9aaea0a8.png) | ![字幕处理](https://youke1.picui.cn/s1/2025/08/01/688ca9aacaf44.png) |

| 音频处理 | 命令预览 |
|----------|----------|
| ![音频处理](https://youke1.picui.cn/s1/2025/08/01/688ca9aaa611c.png) | ![命令预览](https://youke1.picui.cn/s1/2025/08/01/688ca9a96c782.png) |

## 🛠️ 使用指南

### 字幕处理工具
1. 选择"烧录字幕到视频"或"从视频提取软字幕"选项卡
2. 输入视频/字幕文件名（包括后缀）
3. 根据需要调整高级选项（字幕轨道、编码格式等）
4. 点击"生成FFmpeg命令"按钮
5. 复制命令到视频文件所在目录的命令行中执行

### 音频处理工具
1. 选择"提取音频"或"合并音视频"选项卡
2. 输入源文件名称
3. 选择输出格式与质量参数
4. 可选择自定义输出文件名
5. 生成并复制命令执行

## 📜 许可证

本项目采用 [MIT 许可证](LICENSE)

## 📞 联系

如有任何问题或建议，请通过邮箱联系：xiaokuiace@gmail.com

---

**让复杂的FFmpeg命令变得简单直观！** 🎥➡️🔄➡️🎬