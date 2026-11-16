"""add bookmarks table

Revision ID: add_bookmarks_001
Revises: fdf8821871d7
Create Date: 2026-11-16 00:00:00.000000

"""
import sqlalchemy as sa
from alembic import op

revision = "add_bookmarks_001"
down_revision = "fdf8821871d7"
branch_labels = None
depends_on = None


def create_bookmarks_table() -> None:
    op.create_table(
        "bookmarks",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "article_id",
            sa.Integer,
            sa.ForeignKey("articles.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    op.create_primary_key("pk_bookmarks", "bookmarks", ["user_id", "article_id"])
    op.create_index("idx_bookmarks_user", "bookmarks", ["user_id"])


def upgrade() -> None:
    create_bookmarks_table()


def downgrade() -> None:
    op.drop_table("bookmarks")
