class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = id
        self._name = name
        self._category = category
        if name and category:
            self.create_magazine()

    def create_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
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
        if 2 <= len(value) <= 16:
            self._name = value
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (value, self._id))
            conn.commit()
            conn.close()
        else:
            raise ValueError("Name must be between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if len(value) > 0:
            self._category = value
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (value, self._id))
            conn.commit()
            conn.close()
        else:
            raise ValueError("Category must be longer than 0 characters.")

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles WHERE magazine_id = ?
        """, (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(*article) for article in articles]

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(*author) for author in authors]

    def article_titles(self):
        articles = self.articles()
        return [article.title for article in articles] if articles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self._id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(*author) for author in authors] if authors else None

    def __repr__(self):
        return f'<Magazine {self._name}>'
