from sqlalchemy import Column, DateTime, Integer, ForeignKey, UniqueConstraint

from .meta import Base


class AurnHourly(Base):
    __tablename__ = 'aurn_hourly'
    __table_args__ = (
        UniqueConstraint('time', 'site_id', name='uix_1'),
    )
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    site_id = Column(ForeignKey('aurn_sites.id'), nullable=False)
    ozone = Column(Integer)
    no2 = Column(Integer)
    so2 = Column(Integer)
    pm25 = Column(Integer)
    pm10 = Column(Integer)

    def __str__(self):
        return f'<AurnHourly site_id={self.site_id} time={self.time} ' \
            f'pm10={self.pm10}>'
