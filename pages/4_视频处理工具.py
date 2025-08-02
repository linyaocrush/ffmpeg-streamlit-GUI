import streamlit as st
import matplotlib.font_manager as fm
from fontTools.ttLib import TTFont
import os

# 设置页面标题和图标
st.set_page_config(page_title="FFmpeg 视频处理工具", page_icon="🎬")

# 页面标题
st.title("FFmpeg 视频处理工具 🎬")

# 创建选项卡
tab1, tab2, tab3, tab4 = st.tabs(["视频剪辑 ✂️", "视频合并 🔄", "视频处理 ⚙️", "视频水印 🧧"])

# 视频剪辑选项卡
with tab1:
    st.header("视频剪辑工具 ✂️")
    
    # 输入视频文件名
    video_file_clip = st.text_input("视频文件名（包括后缀）", "example.mp4", key="video_file_clip")
    
    # 时间输入方式选择
    time_option = st.radio("选择时间输入方式", ["开始时间和结束时间", "开始时间和持续时间"])
    
    # 初始化时间变量
    start_time = "00:00:00"
    end_time = "00:00:10"
    duration = "00:00:10"
    
    # 根据选择显示不同的输入框
    if time_option == "开始时间和结束时间":
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.text_input("开始时间 (HH:MM:SS)", "00:00:00", key="start_time")
        with col2:
            end_time = st.text_input("结束时间 (HH:MM:SS)", "00:00:10", key="end_time")
    else:
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.text_input("开始时间 (HH:MM:SS)", "00:00:00", key="start_time_duration")
        with col2:
            duration = st.text_input("持续时间 (HH:MM:SS)", "00:00:10", key="duration")
    
    # 自定义输出文件名
    output_filename_clip = st.text_input("自定义输出文件名（可选）", "", key="output_filename_clip",
                                         placeholder="不包括后缀")
    
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成视频剪辑命令 🎛️", type="primary", key="clip_button"):
        # 构造输出文件名
        if output_filename_clip:
            output_filename = f"{output_filename_clip}.mp4"
        else:
            input_name = video_file_clip.rsplit('.', 1)[0] if '.' in video_file_clip else video_file_clip
            output_filename = f"{input_name}_clipped.mp4"
        
        # 构建FFmpeg命令
        if time_option == "开始时间和结束时间":
            # 计算持续时间（简化处理，实际应用中可能需要更复杂的计算）
            command = f"ffmpeg -i \"{video_file_clip}\" -ss {start_time} -to {end_time} -c copy \"{output_filename}\""
        else:
            command = f"ffmpeg -i \"{video_file_clip}\" -ss {start_time} -t {duration} -c copy \"{output_filename}\""
        
        # 显示生成的命令
        st.text_area("生成的FFmpeg命令", command, height=150, key="clip_command_output")
        st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保视频文件在同一目录下。")

# 视频合并选项卡
with tab2:
    st.header("视频合并工具 🔄")
    
    # 使用st.session_state来管理动态输入框
    if "video_files" not in st.session_state:
        st.session_state.video_files = ["", ""]
    
    # 显示输入框
    for i, video_file in enumerate(st.session_state.video_files):
        st.session_state.video_files[i] = st.text_input(f"视频文件 {i+1}（包括后缀）", 
                                                        video_file, 
                                                        key=f"video_file_merge_{i}")
    
    # 添加和删除按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ 添加视频文件"):
            st.session_state.video_files.append("")
            st.rerun()  # 修改这一行
    with col2:
        if len(st.session_state.video_files) > 2:
            if st.button("➖ 删除最后一个"):
                st.session_state.video_files.pop()
                st.rerun()  # 修改这一行

    # 自定义输出文件名
    output_filename_merge = st.text_input("自定义输出文件名（可选）", "", key="output_filename_merge",
                                          placeholder="不包括后缀")
    
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成视频合并命令 🎛️", type="primary", key="merge_button"):
        # 检查是否有空的输入框
        if any(not video_file.strip() for video_file in st.session_state.video_files):
            st.error("请填写所有视频文件名！")
        else:
            # 构造输出文件名
            if output_filename_merge:
                output_filename = f"{output_filename_merge}.mp4"
            else:
                output_filename = "merged_video.mp4"
            
            # 创建临时文件列表
            file_list_content = "\n".join([f"file '{video_file}'" for video_file in st.session_state.video_files])
            
            # 保存文件列表到临时文件（实际应用中可能需要更复杂的处理）
            # 这里我们直接生成命令说明
            command = f"ffmpeg -f concat -safe 0 -i <(echo '{file_list_content}') -c copy \"{output_filename}\""
            
            # 显示生成的命令
            st.text_area("生成的FFmpeg命令", command, height=200, key="merge_command_output")
            st.info("注意：上述命令使用了Bash语法 (<(...) 进程替换)。在Windows上，您需要先创建一个包含以下内容的文本文件 'file_list.txt'：")
            
            # 显示文件列表内容
            st.code(file_list_content, language="text")
            st.info("然后使用命令：ffmpeg -f concat -safe 0 -i file_list.txt -c copy \"" + output_filename + "\"")
            st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保所有视频文件在同一目录下。")

