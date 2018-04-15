from django.contrib import admin
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    re_path('^gql', csrf_exempt(GraphQLView.as_view(batch=True))),
]
