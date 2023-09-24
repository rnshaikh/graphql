import json
import graphene

from django.shortcuts import get_object_or_404

from graphene_django import DjangoObjectType

from user.models import User
from user.utils import generate_oauth_token


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


class LoginType(graphene.Scalar):

    @staticmethod
    def serialize(token_details):
        return token_details


class LoginUser(graphene.Mutation):

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    output = graphene.Field(LoginType)

    def mutate(parent, info, email, password):
        import pdb
        pdb.set_trace()

        user = get_object_or_404(User, email=email)
        if not user.check_password(password):
            raise Exception("Invalid email and password")

        login_success_data = generate_oauth_token(email, password)

        if login_success_data.status_code != 200:
            raise Exception("Invalid email and password")

        responce_dict = json.loads(login_success_data._content)

        return LoginUser(output=responce_dict)


class Mutation(graphene.ObjectType):

    create_user = CreateUser.Field()
    delete_users = DeleteUsers.Field()
    login_user = LoginUser.Field()


class Query(graphene.ObjectType):

    users = graphene.relay.ConnectionField(UserConnection)

    def resolve_users(parent, info, **kwargs):
        return User.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)

