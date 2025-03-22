from fastapi import APIRouter, HTTPException
from app.models.schema import DocumentInput, QueryInput, QueryOutput
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()


@router.post("/documents", status_code=201)
async def add_document(document: DocumentInput):
    """添加文档到知识库"""
    try:
        result = rag_service.add_document(document)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加文档失败: {str(e)}")


@router.post("/query", response_model=QueryOutput)
async def query(query_input: QueryInput):
    """处理查询并返回回答"""
    try:
        response = rag_service.query(query_input)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询处理失败: {str(e)}")


@router.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok"} 