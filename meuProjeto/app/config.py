import os


class Config:
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_secreta_super_segura'
   
   # Caminho para o banco SQLite do projeto
   DATABASE_PATH = 'MEUS FILMES PROJETO.db'