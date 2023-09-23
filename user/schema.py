import graphene
from graphene_django import DjangoObjectType

from user.models import User


class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = ('id', 'email', 'gender', 'password')
        interfaces = (graphene.relay.Node, )


class UserConnection(graphene.Connection):

    class Meta:
        node = UserType


class UserInputType(graphene.InputObjectType):

    email = graphene.String()
    gender = graphene.String()
    password = graphene.String()


class CreateUser(graphene.Mutation):

    class Arguments:
        user_input = graphene.Argument(UserInputType, required=True)

    user = graphene.Field(UserType)

    def mutate(parent, info, **kwargs):

        user = kwargs.get('user_input', None)
        obj = User(**user)
        obj.save()
        return CreateUser(user=obj)


class DeleteUsers(graphene.Mutation):

    class Arguments:
        id = graphene.Int(required=False)

    count = graphene.Int()

    def mutate(parent, info, id=None, *kwargs):

        users = User.objects.all().delete()
        return DeleteUsers(count=users[0])


class Mutation(graphene.ObjectType):

    create_user = CreateUser.Field()
    delete_users = DeleteUsers.Field()


class Query(graphene.ObjectType):

    users = graphene.relay.ConnectionField(UserConnection)

    def resolve_users(parent, info, **kwargs):
        return User.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)