# 视频处理选项卡
with tab3:
    st.header("视频处理工具 ⚙️")
    
    # 输入视频文件名
    video_file_process = st.text_input("视频文件名（包括后缀）", "example.mp4", key="video_file_process")
    
    # 处理选项
    st.subheader("选择处理选项")
    
    # 缩放视频
    resize_option = st.checkbox("缩放视频", key="resize_option")
    if resize_option:
        col1, col2 = st.columns(2)
        with col1:
            width = st.number_input("宽度 (像素)", min_value=1, value=1920, key="width")
        with col2:
            height = st.number_input("高度 (像素)", min_value=1, value=1080, key="height")
    
    # 快进/慢放
    speed_option = st.checkbox("调整播放速度", key="speed_option")
    if speed_option:
        speed_factor = st.slider("速度倍数", 0.1, 4.0, 1.0, 0.1, key="speed_factor")
    
    # 裁剪视频
    crop_option = st.checkbox("裁剪视频", key="crop_option")
    if crop_option:
        st.info("裁剪参数 (x, y为裁剪起始点，w, h为裁剪区域宽高)")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            crop_x = st.number_input("X坐标", value=0, key="crop_x")
        with col2:
            crop_y = st.number_input("Y坐标", value=0, key="crop_y")
        with col3:
            crop_w = st.number_input("裁剪宽度", min_value=1, value=1920, key="crop_w")
        with col4:
            crop_h = st.number_input("裁剪高度", min_value=1, value=1080, key="crop_h")
    
    # 旋转视频
    rotate_option = st.checkbox("旋转视频", key="rotate_option")
    if rotate_option:
        rotation = st.selectbox("旋转角度", ["90度顺时针", "90度逆时针", "180度"], key="rotation")
    
    # 自定义输出文件名
    output_filename_process = st.text_input("自定义输出文件名（可选）", "", key="output_filename_process",
                                            placeholder="不包括后缀")
    
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成视频处理命令 🎛️", type="primary", key="process_button"):
        # 构造输出文件名
        if output_filename_process:
            output_filename = f"{output_filename_process}.mp4"
        else:
            input_name = video_file_process.rsplit('.', 1)[0] if '.' in video_file_process else video_file_process
            output_filename = f"{input_name}_processed.mp4"
        
        # 构建FFmpeg命令
        cmd_parts = [f"ffmpeg -i \"{video_file_process}\""]
        
        # 添加滤镜
        filters = []
        
        # 添加缩放滤镜
        if resize_option:
            filters.append(f"scale={width}:{height}")
        
        # 添加速度滤镜
        if speed_option:
            # 使用setpts滤镜调整视频速度，atempo调整音频速度（atempo范围0.5-2.0）
            if speed_factor >= 0.5 and speed_factor <= 2.0:
                filters.append(f"setpts={1/speed_factor:.2f}*PTS")
                cmd_parts.append(f"-filter:a atempo={speed_factor}")
            else:
                filters.append(f"setpts={1/speed_factor:.2f}*PTS")
                # 对于超出atempo范围的速度，需要其他处理方式
        
        # 添加裁剪滤镜
        if crop_option:
            filters.append(f"crop={crop_w}:{crop_h}:{crop_x}:{crop_y}")
        
        # 添加旋转滤镜
        if rotate_option:
            if rotation == "90度顺时针":
                filters.append("transpose=1")
            elif rotation == "90度逆时针":
                filters.append("transpose=2")
            elif rotation == "180度":
                filters.append("transpose=1,transpose=1")
        
        # 应用滤镜
        if filters:
            cmd_parts.append(f"-vf \"{'.'.join(filters)}\"")
        
        # 添加输出文件
        cmd_parts.append(f"\"{output_filename}\"")
        
        # 组合命令
        command = " ".join(cmd_parts)
        
        # 显示生成的命令
        st.text_area("生成的FFmpeg命令", command, height=150, key="process_command_output")
        st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保视频文件在同一目录下。")

