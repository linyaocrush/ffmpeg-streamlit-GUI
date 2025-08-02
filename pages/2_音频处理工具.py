import streamlit as st

# 设置页面标题和图标
st.set_page_config(page_title="FFmpeg 音频处理工具", page_icon="🎵")

# 页面标题
st.title("FFmpeg 音频处理工具 🎵")

# 创建选项卡
# 修改这里的标签页创建，添加新的标签页
tab1, tab2, tab3, tab4, tab5 = st.tabs(["提取音频 📤", "合并音视频 🔄", "删除音频轨 🗑️", "音频剪辑 ✂️", "音频转码/转格式 🔄"])

# 提取音频选项卡
with tab1:
    st.header("从视频中提取音频 📤")
    
    # 使用列来组织输入字段
    col1, col2 = st.columns(2)
    with col1:
        # 输入视频文件名
        video_file_extract = st.text_input("视频文件名（包括后缀）", "example.mp4", key="video_file_extract")
    with col2:
        # 选择音频格式
        audio_formats = ["mp3", "aac", "wav", "flac", "m4a"]
        audio_format = st.selectbox("输出音频格式", audio_formats, key="audio_format")
    
    # 使用列来组织质量和自定义输出文件名
    col3, col4 = st.columns(2)
    with col3:
        # 音频质量选项
        quality_options = ["高质量", "中等质量", "低质量"]
        quality = st.selectbox("音频质量", quality_options, key="quality")
    with col4:
        # 自定义输出文件名
        custom_output_filename_extract = st.text_input("自定义输出文件名（可选）", "", key="extract_filename", 
                                                       placeholder="不包括后缀")
    
    # 高级选项
    with st.expander("高级选项 ⚙️"):
        audio_bitrate = st.text_input("音频码率", "192k", placeholder="例如: 128k, 192k, 320k", key="audio_bitrate")
        audio_channels = st.selectbox("声道数", ["保持原样", "单声道", "立体声"], key="audio_channels")
        
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成提取音频命令 🎛️", type="primary", key="extract_button"):
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
        st.text_area("生成的FFmpeg命令", command, height=150, key="extract_command_output")
        st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保视频文件在同一目录下。")

# 合并音视频选项卡
with tab2:
    st.header("合并音频和视频 🔄")
    
    # 使用列来组织输入字段
    col1, col2 = st.columns(2)
    with col1:
        # 输入文件名
        video_file_merge = st.text_input("视频文件名（包括后缀）", "video.mp4", key="video_file_merge")
    with col2:
        audio_file_merge = st.text_input("音频文件名（包括后缀）", "audio.mp3", key="audio_file_merge")
    
    # 使用列来组织输出格式和自定义输出文件名
    col3, col4 = st.columns(2)
    with col3:
        # 输出格式
        output_formats = ["mp4", "mkv", "avi", "mov"]
        output_format_merge = st.selectbox("输出封装格式", output_formats, key="output_format_merge")
    with col4:
        # 自定义输出文件名
        custom_output_filename_merge = st.text_input("自定义输出文件名（可选）", "", key="merge_filename",
                                                     placeholder="不包括后缀")
    
    # 高级选项
    with st.expander("高级选项 ⚙️"):
        video_codec = st.selectbox("视频编码器", ["保持原样", "libx264", "libx265", "mpeg4"], key="video_codec")
        audio_codec = st.selectbox("音频编码器", ["保持原样", "aac", "mp3", "flac"], key="audio_codec")
        
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成合并音视频命令 🎛️", type="primary", key="merge_button"):
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
        st.text_area("生成的FFmpeg命令", command, height=150, key="merge_command_output")
        st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保视频和音频文件在同一目录下。")

# 删除音频轨选项卡
with tab3:
    st.header("删除视频中的音频轨 🗑️")
    
    # 输入视频文件名
    video_file_remove = st.text_input("视频文件名（包括后缀）", "example.mp4", key="video_file_remove")
    
    # 选择删除模式
    remove_mode = st.radio("选择删除模式", ["删除所有音频轨", "删除指定音频轨"], key="remove_mode")
    
    # 如果选择删除指定音频轨，则显示轨道编号输入
    if remove_mode == "删除指定音频轨":
        track_number = st.number_input("音频轨编号（从0开始）", min_value=0, value=0, key="track_number")
    
    # 自定义输出文件名
    custom_output_filename_remove = st.text_input("自定义输出文件名（可选）", "", key="remove_filename",
                                                   placeholder="不包括后缀")
    
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成删除音频轨命令 🎛️", type="primary", key="remove_button"):
        # 构造输出文件名
        if custom_output_filename_remove:
            output_filename = custom_output_filename_remove
        else:
            # 根据输入文件名生成输出文件名
            input_name = video_file_remove.rsplit('.', 1)[0] if '.' in video_file_remove else video_file_remove
            output_filename = f"{input_name}_no_audio"
        
        # 添加文件扩展名
        file_extension = video_file_remove.split('.')[-1] if '.' in video_file_remove else 'mp4'
        output_filename_with_ext = f"{output_filename}.{file_extension}"
        
        # 构建FFmpeg命令
        if remove_mode == "删除所有音频轨":
            command = f"ffmpeg -i \"{video_file_remove}\" -c copy -an \"{output_filename_with_ext}\""
        else:
            # 删除指定音频轨的命令
            command = f"ffmpeg -i \"{video_file_remove}\" -map 0 -c copy -map -0:a:{track_number} \"{output_filename_with_ext}\""
        
        # 显示生成的命令
        st.text_area("生成的FFmpeg命令", command, height=150, key="remove_command_output")
        st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保视频文件在同一目录下。")

