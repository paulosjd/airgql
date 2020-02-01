from functools import partial
from typing import List, Optional

import graphene
from graphene import Int, Float, String

from aqrecs.models import AurnHourly, AurnSite
from aqrecs.models.aurn_site import AurnEnvironments, AurnRegions
from aqrecs.schema_types import AurnSiteType, AurnHourlyType
from aqrecs.utils import get_time_filter_params, haversine


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
        hours=Int(required=False),
        site_ids=graphene.List(of_type=Int, required=False),
        region=String(required=False),
        environ=String(required=False),
        latitude=Float(required=False),
        longitude=Float(required=False),
        geo_limit_by=Int(required=False),
    )

    # TODO  where filter_kwargs is None, so empty list, how do error message say that not match anything, GraphQLError ?

    @staticmethod
    def resolve_hourly_data(root, info, *args, **kwargs):
        # sa db_session object: info.context['session']
        geo = [kwargs.pop(k, 0) for k in ['latitude', 'longitude']]
        enum_kwargs = {k: kwargs.pop(k, 0) for k in ['region', 'environ']}
        site_kwargs = Query.get_site_filter_kwargs_dict(
            {k: v for k, v in enum_kwargs.items() if v}
        )
        site_ids = kwargs.get('site_ids')
        if not site_ids:
            sites = Query.get_aurn_sites(
                info, site_kwargs, geo, geo_limit=kwargs.get('geo_limit_by')
            )
            site_ids = [site.id for site in sites]

        start_dt, end_dt = get_time_filter_params(kwargs)
        results = AurnHourlyType.get_query(info).filter(
            AurnHourly.time >= start_dt,
            AurnHourly.time <= end_dt,
            AurnHourly.site_id.in_(site_ids)
        ).all()

        return results

    @staticmethod
    def resolve_sites(root, info, *args, **kwargs):
        geo = [kwargs.pop(k, 0) for k in ['latitude', 'longitude']]
        filter_kwargs = Query.get_site_filter_kwargs_dict(kwargs)
        if filter_kwargs is None:
            return []
        sites = Query.get_aurn_sites(info, filter_kwargs, geo,
                                     geo_limit=kwargs.get('geo_limit_by'))
        return sites

    @staticmethod
    def get_site_filter_kwargs_dict(kwargs: dict) -> Optional[dict]:
        filter_kwargs = {}
        for k, v in kwargs.items():
            # noinspection PyProtectedMember
            if k in AurnSiteType._meta.fields:
                if k in ['region', 'environ']:
                    enum = AurnRegions if k == 'region' else AurnEnvironments
                    param = enum.get_value_from_name(v)
                    if not param:
                        return None
                    filter_kwargs[k] = param
                else:
                    filter_kwargs[k] = v
        return filter_kwargs

    @staticmethod
    def get_aurn_sites(
            info: dict,
            filter_kwargs: dict,
            geo: list,
            geo_limit: int = None,
    ) -> List[AurnSite]:
        query = AurnSiteType.get_query(info)
        sites = query.filter_by(**filter_kwargs).all()

        if all(geo):
            haver = partial(haversine, origin_lon=geo[1], origin_lat=geo[0])
            sites = sorted(sites, key=haver)
            if geo_limit:
                sites = sites[:geo_limit]

        return sites


# noinspection PyTypeChecker
aurn_sites_schema = graphene.Schema(query=Query)
