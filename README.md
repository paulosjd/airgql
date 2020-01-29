
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

GraphiQL browser. Alternatively, execute graphql query from pshell:

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

Example GraphQL Queries
------------------------

Query by geographical proximity:

    query {
          sites(geoLimitBy: 10, latitude: 52.46, longitude: -0.54) {
            name
            latitude
            environ
          }
        }

Response:

    {
      "sites": [
        {
          "name": "Sandy Roadside",
          "latitude": "52.132417",
          "environ": "Urban Traffic"
        },
        {
          "name": "Leicester University",
          "latitude": "52.619823",
          "environ": "Urban Background"
        },
        {
          "name": "Leicester A594 Roadside",
          "latitude": "52.638677",
          "environ": "Urban Traffic"
        },
        {
          "name": "Cambridge Roadside",
          "latitude": "52.202370",
          "environ": "Urban Traffic"
        },
        {
          "name": "Wicken Fen",
          "latitude": "52.298500",
          "environ": "Rural Background"
        },
        {
          "name": "Luton A505 Roadside",
          "latitude": "51.892293",
          "environ": "Urban Traffic"
        },
        {
          "name": "Coventry Binley Road",
          "latitude": "52.407708",
          "environ": "Urban Traffic"
        },
        {
          "name": "Nottingham Centre",
          "latitude": "52.954730",
          "environ": "Urban Background"
        },
        {
          "name": "Coventry Allesley",
          "latitude": "52.411563",
          "environ": "Urban Background"
        },
        {
          "name": "Leamington Spa",
          "latitude": "52.288810",
          "environ": "Urban Background"
        }
      ]
    }