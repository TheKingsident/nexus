import django_filters
from .models import Movie, Genre


class MovieFilter(django_filters.FilterSet):
    """Custom filter for movies"""
    title = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='release_date__year')
    min_rating = django_filters.NumberFilter(field_name='vote_average', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='vote_average', lookup_expr='lte')
    genre = django_filters.ModelChoiceFilter(
        field_name='genres',
        queryset=Genre.objects.all(),
        to_field_name='id'
    )
    
    class Meta:
        model = Movie
        fields = ['title', 'year', 'min_rating', 'max_rating', 'genre']
