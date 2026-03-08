"""
初始化标签数据

@author LiuHuiYu
"""
from sqlalchemy.orm import Session
from models import Tag, engine, SessionLocal

def init_tags():
    """初始化一些常用标签"""
    db = SessionLocal()
    try:
        # 定义常用标签
        tags_data = [
            {"name": "做饭", "color": "#3498db"},
            {"name": "烤箱", "color": "#e74c3c"},
            {"name": "红薯", "color": "#f39c12"},
            {"name": "生活", "color": "#2ecc71"},
            {"name": "食谱", "color": "#9b59b6"},
            {"name": "技巧", "color": "#1abc9c"},
            {"name": "健康", "color": "#e67e22"},
            {"name": "美食", "color": "#34495e"},
        ]
        
        for tag_data in tags_data:
            # 检查是否已存在
            existing = db.query(Tag).filter_by(name=tag_data["name"]).first()
            if not existing:
                tag = Tag(**tag_data)
                db.add(tag)
                print(f"创建标签：{tag_data['name']}")
        
        db.commit()
        print("标签初始化完成!")
        
        # 显示所有标签
        all_tags = db.query(Tag).all()
        print(f"\n数据库中共有 {len(all_tags)} 个标签:")
        for tag in all_tags:
            print(f"  - {tag.name} (#{tag.color})")
            
    except Exception as e:
        print(f"初始化失败：{e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_tags()
