from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from products.routers import router as product_router
from manga.routers import router as manga_router
from chatai.routers import router as chatai_router
from chatai.views import router as chat_template_router

from fastapi_pagination import add_pagination


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


app.include_router(product_router)
app.include_router(manga_router)
app.include_router(chatai_router)
app.include_router(chat_template_router)

add_pagination(app)
