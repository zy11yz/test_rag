from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from app.core.config import OPENAI_API_KEY, OPENAI_API_BASE, CHROMA_DB_DIR, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL


class DocumentService:
    """文档处理服务"""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_API_BASE
        )
        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_DB_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        # 创建或获取集合
        self.collection = self.chroma_client.get_or_create_collection("documents")

    def process_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """处理文本并返回文档块"""
        if metadata is None:
            metadata = {}
        
        # 分割文本
        texts = self.text_splitter.split_text(text)
        
        # 创建文档对象
        documents = [
            Document(page_content=t, metadata=metadata) 
            for t in texts
        ]
        
        return documents

    def add_documents(self, documents: List[Document]) -> List[str]:
        """将文档添加到向量存储"""
        # 获取文档内容和元数据
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # 生成嵌入并添加到集合
        embeddings = self.embeddings.embed_documents(texts)
        
        # 生成ID
        ids = [f"doc_{i}" for i in range(self.collection.count(), self.collection.count() + len(texts))]
        
        # 添加到集合
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids

    def search_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        # 计算查询嵌入
        query_embedding = self.embeddings.embed_query(query)
        
        # 搜索相似文档
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # 格式化结果
        documents = []
        if results["documents"]:
            for i, content in enumerate(results["documents"][0]):
                documents.append({
                    "content": content,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": results["distances"][0][i] if results["distances"] else None
                })
            
        return documents 