import graphene

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


from graphql_relay import from_global_id
from polls.models import Question, Choice


from graphql_tutorial.custom_filters import QuestionFilter
from graphql_tutorial.permission_decorator import permission_required
from graphql_tutorial.custom_permission import is_authenticated


class ChoiceType(DjangoObjectType):

    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'vote_count', 'question')
        interfaces = (graphene.relay.Node, )


class ChoiceConnection(graphene.relay.Connection):

    class Meta:
        node = ChoiceType


class QuestionType(DjangoObjectType):

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date', 'choice_set')
        interfaces = (graphene.relay.Node, )

    choice_set = graphene.relay.ConnectionField(ChoiceConnection)

    def resolve_choice_set(parent, info, **kwargs):
        return parent.choice_set.all()


class QuestionConnection(graphene.relay.Connection):

    class Meta:
        node = QuestionType


class ChoiceInputType(graphene.InputObjectType):

    id = graphene.ID(required=False)
    choice_text = graphene.String()


class CreateQuestion(graphene.relay.ClientIDMutation):

    class Input:
        question_text = graphene.String()
        choices_set = graphene.List(ChoiceInputType, required=False)

    question = graphene.Field(QuestionType)
    choice_set = graphene.List(ChoiceType, required=False)

    @classmethod
    def mutate_and_get_payload(cls, parent, info, question_text, choices_set):
        obj = Question(question_text=question_text)
        obj.save()
        choices_list = []
        for i in choices_set:
            ob = Choice(choice_text=i['choice_text'], question=obj)
            ob.save()
            choices_list.append(ob)
        return CreateQuestion(question=obj, choice_set=choices_list)


class UpdateQuestion(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.ID()
        question_text = graphene.String()

    question = graphene.Field(QuestionType)

    @classmethod
    def mutate_and_get_payload(cls, parent, info, id, question_text):

        id = from_global_id(id)[1]
        obj = Question.objects.get(id=id)
        obj.question_text = question_text
        obj.save()
        return UpdateQuestion(question=obj)


class DeleteQuestion(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.ID()

    question = graphene.Field(QuestionType)
    ok = graphene.Boolean()


    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):

        if not is_authenticated(info.context.user):
            raise Exception("Permission Denied")

        id = kwargs.get('client_mutation_id', None)
        id = from_global_id(id)[1]
        obj = Question.objects.get(id=id)
        obj.delete()
        return DeleteQuestion(ok=True, question=None)


class Mutation(graphene.ObjectType):

    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field()


class Query(graphene.ObjectType):

    question = graphene.relay.Node.Field(QuestionType)
    questions = DjangoFilterConnectionField(QuestionType,
                                            filterset_class=QuestionFilter)
    choices = graphene.relay.ConnectionField(ChoiceConnection)
    choice = graphene.relay.Node.Field(ChoiceType)

    @permission_required(is_authenticated)
    def resolve_questions(self, info, **kwargs):
        return Question.objects.all()

    @permission_required(is_authenticated)
    def resolve_question(self, info, id):
        return Question.objects.get(id=id)

    @permission_required(is_authenticated)
    def resolve_choices(self, info, **kwargs):
        return Choice.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)

