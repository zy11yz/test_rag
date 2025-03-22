from pydantic import BaseModel, Field
from typing import List, Optional


class DocumentInput(BaseModel):
    """文档输入模型"""
    content: str = Field(..., description="文档内容")
    metadata: Optional[dict] = Field(default={}, description="文档元数据")


class QueryInput(BaseModel):
    """用户查询输入模型"""
    query: str = Field(..., description="用户问题")
    top_k: int = Field(default=3, description="返回的相关文档数量")


class DocumentOutput(BaseModel):
    """文档输出模型"""
    content: str = Field(..., description="文档内容")
    metadata: dict = Field(default={}, description="文档元数据")
    score: Optional[float] = Field(default=None, description="相关性分数")


class QueryOutput(BaseModel):
    """查询输出模型"""
    query: str = Field(..., description="原始查询")
    answer: str = Field(..., description="生成的回答")
    sources: List[DocumentOutput] = Field(default=[], description="回答的来源文档") 