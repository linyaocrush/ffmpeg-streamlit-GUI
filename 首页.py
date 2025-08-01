import streamlit as st

st.set_page_config(page_title="FFmpeg 工具集", page_icon="🎬")

st.title("🎬 FFmpeg 工具集")
st.markdown("""
欢迎使用 FFmpeg 工具集！这是一个集合了多种 FFmpeg 实用工具的 Web 应用。

## 当前可用工具
- **字幕烧录命令生成器** - 生成 FFmpeg 字幕烧录命令
- **音频处理工具** - 提取视频中的音频以及合并音频和视频

请选择您要使用的工具：
""")

if st.button("字幕处理工具"):
    st.switch_page("pages/1_字幕处理工具.py")

if st.button("音频处理工具"):
    st.switch_page("pages/2_音频处理工具.py")

st.markdown("""
---
### 关于本工具
本工具集旨在简化 FFmpeg 命令的生成过程，特别是针对字幕烧录等常见任务。
通过图形界面选择参数，自动生成相应的 FFmpeg 命令，无需记忆复杂的命令行参数。
""")