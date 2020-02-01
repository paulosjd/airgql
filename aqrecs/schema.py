from datetime import datetime
from functools import partial

import graphene
from graphene import Int, Float, List, String

from aqrecs.models.aurn_site import AurnEnvironments, AurnRegions, AurnSite
from aqrecs.schema_types import AurnSiteType, AurnHourlyType
from aqrecs.utils.haversine import haversine


# info.context['session'].query  <bound method <sqlalchemy.orm.se...4950C0EF0>>

class Query(graphene.ObjectType):

    sites = graphene.List(
        of_type=AurnSiteType,
        name=String(required=False),
        site_code=String(required=False),
        region=String(required=False),
        environ=String(required=False),
        latitude=Float(required=False),
        longitude=Float(required=False),
        geo_limit_by=Int(required=False),
    )

    hourly_data = graphene.List(
        of_type=AurnHourlyType,
        start_date=String(required=False),
        end_date=String(required=False),
        # n most recent hours , effectively like limit_by
        hours=Int(required=False),
        site_ids=List(of_type=Int, required=False),
        latitude=Float(required=False),
        longitude=Float(required=False),
        geo_limit_by=Int(required=False),
    )

    @staticmethod
    def resolve_hourly_data(root, info, *args, **kwargs):
        query = AurnHourlyType.get_query(info)
        print(len(query.all()))
        # query = AurnSiteType.get_query(info)
        geo = [kwargs.pop(k, 0) for k in ['latitude', 'longitude']]
        site_ids = kwargs.get('site_ids')
        site_kwargs = {}  # TODO add args like region to hourlydata objtype and do for k in kwargs, if k in ['region' , etc]
        # TODO                  site_kwargs[k] = kwargs.pop(k)
        if not site_ids:
            sites_q = Query.get_aurn_sites(
                info, site_kwargs, geo, geo_limit=kwargs.get('geo_limit_by')
            )
            site_ids = [site.id for site in sites_q]
            print(site_ids)
        print(len(query.all()))
        print(info.context['session'].query)

        # sites =  info.someattr.dbsession.quern(AurnSite.id, AurnSite.latitude, AurnSite.longitude)

    @staticmethod
    def resolve_sites(root, info, *args, **kwargs):
        filter_kwargs = {}
        geo = [kwargs.pop(k, 0) for k in ['latitude', 'longitude']]
        for k, v in kwargs.items():
            if k in AurnSiteType._meta.fields:
                if k in ['region', 'environ']:
                    enum = AurnRegions if k == 'region' else AurnEnvironments
                    param = enum.get_value_from_name(v)
                    if not param:
                        return []
                    filter_kwargs[k] = param
                else:
                    filter_kwargs[k] = v
        sites = Query.get_aurn_sites(info, filter_kwargs, geo,
                                     geo_limit=kwargs.get('geo_limit_by'))
        return sites

    @staticmethod
    def get_aurn_sites(
            info: dict,
            filter_kwargs: dict,
            geo: list,
            geo_limit: int = None,
    ):
        query = AurnSiteType.get_query(info)
        sites = query.filter_by(**filter_kwargs).all()

        if all(geo):
            haver = partial(haversine, origin_lon=geo[1], origin_lat=geo[0])
            sites = sorted(sites, key=haver)
            if geo_limit:
                sites = sites[:geo_limit]

        return sites


aurn_sites_schema = graphene.Schema(query=Query)
# from aqrecs.schema import aurn_sites_schema
# result = aurn_sites_schema.execute(
#     """
#     query {
#       sites(region:"East Midlands", latitude: -40.343, longitude: 0.543) {
#         name
#         latitude
#         environ
#       }
#     }
#     """
#     , context={'session': dbsession}  # Within pshell
# )
# return data pass through some func which replace e.g UT with urban traffic