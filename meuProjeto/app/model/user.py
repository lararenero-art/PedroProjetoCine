from app.database import get_db_cursor
from werkzeug.security import check_password_hash, generate_password_hash


class User:

  def __init__(self, id, username, email, password_hash):
    self.id = id
    self.username = username
    self.email = email
    self.password_hash = password_hash

  @classmethod
  def create(cls, username, email, password):
    """Cadastra um novo usuário no SQLite"""
    password_hash = generate_password_hash(password)
    sql = """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """
    try:
      with get_db_cursor() as cursor:
        cursor.execute(sql, (username, email, password_hash))
        user_id = cursor.lastrowid
        return cls(user_id, username, email, password_hash)
    except Exception:
      return None  # Trata e-mail ou username duplicado

  @classmethod
  def find_by_email(cls, email):
    """Busca usuário por e-mail"""
    sql = 'SELECT id, username, email, password_hash FROM users WHERE email = ?'
    with get_db_cursor() as cursor:
      cursor.execute(sql, (email,))
      row = cursor.fetchone()
      if row:
        return cls(row['id'], row['username'], row['email'], row['password_hash'])
    return None

  @classmethod
  def find_by_id(cls, user_id):
    """Busca usuário por ID"""
    sql = 'SELECT id, username, email, password_hash FROM users WHERE id = ?'
    with get_db_cursor() as cursor:
      cursor.execute(sql, (user_id,))
      row = cursor.fetchone()
      if row:
        return cls(row['id'], row['username'], row['email'], row['password_hash'])
    return None

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)