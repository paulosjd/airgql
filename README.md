
Source code for a prototype API which supports GraphQL operations as well as REST.
It is written in Python and libraries used include Pyramid and graphene-sqlalchemy.
Schema revolves around hourly recorded measurements taken sites 
within an automated air pollution monitoring network.

# todo add equivalent REST endpoints

Also provides an example of (implementing a graphiql browser interface in a Pyramid application.
(Provide link), useful development feature for working with GraphQL.

For database setup, run alembic -c development.ini init alembic
In the env.py file that get after , update like:

# add your model's MetaData object here
# for 'autogenerate' support
from pyratest.models.meta import Base
target_metadata = Base.metadata

Alembic database migrations: 

    $ alembic -c development.ini revision --autogenerate -m "some message"   
     
    $ alembic -c development.ini upgrade head

Todo: - code first approach of graphene: at end draw up equivalent schema in graph

Execute graphql query from pshell:

>>> from aqrecs.schema import aurn_sites_schema
>>> result = aurn_sites_schema.execute(
        """
        query {
          sites(region: "North East") {
            name
            region
          }
        }
        """
        , context={'session': dbsession}
    )
>>> result.errors
>>> result.data
OrderedDict([('sites', [OrderedDict([('name', 'Aberdeen'), ('siteCode', 'ABD')]), ...])]), 
