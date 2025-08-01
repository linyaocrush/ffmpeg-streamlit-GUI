# FFmpeg 启动脚本生成器

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)

一个基于Streamlit的图形化工具，帮助用户轻松生成复杂的FFmpeg命令行脚本，无需记忆繁琐的参数。


## ✨ 功能特性

- 🖥️ 直观的图形用户界面，无需命令行经验
- 📽️ 支持多种常见转码操作：格式转换、分辨率调整、码率控制等
- 🔧 自定义编解码器、帧率、比特率等高级参数
- 🔄 实时预览生成的FFmpeg命令
- 📋 一键复制命令到剪贴板
- 💾 保存常用配置为预设模板
- 📊 可视化显示转码前后的文件信息对比

## 🚀 快速开始

### 前置要求
- Python 3.7+
- FFmpeg (已添加到系统PATH)

### 安装方法

1. 克隆仓库(或直接下载)：
```bash
git clone https://github.com/your-username/ffmpeg-command-generator.git
cd ffmpeg-command-generator
```
2. 运行应用：
```bash
双击启动.bat
```
## 🖥️ 界面预览

| 主界面 | 预设管理 |
|-------|----------|
| ![主界面](https://via.placeholder.com/400x250/2D3748/FFFFFF?text=FFmpeg+Generator+Main) | ![预设管理](https://via.placeholder.com/400x250/2D3748/FFFFFF?text=Preset+Management) |

| 命令预览 | 文件信息 |
|----------|----------|
| ![命令预览](https://via.placeholder.com/400x250/2D3748/FFFFFF?text=Command+Preview) | ![文件信息](https://via.placeholder.com/400x250/2D3748/FFFFFF?text=File+Metadata) |

## 🛠️ 使用指南

1. **输入文件名称** - 视频.mp4,字幕.srt等(带文件后缀名
2. **配置转码参数**：
   - 选择输出格式（MP4, MKV, WEBM等）
   - 调整视频设置（分辨率、帧率、码率）
   - 配置音频设置（采样率、声道、音量）
   - 添加滤镜（裁剪、旋转、水印等）
3. **预览命令** - 实时查看生成的FFmpeg命令
4. **执行或保存**：
   - 复制命令并且在视频文件目录打开cmd粘贴以使用

## 🤝 如何贡献

欢迎提交Issue和Pull Request！请遵循以下步骤：

1. Fork项目仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 发起Pull Request

## 📜 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 📞 联系

如有任何问题或建议，请通过邮箱联系：xiaokuiace@gmail.com

---

**让复杂的FFmpeg命令变得简单直观！** 🎥➡️🔄➡️🎬
