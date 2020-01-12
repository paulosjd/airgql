import enum

from sqlalchemy import Column, Enum, Integer, Unicode

from .meta import Base


class AurnEnvironments(enum.Enum):
    rb = 'Rural Background'
    si = 'Suburban Industrial'
    sb = 'Suburban Background'
    ub = 'Urban Background'
    ut = 'Urban Traffic'
    ui = 'Urban Industrial'

# = ''.join([s[0] for s in value.split('-')])
# getattr(AurnEnvironments, val)


class AurnRegions(enum.Enum):
    cs = 'Central Scotland'
    em = 'East Midlands'
    e = 'Eastern'
    gl = 'Greater London'
    h = 'Highlands'
    ne = 'North East'
    nes = 'North East Scotland'
    ni = 'Northern Ireland'
    nwa = 'North Wales'
    nw = 'North West'
    sb = 'Scottish Borders'
    se = 'South East'
    swa = 'South Wales'
    sw = 'South West'
    wm = 'West Midlands'
    y = 'Yorkshire'

"""
[''.join([s[0] for s in a.split('-')]) if not a.endswith('wales') else ''.join([s[0] for s in a.split('-')]) + 'a' for a in list(sorted(set(regions.values())))]
['cs', 'em', 'e', 'gl', 'h', 'ne', 'nes', 'nwa', 'nw', 'ni', 'sb', 'se', 'swa', 'sw', 'wm', 'y']

[''.join([s[0] for s in a.split('-')]) for a in list(sorted(set(regions.values())))]
['cs', 'em', 'e', 'gl', 'h', 'ne', 'nes', 'nw', 'nw', 'ni', 'sb', 'se', 'sw', 'sw', 'wm', 'y']
getattr(AurnRegions, val)
"""


class AurnSite(Base):
    __tablename__ = 'aurn_sites'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    name = Column(Unicode(50), nullable=False, unique=True)
    site_code = Column(Unicode(10), nullable=False, unique=True)
    environ = Column(Enum(AurnEnvironments), nullable=False)
    region = Column(Enum(AurnRegions), nullable=False)
    latitude = Column(Unicode(50), nullable=False)
    longitude = Column(Unicode(50), nullable=False)

    # hourly_data = db.relationship('HourlyData', backref='owner', lazy='dynamic')
