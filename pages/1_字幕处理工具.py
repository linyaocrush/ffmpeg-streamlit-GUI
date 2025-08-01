import streamlit as st

# 设置页面标题
st.title("FFmpeg字幕处理器")

# 创建选项卡
tab1, tab2 = st.tabs(["烧录字幕到视频", "从视频提取软字幕"])

# 烧录字幕到视频选项卡
with tab1:
    st.header("烧录字幕到视频")
    
    # 输入视频和字幕文件名
    video_file = st.text_input("视频文件名（包括后缀）", "example.mp4", key="video_file_burn")
    subtitle_file = st.text_input("字幕文件名（包括后缀）", "subtitle.srt", key="subtitle_file_burn")

    # 选择是否为软字幕
    soft_subtitle = st.checkbox("使用软字幕（不重新编码视频）")

    # 定义支持的封装格式
    soft_subtitle_formats = ["mkv", "mp4", "mov", "avi", "flv", "webm"]
    hard_subtitle_formats = ["mp4", "mkv", "mov", "avi", "flv", "webm", "wmv", "ts"]

    # 根据字幕类型显示不同的封装格式选项
    if soft_subtitle:
        output_format = st.selectbox("选择输出封装格式（软字幕支持）", soft_subtitle_formats)
    else:
        output_format = st.selectbox("选择输出封装格式（硬字幕支持）", hard_subtitle_formats)

    # 添加自定义输出文件名选项
    output_filename_custom = st.text_input("自定义输出文件名（不包括后缀）", "", key="output_filename_custom_burn")

    # 初始化重新编码选项
    reencode = False

    # 如果是软字幕，让用户选择是否重新编码
    if soft_subtitle:
        reencode = st.checkbox("重新编码视频（软字幕可选）")
    # 如果是硬字幕，强制重新编码
    else:
        reencode = True
        st.info("硬字幕模式下将强制重新编码视频")

    # 如果需要重新编码，则显示编码选项
    if reencode:
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
            bitrate = st.text_input("目标码率 (例如: 1000k)", "1000k", key="bitrate_cbr_burn")
            minrate = bitrate
            maxrate = bitrate
            bufsize = st.text_input("缓冲区大小 (例如: 2000k)", "2000k", key="bufsize_cbr_burn")
        elif bitrate_mode == "可变码率(VBR)":
            bitrate = st.text_input("平均码率 (例如: 1000k)", "1000k", key="bitrate_vbr_burn")
            minrate = st.text_input("最小码率 (例如: 500k)", "500k", key="minrate_vbr_burn")
            maxrate = st.text_input("最大码率 (例如: 1500k)", "1500k", key="maxrate_vbr_burn")
            bufsize = st.text_input("缓冲区大小 (例如: 2000k)", "2000k", key="bufsize_vbr_burn")
        elif bitrate_mode == "恒定质量(CQ/CRF)":
            if codec in ["libx264", "h264_nvenc", "h264_amf", "h264_qsv"]:
                crf_value = st.slider("CRF值 (H.264, 越小质量越高)", 0, 51, 23)
            elif codec in ["libx265", "hevc_nvenc", "hevc_amf", "hevc_qsv"]:
                crf_value = st.slider("CRF值 (H.265, 越小质量越高)", 0, 51, 28)
            else:
                crf_value = st.slider("QP值 (其他编码器, 越小质量越高)", 0, 51, 23)
        elif bitrate_mode == "平均码率(ABR)":
            bitrate = st.text_input("目标码率 (例如: 1000k)", "1000k", key="bitrate_abr_burn")
        else:  # 无损编码
            lossless_option = True
        
        # 帧率
        framerate = st.text_input("帧率 (例如: 30)", "30", key="framerate_burn")
        
        # 线程数
        threads = st.slider("线程数", 1, 16, 4)

    # 生成命令按钮
    if st.button("生成FFmpeg命令"):
        # 构造输出文件名
        if output_filename_custom:
            output_filename = f"{output_filename_custom}.{output_format}"
        else:
            output_filename = f"output_{video_file.rsplit('.', 1)[0]}.{output_format}"
        
        if soft_subtitle:
            # 软字幕命令
            # 根据字幕文件扩展名确定字幕编码器
            if subtitle_file.lower().endswith('.srt'):
                subtitle_codec = 'srt'
            elif subtitle_file.lower().endswith(('.ass', '.ssa')):
                subtitle_codec = 'ass'
            else:
                subtitle_codec = 'copy'  # 默认使用copy
            
            if reencode:
                # 构建软字幕重新编码命令
                cmd_parts = [f"ffmpeg -i \"{video_file}\" -i \"{subtitle_file}\""]
                
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
                
                # 添加帧率和线程数
                cmd_parts.append(f"-r {framerate} -threads {threads}")
                
                # 添加音频和字幕编码参数
                cmd_parts.append(f"-c:a copy -c:s {subtitle_codec} -metadata:s:s:0 language=chi")
                
                # 添加输出文件名
                cmd_parts.append(f"\"{output_filename}\"")
                
                # 组合命令
                command = " ".join(cmd_parts)
            else:
                # 软字幕不重新编码命令
                command = f"ffmpeg -i \"{video_file}\" -i \"{subtitle_file}\" -c:v copy -c:a copy -c:s {subtitle_codec} -metadata:s:s:0 language=chi \"{output_filename}\""
        else:
            # 硬字幕重新编码命令
            cmd_parts = [f"ffmpeg -i \"{video_file}\""]
            
            # 添加字幕滤镜
            cmd_parts.append(f"-vf \"subtitles={subtitle_file}\"")
            
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
            
            # 添加帧率和线程数
            cmd_parts.append(f"-r {framerate} -threads {threads}")
            
            # 添加音频编码参数
            cmd_parts.append("-c:a copy")
            
            # 添加输出文件名
            cmd_parts.append(f"\"{output_filename}\"")
            
            # 组合命令
            command = " ".join(cmd_parts)
        
            # 显示生成的命令
            st.text_area("生成的FFmpeg命令", command, height=150)
            st.info("请将上述命令复制到命令行中执行。确保视频文件和字幕文件在同一目录下。")

