from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, inspect, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
import os

# Configuração do Banco de Dados SQLite
diretorio_principal = os.path.abspath(os.path.dirname(__file__))
URL_DATABASE= f"sqlite:///{os.path.join(diretorio_principal, 'users.db')}"
motor = create_engine(URL_DATABASE)
Base = declarative_base()

# Define SessionLocal como uma função de fábrica para criar sessões locais
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

app = FastAPI()

metadados = MetaData()
metadados.bind = motor  # Associa metadados ao motor

def tabela_existe(metadados, nome_tabela):
    inspetor = inspect(metadados.bind)
    return nome_tabela in inspetor.get_table_names()

# Verifica se a tabela 'users' está criada
if not tabela_existe(metadados, "users"):
    # Tabela não criada, cria-a
    users = Table(
        "users",
        metadados,
        Column("id", Integer, primary_key=True, index=True),
        Column("name", String),
        Column("email", String, unique=True, index=True),
        Column("hashed_password", String), 
    )
    # Cria a tabela
    metadados.create_all(bind=motor)
    print("Tabela 'users' criada com sucesso")
else:
    print("Tabela 'users' já existe")

# Dependência para obter a sessão do banco de dados
def obter_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2PasswordBearer para manipulação de autenticação de token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Hashing de senha
contexto_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo Pydantic para o Usuário
class Usuario(BaseModel):
    name: str
    email: str
    password: str  

# Modelo ORM para o Usuário armazenado no banco de dados
class UsuarioNoBD(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hashed = Column(String) 

# Dependência para verificar a senha
def verificar_senha(senha_plana, password_hashed):
    return contexto_pwd.verify(senha_plana, password_hashed)

# Endpoints FastAPI
@app.post("/register")
def registrar_usuario(usuario: Usuario, request: Request, db: Session = Depends(obter_db)):
    print("Dados recebidos no endpoint /register:", request.json())
    password_hashed = contexto_pwd.hash(usuario.password)
    db_usuario = UsuarioNoBD(name=usuario.name, email=usuario.email, password_hashed=password_hashed)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return {"mensagem": "Usuário registrado com sucesso"}

@app.post("/login")
def login_usuario(usuario: Usuario, request: Request, db: Session = Depends(obter_db)):
    print("Dados recebidos no endpoint /login:", request.json())
    db_user = db.query(UsuarioNoBD).filter(UsuarioNoBD.email == usuario.email).first()
    if not db_user or not verificar_senha(usuario.password, db_user.password_hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos")
    return db_user.name