from pyramid.view import view_config
from sqlalchemy import exc

from aqrecs import models
from aqrecs.schema import aurn_sites_schema

template_path = '../templates/mytemplate.mako'


@view_config(route_name='home', renderer=template_path)
def my_view(request):
    # query = request.dbsession.query(models.Account)
    # one = query.filter(models.Account.name == 'Foobar Ltd').first()
    return {'one': 'foo'}




@view_config(route_name='index', renderer='json')
def graph_view(req):
    print(req.params)
    if req.params.get('query'):
        print('type of q is %s' % type(req.params['query']))
        query = str(req.params['query'])
        print(query)
        result = aurn_sites_schema.execute(
            """
            query {
              sites(region:"East Midlands", latitude: -40.343, longitude: 0.543) {
                name
                latitude
                environ
              }
            }
            """
            , context={'session': req.dbsession}  # Within pshell
        )
        if result.data:
            return {'data': result.data}
        else:
            return {'errors': [{'message': str(i)} for i in result.errors]}
    # query = request.dbsession.query(models.Account)
    # one = query.filter(models.Account.name == 'Foobar Ltd').first()
    result = aurn_sites_schema.execute(
        """
        query {
          sites(region:"East Midlands", latitude: -40.343, longitude: 0.543) {
            name
            latitude
            environ
          }
        }
        """
        , context={'session': req.dbsession}  # Within pshell
    )
    if result.data:
        return {'data': result.data}
    elif result.errors:
        return {'errors': [{'message': str(i)} for i in result.errors]}
    return {'one': 'foo'}


