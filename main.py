from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from models import Recinto, RecintoCreate, RecintoUpdate, Evento, EventoCreate, EventoUpdate
from database import get_db

app = FastAPI()

@app.get("/recintos")
async def get_recintos(db: Session = Depends(get_db)):
    # Recogemos todos los datos y los mostramos
    return db.query(Recinto).all()

@app.post("/recintos/create")
async def post_recintos(recinto: RecintoCreate, db: Session = Depends(get_db)):
    # Rellenamos los campos
    db_recinto = Recinto(
        nombre = recinto.nombre,
        ciudad = recinto.ciudad,
        capacidad = recinto.capacidad
    )
    db.add(db_recinto)
    db.commit()
    db.refresh(db_recinto)
    return db_recinto

@app.put("/recintos/update/{recinto_id}")
async def put_recintos(recinto_id: int, recinto_update: RecintoUpdate, db: Session = Depends(get_db)):
    # Buscamos al recinto en la base de datos
    db_recinto = db.query(Recinto).filter(Recinto.id == recinto_id).first()

    if not db_recinto:
        # Lanzamos un error si no existe el recinto
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    
    # Excluimos los datos que estén en blanco
    actualizar_datos = recinto_update.model_dump(exclude_unset=True)

    for clave, valor in actualizar_datos.items():
        # Actualizamos los cambios
        setattr(db_recinto, clave, valor)

    db.commit()
    db.refresh(db_recinto)
    return db_recinto

@app.delete("/recintos/delete/{recinto_id}")
async def delete_recintos(recinto_id: int, db: Session = Depends(get_db)):
    # Buscamos al recinto en la base de datos
    db_recinto = db.query(Recinto).filter(Recinto.id == recinto_id).first()

    if not db_recinto:
        # Lanzamos un error si no existe el recinto
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    
    db.delete(db_recinto)
    db.commit()
    return {"detail": "Recinto eliminado correctamente"}

@app.get("/eventos")
async def get_eventos(evento_ciudad: Optional[str] = None, db: Session = Depends(get_db)):
    ''' Recogemos todos los recintos o, si se pasa una ciudad, recogemos los 
    recintos que estén en esa ciudad'''
    query = db.query(Evento)
    
    if evento_ciudad:
        # Recogemos los recintos según la ciudad, si esta se ha enviado
        query = query.join(Evento.recinto).filter(Recinto.ciudad.ilike(f"%{evento_ciudad}%"))
    
    return query.all()

@app.post("/eventos")
async def post_eventos(evento: EventoCreate, db: Session = Depends(get_db)):
    # Rellenamos los campos
    db_evento = Evento(
        nombre = evento.nombre,
        fecha = evento.fecha,
        precio = evento.precio,
        tickets_vendidos = evento.tickets_vendidos,
        recinto_id = evento.recinto_id
    )
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

@app.patch("/eventos/{evento_id}/comprar")
async def patch_eventos(cantidad: int, evento_id: int, db: Session = Depends(get_db)):
    # Buscamos al evento en la base de datos
    db_evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not db_evento:
        # Lanzamos un error si no existe el evento
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    if cantidad < 0:
        # Lanzamos un error si la cantidad es negativa
        raise HTTPException(status_code=400, detail="No se pueden vender un número negativo de entradas")
    elif cantidad + db_evento.tickets_vendidos > db_evento.recinto.capacidad:
        # Lanzamos un error si el total de los tickets vendidos superan la capacidad del recinto
        raise HTTPException(status_code=400, detail="No se pueden vender más entradas que la capacidad disponible")
    else:    
        db_evento.tickets_vendidos += cantidad
    
    db.commit()
    db.refresh(db_evento)
    return db_evento

@app.put("/eventos/{evento_id}")
async def put_eventos(evento_id: int, evento_update: EventoUpdate, db: Session = Depends(get_db)):
    # Buscamos al evento en la base de datos
    db_evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not db_evento:
        # Lanzamos un error si no existe el evento
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    # Excluimos los datos que estén en blanco
    actualizar_datos = evento_update.model_dump(exclude_unset=True)

    for clave, valor in actualizar_datos.items():
        # Actualizamos los datos
        setattr(db_evento, clave, valor)
    
    db.commit()
    db.refresh(db_evento)
    return db_evento

@app.delete("/eventos/{evento_id}")
async def delete_eventos(evento_id: int, db: Session = Depends(get_db)):

    # Buscamos al evento en la base de datos
    db_evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not db_evento:
        # Lanzamos un error si no existe el evento
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    db.delete(db_evento)
    db.commit()
    return {"detail": "Evento eliminado correctamente"}
