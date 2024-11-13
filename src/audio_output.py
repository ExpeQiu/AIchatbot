import os
import tempfile
import subprocess
from gtts import gTTS
from config import *
from utils.cache_manager import CacheManager

class AudioOutput:
    def __init__(self):
        self.cache_manager = CacheManager()
        
    def speak(self, text):
        """使用F5-TTS将文字转换为语音输出（带缓存）"""
        try:
            # 检查缓存
            cached_audio = self.cache_manager.get_audio_cache(text)
            if cached_audio:
                print("使用缓存的音频文件")
                os.system(f"play {cached_audio}")
                return

            # 创建临时文件保存生成的音频
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                output_path = temp_file.name

            # 调用F5-TTS命令行工具生成语音
            cmd = [
                'f5-tts_infer-cli',
                '--model', F5TTS_MODEL,
                '--ref_audio', REF_AUDIO,
                '--ref_text', REF_TEXT,
                '--gen_text', text,
                '--output', output_path
            ]
            
            subprocess.run(cmd, check=True)
            
            # 缓存生成的音频
            self.cache_manager.set_audio_cache(text, output_path)
            
            # 播放生成的音频
            os.system(f"play {output_path}")
            
            # 删除临时文件
            os.unlink(output_path)
            
        except Exception as e:
            print(f"F5-TTS错误: {e}")
            # 如果F5-TTS失败，回退到gTTS
            self._fallback_speak(text)

    def _fallback_speak(self, text):
        """回退到gTTS的音频输出"""
        try:
            tts = gTTS(text=text, lang=AUDIO_LANG)
            tts.save("response.mp3")
            os.system("mpg321 response.mp3")
            os.remove("response.mp3")
        except Exception as e:
            print(f"gTTS错误: {e}")