import pygame
import time
import threading
from queue import Queue
from typing import Dict, List
from config import *

class DisplayManager:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        
        # 设置显示屏参数
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("语音助手")
        
        # 初始化字体
        self.font = pygame.font.Font(FONT_PATH, 20)
        self.small_font = pygame.font.Font(FONT_PATH, 16)
        
        # 对话历史队列
        self.conversation_queue = Queue(maxsize=MAX_DISPLAY_MESSAGES)
        
        # 状态变量
        self.is_listening = False
        self.volume_level = 0
        self.system_status = "待机"
        
        # 启动显示线程
        self.running = True
        self.display_thread = threading.Thread(target=self._display_loop)
        self.display_thread.daemon = True
        self.display_thread.start()
    
    def _display_loop(self):
        """显示循环"""
        while self.running:
            try:
                self._update_display()
                time.sleep(0.1)  # 控制刷新率
            except Exception as e:
                print(f"显示更新错误: {e}")
    
    def _update_display(self):
        """更新显示内容"""
        # 清屏
        self.screen.fill(BACKGROUND_COLOR)
        
        # 绘制状态栏
        self._draw_status_bar()
        
        # 绘制对话内容
        self._draw_conversations()
        
        # 绘制音量条
        self._draw_volume_bar()
        
        # 更新显示
        pygame.display.flip()
    
    def _draw_status_bar(self):
        """绘制状态栏"""
        status_text = f"状态: {self.system_status}"
        status_surface = self.small_font.render(status_text, True, TEXT_COLOR)
        self.screen.blit(status_surface, (10, 10))
        
        # 绘制时间
        time_text = time.strftime("%H:%M:%S")
        time_surface = self.small_font.render(time_text, True, TEXT_COLOR)
        self.screen.blit(time_surface, (self.width - 100, 10))
    
    def _draw_conversations(self):
        """绘制对话内容"""
        y_pos = 50
        for msg in list(self.conversation_queue.queue):
            # 用户输入
            if msg.get('user_input'):
                user_text = f"用户: {msg['user_input']}"
                user_surface = self.font.render(user_text, True, USER_TEXT_COLOR)
                self.screen.blit(user_surface, (10, y_pos))
                y_pos += 30
            
            # AI回答
            if msg.get('bot_response'):
                bot_text = f"助手: {msg['bot_response']}"
                # 处理长文本换行
                wrapped_text = self._wrap_text(bot_text)
                for line in wrapped_text:
                    line_surface = self.font.render(line, True, BOT_TEXT_COLOR)
                    self.screen.blit(line_surface, (10, y_pos))
                    y_pos += 30
            
            y_pos += 10  # 对话间距
    
    def _draw_volume_bar(self):
        """绘制音量条"""
        bar_height = 100
        bar_width = 20
        x_pos = self.width - 30
        y_pos = self.height - bar_height - 10
        
        # 绘制背景
        pygame.draw.rect(self.screen, (100, 100, 100),
                        (x_pos, y_pos, bar_width, bar_height))
        
        # 绘制音量level
        volume_height = int(bar_height * (self.volume_level / 100))
        pygame.draw.rect(self.screen, (0, 255, 0),
                        (x_pos, y_pos + bar_height - volume_height,
                         bar_width, volume_height))
    
    def _wrap_text(self, text: str, max_chars: int = 30) -> List[str]:
        """文本换行处理"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def update_conversation(self, user_input: str, bot_response: str):
        """更新对话内容"""
        if self.conversation_queue.full():
            self.conversation_queue.get()  # 移除最旧的对话
        
        self.conversation_queue.put({
            'user_input': user_input,
            'bot_response': bot_response
        })
    
    def update_status(self, status: str):
        """更新系统状态"""
        self.system_status = status
    
    def update_volume(self, level: int):
        """更新音量级别"""
        self.volume_level = min(max(level, 0), 100)
    
    def cleanup(self):
        """清理资源"""
        self.running = False
        pygame.quit() 