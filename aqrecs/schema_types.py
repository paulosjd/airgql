from graphene.types import String
from graphene_sqlalchemy import SQLAlchemyObjectType

from aqrecs.models import AurnHourly, AurnSite


class EnumValueType(String):

    @staticmethod
    def serialize(enum):
        return enum.value


class AurnRegionType(String):

    @staticmethod
    def serialize(enum):
        return enum.value


class AurnSiteType(SQLAlchemyObjectType):
    region = EnumValueType()
    environ = EnumValueType()

    class Meta:
        model = AurnSite
        only_fields = (
            'id', 'name', 'site_code', 'latitude', 'longitude'
        )


class AurnHourlyType(SQLAlchemyObjectType):
    class Meta:
        model = AurnHourly
        only_fields = (
            'time', 'site_id', 'ozone', 'no2', 'so2', 'pm25', 'pm10'
        )
