import speech_recognition as sr
import pyaudio
import struct
import pvporcupine
from config import *

class AudioInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # 优化识别器参数
        self.recognizer.energy_threshold = 300  # 声音检测阈值
        self.recognizer.dynamic_energy_threshold = True  # 动态能量阈值
        self.recognizer.dynamic_energy_adjustment_damping = 0.15  # 动态调整阻尼
        self.recognizer.dynamic_energy_ratio = 1.5  # 动态能量比率
        self.recognizer.pause_threshold = 0.8  # 停顿阈值
        self.recognizer.operation_timeout = None  # 操作超时
        
        # 初始化Porcupine唤醒词检测器
        self.porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keywords=['hey computer'],
            sensitivities=[0.5]
        )
        
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=AUDIO_FORMAT,  # 使用优化后的音频格式
            input=True,
            frames_per_buffer=AUDIO_CHUNK_OPTIMIZE  # 使用优化后的块大小
        )

    def wait_for_wake_word(self):
        """等待唤醒词"""
        print(f"等待唤醒词 '{WAKE_WORD}'...")
        try:
            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    print("检测到唤醒词！")
                    return True
                    
        except KeyboardInterrupt:
            print("停止监听唤醒词")
            return False

    def listen(self):
        """录制用户声音输入（优化版）"""
        with sr.Microphone(
            sample_rate=16000,  # 固定采样率
            chunk_size=AUDIO_CHUNK_OPTIMIZE  # 使用优化后的块大小
        ) as source:
            # 动态噪声调整
            print("调整环境噪声...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("请说话...")
            try:
                # 使用超时机制
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(
                    audio,
                    language=AUDIO_LANG,
                    show_all=False  # 只返回最可能的结果
                )
                print(f"您说: {text}")
                return text
            except sr.WaitTimeoutError:
                print("等待超时")
                return None
            except sr.UnknownValueError:
                print("无法识别语音")
                return None
            except sr.RequestError as e:
                print(f"语音识别服务错误: {e}")
                return None

    def cleanup(self):
        """清理资源"""
        self.audio_stream.close()
        self.pa.terminate()
        self.porcupine.delete() 