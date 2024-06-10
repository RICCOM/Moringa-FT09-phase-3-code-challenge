from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self._name = name
        if name:
            self.create_author()

    def create_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot change the author's name after it is set.")

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(*article) for article in articles]

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(*magazine) for magazine in magazines]

    def __repr__(self):
        return f'<Author {self._name}>'
