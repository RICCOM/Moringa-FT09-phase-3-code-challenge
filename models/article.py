from database.connection import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None, author=None, magazine=None):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        if author and magazine and title:
            self.create_article(author, magazine)

    def create_article(self, author, magazine):
        self._author_id = author.id
        self._magazine_id = magazine.id
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                       (self._title, self._content, self._author_id, self._magazine_id))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise AttributeError("Cannot change the title after it is set.")

    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?
        """, (self._id,))
        author = cursor.fetchone()
        conn.close()
        return Author(*author) if author else None

    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        """, (self._id,))
        magazine = cursor.fetchone()
        conn.close()
        return Magazine(*magazine) if magazine else None

    def __repr__(self):
        return f'<Article {self._title}>'
