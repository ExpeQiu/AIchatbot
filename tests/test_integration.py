import unittest
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chatbot import VoiceChatBot
from src.web_server import web_server
from src.models.conversation import DatabaseManager

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """测试类开始前的设置"""
        # 初始化测试数据库
        cls.test_db_path = "data/test_conversations.db"
        cls.db = DatabaseManager(cls.test_db_path)
        
        # 启动Web服务器
        web_server.start(port=5001)  # 使用不同的端口避免冲突
        time.sleep(1)  # 等待服务器启动
        
    @classmethod
    def tearDownClass(cls):
        """测试类结束后的清理"""
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
            
    def test_conversation_flow(self):
        """测试完整的对话流程"""
        # 模拟对话
        user_input = "今天天气怎么样"
        bot_response = "今天天气晴朗，适合外出"
        
        # 添加对话记录
        web_server.add_conversation(user_input, bot_response)
        
        # 验证数据库记录
        conversations = self.db.get_conversations(limit=1)
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0]['user_input'], user_input)
        self.assertEqual(conversations[0]['bot_response'], bot_response)
        
    def test_web_api(self):
        """测试Web API"""
        import requests
        
        # 测试获取对话历史
        response = requests.get('http://localhost:5001/api/conversations')
        self.assertEqual(response.status_code, 200)
        
        # 测试搜索功能
        response = requests.get('http://localhost:5001/api/search?q=天气')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)

if __name__ == '__main__':
    unittest.main() 