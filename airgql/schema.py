import graphene
from graphene import Enum, String

from airgql.models.aurn_site import AurnEnvironments, AurnRegions
from airgql.schema_types import AurnSiteType, AurnHourlyType


class Query(graphene.ObjectType):
    """ Todo: ability to query on lat and lon - decide how """
    sites = graphene.List(
        of_type=AurnSiteType,
        name=String(required=False),
        site_code=String(required=False),
        region=String(required=False),
        environ=String(required=False),
    )

    @staticmethod
    def resolve_sites(root, info, *args, **kwargs):
        filter_kwargs = {}
        for k, v in kwargs.items():
            if k in AurnSiteType._meta.fields:
                if k in ['region', 'environ']:
                    enum = AurnRegions if k == 'region' else AurnEnvironments
                    param = enum.get_value_from_name(v)
                    print('param is', param)
                    if param:
                        filter_kwargs[k] = param
                else:
                    filter_kwargs[k] = v
        print(filter_kwargs)
        query = AurnSiteType.get_query(info)
        #  query = query.filter_by(**filter_kwargs)
        return query.filter_by(**filter_kwargs).all()


aurn_sites_schema = graphene.Schema(query=Query)
# result = aurn_sites_schema.execute(
#     """
#     query {
#       sites(region:"East Midlands") {
#         name
#         latitude
#       }
#     }
#     """
#     , context={'session': dbsession}  # Within pshell
# )
