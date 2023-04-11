from sqlalchemy import Column, Table, Integer, String, TIMESTAMP, Float, ForeignKey
from sqlalchemy import MetaData

import datetime

metadata = MetaData()

genre = Table(
    "genre",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, unique=True),
    Column("title", String, nullable=False),
)


manga = Table(
    "manga",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("title_id", Integer, nullable=True),
    Column("en_name", String, nullable=False),
    Column("ru_name", String, nullable=False),
    Column("dir", String, nullable=False),
    Column("image", String, nullable=False),
    Column("description", String, nullable=True),
    Column("issue_year", Integer, nullable=False),
    Column("type", String, nullable=False),
    Column("likes", Integer, default=0),
    Column("views", Integer, default=0),
    Column("rating", Float, default=0.0),
    Column("chapters_quantity", Integer, default=0),
    Column("genre_id", ForeignKey("genre.id")),
    Column("created_at", TIMESTAMP, default=datetime.datetime.now()),
)
