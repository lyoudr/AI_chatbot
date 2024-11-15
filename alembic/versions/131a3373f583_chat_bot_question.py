"""chat bot question

Revision ID: 131a3373f583
Revises: 7b3f479fad9b
Create Date: 2024-08-27 13:52:35.892007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '131a3373f583'
down_revision: Union[str, None] = '7b3f479fad9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_bot', sa.Column('question', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat_bot', 'question')
    # ### end Alembic commands ###
