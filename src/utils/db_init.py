from ..models.conversation import DatabaseManager, Base
from sqlalchemy import create_engine
import os

def init_database():
    """初始化数据库"""
    try:
        # 确保数据目录存在
        os.makedirs("data", exist_ok=True)
        
        # 创建数据库引擎
        engine = create_engine('sqlite:///data/conversations.db')
        
        # 创建所有表
        Base.metadata.create_all(engine)
        
        print("数据库初始化成功！")
        return True
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        return False

if __name__ == "__main__":
    init_database() 