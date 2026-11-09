from app.database import get_db_cursor

class Movie:
    def __init__(self, id, title, release_year, poster_url, synopsis):
        self.id = id
        self.title = title
        self.release_year = release_year
        self.poster_url = poster_url
        self.synopsis = synopsis

    @classmethod
    def create(cls, title, release_year, poster_url, synopsis):
        """Cadastra um novo filme no banco de dados"""
        sql = """
            INSERT INTO movies (title, release_year, poster_url, synopsis)
            VALUES (?, ?, ?, ?)
        """
        with get_db_cursor() as cursor:
            cursor.execute(sql, (title, release_year, poster_url, synopsis))
            return cursor.lastrowid

    @classmethod
    def find_by_id(cls, movie_id):
        """Busca um filme específico pelo seu ID"""
        sql = "SELECT id, title, release_year, poster_url, synopsis FROM movies WHERE id = ?"
        with get_db_cursor() as cursor:
            cursor.execute(sql, (movie_id,))
            row = cursor.fetchone()
            if row:
                return cls(row['id'], row['title'], row['release_year'], row['poster_url'], row['synopsis'])
        return None

    @classmethod
    def get_all(cls):
        """Retorna todos os filmes"""
        sql = "SELECT id, title, release_year, poster_url, synopsis FROM movies"
        with get_db_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [cls(r['id'], r['title'], r['release_year'], r['poster_url'], r['synopsis']) for r in rows]