# 视频水印选项卡
with tab4:
    st.header("视频水印工具 🧧")
    
    # 输入视频文件名
    video_file_watermark = st.text_input("视频文件名（包括后缀）", "example.mp4", key="video_file_watermark")
    
    # 水印类型选择
    watermark_type = st.radio("选择水印类型", ["文字水印", "图片水印"])
    
    # 文字水印选项
    if watermark_type == "文字水印":
        text_content = st.text_input("水印文字内容", "Watermark", key="text_content")
        font_size = st.slider("字体大小", 10, 100, 24, key="font_size")
        font_color = st.color_picker("字体颜色", "#FFFFFF", key="font_color")
        
        # 获取系统字体列表
        try:
            # 扫描字体并读取中文名称或英文名称
            font_paths = fm.findSystemFonts(fontext='ttf') + fm.findSystemFonts(fontext='otf')
            name_map = {}
            for fp in font_paths[:500]:  # 限制字体数量
                try:
                    tt = TTFont(fp, lazy=True)
                    name_record = None
                    for rec in tt['name'].names:
                        # 优先中文名称 (langID 2052,3076)
                        if rec.nameID == 1 and rec.platformID == 3 and rec.langID in (2052, 3076):
                            name_record = rec
                            break
                    if name_record:
                        display = name_record.string.decode(name_record.getEncoding())
                    else:
                        # fallback to English
                        en = tt['name'].getName(1, 1, 0, 0x0409)
                        display = en.string.decode('utf-16-be') if en else os.path.basename(fp)
                    name_map[display] = fp
                except Exception:
                    continue
            if name_map:
                # 修改前的代码：
                # sorted_fonts = sorted(name_map.keys())
                
                # 修改后的代码：
                # 将中文字体显示在最前面
                font_names = list(name_map.keys())
                chinese_fonts = [name for name in font_names if any('\u4e00' <= char <= '\u9fff' for char in name)]
                english_fonts = [name for name in font_names if not any('\u4e00' <= char <= '\u9fff' for char in name)]
                sorted_fonts = sorted(chinese_fonts) + sorted(english_fonts)
                
                # 字体选择
                selected_font_name = st.selectbox("选择字体（中文/英文）", sorted_fonts, index=0, key="font_selection")
                font_path = name_map[selected_font_name]
            else:
                st.error("未找到系统字体！")
                sorted_fonts = ['Arial', 'SimHei', 'SimSun', 'Microsoft YaHei']
                font_names = {name: name for name in sorted_fonts}
                selected_font_name = st.selectbox("选择字体", sorted_fonts, index=0, key="font_selection_default")
                font_path = font_names[selected_font_name]
        except Exception as e:
            # 如果无法获取系统字体，使用默认字体列表
            sorted_fonts = ['Arial', 'SimHei', 'SimSun', 'Microsoft YaHei']
            font_names = {name: name for name in sorted_fonts}
            selected_font_name = st.selectbox("选择字体", sorted_fonts, index=0, key="font_selection_default")
            font_path = font_names[selected_font_name]
        
        # 注意：删除了重复的字体选择框
        # selected_font_name = st.selectbox("选择字体", sorted_fonts, index=0, key="font_selection")  # 这行需要删除
        
    # 图片水印选项
    else:
        image_file = st.text_input("水印图片文件名（包括后缀）", "watermark.png", key="image_file")
        
    # 水印位置设置
    st.subheader("水印位置")
    position_option = st.selectbox("选择水印位置", 
                                  ["左上角", "右上角", "左下角", "右下角", "中心", "自定义"])
    
    # 自定义位置设置
    if position_option == "自定义":
        col1, col2 = st.columns(2)
        with col1:
            x_position = st.number_input("X坐标 (像素)", value=10, key="x_position")
        with col2:
            y_position = st.number_input("Y坐标 (像素)", value=10, key="y_position")
    
    # 水印透明度
    opacity = st.slider("水印透明度", 0.0, 1.0, 0.5, 0.1, key="opacity")
    
    # 自定义输出文件名
    output_filename_watermark = st.text_input("自定义输出文件名（可选）", "", key="output_filename_watermark",
                                             placeholder="不包括后缀")
    
    # 生成命令按钮
    st.markdown("---")
    if st.button("生成视频水印命令 🎛️", type="primary", key="watermark_button"):
        # 构造输出文件名
        if output_filename_watermark:
            output_filename = f"{output_filename_watermark}.mp4"
        else:
            input_name = video_file_watermark.rsplit('.', 1)[0] if '.' in video_file_watermark else video_file_watermark
            output_filename = f"{input_name}_watermarked.mp4"
        
        # 构建FFmpeg命令
        if watermark_type == "文字水印":
            # 处理颜色格式
            color_hex = font_color.lstrip('#')
            
            # 根据位置设置水印参数
            if position_option == "左上角":
                position = "x=10:y=10"
            elif position_option == "右上角":
                position = "x=w-tw-10:y=10"
            elif position_option == "左下角":
                position = "x=10:y=h-th-10"
            elif position_option == "右下角":
                position = "x=w-tw-10:y=h-th-10"
            elif position_option == "中心":
                position = "x=(w-tw)/2:y=(h-th)/2"
            else:  # 自定义
                position = f"x={x_position}:y={y_position}"
            
            if 'name_map' in locals():
                font_path = name_map.get(selected_font_name, selected_font_name)
            else:
                font_path = font_names.get(selected_font_name, selected_font_name)

            escaped_font_path = font_path.replace('\\', '/').replace(':', '\\:').replace(' ', '\\ ')
            command = f"ffmpeg -i \"{video_file_watermark}\" -vf \"drawtext=text='{text_content}':fontsize={font_size}:fontcolor=0x{color_hex}@{opacity}:fontfile='{escaped_font_path}':{position}\" -y \"{output_filename}\""
        else:
            # 根据位置设置图片水印参数
            if position_option == "左上角":
                position = "x=10:y=10"
            elif position_option == "右上角":
                position = "x=W-w-10:y=10"
            elif position_option == "左下角":
                position = "x=10:y=H-h-10"
            elif position_option == "右下角":
                position = "x=W-w-10:y=H-h-10"
            elif position_option == "中心":
                position = "x=(W-w)/2:y=(H-h)/2"
            else:  # 自定义
                position = f"x={x_position}:y={y_position}"
            
            # 构建图片水印命令
            command = f"ffmpeg -i \"{video_file_watermark}\" -i \"{image_file}\" -filter_complex \"[1:v]format=rgba,colorchannelmixer=aa={opacity}[logo];[0:v][logo]overlay={position}\" -y \"{output_filename}\""
        
        # 显示生成的命令
        st.text_area("生成的FFmpeg命令", command, height=150, key="watermark_command_output")
        st.success("✅ 命令已生成！请将上述命令复制到命令行中执行。确保视频文件在同一目录下。")
