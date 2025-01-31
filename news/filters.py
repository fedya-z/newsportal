from django.forms import DateTimeInput, Select
from django_filters import FilterSet, CharFilter, DateTimeFilter, ChoiceFilter
from .models import Post, Category

class PostFilter(FilterSet):
    post_name = CharFilter(field_name='post_name', lookup_expr='icontains', label='Название')
    category = ChoiceFilter(
        field_name='category__category_name',
        label='Категория',
        choices=lambda: [(category.category_name, category.category_name) for category in Category.objects.all()],
        widget=Select(attrs={'class': 'form-control'}),
    )
    time_in_post = DateTimeFilter(
        field_name='added_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'post_name': ['icontains'],
            'category': ['exact'],
            'time_in_post': ['gte'],
        }