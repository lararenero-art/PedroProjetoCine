import sqlite3
from contextlib import contextmanager

DB_FILE = 'MEUS FILMES PROJETO.db'  # Nome do teu ficheiro de base de dados


def init_db():
  """Cria as tabelas no SQLite se não existirem."""
  with get_db_cursor() as cursor:
    # Tabela de Usuários
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    # Tabela de Filmes
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                release_year INTEGER NOT NULL,
                poster_url TEXT,
                synopsis TEXT
            )
        """)

    # Tabela de Avaliações
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_id INTEGER NOT NULL,
                rating REAL NOT NULL,
                is_fresh INTEGER NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE
            )
        """)


@contextmanager
def get_db_cursor():
  """Context Manager: abre conexão com o SQLite, executa o SQL e fecha sozinho."""
  conn = sqlite3.connect(DB_FILE)
  conn.row_factory = sqlite3.Row  # Permite aceder colunas pelo nome
  cursor = conn.cursor()
  try:
    yield cursor
    conn.commit()
  except Exception as e:
    conn.rollback()
    raise e
  finally:
    cursor.close()
    conn.close()