from pydantic import BaseModel


class MangaListSchema(BaseModel):
    id: int
    en_name: str
    ru_name: str
    dir: str
    image: str
    desciption: str
    issue_date: str
    likes: int
    views: int
    rating: int
    chapters_quantity: int
    genre_id: int
