from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from database import get_db, engine
from datetime import datetime
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class SGToDos(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

class SCToDo(BaseModel):
    title: str
    description: str

@app.get("/to_dos")
def get_to_dos(db: Session = Depends(get_db)) -> List[SGToDos]:
    to_dos = select(models.ToDo)
    result = db.execute(to_dos)
    result = result.scalars().all()
    return result

@app.post("/to_dos")
def create_to_do(data:SCToDo,db: Session = Depends(get_db)):
    to_do = models.ToDo(**data.dict())
    db.add(to_do)
    # db.add_all([to_do])
    db.commit()


@app.delete('/to_do/{to_do_id}')
def delete_to_do(to_do_id:int,db:Session = Depends(get_db)):
    query = select(models.ToDo).filter_by(id=to_do_id)
    to_do = db.execute(query)
    to_do = to_do.scalar_one_or_none()
    if to_do is None:
        raise HTTPException(status_code=404,detail='not found to_do with this id')
    db.delete(to_do)
    db.commit()
    return 'deleted'


@app.patch('/to_do/{to_do_id}')
def update_to_do(to_do_id:int,data:SCToDo,db:Session=Depends(get_db)):
    query = select(models.ToDo).filter_by(id=to_do_id)
    to_do = db.execute(query)
    to_do = to_do.scalar_one_or_none()
    if to_do is None:
        raise HTTPException(status_code=404,detail='not found to_do with this id')
    to_do.title = data.title
    to_do.description = data.description
    db.commit()
    db.refresh(to_do)
    return to_do