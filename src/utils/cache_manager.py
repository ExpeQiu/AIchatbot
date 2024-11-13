import os
import json
import time
import hashlib
from typing import Dict, Any
from functools import lru_cache
from config import *

class CacheManager:
    def __init__(self):
        self.cache_dir = CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
        self.api_cache: Dict[str, Dict] = {}
        self.load_api_cache()

    def load_api_cache(self):
        """加载API缓存"""
        cache_file = os.path.join(self.cache_dir, 'api_cache.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    # 清理过期缓存
                    current_time = time.time()
                    self.api_cache = {
                        k: v for k, v in cache_data.items()
                        if current_time - v['timestamp'] < API_CACHE_TTL
                    }
            except Exception as e:
                print(f"加载API缓存出错: {e}")
                self.api_cache = {}

    def save_api_cache(self):
        """保存API缓存"""
        cache_file = os.path.join(self.cache_dir, 'api_cache.json')
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.api_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存API缓存出错: {e}")

    def get_cache_key(self, data: str) -> str:
        """生成缓存键"""
        return hashlib.md5(data.encode()).hexdigest()

    def get_api_cache(self, key: str) -> Any:
        """获取API缓存"""
        if key in self.api_cache:
            cache_data = self.api_cache[key]
            if time.time() - cache_data['timestamp'] < API_CACHE_TTL:
                return cache_data['data']
        return None

    def set_api_cache(self, key: str, data: Any):
        """设置API缓存"""
        self.api_cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
        self.save_api_cache()

    @lru_cache(maxsize=AUDIO_CACHE_SIZE)
    def get_audio_cache(self, text: str) -> str:
        """获取音频缓存"""
        cache_key = self.get_cache_key(text)
        audio_path = os.path.join(self.cache_dir, f"{cache_key}.wav")
        return audio_path if os.path.exists(audio_path) else None

    def set_audio_cache(self, text: str, audio_path: str):
        """设置音频缓存"""
        cache_key = self.get_cache_key(text)
        cached_path = os.path.join(self.cache_dir, f"{cache_key}.wav")
        try:
            import shutil
            shutil.copy2(audio_path, cached_path)
        except Exception as e:
            print(f"缓存音频文件失败: {e}") 