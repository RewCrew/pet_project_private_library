from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    Float,
    Integer,
    MetaData,
    String,
    Table,
)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

books = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('subtitle', String, nullable=False),
    Column('authors', String, nullable=False),
    Column('publisher', String, nullable=False),
    Column('isbn10', String, nullable=True),
    Column('isbn13', BigInteger, nullable=False),
    Column('pages', Integer, nullable=False),
    Column('year', Integer, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('desc', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('image', String, nullable=False),
    Column('url', String, nullable=False),
    Column('desc', String, nullable=False)
)

userbooks = Table(
    'userbooks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_isbn', BigInteger, nullable=False),
    Column('prebooked_by_user_id', Integer, nullable=True),
    Column('finally_booked_by_user_id', Integer, nullable=True),
    Column('booked_date', Date, nullable=False),
    Column('order_for_days', Integer, nullable=True),
    Column('returned', Boolean, default=False),
    Column('return_date', Date, nullable=True),
    Column('booked_forever', Boolean, default=False),
    Column('user_id_history', Integer, nullable=True)
)
