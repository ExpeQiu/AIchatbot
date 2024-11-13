from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    user_input = Column(String, nullable=False)
    bot_response = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_input': self.user_input,
            'bot_response': self.bot_response,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

class DatabaseManager:
    def __init__(self, db_path="data/conversations.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_conversation(self, user_input: str, bot_response: str):
        """添加新对话"""
        conversation = Conversation(
            user_input=user_input,
            bot_response=bot_response
        )
        self.session.add(conversation)
        self.session.commit()
        return conversation.to_dict()
    
    def get_conversations(self, limit: int = 100, offset: int = 0):
        """获取对话历史"""
        conversations = self.session.query(Conversation)\
            .order_by(Conversation.timestamp.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        return [conv.to_dict() for conv in conversations]
    
    def search_conversations(self, query: str):
        """搜索对话"""
        conversations = self.session.query(Conversation)\
            .filter(
                (Conversation.user_input.like(f'%{query}%')) |
                (Conversation.bot_response.like(f'%{query}%'))
            )\
            .order_by(Conversation.timestamp.desc())\
            .all()
        return [conv.to_dict() for conv in conversations] 