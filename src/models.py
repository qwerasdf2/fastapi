from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):pass

class Documents(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    date = Column(TIMESTAMP, default=datetime.utcnow())


class DocumentsText(Base):
    __tablename__ = 'documents_text'

    id = Column(Integer, primary_key=True)
    id_doc = Column(Integer, ForeignKey('documents.id', ondelete='cascade'))
    text = Column(String)


# metadata = MetaData()

# documents = Table(
#     'documents',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('path', String),
#     Column('date', TIMESTAMP, default=datetime.utcnow()),
# )

# documents_text = Table(
#     'documents_text',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('id_doc', Integer, ForeignKey('documents.id')),
#     Column('text', String),
# )