"""
Book API - 交互式书本
基于 Deep Tutor 的 Book 模块
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger("daydayup")

router = APIRouter()


class Book(BaseModel):
    """书本模型"""
    id: str
    title: str
    author: str
    description: str
    cover_image: Optional[str] = None
    chapters: List[Dict[str, Any]]
    total_pages: int
    difficulty: str  # beginner, intermediate, advanced
    category: str
    tags: List[str]
    is_interactive: bool = True
    created_at: str


class Chapter(BaseModel):
    """章节模型"""
    id: str
    book_id: str
    title: str
    content: str
    page_number: int
    exercises: List[Dict[str, Any]]
    notes: List[Dict[str, Any]]
    highlights: List[Dict[str, Any]]


class ReadingProgress(BaseModel):
    """阅读进度"""
    book_id: str
    user_id: str
    current_chapter: int
    current_page: int
    total_reading_time: int  # minutes
    completion_percentage: float
    last_read_at: str
    bookmarks: List[int]
    notes: List[Dict[str, Any]]


# 示例书本
SAMPLE_BOOKS = [
    {
        "id": "book_1",
        "title": "Python 编程入门",
        "author": "AI 导师",
        "description": "从零开始学习 Python 编程，适合初学者的交互式教程",
        "cover_image": "📘",
        "chapters": [
            {"id": "ch_1", "title": "第一章：Python 简介", "page_count": 10},
            {"id": "ch_2", "title": "第二章：基础语法", "page_count": 15},
            {"id": "ch_3", "title": "第三章：数据类型", "page_count": 20},
            {"id": "ch_4", "title": "第四章：控制流程", "page_count": 18},
            {"id": "ch_5", "title": "第五章：函数", "page_count": 22}
        ],
        "total_pages": 85,
        "difficulty": "beginner",
        "category": "编程",
        "tags": ["Python", "编程", "入门"],
        "is_interactive": True,
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "book_2",
        "title": "英语语法精讲",
        "author": "AI 导师",
        "description": "系统学习英语语法，配有大量练习题",
        "cover_image": "📗",
        "chapters": [
            {"id": "ch_1", "title": "第一章：名词", "page_count": 12},
            {"id": "ch_2", "title": "第二章：动词", "page_count": 15},
            {"id": "ch_3", "title": "第三章：形容词和副词", "page_count": 10},
            {"id": "ch_4", "title": "第四章：时态", "page_count": 25},
            {"id": "ch_5", "title": "第五章：从句", "page_count": 20}
        ],
        "total_pages": 82,
        "difficulty": "intermediate",
        "category": "语言",
        "tags": ["英语", "语法", "学习"],
        "is_interactive": True,
        "created_at": "2024-01-01T00:00:00Z"
    }
]


@router.get("/list")
async def get_books():
    """获取书本列表"""
    logger.debug("[Book] Getting book list")
    
    return {
        "books": SAMPLE_BOOKS,
        "total": len(SAMPLE_BOOKS)
    }


@router.get("/{book_id}")
async def get_book(book_id: str):
    """获取书本详情"""
    logger.debug(f"[Book] Getting book: {book_id}")
    
    book = next((b for b in SAMPLE_BOOKS if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book not found: {book_id}")
    
    return book


@router.get("/{book_id}/chapters")
async def get_chapters(book_id: str):
    """获取书本章节"""
    logger.debug(f"[Book] Getting chapters for book: {book_id}")
    
    book = next((b for b in SAMPLE_BOOKS if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book not found: {book_id}")
    
    return {
        "book_id": book_id,
        "chapters": book.get("chapters", [])
    }


@router.get("/{book_id}/chapters/{chapter_id}")
async def get_chapter(book_id: str, chapter_id: str):
    """获取章节内容"""
    logger.debug(f"[Book] Getting chapter {chapter_id} from book {book_id}")
    
    book = next((b for b in SAMPLE_BOOKS if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book not found: {book_id}")
    
    chapter = next((c for c in book.get("chapters", []) if c["id"] == chapter_id), None)
    if not chapter:
        raise HTTPException(status_code=404, detail=f"Chapter not found: {chapter_id}")
    
    # 模拟章节内容
    chapter_content = {
        "id": chapter_id,
        "book_id": book_id,
        "title": chapter["title"],
        "content": f"这是 {chapter['title']} 的内容...\n\n（实际内容会从这里加载）\n\n" + "=" * 50 + "\n\n" * 5,
        "page_number": chapter.get("page_count", 1),
        "exercises": [
            {
                "id": "ex_1",
                "type": "multiple_choice",
                "question": "本节的主要概念是什么？",
                "options": ["选项A", "选项B", "选项C", "选项D"],
                "correct_answer": 0
            },
            {
                "id": "ex_2",
                "type": "fill_blank",
                "question": "请填写空白：_____ 是 Python 的基本数据类型之一。",
                "answer": "字符串"
            }
        ],
        "notes": [],
        "highlights": []
    }
    
    return chapter_content


@router.get("/{book_id}/progress")
async def get_reading_progress(book_id: str, user_id: str = "default"):
    """获取阅读进度"""
    logger.debug(f"[Book] Getting reading progress for book {book_id}, user {user_id}")
    
    book = next((b for b in SAMPLE_BOOKS if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book not found: {book_id}")
    
    # 模拟阅读进度
    return {
        "book_id": book_id,
        "user_id": user_id,
        "current_chapter": 2,
        "current_page": 15,
        "total_reading_time": 120,  # minutes
        "completion_percentage": 25.0,
        "last_read_at": "2024-01-15T10:30:00Z",
        "bookmarks": [5, 12, 18],
        "notes": [
            {
                "id": "note_1",
                "chapter_id": "ch_1",
                "page": 5,
                "content": "这是一个重要的概念",
                "created_at": "2024-01-14T15:00:00Z"
            }
        ]
    }


@router.post("/{book_id}/progress")
async def update_reading_progress(book_id: str, request: Dict[str, Any], user_id: str = "default"):
    """更新阅读进度"""
    logger.info(f"[Book] Updating reading progress for book {book_id}, user {user_id}")
    
    return {
        "success": True,
        "book_id": book_id,
        "progress": {
            "current_chapter": request.get("current_chapter", 1),
            "current_page": request.get("current_page", 1),
            "last_read_at": "2024-01-15T10:30:00Z"
        }
    }


@router.post("/{book_id}/notes")
async def add_note(book_id: str, request: Dict[str, Any], user_id: str = "default"):
    """添加笔记"""
    logger.info(f"[Book] Adding note to book {book_id}")
    
    import uuid
    from datetime import datetime
    
    note = {
        "id": f"note_{uuid.uuid4().hex[:8]}",
        "book_id": book_id,
        "chapter_id": request.get("chapter_id"),
        "page": request.get("page", 1),
        "content": request.get("content", ""),
        "created_at": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "note": note
    }


@router.post("/{book_id}/bookmarks")
async def add_bookmark(book_id: str, request: Dict[str, Any], user_id: str = "default"):
    """添加书签"""
    logger.info(f"[Book] Adding bookmark to book {book_id}, page {request.get('page')}")
    
    return {
        "success": True,
        "book_id": book_id,
        "page": request.get("page"),
        "message": "Bookmark added successfully"
    }


@router.post("/{book_id}/exercises/{exercise_id}/submit")
async def submit_exercise(book_id: str, exercise_id: str, request: Dict[str, Any]):
    """提交练习答案"""
    logger.info(f"[Book] Submitting exercise {exercise_id} for book {book_id}")
    
    answer = request.get("answer")
    
    # 模拟答案检查
    is_correct = True  # 实际应该检查答案
    
    return {
        "success": True,
        "exercise_id": exercise_id,
        "is_correct": is_correct,
        "feedback": "回答正确！" if is_correct else "再试一次，注意理解概念。",
        "explanation": "这里是详细的解释..."
    }


@router.get("/categories")
async def get_categories():
    """获取书本分类"""
    return {
        "categories": [
            {"id": "programming", "name": "编程", "icon": "💻", "count": 15},
            {"id": "language", "name": "语言", "icon": "🌍", "count": 12},
            {"id": "math", "name": "数学", "icon": "🔢", "count": 8},
            {"id": "science", "name": "科学", "icon": "🔬", "count": 10},
            {"id": "history", "name": "历史", "icon": "📜", "count": 6},
            {"id": "art", "name": "艺术", "icon": "🎨", "count": 5}
        ]
    }


@router.get("/recommendations")
async def get_recommendations(user_id: str = "default"):
    """获取推荐书本"""
    return {
        "recommendations": [
            {
                "book_id": "book_1",
                "reason": "基于你的编程学习进度推荐",
                "confidence": 0.95
            },
            {
                "book_id": "book_2",
                "reason": "适合你的英语水平",
                "confidence": 0.88
            }
        ]
    }
