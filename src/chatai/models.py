from sqlalchemy import Table, Column, Integer, String, MetaData, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

import datetime

from scripts.utils import get_random_string
#from src.scripts.utils import get_random_string


metadata = MetaData()


connection = Table(
    "connection",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("code", String, default=get_random_string(), nullable=False),
    Column("ws_code", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.datetime.now()),
)


promt = Table(
    "promt",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.datetime.now()),
)


answer = Table(
    "answer",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.datetime.now()),
)