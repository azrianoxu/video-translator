from audio_extractor import AudioExtractor
from subtitle_generator import SubtitleGenerator
from subtitle_translator_gpt import SubtitleTranslator
import os
from typing import Optional

class VideoTranslator:
    def __init__(self, api_key: str):
        """初始化视频翻译器
        
        Args:
            api_key (str): OpenAI API密钥
        """
        self.audio_extractor = AudioExtractor(video_path)
        self.subtitle_generator = SubtitleGenerator()
        self.subtitle_translator = SubtitleTranslator(api_key)
        
    def translate_video(self, video_path: str, output_dir: Optional[str] = None, target_lang: str = "Chinese"):
        """翻译视频文件
        
        Args:
            video_path (str): 视频文件路径
            output_dir (Optional[str]): 输出目录，如果未提供则使用视频所在目录
            target_lang (str): 目标语言代码，默认为中文(zh)
            
        Returns:
            dict: 包含各步骤输出文件路径的字典
        """
        if output_dir is None:
            output_dir = os.path.dirname(video_path)
            
        # 1. 提取音频
        print("正在提取音频...")
        audio_path = self.audio_extractor.extract_audio()
        print(f"音频已提取到: {audio_path}")
        
        # 2. 生成字幕
        print("\n正在生成字幕...")
        srt_path = self.subtitle_generator.generate_subtitles(audio_path)
        print(f"字幕已生成到: {srt_path}")
        
        # 3. 翻译字幕
        print("\n正在翻译字幕...")
        translated_srt_path = self.subtitle_translator.translate_subtitles(srt_path, target_lang=target_lang)
        print(f"翻译后的字幕已保存到: {translated_srt_path}")
        
        # 4. 清理临时音频文件
        print("\n正在清理临时文件...")
        self._cleanup_audio(audio_path)
        
        return {
            "srt_path": srt_path,
            "translated_srt_path": translated_srt_path
        }
        
    def _cleanup_audio(self, audio_path: str):
        """清理临时音频文件
        
        Args:
            audio_path (str): 要删除的音频文件路径
        """
        try:
            os.remove(audio_path)
            print(f"已删除临时音频文件: {audio_path}")
        except Exception as e:
            print(f"删除音频文件失败: {e}")

# 示例用法
if __name__ == "__main__":
    # 替换为你的API key
    API_KEY = "YOUR API KEY"



    video_path_list = [r"YOUR VIDEO PATH"]
    # 翻译视频
    for video_path in video_path_list:
    
    # 创建视频翻译器实例
        translator = VideoTranslator(API_KEY)
    
    
        result = translator.translate_video(video_path, target_lang="Chinese")
        
        print("\n翻译完成！")
        print(f"原始字幕: {result['srt_path']}")
        print(f"翻译字幕: {result['translated_srt_path']}")
