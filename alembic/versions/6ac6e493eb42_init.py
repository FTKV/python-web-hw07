"""'Init'

Revision ID: 6ac6e493eb42
Revises: 
Create Date: 2023-09-29 19:53:25.632332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ac6e493eb42'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=79), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('lecturers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=79), nullable=False),
    sa.Column('last_name', sa.String(length=79), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=79), nullable=False),
    sa.Column('lecturer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=79), nullable=False),
    sa.Column('last_name', sa.String(length=79), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grades')
    op.drop_table('students')
    op.drop_table('courses')
    op.drop_table('lecturers')
    op.drop_table('groups')
    # ### end Alembic commands ###
