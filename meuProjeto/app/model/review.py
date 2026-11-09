from app.database import get_db_cursor

class Review:
    def __init__(self, id, user_id, movie_id, rating, is_fresh, content, created_at=None, movie_title=None, poster_url=None, username=None):
        self.id = id
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.is_fresh = is_fresh
        self.content = content
        self.created_at = created_at
        # Atributos extras vindos de JOINs
        self.movie_title = movie_title
        self.poster_url = poster_url
        self.username = username

    @classmethod
    def create(cls, user_id, movie_id, rating, is_fresh, content):
        """Cria uma nova avaliação de filme"""
        sql = """
            INSERT INTO reviews (user_id, movie_id, rating, is_fresh, content)
            VALUES (?, ?, ?, ?, ?)
        """
        with get_db_cursor() as cursor:
            cursor.execute(sql, (user_id, movie_id, rating, is_fresh, content))
            return cursor.lastrowid

    @classmethod
    def find_by_user(cls, user_id):
        """Busca toda a 'estante' do utilizador (com dados do filme gravado)"""
        sql = """
            SELECT r.*, m.title as movie_title, m.poster_url 
            FROM reviews r
            JOIN movies m ON r.movie_id = m.id
            WHERE r.user_id = ?
            ORDER BY r.created_at DESC
        """
        with get_db_cursor() as cursor:
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            return [
                cls(
                    id=r['id'], user_id=r['user_id'], movie_id=r['movie_id'],
                    rating=r['rating'], is_fresh=r['is_fresh'], content=r['content'],
                    created_at=r['created_at'], movie_title=r['movie_title'], poster_url=r['poster_url']
                ) for r in rows
            ]