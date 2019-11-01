from django.db.models import F

from django_filters import FilterSet
from django_filters.filters import NumberFilter, CharFilter

from backend.models import Response


class ResponseFilter(FilterSet):
    project = NumberFilter(method="filter_project")
    answer_type = CharFilter(method="filter_answer_type")

    class Meta:
        model = Response
        fields = ("project", "answer_type")

    def filter_project(self, queryset, name, value):
        if value:
            queryset = queryset.filter(evaluation__phase__project=value)
        return queryset

    def filter_answer_type(self, queryset, name, value):
        if value:
            queryset = queryset.filter(question__answer_type=value)
        return queryset