# 音频剪辑选项卡
with tab4:
    st.header("音频剪辑 ✂️")
    
    # 输入音频文件名
    audio_file_clip = st.text_input("音频文件名（包括后缀）", "input.mp3", key="audio_file_clip")
    
    # 使用列来组织开始时间和结束时间
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.text_input("开始时间", "00:00:00", placeholder="HH:MM:SS 或秒数", key="start_time")
    with col2:
        end_time = st.text_input("结束时间", "00:01:00", placeholder="HH:MM:SS 或秒数", key="end_time")
    
    # 自定义输出文件名
    custom_output_filename_clip = st.text_input("自定义输出文件名（可选）", "", key="clip_filename",
                                                 placeholder="不包括后缀")
    
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成音频剪辑命令 🎛️", type="primary", key="clip_button"):
        # 构造输出文件名
        if custom_output_filename_clip:
            output_filename = custom_output_filename_clip
        else:
            # 根据输入文件名生成输出文件名
            input_name = audio_file_clip.rsplit('.', 1)[0] if '.' in audio_file_clip else audio_file_clip
            output_filename = f"{input_name}_clipped"
        
        # 添加文件扩展名
        file_extension = audio_file_clip.split('.')[-1] if '.' in audio_file_clip else 'mp3'
        output_filename_with_ext = f"{output_filename}.{file_extension}"
        
        # 构建FFmpeg命令
        command = f"ffmpeg -i \"{audio_file_clip}\" -ss {start_time} -to {end_time} -c copy \"{output_filename_with_ext}\""
        
        # 显示生成的命令
        st.text_area("生成的FFmpeg命令", command, height=150, key="clip_command_output")
        st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保音频文件在同一目录下。")

# 音频转码/转格式选项卡
with tab5:
    st.header("音频转码/转格式 🔄")
    
    # 输入音频文件名
    audio_file_convert = st.text_input("音频文件名（包括后缀）", "input.mp3", key="audio_file_convert")
    
    # 使用列来组织输出格式和自定义输出文件名
    col1, col2 = st.columns(2)
    with col1:
        # 选择输出音频格式
        output_audio_formats = ["mp3", "aac", "wav", "flac", "m4a", "ogg", "wma"]
        output_audio_format = st.selectbox("输出音频格式", output_audio_formats, key="output_audio_format")
    with col2:
        # 自定义输出文件名
        custom_output_filename_convert = st.text_input("自定义输出文件名（可选）", "", key="convert_filename",
                                                       placeholder="不包括后缀")
    
    # 高级选项
    with st.expander("高级选项 ⚙️"):
        # 音频编码器选择
        audio_encoders = {
            "mp3": ["libmp3lame"],
            "aac": ["aac", "libfdk_aac"],
            "wav": ["pcm_s16le"],
            "flac": ["flac"],
            "m4a": ["aac", "libfdk_aac"],
            "ogg": ["libvorbis"],
            "wma": ["wmav2"]
        }
        selected_encoder = st.selectbox("音频编码器", audio_encoders.get(output_audio_format, ["默认"]), key="audio_encoder")
        
        # 码率控制
        bitrate_options = ["64k", "128k", "192k", "256k", "320k"]
        audio_bitrate_convert = st.selectbox("音频码率", bitrate_options, key="audio_bitrate_convert")
        
        # 采样率
        sample_rates = ["保持原样", "22050", "44100", "48000", "96000"]
        sample_rate = st.selectbox("采样率", sample_rates, key="sample_rate")
        
        # 声道数
        channels_options = ["保持原样", "单声道", "立体声"]
        channels = st.selectbox("声道数", channels_options, key="channels")
    
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成音频转码命令 🎛️", type="primary", key="convert_button"):
        # 构造输出文件名
        if custom_output_filename_convert:
            output_filename = custom_output_filename_convert
        else:
            # 根据输入文件名生成输出文件名
            input_name = audio_file_convert.rsplit('.', 1)[0] if '.' in audio_file_convert else audio_file_convert
            output_filename = f"{input_name}_converted"
        
        # 添加文件扩展名
        output_filename_with_ext = f"{output_filename}.{output_audio_format}"
        
        # 构建FFmpeg命令
        cmd_parts = [f"ffmpeg -i \"{audio_file_convert}\""]
        
        # 添加编码器
        if selected_encoder != "默认":
            cmd_parts.append(f"-c:a {selected_encoder}")
        
        # 添加码率
        cmd_parts.append(f"-b:a {audio_bitrate_convert}")
        
        # 添加采样率
        if sample_rate != "保持原样":
            cmd_parts.append(f"-ar {sample_rate}")
        
        # 添加声道数
        if channels != "保持原样":
            if channels == "单声道":
                cmd_parts.append("-ac 1")
            elif channels == "立体声":
                cmd_parts.append("-ac 2")
        
        # 添加输出文件名
        cmd_parts.append(f"\"{output_filename_with_ext}\"")
        
        # 组合命令
        command = " ".join(cmd_parts)
        # 显示生成的命令
        st.text_area("生成的FFmpeg命令", command, height=150, key="convert_command_output")
        st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保音频文件在同一目录下。")
