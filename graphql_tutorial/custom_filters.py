import django_filters

from polls.models import Question


class QuestionFilter(django_filters.FilterSet):

    from_pub_date = django_filters.DateFilter(method='from_pub_date_filter')
    to_pub_date = django_filters.DateFilter(method='to_pub_date_filter')
    pub_date = django_filters.DateFromToRangeFilter(field_name='pub_date')

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date')

    def from_pub_date_filter(self, queryset, name, value):
        queryset = queryset.filter(pub_date__gte=value).distinct()
        return queryset

    def to_pub_date_filter(self, queryset, name, value):
        queryset = queryset.filter(pub_date__lte=value).distinct()
        return queryset
