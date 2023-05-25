# from django.forms import DateInput, SelectDateWidget
from django_filters import FilterSet, DateFromToRangeFilter, ModelChoiceFilter, CharFilter
from django_filters.widgets import RangeWidget

from .models import Article
from django.contrib.auth.models import User


class ArticleFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        lookup_expr='exact',
        label=('Автор'),
        empty_label='Все авторы'
    )

    title = CharFilter(
        lookup_expr='icontains',
        label='Заголовок содержит',
    )

    text = CharFilter(
        lookup_expr='icontains',
        label='Объявление содержит',
    )

    publication_date = DateFromToRangeFilter(
        label='Период публикации',
        widget=RangeWidget(attrs={'type': 'date'}),
    )

    class Meta:
        model = Article
        fields = {
            'category': ['exact']
        }

#
# class ArticleResponseFilter(FilterSet):
#     article = django_filters.ModelChoiceFilter(
#         field_name='articles',
#         queryset=None,
#         label='',
#         empty_label='Выбрать заголовок',
#     )