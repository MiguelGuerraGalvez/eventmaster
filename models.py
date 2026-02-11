from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from typing import Optional
from database import Base
from datetime import datetime


class Recinto(Base):
    # Modelo de la tabla 'recintos' de la base de datos
    __tablename__ = "recintos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ciudad = Column(String)
    capacidad = Column(Integer)
    eventos = relationship("Evento", back_populates="recinto")

class RecintoBase(BaseModel):
    # Modelo base para la creación y actualización de recintos
    nombre: str
    ciudad: str
    # Hacemos que mínimo la capacidad sea 1
    capacidad: int = Field(..., gt=0, description="Debe haber capacidad para alguna persona")

class RecintoCreate(RecintoBase):
    # Modelo para la creación de nuevos recintos
    id: Optional[int] = None

class RecintoUpdate(RecintoBase):
    # Modelo para la actualización de los recintos
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    # Hacemos que mínimo la capacidad sea 1
    capacidad: Optional[int] = Field(None, gt=0, description="Debe haber capacidad para alguna persona")

class RecintoResponse(RecintoBase):
    # Modelo para enviar la información del recinto al cliente
    id: int
    class Config:
        from_attributes = True

class Evento(Base):
    # Modelo de la tabla 'eventos' de la base de datos
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    fecha = Column(DateTime)
    precio = Column(Float)
    tickets_vendidos = Column(Integer, default=0)
    recinto_id = Column(Integer, ForeignKey("recintos.id"))
    recinto = relationship("Recinto", back_populates="eventos")

class EventoBase(BaseModel):
    # Modelo base para la creación y actualización de eventos
    nombre: str
    fecha: datetime
    # Hacemos que el precio sea mínimo 0
    precio: float = Field(..., ge=0, description="El precio debe ser positivo")
    # Hacemos que los tickets_vendidos sean mínimo 0
    tickets_vendidos: int = Field(..., ge=0, description="Debe haber mínimo 0 tickets vendidos")
    recinto_id: int

class EventoCreate(EventoBase):
    # Modelo para la creación de eventos
    id: Optional[int] = None

class EventoUpdate(EventoBase):
    # Modelo para la actualización de eventos
    nombre: Optional[str] = None
    fecha: Optional[datetime] = None
    # Hacemos que el precio sea mínimo 0
    precio: Optional[float] = Field(None, ge=0, description="El precio debe ser positivo")
    # Hacemos que los tickets vendidos sean mínimo 0
    tickets_vendidos: Optional[int] = Field(None, ge=0, description="Debe haber mínimo 0 tickets vendidos")
    recinto_id: Optional[int] = None
