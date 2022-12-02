# hackernews
import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType

from .models import Componente

class ComponenteType(DjangoObjectType):
    class Meta:
        model = Componente


class Query(graphene.ObjectType):
    componentes = graphene.List(ComponenteType)

    def resolve_componentes(self, info, **kwargs):
        return Componente.objects.all()
# ...code
#1
class CreateComponente(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    semestre = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        name= graphene.String()
        semestre= graphene.String()

    def mutate(self, info, name, semestre):
        user = info.context.user or None

        componente = Componente(
            name=name,
            semestre=semestre,
            posted_by = user
        )
        componente.save()

        return CreateComponente(
            id=componente.id,
            name=componente.name,
            posted_by = componente.posted_by,     
        )


#4
class Mutation(graphene.ObjectType):
    create_componente = CreateComponente.Field()
