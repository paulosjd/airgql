import json
from json.decoder import JSONDecodeError

from pyramid.exceptions import HTTPNotFound
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config

from aqrecs.schema import aurn_sites_schema


@view_config(route_name='graphiql')
def render_graphiql(request):
    if request.registry.settings.get('graphiql_enabled') != 'true':
        raise HTTPNotFound()
    try:
        result = aurn_sites_schema.execute(
                request.json_body['query'],
                context={'session': request.dbsession}
        )
    except (KeyError, JSONDecodeError):
        return Response(render('../templates/graphiql.mako', {}, request))

    if result.data:
        return Response(json.dumps(result.data))
    return Response(json.dumps([{'message': str(i)} for i in result.errors]))
