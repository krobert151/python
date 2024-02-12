from sqlalchemy import Column, Integer, String

from db import Base


class AlumnoDB(Base):
    __tablename__ = 'alumno'

    id= Column(Integer, primary_key=True, index=True)
    name= Column(String)
    age= Column(Integer)