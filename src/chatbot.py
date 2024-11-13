from .audio_input import AudioInput
from .audio_output import AudioOutput
from .api_client import APIClient
from .web_server import web_server

class VoiceChatBot:
    def __init__(self):
        self.audio_input = AudioInput()
        self.audio_output = AudioOutput()
        self.api_client = APIClient()
        
        # 启动Web服务器
        web_server.start()

    def run(self):
        """运行聊天机器人"""
        try:
            while True:
                # 等待唤醒词
                if self.audio_input.wait_for_wake_word():
                    # 播放提示音
                    self.audio_output.speak("我在听")
                    
                    # 获取用户输入
                    user_input = self.audio_input.listen()
                    if user_input:
                        ai_response = self.api_client.get_ai_response(user_input)
                        self.audio_output.speak(ai_response)
                        
                        # 添加到对话历史
                        web_server.add_conversation(user_input, ai_response)
                
        finally:
            # 清理资源
            self.audio_input.cleanup()

if __name__ == "__main__":
    bot = VoiceChatBot()
    bot.run() 