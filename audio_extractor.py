import os
import subprocess

class AudioExtractor:
    def __init__(self, video_path):
        """初始化音频提取器
        
        Args:
            video_path (str): 视频文件路径
        """
        self.video_path = video_path
        
    def extract_audio(self, output_path=None):
        """提取音频并保存
        
        Args:
            output_path (str, optional): 音频输出路径. 如果未提供，则保存到视频同目录
            
        Returns:
            str: 保存的音频文件路径
        """
        if output_path is None:
            base_path = os.path.splitext(self.video_path)[0]
            output_path = f"{base_path}.wav"
            
        command = [
            'ffmpeg',
            '-i', self.video_path,
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar','16k',
            '-ac','1',
            output_path
        ]
        
        subprocess.run(command, check=True)
        return output_path

# 示例用法
if __name__ == "__main__":
    # 示例视频路径
    video_path = r"YOUR VIDEO PATH"
    
    # 创建音频提取器实例
    extractor = AudioExtractor(video_path)
    
    # 提取音频
    audio_path = extractor.extract_audio()
    
    print(f"音频已提取到: {audio_path}")