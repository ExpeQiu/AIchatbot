import openai
from config import *
from .knowledge_base import KnowledgeBase
from .location_service import LocationService
import re

class APIClient:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.knowledge_base = KnowledgeBase()
        self.location_service = LocationService()
        
    def is_location_query(self, text: str) -> bool:
        """判断是否是位置查询"""
        location_keywords = [
            "附近", "哪里有", "推荐", "地方", "好吃的", "餐厅",
            "美食", "小吃", "在哪", "怎么去", "地址"
        ]
        return any(keyword in text for keyword in location_keywords)
    
    def get_ai_response(self, text: str) -> str:
        """获取回答，根据问题类型选择不同的处理方式"""
        try:
            # 检查是否是位置查询
            if self.is_location_query(text):
                # 提取查询关键词
                search_query = text.replace("附近", "").replace("推荐", "").replace("哪里有", "")
                if "美食" not in search_query and "好吃" in text:
                    search_query += "美食"
                
                # 搜索附近地点
                places = self.location_service.search_nearby_places(search_query)
                if places:
                    return self.location_service.format_response(places)
            
            # 非位置查询，按原有逻辑处理
            similar_q, answer, similarity = self.knowledge_base.find_similar_question(text)
            
            if answer and similarity >= 0.8:
                print(f"从知识库找到匹配答案 (相似度: {similarity:.2f})")
                print(f"原问题: {similar_q}")
                return answer
            
            print("未找到匹配答案，调用OpenAI API...")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": text}
                ]
            )
            answer = response.choices[0].message.content
            
            # 将新的问答对添加到知识库
            self.knowledge_base.add_qa_pair(text, answer)
            
            print(f"AI回答: {answer}")
            return answer
            
        except Exception as e:
            print(f"获取回答时出错: {e}")
            return "抱歉，我遇到了一些问题。"