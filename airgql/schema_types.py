import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from airgql.models import AurnSite, AurnHourly


class AurnSiteType(SQLAlchemyObjectType):

    class Meta:
        model = AurnSite
        only_fields = (
            'name', 'site_code', 'environ', 'region', 'latitude', 'longitude'
        )


class AurnHourlyType(SQLAlchemyObjectType):
    class Meta:
        model = AurnHourly
        only_fields = (
            'time', 'site_id', 'ozone', 'no2', 'so2', 'pm25', 'pm10'
        )
