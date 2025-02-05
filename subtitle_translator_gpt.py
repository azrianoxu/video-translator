# coding:utf-8
import os
from typing import Optional
from openai import OpenAI

class SubtitleTranslator:
    def __init__(self, api_key: str):
        """初始化字幕翻译器
        
        Args:
            api_key (str): OpenAI API密钥
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url="CHATGPT_BASE_URL"
        )
        
    def translate_subtitles(self, srt_path: str, output_path: Optional[str] = None, target_lang: str = "Chinese"):
        """翻译字幕文件
        
        Args:
            srt_path (str): 原始srt文件路径
            output_path (Optional[str]): 输出srt文件路径，如果未提供则保存到原文件同目录
            target_lang (str): 目标语言代码，默认为中文(zh)
            
        Returns:
            str: 翻译后的srt文件路径
        """
        if output_path is None:
            base_path = os.path.splitext(srt_path)[0]
            base_file = base_path.split('_')[0]
            output_path = f"{base_file}.srt"
            
        # 读取原始字幕
        subtitles = self._read_srt(srt_path)
        
        # 翻译字幕内容
        translated_subtitles = []
        for sub in subtitles:
            translated_text = self._translate_text(sub["text"], sub["timing"], target_lang)
            translated_subtitles.append({
                "index": sub["index"],
                "timing": sub["timing"],
                "text": translated_text
            })
            
        # 写入翻译后的字幕
        self._write_srt(output_path, translated_subtitles)
        return output_path
        
    def _read_srt(self, file_path: str) -> list:
        """读取srt文件内容
        
        Args:
            file_path (str): srt文件路径
            
        Returns:
            list: 字幕内容列表，每个元素包含index, timing, text
        """
        subtitles = []
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():
                index = int(lines[i].strip())
                timing = lines[i+1].strip()
                text = ""
                i += 2
                while i < len(lines) and lines[i].strip() != "":
                    text += lines[i].strip() + " "
                    i += 1
                subtitles.append({
                    "index": index,
                    "timing": timing,
                    "text": text.strip()
                })
            i += 1
        return subtitles
        
    def _write_srt(self, file_path: str, subtitles: list):
        """写入srt文件
        
        Args:
            file_path (str): 输出文件路径
            subtitles (list): 字幕内容列表
        """
        with open(file_path, "w", encoding="utf-8") as f:
            for sub in subtitles:
                f.write(f"{sub['index']}\n")
                f.write(f"{sub['timing']}\n")
                f.write(f"{sub['text']}\n\n")
                
    def _translate_text(self, text: str, timing: str, target_lang: str) -> str:
        """调用API翻译文本
        
        Args:
            text (str): 要翻译的文本
            timing (str): 字幕时间
            target_lang (str): 目标语言代码
            
        Returns:
            str: 翻译后的文本
        """
        prompt = """
        你是一个翻译专家,将用户输入的文本直接翻译成中文。
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=1.3,
            stream=False
        )
        translated_text = response.choices[0].message.content
        print(f"时间: {timing}")
        print(f"源语言: {text}")
        print(f"翻译后: {translated_text}")
        print("-" * 50)
        return translated_text

# 示例用法
if __name__ == "__main__":
    # 替换为你的API key
    API_KEY = "YOUR API KEY"
    
    # 示例srt文件路径
    srt_path = r"YOUR SRT FILE PATH"
    
    # 创建字幕翻译器实例
    translator = SubtitleTranslator(API_KEY)

    
    # 翻译字幕
    translated_path = translator.translate_subtitles(srt_path)
    
    print(f"翻译后的字幕已保存到: {translated_path}")
