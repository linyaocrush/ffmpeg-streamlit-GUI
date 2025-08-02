import streamlit as st

st.set_page_config(page_title="FFmpeg 工具集", page_icon="🎬")

# 页面标题和欢迎信息
st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #4CAF50;">🎬 FFmpeg 命令生成工具</h1>
    <p style="font-size: 18px; color: #666;">欢迎使用 FFmpeg 命令生成工具！这是一个快速生成ffmpeg启动脚本的项目。</p>
</div>
""", unsafe_allow_html=True)

# 工具介绍
st.markdown("""
<div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
    <h2 style="color: #2c3e50;">🛠️ 当前可用工具</h2>
    <ul style="font-size: 16px; color: #34495e;">
        <li><strong>字幕处理工具</strong> - 将字幕和视频合成为一个文件</li>
        <li><strong>音频处理工具</strong> - 提取视频中的音频以及合并音频和视频</li>
        <li><strong>视频转码工具</strong> - 视频格式转换和编码参数调整</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 工具选择区域
st.markdown("""
<div style="text-align: center; margin: 30px 0;">
    <h2 style="color: #2c3e50;">🔍 请选择您要使用的工具</h2>
</div>
""", unsafe_allow_html=True)

# 按钮容器
button_col1, button_col2, button_col3 = st.columns(3)

with button_col1:
    if st.button("字幕处理工具", key="subtitle_btn", help="生成字幕处理命令"):
        st.switch_page("pages/1_字幕处理工具.py")

with button_col2:
    if st.button("音频处理工具", key="audio_btn", help="提取或合并音频"):
        st.switch_page("pages/2_音频处理工具.py")

with button_col3:
    if st.button("视频转码工具", key="transcode_btn", help="视频格式转换和编码"):
        st.switch_page("pages/3_视频转码工具.py")

# 添加新按钮
with st.columns(3)[2]:  # 使用新的列布局
    if st.button("视频处理工具", key="video_processing_btn", help="视频剪辑、合并和处理"):
        st.switch_page("pages/4_视频处理工具.py")

# 关于本工具
st.markdown("""
<div style="background-color: #fff8dc; padding: 15px; border-radius: 10px; margin-top: 30px;">
    <h3 style="color: #2c3e50;">ℹ️ 关于本工具</h3>
    <p style="font-size: 15px; color: #34495e;">
    本工具集旨在简化 FFmpeg 命令的生成过程，特别是针对字幕烧录等常见任务。
    通过图形界面选择参数，自动生成相应的 FFmpeg 命令，无需记忆复杂的命令行参数。
    </p>
</div>
""", unsafe_allow_html=True)

# 页脚
st.markdown("""
<hr>
<div style="text-align: center; color: #95a5a6; font-size: 14px; padding: 10px;">
    <p>FFmpeg 工具集 © 2023 | 简化您的多媒体处理工作流</p>
</div>
""", unsafe_allow_html=True)