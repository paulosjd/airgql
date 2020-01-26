import enum

from sqlalchemy import Column, Enum, Integer, Unicode

from .meta import Base


class BaseEnum(enum.Enum):
    @classmethod
    def get_value_from_name(cls, itm: str) -> str:
        """ Human-readable long name to enum name """
        try:
            return {
                a.value.upper(): a.name for a in list(cls)
                    }.get(itm.replace('-', ' ').upper())
        except AttributeError:
            pass


class AurnEnvironments(BaseEnum):
    RB = 'Rural Background'
    SI = 'Suburban Industrial'
    SB = 'Suburban Background'
    UB = 'Urban Background'
    UT = 'Urban Traffic'
    UI = 'Urban Industrial'


class AurnRegions(BaseEnum):
    CS = 'Central Scotland'
    EM = 'East Midlands'
    E = 'Eastern'
    GL = 'Greater London'
    H = 'Highlands'
    NE = 'North East'
    NES = 'North East Scotland'
    NI = 'Northern Ireland'
    NWA = 'North Wales'
    NW = 'North West'
    SB = 'Scottish Borders'
    SE = 'South East'
    SWA = 'South Wales'
    SW = 'South West'
    WM = 'West Midlands'
    Y = 'Yorkshire'


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
    def environment_type(self) -> str:
        return self.environ.value

    # hourly_data = db.relationship('HourlyData', backref='owner', lazy='dynamic')
