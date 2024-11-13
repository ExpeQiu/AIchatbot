import os
from dotenv import load_dotenv
import pyaudio

load_dotenv()

# OpenAI API配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Picovoice访问密钥，需要从 https://console.picovoice.ai/ 获取
PICOVOICE_ACCESS_KEY = os.getenv('PICOVOICE_ACCESS_KEY')

# 音频配置
AUDIO_LANG = "zh-CN"  # 中文
RATE = 16000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

# 唤醒词配置
WAKE_WORD = "小明同学"

# F5-TTS配置
F5TTS_MODEL = "F5-TTS"  # 使用默认模型
REF_AUDIO = "path/to/reference_audio.wav"  # 参考音频路径
REF_TEXT = "参考音频的文本内容"  # 参考音频的文本

# 百度地图配置
BAIDU_MAP_AK = os.getenv('BAIDU_MAP_AK')  # 百度地图API密钥

# 默认位置配置（可以设置为用户常用地点）
DEFAULT_LOCATION = os.getenv('DEFAULT_LOCATION', "116.403963,39.915119")  # 默认北京天安门

# 缓存配置
CACHE_DIR = "cache"  # 缓存目录
AUDIO_CACHE_SIZE = 100  # 音频缓存数量限制
API_CACHE_TTL = 3600  # API缓存过期时间（秒）
AUDIO_CHUNK_OPTIMIZE = 4096  # 优化后的音频块大小
AUDIO_FORMAT = pyaudio.paFloat32  # 优化后的音频格式