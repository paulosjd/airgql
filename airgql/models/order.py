# from sqlalchemy import Column, DateTime, Integer, Unicode, ForeignKey
#
# from .meta import Base
#
#
# class Order(Base):
#     __tablename__ = 'orders'
#     id = Column(Integer, primary_key=True)
#     date = Column(DateTime, nullable=False)
#     reference = Column(Unicode(40), nullable=False, default='')
#     account_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'),
#                         nullable=False)
