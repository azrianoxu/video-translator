# 视频翻译工具 (Video Translator)

这是一个强大的视频翻译工具，可以自动从视频中提取音频，生成字幕，并将字幕翻译成目标语言。

## 功能特点

- 从视频文件中提取音频
- 使用Whisper模型自动生成字幕
- 使用GPT模型进行高质量字幕翻译
- 支持多种语言翻译
- 自动清理临时文件

## 系统要求

- Python 3.8+
- FFmpeg（用于音频提取）
- CUDA支持（推荐，用于加速Whisper模型）

## 安装步骤

1. 克隆仓库：
```bash
git clone [repository-url]
cd video-translator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 安装FFmpeg（如果尚未安装）：
- Windows: 从[FFmpeg官网](https://ffmpeg.org/download.html)下载并添加到系统PATH
- Linux: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`

## 使用方法

1. 准备工作：
   - 获取OpenAI API密钥
   - 准备要翻译的视频文件

2. 基本用法：
```python
from video_translator import VideoTranslator

# 初始化翻译器
translator = VideoTranslator(api_key="your-api-key")

# 翻译视频
result = translator.translate_video(
    video_path="path/to/your/video.mp4",
    target_lang="Chinese"  # 目标语言
)

# 输出文件路径
print(f"原始字幕: {result['srt_path']}")
print(f"翻译字幕: {result['translated_srt_path']}")
```

## 主要组件

- `VideoTranslator`: 主要的翻译器类，协调整个翻译流程
- `AudioExtractor`: 负责从视频中提取音频
- `SubtitleGenerator`: 使用Whisper模型生成字幕
- `SubtitleTranslator`: 使用GPT模型翻译字幕

## 注意事项

- 请确保有足够的磁盘空间用于临时文件
- 翻译速度取决于视频长度和API响应时间
- 建议使用支持CUDA的GPU来加速字幕生成过程

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！ 
 