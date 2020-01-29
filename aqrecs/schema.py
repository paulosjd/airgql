from functools import partial

import graphene
from graphene import Int, Float, String

from aqrecs.models.aurn_site import AurnEnvironments, AurnRegions
from aqrecs.schema_types import AurnSiteType, AurnHourlyType
from aqrecs.utils.haversine import haversine


class Query(graphene.ObjectType):

    # hourly_data  -- ensure that ordered-by most recent
    # (rely on id order? -cannot - i.e. desc?) and limit..

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

    @staticmethod
    def resolve_sites(root, info, *args, **kwargs):
        print('typ of root is %s' % type(root))
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
        query = AurnSiteType.get_query(info)
        sites = query.filter_by(**filter_kwargs).all()
        if all(geo):
            haver = partial(haversine, origin_lon=geo[1], origin_lat=geo[0])
            sites = sorted(sites, key=haver)
            if kwargs.get('geo_limit_by'):
                sites = sites[:kwargs['geo_limit_by']]
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