"""updates

Revision ID: cdb4494d5673
Revises: 32d8493c7497
Create Date: 2025-05-23 17:14:18.528452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdb4494d5673'
down_revision: Union[str, None] = '32d8493c7497'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('firebase_token', sa.String(), nullable=False))
    op.add_column('users', sa.Column('authentication_method', sa.Enum('GOOGLE', 'EMAIL', 'Apple', name='authmethodenum'), nullable=True))
    op.add_column('users', sa.Column('device_type', sa.Enum('ANDROID', 'IOS', 'WEB', name='devicetypeenum'), nullable=True))
    op.add_column('users', sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'OTHER', name='genderenum'), nullable=False))
    op.create_index(op.f('ix_users_firebase_token'), 'users', ['firebase_token'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_firebase_token'), table_name='users')
    op.drop_column('users', 'gender')
    op.drop_column('users', 'device_type')
    op.drop_column('users', 'authentication_method')
    op.drop_column('users', 'firebase_token')
    # ### end Alembic commands ###
