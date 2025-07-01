
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models import User
from db import get_db

router = APIRouter(prefix="/api/v1")
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # 查询用户
    user = db.query(User).filter(User.nick_name == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="账号或密码错误")
    return {"message": "登录成功", "username": username}

