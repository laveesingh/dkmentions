import graphene

import dkmentions.schema

class Queries(graphene.ObjectType, dkmentions.schema.Query):
    dummy = graphene.String()


schema = graphene.Schema(query=Queries)
