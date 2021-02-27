from datetime import datetime
import os

import sqlalchemy


def run():
    db = DB()

    db.init_metadata()
    db.add_base_data()
    db.show_funny_posts()
    db.update_lol_post()
    db.delete_less_funny_post()


class DB:
    engine = None
    db_conn_string = None
    db_path = None
    db_metadata = None
    posts_table = None

    def __init__(self):
        DB.init_engine()

    @staticmethod
    def init_engine():
        if DB.engine is not None:
            return

        DB.db_path = os.path.abspath("data/blog.sqlite_db")
        DB.db_conn_string = "sqlite:///{0}".format(DB.db_path).replace("\\", "/")  # yes, even on Windows.

        print(DB.db_conn_string)
        DB.engine = sqlalchemy.create_engine(DB.db_conn_string, echo=True)

    @staticmethod
    def init_metadata():
        if DB.db_metadata:
            return

        DB.db_metadata = sqlalchemy.MetaData(bind=DB.engine)

        # Posts table definition (via core):
        DB.posts_table = sqlalchemy.Table(
            'Posts', DB.db_metadata,
            sqlalchemy.Column('ID', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('Title', sqlalchemy.String, nullable=False),
            sqlalchemy.Column('Content', sqlalchemy.String, nullable=True),
            sqlalchemy.Column('Published', sqlalchemy.DateTime, nullable=False, default=datetime.now),
        )

        DB.db_metadata.create_all()

    @staticmethod
    def add_base_data():
        posts = DB.posts_table

        with DB.engine.connect() as conn:
            cnt = conn.execute(sqlalchemy.select([sqlalchemy.func.count()]).select_from("Posts")).fetchone()[0]
            if cnt:
                print("data already inserted, exiting")
                return

        statement = posts.insert().values(Title="First post", Content="Content of first post")
        print("To run: {0}".format(statement))

        with DB.engine.connect() as conn:
            conn.execute(statement)
            conn.execute(posts.insert().values(Title="Second post", Content="Content of second post"))
            conn.execute(posts.insert().values(Title="Funny post", Content="This will make you laugh"))
            conn.execute(posts.insert().values(Title="Totally funny post", Content="This will make you laugh LOL"))

    @staticmethod
    def show_funny_posts():
        posts = DB.posts_table
        statement = posts.select() \
            .where(posts.c.Title.like('%Funny%'))

        with DB.engine.connect() as conn:
            res = conn.execute(statement)
            for p in res:
                print(p)

    @staticmethod
    def update_lol_post():
        posts = DB.posts_table
        statement = posts.update() \
            .where(posts.c.Title == "Totally funny post") \
            .values(Content="This will make you LOL!")

        with DB.engine.connect() as conn:
            conn.execute(statement)

    @staticmethod
    def delete_less_funny_post():
        posts = DB.posts_table
        statement = posts.delete() \
            .where(posts.c.Title == "Funny post")

        with DB.engine.connect() as conn:
            conn.execute(statement)

