from graphene import ObjectType, String, Int, Schema, Field


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()
    foo = Field(String, num=Int(default_value=0), bar=Int())

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

    def resolve_foo(self, info, num, bar):
        data = {0: 'abc', 1: 'eds', 2: 'dte'}
        return data.get(bar) or data.get(num, 'not found')


schema = Schema(query=Query)


result = schema.execute('{ hello, goodbye, foo(bar: 2)}')
result2 = schema.execute('{ hello, goodbye, foo(num: 1, bar: 4)}')
print(result.data)
print(result2.data['foo'])

# or passing the argument in the query
result = schema.execute('{ hello(name: "GraphQL") }')
print(result.data['hello'])


result1 = schema.execute('{ foo(bar: 2)}')
result2 = schema.execute('{ foo(num: 1, bar: 4)}')
print(result1.data['foo'], result2.data['foo'])