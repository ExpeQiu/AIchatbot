from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from typing import Dict, List, Tuple
import os

class KnowledgeBase:
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        self.model = SentenceTransformer(model_name)
        self.faiss_index = None
        self.qa_pairs: List[Dict] = []
        self.vector_dimension = 384  # 根据模型调整维度
        
        # 初始化FAISS索引
        self.faiss_index = faiss.IndexFlatL2(self.vector_dimension)
        
        # 加载预定义的问答对
        self.load_qa_pairs()
    
    def load_qa_pairs(self, qa_file: str = "data/qa_pairs.json"):
        """加载预定义的问答对"""
        if not os.path.exists(qa_file):
            print(f"QA文件 {qa_file} 不存在，创建空的知识库")
            self.save_qa_pairs(qa_file)
            return

        try:
            with open(qa_file, 'r', encoding='utf-8') as f:
                self.qa_pairs = json.load(f)
                
            # 将问题转换为向量并添加到索引中
            if self.qa_pairs:
                questions = [qa['question'] for qa in self.qa_pairs]
                vectors = self.model.encode(questions)
                self.faiss_index.add(vectors.astype(np.float32))
                
        except Exception as e:
            print(f"加载QA对时出错: {e}")
            self.qa_pairs = []
    
    def save_qa_pairs(self, qa_file: str = "data/qa_pairs.json"):
        """保存问答对到文件"""
        os.makedirs(os.path.dirname(qa_file), exist_ok=True)
        with open(qa_file, 'w', encoding='utf-8') as f:
            json.dump(self.qa_pairs, f, ensure_ascii=False, indent=2)
    
    def add_qa_pair(self, question: str, answer: str):
        """添加新的问答对"""
        # 添加到问答对列表
        self.qa_pairs.append({
            'question': question,
            'answer': answer
        })
        
        # 添加到FAISS索引
        vector = self.model.encode([question])[0]
        self.faiss_index.add(np.array([vector]).astype(np.float32))
        
        # 保存更新后的问答对
        self.save_qa_pairs()
    
    def find_similar_question(self, query: str, threshold: float = 0.8) -> Tuple[str, str, float]:
        """查找最相似的问题及其答案"""
        # 将查询转换为向量
        query_vector = self.model.encode([query])[0].astype(np.float32)
        
        # 搜索最相似的问题
        distances, indices = self.faiss_index.search(
            np.array([query_vector]), 
            1  # 只获取最相似的一个结果
        )
        
        # 如果没有找到结果或相似度低于阈值
        if len(indices) == 0 or distances[0][0] > threshold:
            return None, None, 0.0
            
        # 返回最相似的问题和答案
        qa_pair = self.qa_pairs[indices[0][0]]
        similarity = 1 - (distances[0][0] / 2)  # 转换距离为相似度
        return qa_pair['question'], qa_pair['answer'], similarity 