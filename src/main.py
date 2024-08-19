import uvicorn
from db import create_tables, get_db
from sqlmodel import Session, select
from models import Cliente, ClienteIn, MessageResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status


app = FastAPI(
    title='Cliente API', 
    description='Api para gerenciar clientes.'
)


@app.get('/clientes')
async def find_all_costumers(db: Session = Depends(get_db)) -> list[Cliente]:
    query = select(Cliente)
    return db.exec(query).all()


@app.get('/clientes/{id}')
async def find_costumer_by_id(id: int, db: Session = Depends(get_db)) -> Cliente:
    query = select(Cliente).where(Cliente.id == id)
    costumer = db.exec(query).first()

    if costumer is None:
        raise HTTPException(
            detail="Cliente não encontrado", 
            status_code=status.HTTP_404_NOT_FOUND
        )

    return costumer


@app.post('/clientes', status_code=status.HTTP_201_CREATED)
async def create_new_costumer(
    costumer_data: ClienteIn, 
    db: Session = Depends(get_db)
) -> MessageResponse:
    try:
        costumer = Cliente(**costumer_data.model_dump())
        db.add(costumer)
        db.commit()
    except:
        raise HTTPException(
            detail='Houve um erro ao cadastrar cliente.',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return MessageResponse(detail='Cliente cadastrado com sucesso.')


@app.put('/clientes/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_costumer(
    id: int, 
    costumer_data: ClienteIn, 
    db: Session = Depends(get_db)
) -> MessageResponse:
    query = select(Cliente).where(Cliente.id == id)
    costumer = db.exec(query).first()

    if costumer is None:
        raise HTTPException(
            detail="Cliente não encontrado", 
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    try:
        costumer.nome = costumer_data.nome
        costumer.email = costumer_data.email
        costumer.endereco = costumer_data.endereco

        db.commit()
    except:
        raise HTTPException(
            detail='Houve um erro ao editar cliente.',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return MessageResponse(detail='Cliente editado com sucesso.')


@app.delete('/clientes/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_costumer(id: int, db: Session = Depends(get_db)) -> MessageResponse:
    query = select(Cliente).where(Cliente.id == id)
    costumer = db.exec(query).first()

    if costumer is None:
        raise HTTPException(
            detail="Cliente não encontrado", 
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    try:
        db.delete(costumer)
        db.commit()
    except:
        raise HTTPException(
            detail='Houve um erro ao excluir cliente.',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return MessageResponse(detail='Cliente excluido com sucesso.')


# Cors Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    create_tables()
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
