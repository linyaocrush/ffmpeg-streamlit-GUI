import streamlit as st

# 设置页面标题
st.title("FFmpeg视频转码工具")

# 输入视频文件名
video_file = st.text_input("视频文件名（包括后缀）", "example.mp4")

# 选择输出封装格式
output_formats = ["mp4", "mkv", "mov", "avi", "flv", "webm", "wmv", "ts"]
output_format = st.selectbox("选择输出封装格式", output_formats)

# 添加自定义输出文件名选项
output_filename_custom = st.text_input("自定义输出文件名（不包括后缀）", "")

# 编码选项
st.header("编码选项")

# 选择CPU或GPU编码
encoding_type = st.radio("选择编码类型", ("CPU", "GPU"))

# 根据编码类型显示不同的编码器选项
if encoding_type == "CPU":
    # CPU编码器选项
    cpu_codec_options = [
        "libx264", "libx265", "mpeg4", "vp8", "vp9", "h264_nvenc", 
        "hevc_nvenc", "h264_amf", "hevc_amf", "h264_qsv", "hevc_qsv",
        "h264_videotoolbox", "hevc_videotoolbox"
    ]
    codec = st.selectbox("选择CPU编码器", cpu_codec_options)
else:  # GPU编码
    # 选择GPU品牌
    gpu_brand = st.selectbox("选择GPU品牌", ("NVIDIA", "AMD", "Intel"))
    
    # 根据GPU品牌显示对应的编码器
    if gpu_brand == "NVIDIA":
        gpu_codec_options = ["h264_nvenc", "hevc_nvenc", "av1_nvenc"]
    elif gpu_brand == "AMD":
        gpu_codec_options = ["h264_amf", "hevc_amf", "av1_amf"]
    else:  # Intel
        gpu_codec_options = ["h264_qsv", "hevc_qsv", "av1_qsv"]
    
    codec = st.selectbox(f"选择{gpu_brand} GPU编码器", gpu_codec_options)

# 网页优化选项
web_optimization = st.checkbox("启用网页优化（针对网络流媒体播放优化）")

# 码率控制模式
bitrate_mode = st.selectbox("选择码率控制模式", (
    "固定码率(CBR)", 
    "可变码率(VBR)", 
    "恒定质量(CQ/CRF)", 
    "平均码率(ABR)",
    "无损编码(Lossless)"
))

# 根据码率控制模式显示不同的参数输入
if bitrate_mode == "固定码率(CBR)":
    bitrate = st.text_input("目标码率 (例如: 1000k)", "1000k")
    minrate = bitrate
    maxrate = bitrate
    bufsize = st.text_input("缓冲区大小 (例如: 2000k)", "2000k")
elif bitrate_mode == "可变码率(VBR)":
    bitrate = st.text_input("平均码率 (例如: 1000k)", "1000k")
    minrate = st.text_input("最小码率 (例如: 500k)", "500k")
    maxrate = st.text_input("最大码率 (例如: 1500k)", "1500k")
    bufsize = st.text_input("缓冲区大小 (例如: 2000k)", "2000k")
elif bitrate_mode == "恒定质量(CQ/CRF)":
    if codec in ["libx264", "h264_nvenc", "h264_amf", "h264_qsv"]:
        crf_value = st.slider("CRF值 (H.264, 越小质量越高)", 0, 51, 23)
    elif codec in ["libx265", "hevc_nvenc", "hevc_amf", "hevc_qsv"]:
        crf_value = st.slider("CRF值 (H.265, 越小质量越高)", 0, 51, 28)
    else:
        crf_value = st.slider("QP值 (其他编码器, 越小质量越高)", 0, 51, 23)
elif bitrate_mode == "平均码率(ABR)":
    bitrate = st.text_input("目标码率 (例如: 1000k)", "1000k")
else:  # 无损编码
    lossless_option = True

# 帧率
framerate = st.text_input("帧率 (例如: 30)", "30")

# 分辨率调整选项
st.header("分辨率调整（可选）")
resize_option = st.checkbox("调整视频分辨率")
if resize_option:
    width = st.number_input("宽度 (像素)", min_value=1, value=1920)
    height = st.number_input("高度 (像素)", min_value=1, value=1080)
    # 保持宽高比选项
    keep_aspect_ratio = st.checkbox("保持宽高比", value=True)

# 音频选项
st.header("音频选项")
audio_codec = st.selectbox("音频编码器", ["保持原样", "aac", "mp3", "flac", "copy"])

