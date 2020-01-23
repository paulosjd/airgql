import graphene
from graphene import String

from airgql.schema_types import AurnSiteType, AurnHourlyType


class Query(graphene.ObjectType):
    sites = graphene.List(
        of_type=AurnSiteType,
        name=String(required=False)
        # author_id=graphene.Argument(type=graphene.Int, required=False),
    )

    @staticmethod
    def resolve_sites(root, info, *args, **kwargs):
        print(args)
        print(kwargs)
        query = AurnSiteType.get_query(info)
        return query.all()


aurn_sites_schema = graphene.Schema(query=Query)

# From pshell (need access to dbsession):
# result = aurn_sites_schema.execute(
#     """
#     query {
#       sites(name:"Aberdeen") {
#         name
#         siteCode
#       }
#     }
#     """
#     , context={'session': dbsession}
# )