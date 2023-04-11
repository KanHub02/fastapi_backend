from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    Boolean,
    Float,
    ForeignKey,
    TIMESTAMP,
)
from sqlalchemy import MetaData

import datetime


metadata = MetaData()


category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("is_deleted", Boolean, default=False),
)


product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("price", Float, default=0.0),
    Column("category_id", Integer, ForeignKey(category.c.id)),
    Column("is_deleted", Boolean, default=False),
    Column("created_at", TIMESTAMP, default=datetime.datetime.now()),
)


# cart = Table(
#     "cart",
#     metadata,
# )


# order = Table(
#     "order",
#     metadata,
# )
