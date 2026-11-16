import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from app.models.domain.articles import Article
from app.models.domain.users import UserInDB

pytestmark = pytest.mark.asyncio


async def test_bookmark_article(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
) -> None:
    response = await authorized_client.post(
        app.url_path_for("articles:bookmark-article", slug=test_article.slug)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["article"]["bookmarked"] is True


async def test_unbookmark_article(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
) -> None:
    await authorized_client.post(
        app.url_path_for("articles:bookmark-article", slug=test_article.slug)
    )
    response = await authorized_client.delete(
        app.url_path_for("articles:unbookmark-article", slug=test_article.slug)
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["article"]["bookmarked"] is False


async def test_list_user_bookmarks(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
) -> None:
    await authorized_client.post(
        app.url_path_for("articles:bookmark-article", slug=test_article.slug)
    )
    response = await authorized_client.get(
        app.url_path_for("users:list-bookmarks")
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["articlesCount"] == 1
    assert len(response.json()["articles"]) == 1
    assert response.json()["articles"][0]["slug"] == test_article.slug


async def test_list_user_bookmarks_empty(
    app: FastAPI,
    authorized_client: AsyncClient,
) -> None:
    response = await authorized_client.get(
        app.url_path_for("users:list-bookmarks")
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["articlesCount"] == 0
    assert len(response.json()["articles"]) == 0


async def test_bookmark_requires_auth(
    app: FastAPI,
    client: AsyncClient,
    test_article: Article,
) -> None:
    response = await client.post(
        app.url_path_for("articles:bookmark-article", slug=test_article.slug)
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_list_bookmarks_requires_auth(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    response = await client.get(app.url_path_for("users:list-bookmarks"))
    assert response.status_code == status.HTTP_403_FORBIDDEN
