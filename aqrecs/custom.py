import datetime
from graphene.types import Scalar
from graphql.language import ast


class MyDateTime(Scalar):

    @staticmethod
    def serialize(dt):
        return dt.isoformat()

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(
                node.value, "%Y-%m-%dT%H:%M:%S.%f")

    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")


from graphene import ObjectType, String, Int, Schema, Field


class Query(ObjectType):
    mytime = MyDateTime()

    def resolve_mytime(self, info):
        return datetime.datetime.now()


schema = Schema(query=Query)

result = schema.execute('{ mytime }')
print(result.data)
