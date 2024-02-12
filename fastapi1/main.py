from contextlib import asynccontextmanager
from http.client import HTTPException
from typing import Optional, List

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

from db import Base, engine, get_session, Session
from models.Alumno import AlumnoDB


class Alumno(BaseModel):
    id: Optional[int]
    name: str
    age: int

    class Config:
        from_attributes = True


# @app.on_event('startup')
# def create_db():
#    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/", response_model=Alumno, status_code=HTTP_201_CREATED)
async def post(alumno: Alumno, session: Session = Depends(get_session)) -> Alumno:
    new_user = AlumnoDB(name=alumno.name, age=alumno.age)
    session.add(new_user)
    session.commit()

    return Alumno.from_orm(new_user)


@app.get("/{alumno_id}", response_model=Alumno)
async def get(alumno_id: int, session: Session = Depends(get_session)) -> Alumno:
    person = session.query(AlumnoDB).filter(AlumnoDB.id == alumno_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Alumno not found")
    else:
        return person


@app.get("/", response_model=List[Alumno])
async def get_all(session: Session = Depends(get_session)) -> List[Alumno]:
    alumnos = session.query(AlumnoDB).all()
    return alumnos


@app.put("/{alumno_id}", response_model=Alumno)
async def put(alumno_id: int, alumno: Alumno, session: Session = Depends(get_session)) -> Alumno:
    existing_alumno = session.query(AlumnoDB).filter(AlumnoDB.id == alumno_id).first()
    if existing_alumno is None:
        raise HTTPException(status_code=404, detail="Alumno not found")
    existing_alumno.name = alumno.name
    existing_alumno.age = alumno.age
    session.commit()
    return existing_alumno

@app.delete("/{alumno_id}")
async def delete(alumno_id: int, session: Session = Depends(get_session)):
    existing_alumno = session.query(AlumnoDB).filter(AlumnoDB.id == alumno_id).first()
    if existing_alumno is None:
        raise HTTPException(status_code=404, detail="Alumno not found")
    session.delete(existing_alumno)
    session.commit()
    return {"message": "Borrao"}