from app.services.document_service import DocumentService
from app.services.llm_service import LLMService
from app.models.schema import DocumentInput, QueryInput, QueryOutput, DocumentOutput
from typing import List, Dict, Any


class RAGService:
    """RAG服务"""

    def __init__(self):
        self.document_service = DocumentService()
        self.llm_service = LLMService()

    def add_document(self, document_input: DocumentInput) -> Dict[str, Any]:
        """添加文档到知识库"""
        # 处理文档
        documents = self.document_service.process_text(
            document_input.content, 
            document_input.metadata
        )
        
        # 添加文档到向量存储
        ids = self.document_service.add_documents(documents)
        
        return {
            "message": f"成功添加了 {len(ids)} 个文档块",
            "document_ids": ids
        }

    def query(self, query_input: QueryInput) -> QueryOutput:
        """处理用户查询"""
        # 搜索相关文档
        documents = self.document_service.search_documents(
            query_input.query,
            top_k=query_input.top_k
        )
        
        # 生成回答
        answer = self.llm_service.generate_answer(
            query_input.query,
            documents
        )
        
        # 准备输出
        source_docs = [
            DocumentOutput(
                content=doc["content"],
                metadata=doc["metadata"],
                score=doc["score"]
            )
            for doc in documents
        ]
        
        return QueryOutput(
            query=query_input.query,
            answer=answer,
            sources=source_docs
        ) 