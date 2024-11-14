import unittest
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.conversation import DatabaseManager
from src.utils.db_init import init_database
from src.utils.db_manager import DBUtils

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """测试前初始化"""
        # 使用测试数据库
        self.test_db_path = "data/test_conversations.db"
        self.db = DatabaseManager(self.test_db_path)
        
    def tearDown(self):
        """测试后清理"""
        # 删除测试数据库
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
    def test_database_init(self):
        """测试数据库初始化"""
        self.assertTrue(init_database())
        self.assertTrue(os.path.exists("data/conversations.db"))
        
    def test_add_conversation(self):
        """测试添加对话"""
        # 添加测试对话
        conv = self.db.add_conversation(
            user_input="你好",
            bot_response="你好，我是小明"
        )
        
        # 验证返回的对话数据
        self.assertIsNotNone(conv)
        self.assertEqual(conv['user_input'], "你好")
        self.assertEqual(conv['bot_response'], "你好，我是小明")
        
    def test_get_conversations(self):
        """测试获取对话历史"""
        # 添加多条测试对话
        test_conversations = [
            ("你好", "你好，我是小明"),
            ("今天天气怎么样", "今天天气晴朗"),
            ("再见", "再见，欢迎下次再来")
        ]
        
        for user_input, bot_response in test_conversations:
            self.db.add_conversation(user_input, bot_response)
            
        # 测试获取所有对话
        conversations = self.db.get_conversations(limit=10)
        self.assertEqual(len(conversations), 3)
        
        # 测试分页
        conversations = self.db.get_conversations(limit=2)
        self.assertEqual(len(conversations), 2)
        
    def test_search_conversations(self):
        """测试搜索对话"""
        # 添加测试数据
        test_conversations = [
            ("今天天气真好", "是的，天气晴朗"),
            ("推荐附近的餐厅", "这里有几家不错的餐厅"),
            ("明天会下雨吗", "明天可能会下雨")
        ]
        
        for user_input, bot_response in test_conversations:
            self.db.add_conversation(user_input, bot_response)
            
        # 测试搜索
        results = self.db.search_conversations("天气")
        self.assertEqual(len(results), 2)  # 应该找到2条包含"天气"的对话
        
        results = self.db.search_conversations("餐厅")
        self.assertEqual(len(results), 1)  # 应该找到1条包含"餐厅"的对话

class TestDatabaseUtils(unittest.TestCase):
    def setUp(self):
        """测试前初始化"""
        self.test_backup_path = "data/test_backup"
        os.makedirs(self.test_backup_path, exist_ok=True)
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.test_backup_path):
            shutil.rmtree(self.test_backup_path)
            
    def test_backup_restore(self):
        """测试备份和恢复功能"""
        # 创建测试数据
        db = DatabaseManager()
        db.add_conversation("测试备份", "这是一条测试数据")
        
        # 测试备份
        self.assertTrue(DBUtils.backup_database(self.test_backup_path))
        backup_file = os.path.join(self.test_backup_path, "conversations_backup.json")
        self.assertTrue(os.path.exists(backup_file))
        
        # 测试恢复
        self.assertTrue(DBUtils.restore_database(backup_file))

if __name__ == '__main__':
    unittest.main() 