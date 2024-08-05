"""create summary table

Revision ID: 958ac472dc08
Revises: e21b2a2c9fe8
Create Date: 2024-06-12 17:20:36.909356

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '958ac472dc08'
down_revision = 'e21b2a2c9fe8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('ALTER TABLE summary ALTER COLUMN id TYPE UUID USING id::uuid')
    op.create_table('summary_v2',
    sa.Column("id", sa.UUID(), nullable=False),
    sa.Column('summary_title', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('user_id', sa.UUID(as_uuid=True), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('embedding', postgresql.ARRAY(sa.Float()), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_column('create_datetime')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_datetime', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))

    op.drop_table('summary')
    # ### end Alembic commands ###
