"""updated_at and requested_by fields added

Revision ID: 66faa7e1a6e3
Revises: b4bc3fd55f1f
Create Date: 2022-09-11 00:55:06.806360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66faa7e1a6e3'
down_revision = 'b4bc3fd55f1f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('definition', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('definition', sa.Column('requested_by', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'definition', 'bot_user', ['requested_by'], ['id'])
    op.add_column('urban_dictionary', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('urban_dictionary', sa.Column('requested_by', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'urban_dictionary', 'bot_user', ['requested_by'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'urban_dictionary', type_='foreignkey')
    op.drop_column('urban_dictionary', 'requested_by')
    op.drop_column('urban_dictionary', 'created_at')
    op.drop_constraint(None, 'definition', type_='foreignkey')
    op.drop_column('definition', 'requested_by')
    op.drop_column('definition', 'created_at')
    # ### end Alembic commands ###