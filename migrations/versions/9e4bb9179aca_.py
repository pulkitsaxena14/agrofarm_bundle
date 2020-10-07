"""empty message

Revision ID: 9e4bb9179aca
Revises: 
Create Date: 2020-10-08 00:14:42.284775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e4bb9179aca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('details', sa.String(), nullable=False),
    sa.Column('asked', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('upvotes', sa.Integer(), nullable=True),
    sa.Column('downvotes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ans', sa.String(), nullable=False),
    sa.Column('answered', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('q_id', sa.Integer(), nullable=False),
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('upvotes', sa.Integer(), nullable=True),
    sa.Column('downvotes', sa.Integer(), nullable=True),
    sa.Column('accepted', sa.Enum('YES', 'NO', name='ACCEPT_ANS'), nullable=True),
    sa.ForeignKeyConstraint(['q_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('q_votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('q_id', sa.Integer(), nullable=False),
    sa.Column('vote', sa.Enum('UP', 'DOWN', name='VOTE_TYPE'), nullable=True),
    sa.ForeignKeyConstraint(['q_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('u_id', 'q_id')
    )
    op.create_table('a_votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('a_id', sa.Integer(), nullable=False),
    sa.Column('vote', sa.Enum('UP', 'DOWN', name='VOTE_TYPE'), nullable=True),
    sa.ForeignKeyConstraint(['a_id'], ['answers.id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('u_id', 'a_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('a_votes')
    op.drop_table('q_votes')
    op.drop_table('answers')
    op.drop_table('questions')
    op.drop_table('users')
    op.drop_table('login')
    # ### end Alembic commands ###