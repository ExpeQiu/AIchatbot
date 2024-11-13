from ..models.conversation import DatabaseManager
import json
import os

class DBUtils:
    @staticmethod
    def backup_database(backup_path="data/backup"):
        """备份数据库"""
        try:
            os.makedirs(backup_path, exist_ok=True)
            db = DatabaseManager()
            conversations = db.get_conversations(limit=None)  # 获取所有对话
            
            # 保存为JSON文件
            backup_file = os.path.join(backup_path, "conversations_backup.json")
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, ensure_ascii=False, indent=2)
                
            print(f"数据库备份成功: {backup_file}")
            return True
            
        except Exception as e:
            print(f"数据库备份失败: {e}")
            return False
    
    @staticmethod
    def restore_database(backup_file="data/backup/conversations_backup.json"):
        """从备份恢复数据库"""
        try:
            if not os.path.exists(backup_file):
                print(f"备份文件不存在: {backup_file}")
                return False
                
            db = DatabaseManager()
            
            # 读取备份文件
            with open(backup_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
            
            # 恢复对话记录
            for conv in conversations:
                db.add_conversation(
                    user_input=conv['user_input'],
                    bot_response=conv['bot_response']
                )
                
            print("数据库恢复成功！")
            return True
            
        except Exception as e:
            print(f"数据库恢复失败: {e}")
            return False 