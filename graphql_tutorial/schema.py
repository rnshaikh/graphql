import graphene

from polls.schema import Mutation as PollMutation, Query as PollQuery
from user.schema import Mutation as UserMutation, Query as UserQuery


class Query(PollQuery, UserQuery, graphene.ObjectType):

    pass


class Mutation(UserMutation, PollMutation, graphene.ObjectType):

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
