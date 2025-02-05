import torch
import whisper
import os
import re
from typing import Optional
from faster_whisper import WhisperModel
from langdetect import detect, LangDetectException
from difflib import SequenceMatcher

class SubtitleGenerator:
    def __init__(self, model_name: str = "large-v3"):
        """初始化字幕生成器
        
        Args:
            model_name (str): whisper模型名称，默认为large-v3
        """
        self.model = whisper.load_model(name=model_name)
                
        
    def _is_similar(self, text1: str, text2: str, threshold: float = 0.7) -> bool:
        """检查两段文本是否相似
        
        Args:
            text1 (str): 第一段文本
            text2 (str): 第二段文本
            threshold (float): 相似度阈值，默认0.7
            
        Returns:
            bool: 如果相似度超过阈值返回True
        """
        return SequenceMatcher(None, text1, text2).ratio() > threshold
        
    def _merge_similar_segments(self, segments: list) -> list:
        """合并相似的片段
        
        Args:
            segments (list): 原始片段列表
            
        Returns:
            list: 处理后的片段列表
        """
        if not segments:
            return segments
            
        merged = []
        current = segments[0]
        
        for next_seg in segments[1:]:
            if self._is_similar(current["text"], next_seg["text"]):
                # 如果相似，使用时长较长的片段
                if next_seg["end"] - next_seg["start"] > current["end"] - current["start"]:
                    current = next_seg
            else:
                merged.append(current)
                current = next_seg
                
        merged.append(current)
        return merged
        
    def generate_subtitles(self, audio_path: str, output_path: Optional[str] = None, target_lang: str = 'en'):
        """生成字幕文件
        
        Args:
            audio_path (str): 音频文件路径
            output_path (Optional[str]): 输出srt文件路径，如果未提供则保存到音频同目录
            target_lang (str): 目标语言代码，默认为英语
            
        Returns:
            str: 生成的srt文件路径
        """
        if output_path is None:
            base_path = os.path.splitext(audio_path)[0]
            output_path = f"{base_path}_{target_lang}.srt"
            
        # 转录音频，使用优化后的参数
        result = self.model.transcribe(
            audio_path,
            verbose=True,
            condition_on_previous_text=True,  # 减少重复
            language=target_lang,  # 指定目标语言
            temperature=0,  # 降低随机性
            #best_of=5,  # 增加采样数量以提高准确性
            #beam_size=5,  # 使用beam search提高质量
            #compression_ratio_threshold=2.4,  # 控制语音压缩比
            #no_speech_threshold=0.8,  # 提高无声检测阈值
            #logprob_threshold=-0.8,  # 提高概率阈值
            #prompt_reset_on_temperature=0.4,  # 重置提示温度阈值
            #suppress_tokens=[-1],  # 抑制特殊标记
            #word_timestamps=True  # 启用词级时间戳以提高准确性
        )

        # 合并相似片段
        segments = self._merge_similar_segments(result["segments"])

        # 生成srt格式字幕，包含语言检测和文本清理
        with open(output_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments):
                text = segment["text"].strip()
                start = self._format_time(segment["start"])
                end = self._format_time(segment["end"])
                
                f.write(f"{i+1}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        # 释放GPU缓存
        torch.cuda.empty_cache()
        
        return output_path
        
    def _format_time(self, seconds: float) -> str:
        """将秒数格式化为srt时间格式
        
        Args:
            seconds (float): 秒数
            
        Returns:
            str: 格式化后的时间字符串 (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}".replace(".", ",")

# 示例用法
if __name__ == "__main__":
    # 示例音频路径
    audio_path = r"YOUR AUDIO PATH"
    
    # 创建字幕生成器实例
    generator = SubtitleGenerator()
    
    # 生成字幕
    srt_path = generator.generate_subtitles(audio_path)
    
    print(f"字幕已生成到: {srt_path}")
