from sqlalchemy import Column, Integer, ForeignKey, Time, Date

from .meta import Base

"""
row = site_link.findParent('td').findParent('tr').findAll('td')
row[6].text[:10]
'12/01/2020'
row[6].text[10:]
'22:00'
"""


class AurnHourly(Base):
    __tablename__ = 'aurn_hourly'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    site_id = Column(ForeignKey('sites.id'), nullable=False)
    ozone = Column(Integer)
    no2 = Column(Integer)
    so2 = Column(Integer)
    pm25 = Column(Integer)
    pm10 = Column(Integer)
