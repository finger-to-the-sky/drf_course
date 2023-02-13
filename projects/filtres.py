from django_filters import CharFilter, BooleanFilter, DateTimeFromToRangeFilter
from django_filters.rest_framework import FilterSet
from django_filters.widgets import RangeWidget, BooleanWidget

from projects.models import Project, ToDo


class ProjectFilter(FilterSet):
    name = CharFilter(lookup_expr='contains')

    class Meta:
        model = Project
        fields = ['name']


class ToDoFilter(FilterSet):
    project_id_name = CharFilter(lookup_expr='contains')
    created_at = DateTimeFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS'}))
    is_active = BooleanFilter(widget=BooleanWidget)

    class Meta:
        model = ToDo
        fields = ['project_id_name', 'created_at', 'is_active']