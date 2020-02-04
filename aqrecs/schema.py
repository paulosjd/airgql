from functools import partial
from typing import Iterable, List, Optional, Type, Union

import graphene
from graphene import Int, Float, String
from graphql import GraphQLError

from aqrecs.models import AurnHourly, AurnSite
from aqrecs.models.aurn_site import AurnEnvironments, AurnRegions
from aqrecs.schema_types import AurnSiteType, AurnHourlyType
from aqrecs.utils import get_time_filter_params, haversine


class Query(graphene.ObjectType):
    site_enum_fields = ['region', 'environ']

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

    @staticmethod
    def resolve_hourly_data(root, info, *args, **kwargs):
        # sa db_session object: info.context['session']
        geo = [kwargs.pop(k, 0) for k in ['latitude', 'longitude']]
        enum_kwargs = {k: kwargs.pop(k, 0) for k in ['region', 'environ']}
        enum_kwargs = {k: v for k, v in enum_kwargs.items() if v}
        site_kwargs = Query.get_site_filter_kwargs_dict(enum_kwargs)
        if site_kwargs is None:
            # Means AurnSiteType.get_value_from_name -> None
            messages = Query.get_enum_error_messages(enum_kwargs)
            raise GraphQLError('\n'.join(messages))

        sites = Query.get_aurn_sites(
            info, site_kwargs, geo, geo_limit=kwargs.get('geo_limit_by')
        )
        site_id_kwarg = kwargs.get('site_ids')
        if site_id_kwarg:
            site_ids = [site.id for site in sites if site.id in site_id_kwarg]
        else:
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
            # Means AurnSiteType.get_value_from_name -> None
            messages = Query.get_enum_error_messages(kwargs)
            raise GraphQLError('\n'.join(messages))
        sites = Query.get_aurn_sites(info, filter_kwargs, geo,
                                     geo_limit=kwargs.get('geo_limit_by'))
        return sites

    @staticmethod
    def get_site_filter_kwargs_dict(kwargs: dict) -> Optional[dict]:
        filter_kwargs = {}
        for k, v in kwargs.items():
            # noinspection PyProtectedMember
            if k in AurnSiteType._meta.fields:
                if k in Query.site_enum_fields:
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

        if len(geo) == 2 and all(geo):
            haver = partial(haversine, origin_lon=geo[1], origin_lat=geo[0])
            sites = sorted(sites, key=haver)
            if geo_limit:
                sites = sites[:geo_limit]

        return sites

    @staticmethod
    def get_enum_error_messages(kwargs: dict) -> List[str]:
        messages = []
        for key, value in kwargs.items():
            if key in Query.site_enum_fields and value:
                ar = AurnRegions  # type: Union[Type[AurnRegions], Iterable]
                ae = AurnEnvironments
                evs = [a.value for a in list(ar if key == 'region' else ae)]
                valid_args = ', '.join([f'"{s}"' for s in evs])
                if value not in evs:
                    messages.append(
                        f'Argument "{key}" has invalid value "{value}".'
                        f'\n Expected value in {valid_args}, got "{value}".'
                    )
        return messages

# noinspection PyTypeChecker
aurn_sites_schema = graphene.Schema(query=Query)
