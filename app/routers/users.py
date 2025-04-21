from fastapi import FastAPI, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List
# At the top of your routers/user.py:
import sys
from pathlib import Path
import utils

# This line gets the absolute path to your root directory
ROOT_DIR = Path(__file__).parent.parent  # Goes up one level from 'routers'
sys.path.insert(0, str(ROOT_DIR))
import schemas
import models
from database import engine, get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# routes for users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def createuser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# get users using id
@router.get("/{id}", response_model=schemas.UserResponse)
async def getuser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} was not found")
    return user


