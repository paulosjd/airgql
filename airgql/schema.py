import graphene
from graphene import Int, Float, String

from airgql.models.aurn_site import AurnEnvironments, AurnRegions
from airgql.schema_types import AurnSiteType, AurnHourlyType


class Query(graphene.ObjectType):
    """ Todo: ability to query on lat and lon - decide how
    - Some kind of string argument e.g. '-59.2334, 0.2323' which resolver
    - takes and uses along with another argument optional (has default)
    - called e.g. distance from...or close n sites ... haversine stuff
    - and uses that to filter geographically
    """
    # hourly_data  -- ensure that ordered-by most recent
    # (rely on id order? i.e. desc?) and limit..

    sites = graphene.List(
        of_type=AurnSiteType,
        name=String(required=False),
        site_code=String(required=False),
        region=String(required=False),
        environ=String(required=False),
        latitude=Float(required=False),
        longitude=Float(required=False),
        geo_limit_by=Int(required=False),  # in resolver make default like 10-20
    )

    @staticmethod
    def resolve_sites(root, info, *args, **kwargs):
        filter_kwargs = {}
        geo = [kwargs.pop(k, 0) for k in ['latitude', 'longitude']]
        if all(geo):
            print(geo)  # works, e.g. [-40.343, 0.543]
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
        return query.filter_by(**filter_kwargs).all()


aurn_sites_schema = graphene.Schema(query=Query)
# from airgql.schema import aurn_sites_schema
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