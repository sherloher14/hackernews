import graphene
import graphql_jwt

import links.schema
import users.schema
import ai.schema
import componentes.schema

class Query(users.schema.Query, links.schema.Query, ai.schema.Query, componentes.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, links.schema.Mutation, componentes.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)