# 如果选择了具体的音频编码器，则显示音频参数
if audio_codec != "保持原样" and audio_codec != "copy":
    audio_bitrate = st.text_input("音频码率 (例如: 128k, 192k, 320k)", "192k")
    audio_channels = st.selectbox("声道数", ["保持原样", "单声道", "立体声"])

# 线程数
threads = st.slider("线程数", 1, 16, 4)

# 生成命令按钮
if st.button("生成FFmpeg命令"):
    # 构造输出文件名
    if output_filename_custom:
        output_filename = f"{output_filename_custom}.{output_format}"
    else:
        output_filename = f"transcoded_{video_file.rsplit('.', 1)[0]}.{output_format}"
    
    # 构建FFmpeg命令
    cmd_parts = [f"ffmpeg -i \"{video_file}\""]
    
    # 添加视频编码参数
    cmd_parts.append(f"-c:v {codec}")
    
    # 根据码率控制模式添加相应参数
    if bitrate_mode == "固定码率(CBR)":
        cmd_parts.append(f"-b:v {bitrate} -minrate {minrate} -maxrate {maxrate} -bufsize {bufsize}")
    elif bitrate_mode == "可变码率(VBR)":
        cmd_parts.append(f"-b:v {bitrate} -minrate {minrate} -maxrate {maxrate} -bufsize {bufsize}")
    elif bitrate_mode == "恒定质量(CQ/CRF)":
        if codec in ["libx264", "libx265"]:
            cmd_parts.append(f"-crf {crf_value}")
        else:
            cmd_parts.append(f"-qp {crf_value}")
    elif bitrate_mode == "平均码率(ABR)":
        cmd_parts.append(f"-b:v {bitrate}")
    elif bitrate_mode == "无损编码(Lossless)":
        if codec in ["libx264"]:
            cmd_parts.append("-preset ultrafast -crf 0")
        elif codec in ["libx265"]:
            cmd_parts.append("-preset ultrafast -x265-params lossless=1")
        else:
            cmd_parts.append("-qscale 0")
    
    # 添加网页优化参数
    if web_optimization:
        if codec == "libx264":
            cmd_parts.append("-profile:v baseline -level 3.0 -movflags +faststart")
        elif codec == "libx265":
            cmd_parts.append("-profile:v main -level 3.1 -movflags +faststart")
        elif codec in ["h264_nvenc", "h264_amf", "h264_qsv"]:
            cmd_parts.append("-profile:v baseline -level 3.0 -movflags +faststart")
        elif codec in ["hevc_nvenc", "hevc_amf", "hevc_qsv"]:
            cmd_parts.append("-profile:v main -level 3.1 -movflags +faststart")
        else:
            cmd_parts.append("-movflags +faststart")
    
    # 添加帧率
    cmd_parts.append(f"-r {framerate} -threads {threads}")
    
    # 添加分辨率调整参数
    if resize_option:
        if keep_aspect_ratio:
            cmd_parts.append(f"-vf scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2")
        else:
            cmd_parts.append(f"-vf scale={width}:{height}")
    
    # 添加音频编码参数
    if audio_codec == "保持原样":
        cmd_parts.append("-c:a copy")
    elif audio_codec == "copy":
        cmd_parts.append("-c:a copy")
    else:
        cmd_parts.append(f"-c:a {audio_codec}")
        # 如果选择了具体的音频编码器，则添加音频参数
        if 'audio_bitrate' in locals():
            cmd_parts.append(f"-b:a {audio_bitrate}")
        if 'audio_channels' in locals() and audio_channels != "保持原样":
            if audio_channels == "单声道":
                cmd_parts.append("-ac 1")
            elif audio_channels == "立体声":
                cmd_parts.append("-ac 2")
    
    # 添加输出文件名
    cmd_parts.append(f"\"{output_filename}\"")
    
    # 组合命令
    command = " ".join(cmd_parts)
    
    # 显示生成的命令
    st.text_area("生成的FFmpeg命令", command, height=150)
    st.info("请将上述命令复制到命令行中执行。确保视频文件在同一目录下。")

# 使用说明
st.markdown("""
### 使用说明
1. 在上方输入视频文件名和选择输出封装格式。
2. 设置编码选项，包括编码器类型（CPU/GPU）、码率控制模式等。
3. 可选调整视频分辨率和音频参数。
4. 点击生成FFmpeg命令按钮，复制生成的命令到命令行中执行。
5. 确保视频文件在同一目录下。
""")