# 从视频提取软字幕选项卡
with tab2:
    st.header("从视频提取软字幕")
    
    # 输入视频文件名
    video_file_extract = st.text_input("视频文件名（包括后缀）", "example.mp4", key="video_file_extract")
    
    # 选择字幕轨道
    subtitle_track = st.number_input("字幕轨道编号", min_value=0, value=0, step=1)
    
    # 选择输出字幕格式
    subtitle_formats = ["srt", "ass", "ssa", "sub", "idx", "vtt"]
    output_subtitle_format = st.selectbox("选择输出字幕格式", subtitle_formats)
    
    # 自定义输出文件名
    custom_output_filename_extract = st.text_input("自定义输出文件名（不包括后缀）", "", key="extract_subtitle_filename")
    
    # 高级选项
    with st.expander("高级选项"):
        # 选择字符编码
        encoding_options = ["UTF-8", "GBK", "GB2312", "ASCII"]
        subtitle_encoding = st.selectbox("字符编码", encoding_options)
    
    # 生成命令按钮
    if st.button("生成提取字幕命令"):
        # 构造输出文件名
        if custom_output_filename_extract:
            output_filename = f"{custom_output_filename_extract}.{output_subtitle_format}"
        else:
            output_filename = f"extracted_subtitle.{output_subtitle_format}"
        
        # 构建FFmpeg命令
        cmd_parts = [f"ffmpeg -i \"{video_file_extract}\""]
        
        # 添加字符编码参数
        if subtitle_encoding != "UTF-8":  # UTF-8是默认编码
            cmd_parts.append(f"-sub_charenc {subtitle_encoding}")
        
        # 添加字幕流选择和编码参数
        cmd_parts.append(f"-map 0:s:{subtitle_track} -c:s {output_subtitle_format}")
        
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
1. **烧录字幕到视频**：
   - 在上方输入视频文件名和字幕文件幕文件
2. 选择是否使用软字幕。
3. 根据选择的字幕类型，选择合适的输出封装格式。
4. 如果选择软字幕，可以决定是否重新编码视频；如果选择硬字幕，将强制重新编码视频。
5. 如果需要重新编码，可以选择CPU或GPU编码，并根据选择显示相应的编码器选项。
6. 选择码率控制模式并设置相应参数。
7. 点击"生成FFmpeg命令"按钮。
8. 将生成的命令复制到命令行中执行。
""")