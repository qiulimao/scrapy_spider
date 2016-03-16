"""start fucking webspider

Revision ID: 20fe95271279
Revises: 
Create Date: 2016-03-16 12:06:08.879868

"""

# revision identifiers, used by Alembic.
revision = '20fe95271279'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('seebug',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('ssvid', sa.String(length=32), nullable=False),
    sa.Column('discover_time', sa.Date(), nullable=False),
    sa.Column('commit_time', sa.Date(), nullable=True),
    sa.Column('danger_level', sa.String(length=8), nullable=False),
    sa.Column('bug_type', sa.String(length=32), nullable=True),
    sa.Column('cveid', sa.String(length=16), nullable=True),
    sa.Column('cnnydid', sa.String(length=16), nullable=True),
    sa.Column('cnvdid', sa.String(length=16), nullable=True),
    sa.Column('author', sa.String(length=16), nullable=True),
    sa.Column('commitor', sa.String(length=16), nullable=True),
    sa.Column('zoomeye_dork', sa.String(length=16), nullable=True),
    sa.Column('influence_component', sa.String(length=16), nullable=True),
    sa.Column('bug_abstract', sa.String(length=512), nullable=True),
    sa.Column('url', sa.String(length=256), nullable=False),
    sa.Column('url_md5', sa.String(length=32), nullable=False),
    sa.Column('save_time', sa.DateTime(), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url_md5')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seebug')
    ### end Alembic commands ###
