"""
图片上传 API

@author LiuHuiYu
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from datetime import datetime

router = APIRouter()

# 图片上传目录
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static", "uploads")

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片文件
    
    - **file**: 图片文件
    """
    # 验证文件类型
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型：{file.content_type}。只支持：{', '.join(allowed_types)}"
        )
    
    # 验证文件大小（10MB）
    file_size = 0
    content = await file.read()
    file_size = len(content)
    if file_size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小不能超过 10MB")
    
    try:
        # 生成唯一文件名
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'png'
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # 按日期组织文件
        date_path = datetime.now().strftime("%Y/%m/%d")
        save_dir = os.path.join(UPLOAD_DIR, date_path)
        os.makedirs(save_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(save_dir, unique_filename)
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 生成访问 URL
        url_path = f"/static/uploads/{date_path}/{unique_filename}"
        
        return JSONResponse({
            "success": True,
            "url": url_path,
            "filename": file.filename,
            "size": file_size,
            "type": file.content_type
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败：{str(e)}")
