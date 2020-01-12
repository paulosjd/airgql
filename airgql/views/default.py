from pyramid.view import view_config
from sqlalchemy import exc

from airgql import models

template_path = '../templates/mytemplate.mako'


@view_config(route_name='home', renderer=template_path)
def my_view(request):
    # query = request.dbsession.query(models.Account)
    # one = query.filter(models.Account.name == 'Foobar Ltd').first()
    return {'one': 'foo'}
