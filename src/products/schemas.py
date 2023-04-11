from pydantic import BaseModel


class ProductCreateSchema(BaseModel):
    title: str
    description: str
    price: float
