import graphene
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id

from dkmentions import models


class FacebookPostType(DjangoObjectType):

    class Meta:
        model = models.FacebookPost
        interfaces = (graphene.Node, )


class Query(graphene.AbstractType):
    all_posts = graphene.List(FacebookPostType)
    first_post = graphene.Field(FacebookPostType, id=graphene.ID())

    def resolve_all_posts(self, args=None, context=None, info=None):
        return models.FacebookPost.objects.all()

    def resolve_first_post(self, args=None, context=None, info=None):
        rid = from_global_id(args.get('id', 1))
        return models.FacebookPost.objects.get(pk=rid[1])
