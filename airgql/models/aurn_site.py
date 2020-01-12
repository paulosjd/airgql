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


class AurnSite(Base):
    __tablename__ = 'aurn_sites'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False, unique=True)
    site_code = Column(Unicode(10), nullable=False, unique=True)
    environ = Column(Enum(AurnEnvironments), nullable=False)
    region = Column(Enum(AurnRegions), nullable=False)
    latitude = Column(Unicode(50), nullable=False)
    longitude = Column(Unicode(50), nullable=False)

    @property
    def environment_type(self):
        return self.environ.value

    # hourly_data = db.relationship('HourlyData', backref='owner', lazy='dynamic')
