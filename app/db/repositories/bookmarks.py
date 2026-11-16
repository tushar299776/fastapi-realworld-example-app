from typing import List

from asyncpg import Connection

from app.db.queries.queries import queries
from app.db.repositories.articles import ArticlesRepository
from app.models.domain.articles import Article
from app.models.domain.users import User


class BookmarksRepository:
    def __init__(self, conn: Connection) -> None:
        self.connection = conn
        self._articles_repo = ArticlesRepository(conn)

    async def list_user_bookmarks(
        self,
        *,
        user: User,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Article]:
        """Get articles bookmarked by user, with full metadata."""
        articles_rows = await queries.get_bookmarks_for_user(
            self.connection,
            username=user.username,
            limit=limit,
            offset=offset,
        )

        return [
            await self._articles_repo._get_article_from_db_record(
                article_row=article_row,
                slug=article_row["slug"],
                author_username=article_row["author_username"],
                requested_user=user,
            )
            for article_row in articles_rows
        ]
