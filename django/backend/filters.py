from django.db.models import F, query

from django_filters import FilterSet
from django_filters.filters import NumberFilter, CharFilter, BaseInFilter

from backend import models

# General docs at:
# https://django-filter.readthedocs.io/en/master/guide/tips.html


class CharInFilter(BaseInFilter, CharFilter):
    """Generic filter for IN expressions with chars"""

    pass


class ResponseFilter(FilterSet):
    project = NumberFilter(method="filter_project")
    answer_type = CharFilter(method="filter_answer_type")

    class Meta:
        model = models.Response
        fields = ("project", "answer_type")

    def filter_project(self, queryset, name, value):
        if value:
            queryset = queryset.filter(evaluation__phase__project=value)
        return queryset

    def filter_answer_type(self, queryset, name, value):
        if value:
            queryset = queryset.filter(question__answer_type=value)
        return queryset


class ProjectFilter(FilterSet):
    country_code = CharFilter(field_name="country_code", lookup_expr="contains")

    class Meta:
        model = models.Project
        fields = [
            "name",
            "collaboration__structure",
            "keywords",
            "participants",
            "knowledge_area",
            "project_type",
        ]


class StructureFilter(FilterSet):
    country_code = CharFilter(field_name="country_code", lookup_expr="contains")
    knowledge_areas = CharInFilter(field_name="knowledge_areas")

    class Meta:
        model = models.Structure
        fields = [
            "name",
            "collaboration__project",
            "managers",
            "structure_type",
        ]
