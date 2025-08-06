from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Genre, Movie
from .serializers import GenreSerializer, MovieSerializer, MovieListSerializer
from .filters import MovieFilter


class GenreListView(generics.ListAPIView):
    """List all genres"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = []  # Allow public access


class GenreDetailView(generics.RetrieveAPIView):
    """Get a specific genre with its movies"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = []


class MovieListView(generics.ListAPIView):
    """List movies with filtering and search"""
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = []  # Allow public access
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'overview']
    ordering_fields = ['release_date', 'vote_average', 'vote_count', 'created_at']
    ordering = ['-vote_average', '-vote_count']


class MovieDetailView(generics.RetrieveAPIView):
    """Get detailed movie information"""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = []


class PopularMoviesView(generics.ListAPIView):
    """Get popular movies (high vote average and count)"""
    serializer_class = MovieListSerializer
    permission_classes = []
    
    def get_queryset(self):
        return Movie.objects.filter(
            vote_count__gte=100,  # At least 100 votes
            vote_average__gte=6.0  # At least 6.0 rating
        ).order_by('-vote_average', '-vote_count')[:20]


class RecentMoviesView(generics.ListAPIView):
    """Get recently added movies"""
    serializer_class = MovieListSerializer
    permission_classes = []
    
    def get_queryset(self):
        return Movie.objects.order_by('-created_at')[:20]


@api_view(['GET'])
def movie_search(request):
    """Advanced movie search"""
    query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    min_rating = request.GET.get('min_rating', '')
    year = request.GET.get('year', '')
    
    movies = Movie.objects.all()
    
    if query:
        movies = movies.filter(
            Q(title__icontains=query) | Q(overview__icontains=query)
        )
    
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
    
    if min_rating:
        try:
            movies = movies.filter(vote_average__gte=float(min_rating))
        except ValueError:
            pass
    
    if year:
        try:
            movies = movies.filter(release_date__year=int(year))
        except ValueError:
            pass
    
    movies = movies.distinct().order_by('-vote_average', '-vote_count')[:50]
    serializer = MovieListSerializer(movies, many=True)
    
    return Response({
        'count': movies.count(),
        'results': serializer.data
    })
