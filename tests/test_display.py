import unittest
from src.display import TkinterDisplay

class TestDisplay(unittest.TestCase):
    def setUp(self):
        self.display = TkinterDisplay()
        
    def test_update_conversation(self):
        self.display.update_conversation("测试消息", True)
        # 验证消息显示
        
    def test_update_status(self):
        self.display.update_status("测试状态")
        # 验证状态更新 