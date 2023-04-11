import requests
from sqlalchemy import insert, select, update
from pprint import pprint

from database import get_async_session
from manga.models import manga, genre
from .common import genreslist

# session = get_async_session


class Parser:
    url = "https://api.remanga.org/api/activity/comments/?title_id=8813&page=2&ordering=&count=20"
    url_comments = "https://api.remanga.org/api/activity/comments/?title_id=8813&page=2&ordering=&count=20"
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    }
    domen = "https://remanga.org"
    media_domen = "https://remanga.org"

    @classmethod
    async def create_data(cls, session):

        for i in genreslist:
            stmt = insert(genre).values(title=i)
            await session.execute(stmt)
            await session.commit()

        for i in range(1, 300):
            url = (
                "https://api.remanga.org/api/titles/recommendations/?&count=20&page="
                + str(i)
            )
            request = requests.get(url=url, headers=cls.HEADERS)
            request_data = request.json()
            for item in request_data["content"]:
                global url2
                url2 = f"https://api.remanga.org/api/titles/" + item["dir"] + "/"
                genre_filter_set = item["genres"]
                data = {
                    "title_id": item["id"],
                    "en_name": item["en_name"],
                    "ru_name": item["rus_name"],
                    "dir": item["dir"],
                    "image": cls.media_domen + item["cover_high"],
                    "type": item["type"],
                    "issue_year": item["issue_year"],
                    "rating": item["avg_rating"],
                    "views": item["total_views"],
                    "likes": item["total_votes"],
                    "chapters_quantity": item["count_chapters"],
                }
                if genre_filter_set is not None:
                    for i in genre_filter_set:
                        global genre_filter_name
                        genre_filter_name = i["name"]
                        manga_genre = select(genre).where(
                            genre.c.title == genre_filter_name
                        )
                        data.update({"genre_id": genre_filter_name})

                stmt = insert(manga).values(**data)
                await session.execute(stmt)
                await session.commit()

                detail_request = requests.get(url=url2, headers=cls.HEADERS)
                detail_data = detail_request.json()
                try:
                    created_manga = select(manga).where(
                        manga.c.dir == detail_data["content"]["dir"]
                    )
                    result = await session.execute(created_manga)

                except:
                    continue

                # for m in result:
                #     pprint(m)
                #     description = detail_data["content"]["dir"]
                #     stmt = (
                #         update(manga)
                #         .where(manga.c.en_name == m)
                #         .values(description=description)
                #     )
                #     await session.execute(stmt)
                #     await session.commit()


if __name__ == "__main__":
    Parser.create_data()
