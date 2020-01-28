import graphene
from graphene import ObjectType, Field, Schema


class User(graphene.ObjectType):
    firstName = graphene.String()
    lastName = graphene.String()


class Query(ObjectType):
    user = Field(User)

    def resolve_user(root, info):
        return {'user': root.firstName}


schema = Schema(Query)
user_root = User(firstName="ken", lastName="kensington")
result = schema.execute(
    '''
    query getUser {
        user {firstName}
    }
    ''',
    root=user_root
)
print(result.data)