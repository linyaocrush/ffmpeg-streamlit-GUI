import streamlit as st

# 设置页面标题
st.title("FFmpeg 音频处理工具")

# 创建选项卡
tab1, tab2 = st.tabs(["提取音频", "合并音视频"])

# 提取音频选项卡
with tab1:
    st.header("从视频中提取音频")
    
    # 输入视频文件名
    video_file_extract = st.text_input("视频文件名（包括后缀）", "example.mp4")
    
    # 选择音频格式
    audio_formats = ["mp3", "aac", "wav", "flac", "m4a"]
    audio_format = st.selectbox("选择输出音频格式", audio_formats)
    
    # 音频质量选项
    quality_options = ["高质量", "中等质量", "低质量"]
    quality = st.selectbox("选择音频质量", quality_options)
    
    # 自定义输出文件名
    custom_output_filename_extract = st.text_input("自定义输出文件名（可选）", "", key="extract_filename")
    
    # 高级选项
    with st.expander("高级选项"):
        audio_bitrate = st.text_input("音频码率 (例如: 128k, 192k, 320k)", "192k")
        audio_channels = st.selectbox("声道数", ["保持原样", "单声道", "立体声"])
        
    # 生成命令按钮
    if st.button("生成提取音频命令"):
        # 构造输出文件名
        if custom_output_filename_extract:
            output_filename = custom_output_filename_extract
        else:
            output_filename = f"extracted_audio.{audio_format}"
        
        # 构建FFmpeg命令
        cmd_parts = [f"ffmpeg -i \"{video_file_extract}\""]
        
        # 添加音频编码参数
        if audio_format == "mp3":
            cmd_parts.append("-vn -ar 44100 -ac 2")
            cmd_parts.append(f"-ab {audio_bitrate} -f mp3")
        elif audio_format == "aac":
            cmd_parts.append(f"-vn -acodec aac -ab {audio_bitrate} -f adts")
        elif audio_format == "wav":
            cmd_parts.append("-vn -acodec pcm_s16le -ar 44100 -ac 2")
        elif audio_format == "flac":
            cmd_parts.append("-vn -acodec flac")
        elif audio_format == "m4a":
            cmd_parts.append(f"-vn -acodec aac -ab {audio_bitrate} -f mp4")
        
        # 添加声道设置
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

# 合并音视频选项卡
with tab2:
    st.header("合并音频和视频")
    
    # 输入文件名
    video_file_merge = st.text_input("视频文件名（包括后缀）", "video.mp4")
    audio_file_merge = st.text_input("音频文件名（包括后缀）", "audio.mp3")
    
    # 输出格式
    output_formats = ["mp4", "mkv", "avi", "mov"]
    output_format_merge = st.selectbox("选择输出封装格式", output_formats)
    
    # 自定义输出文件名
    custom_output_filename_merge = st.text_input("自定义输出文件名（可选）", "", key="merge_filename")
    
    # 高级选项
    with st.expander("高级选项"):
        video_codec = st.selectbox("视频编码器", ["保持原样", "libx264", "libx265", "mpeg4"])
        audio_codec = st.selectbox("音频编码器", ["保持原样", "aac", "mp3", "flac"])
        
    # 生成命令按钮
    if st.button("生成合并音视频命令"):
        # 构造输出文件名
        if custom_output_filename_merge:
            output_filename = custom_output_filename_merge
        else:
            output_filename = f"merged_video.{output_format_merge}"
        
        # 构建FFmpeg命令
        cmd_parts = [f"ffmpeg -i \"{video_file_merge}\" -i \"{audio_file_merge}\""]
        
        # 添加编码参数
        if video_codec != "保持原样":
            cmd_parts.append(f"-c:v {video_codec}")
        else:
            cmd_parts.append("-c:v copy")
            
        if audio_codec != "保持原样":
            cmd_parts.append(f"-c:a {audio_codec}")
        else:
            cmd_parts.append("-c:a copy")
        
        # 添加其他参数
        cmd_parts.append("-strict experimental")
        
        # 添加输出文件名
        cmd_parts.append(f"\"{output_filename}\"")
        
        # 组合命令
        command = " ".join(cmd_parts)
        
        # 显示生成的命令
        st.text_area("生成的FFmpeg命令", command, height=150)
        st.info("请将上述命令复制到命令行中执行。确保视频和音频文件在同一目录下。")

# 使用说明
st.markdown("""
### 使用说明
1. **提取音频**：输入视频文件名，选择输出音频格式和质量，点击生成命令按钮。
2. **合并音视频**：输入视频和音频文件名，选择输出格式，点击生成命令按钮。
3. 将生成的命令复制到命令行中执行。
4. 确保所有文件都在同一目录下。
""")