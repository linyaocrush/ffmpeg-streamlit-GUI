import streamlit as st

# 设置页面标题和图标
st.set_page_config(page_title="FFmpeg 视频转码工具", page_icon="🎥")

# 页面标题
st.title("FFmpeg 视频转码工具 🎥")

# 基本设置区域
st.header("基本设置 ⚙️")

# 使用列来组织输入字段
input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    # 输入视频文件名
    video_file = st.text_input("视频文件名（包括后缀）", "example.mp4", key="video_file")

with input_col2:
    # 选择输出封装格式
    output_formats = ["mp4", "mkv", "mov", "avi", "flv", "webm", "wmv", "ts"]
    output_format = st.selectbox("输出封装格式", output_formats, key="output_format")

with input_col3:
    # 添加自定义输出文件名选项
    output_filename_custom = st.text_input("自定义输出文件名（可选）", "", key="output_filename_custom", 
                                           placeholder="不包括后缀")

# 编码选项区域
st.header("编码选项 🎬")

# 选择CPU或GPU编码
codec_col1, codec_col2 = st.columns(2)

with codec_col1:
    encoding_type = st.radio("编码类型", ("CPU", "GPU"), key="encoding_type")

# 根据编码类型显示不同的编码器选项
if encoding_type == "CPU":
    # CPU编码器选项
    with codec_col2:
        cpu_codec_options = [
            "libx264", "libx265", "mpeg4", "vp8", "vp9", "h264_nvenc", 
            "hevc_nvenc", "h264_amf", "hevc_amf", "h264_qsv", "hevc_qsv",
            "h264_videotoolbox", "hevc_videotoolbox"
        ]
        codec = st.selectbox("CPU编码器", cpu_codec_options, key="cpu_codec")
else:  # GPU编码
    # 选择GPU品牌
    with codec_col2:
        gpu_brand = st.selectbox("GPU品牌", ("NVIDIA", "AMD", "Intel"), key="gpu_brand")
    
    # 根据GPU品牌显示对应的编码器
    gpu_col1, gpu_col2 = st.columns(2)
    with gpu_col1:
        if gpu_brand == "NVIDIA":
            gpu_codec_options = ["h264_nvenc", "hevc_nvenc", "av1_nvenc"]
        elif gpu_brand == "AMD":
            gpu_codec_options = ["h264_amf", "hevc_amf", "av1_amf"]
        else:  # Intel
            gpu_codec_options = ["h264_qsv", "hevc_qsv", "av1_qsv"]
        
        codec = st.selectbox(f"{gpu_brand} GPU编码器", gpu_codec_options, key="gpu_codec")

# 网页优化选项
web_optimization = st.checkbox("启用网页优化（针对网络流媒体播放优化）", key="web_optimization")

# 码率控制模式
bitrate_mode = st.selectbox("码率控制模式", (
    "固定码率(CBR)", 
    "可变码率(VBR)", 
    "恒定质量(CQ/CRF)", 
    "平均码率(ABR)",
    "无损编码(Lossless)"
), key="bitrate_mode")

# 根据码率控制模式显示不同的参数输入
if bitrate_mode == "固定码率(CBR)":
    bitrate_col1, bitrate_col2 = st.columns(2)
    with bitrate_col1:
        bitrate = st.text_input("目标码率", "1000k", placeholder="例如: 1000k", key="bitrate_cbr")
        minrate = bitrate
        maxrate = bitrate
    with bitrate_col2:
        bufsize = st.text_input("缓冲区大小", "2000k", placeholder="例如: 2000k", key="bufsize_cbr")
elif bitrate_mode == "可变码率(VBR)":
    bitrate_col1, bitrate_col2, bitrate_col3, bitrate_col4 = st.columns(4)
    with bitrate_col1:
        bitrate = st.text_input("平均码率", "1000k", placeholder="例如: 1000k", key="bitrate_vbr")
    with bitrate_col2:
        minrate = st.text_input("最小码率", "500k", placeholder="例如: 500k", key="minrate_vbr")
    with bitrate_col3:
        maxrate = st.text_input("最大码率", "1500k", placeholder="例如: 1500k", key="maxrate_vbr")
    with bitrate_col4:
        bufsize = st.text_input("缓冲区大小", "2000k", placeholder="例如: 2000k", key="bufsize_vbr")
elif bitrate_mode == "恒定质量(CQ/CRF)":
    if codec in ["libx264", "h264_nvenc", "h264_amf", "h264_qsv"]:
        crf_value = st.slider("CRF值 (H.264)", 0, 51, 23, key="crf_h264")
    elif codec in ["libx265", "hevc_nvenc", "hevc_amf", "hevc_qsv"]:
        crf_value = st.slider("CRF值 (H.265)", 0, 51, 28, key="crf_hevc")
    else:
        crf_value = st.slider("QP值 (其他编码器)", 0, 51, 23, key="qp_other")
elif bitrate_mode == "平均码率(ABR)":
    bitrate = st.text_input("目标码率", "1000k", placeholder="例如: 1000k", key="bitrate_abr")
else:  # 无损编码
    st.info("无损编码已选择，将使用最佳质量设置")

# 帧率
framerate = st.text_input("帧率", "30", placeholder="例如: 30", key="framerate")

# 分辨率调整选项
st.header("分辨率调整 📐")
resize_option = st.checkbox("调整视频分辨率", key="resize_option")

if resize_option:
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        width = st.number_input("宽度 (像素)", min_value=1, value=1920, key="width")
    with res_col2:
        height = st.number_input("高度 (像素)", min_value=1, value=1080, key="height")
    with res_col3:
        # 保持宽高比选项
        keep_aspect_ratio = st.checkbox("保持宽高比", value=True, key="keep_aspect_ratio")

# 音频选项
st.header("音频选项 🔊")
audio_col1, audio_col2 = st.columns(2)

with audio_col1:
    audio_codec = st.selectbox("音频编码器", ["保持原样", "aac", "mp3", "flac", "copy"], key="audio_codec")

# 如果选择了具体的音频编码器，则显示音频参数
if audio_codec != "保持原样" and audio_codec != "copy":
    with audio_col2:
        audio_bitrate = st.text_input("音频码率", "192k", placeholder="例如: 128k, 192k, 320k", key="audio_bitrate")
        audio_channels = st.selectbox("声道数", ["保持原样", "单声道", "立体声"], key="audio_channels")

# 线程数
threads = st.slider("线程数", 1, 16, 4, key="threads")

# 生成命令按钮
st.markdown("---")
if st.button("生成FFmpeg命令 🎛️", type="primary", key="generate_command"):
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
    st.text_area("生成的FFmpeg命令", command, height=150, key="command_output")
    st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保视频文件在同一目录下。")