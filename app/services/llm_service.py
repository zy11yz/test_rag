from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any
from app.core.config import OPENAI_API_KEY, DEFAULT_MODEL, OPENAI_API_BASE


class LLMService:
    """LLM服务"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=DEFAULT_MODEL,
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_API_BASE,
            temperature=0.2
        )
        self.rag_prompt_template = """
        你是一个基于检索增强的AI助手。你的任务是使用给定的上下文信息来回答用户的问题。
        
        ### 上下文信息:
        {context}
        
        ### 用户问题:
        {query}
        
        ### 指南:
        - 仅使用提供的上下文信息来回答问题
        - 如果上下文中没有足够的信息，请说明无法回答，不要编造答案
        - 保持回答简洁明了
        - 引用相关的具体信息来源
        
        ### 回答:
        """
        
        self.prompt = PromptTemplate(
            template=self.rag_prompt_template,
            input_variables=["context", "query"]
        )

    def generate_answer(self, query: str, documents: List[Dict[str, Any]]) -> str:
        """根据文档生成回答"""
        if not documents:
            return "抱歉，我没有找到相关的信息来回答您的问题。"
        
        # 准备上下文
        context = "\n\n".join([f"文档 {i+1}:\n{doc['content']}" for i, doc in enumerate(documents)])
        
        # 直接使用LLM和提示模板进行预测
        response = self.llm.invoke(
            self.prompt.format(
                context=context,
                query=query
            )
        )
        
        return response.content 