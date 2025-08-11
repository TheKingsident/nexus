from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Genre, Movie, FavoriteMovie
from .serializers import GenreSerializer, MovieSerializer, MovieListSerializer, FavoriteMovieSerializer
from .filters import MovieFilter
from datetime import timedelta
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(60 * 60), name='dispatch')
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


@method_decorator(cache_page(60 * 30), name='dispatch')
class PopularMoviesView(generics.ListAPIView):
    """Get popular movies (high vote average and count)"""
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None  # Disable pagination for this view
    
    def get_queryset(self):
        return Movie.objects.filter(
            vote_count__gte=100,  # At least 100 votes
            vote_average__gte=6.0  # At least 6.0 rating
        ).order_by('-vote_average', '-vote_count')[:20]


class TopRatedMoviesView(generics.ListAPIView):
    """Get top rated movies"""
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        return Movie.objects.filter(
            vote_count__gte=50
        ).order_by('-vote_average', '-vote_count')[:20]


class UpcomingMoviesView(generics.ListAPIView):
    """Get upcoming movies"""
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        return Movie.objects.filter(
            release_date__gte=timezone.now().date()
        ).order_by('release_date')[:20]


class NowPlayingMoviesView(generics.ListAPIView):
    """Get now playing movies (recently released)"""
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        # Movies released in the last 6 months
        six_months_ago = timezone.now().date() - timedelta(days=180)
        return Movie.objects.filter(
            release_date__gte=six_months_ago,
            release_date__lte=timezone.now().date()
        ).order_by('-release_date')[:20]


class RecentMoviesView(generics.ListAPIView):
    """Get recently added movies to our database"""
    serializer_class = MovieListSerializer
    permission_classes = []
    
    def get_queryset(self):
        return Movie.objects.order_by('-created_at')[:20]


class FavoriteMoviesView(generics.ListAPIView):
    """List user's favorite movies"""
    serializer_class = MovieListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = []  # Disable filtering to avoid the queryset issue

    def get_queryset(self):
        user = self.request.user
        # Get the movie IDs from user's favorites
        favorite_movie_ids = FavoriteMovie.objects.filter(user=user).values_list('movie_id', flat=True)
        # Return a proper QuerySet of Movie objects
        return Movie.objects.filter(id__in=favorite_movie_ids).select_related().prefetch_related('genres')


@method_decorator(cache_page(60 * 5), name='dispatch')
class TrendingDayMoviesView(generics.ListAPIView):
    """Get trending movies today"""
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        # Return movies with high recent vote activity (proxy for trending)
        return Movie.objects.filter(
            vote_count__gte=50,
            created_at__gte=timezone.now() - timedelta(days=7)  # Recently added
        ).order_by('-vote_average', '-vote_count')[:20]


class TrendingWeekMoviesView(generics.ListAPIView):
    """Get trending movies this week"""
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        # Return movies with high vote counts and ratings (proxy for trending)
        return Movie.objects.filter(
            vote_count__gte=100,
            created_at__gte=timezone.now() - timedelta(days=30)  # Recently added
        ).order_by('-vote_count', '-vote_average')[:20]


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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, movie_id):
    """Add movie to user's favorites"""
    try:
        movie = Movie.objects.get(id=movie_id)
        favorite, created = FavoriteMovie.objects.get_or_create(
            user=request.user, 
            movie=movie
        )
        if created:
            return Response({'message': 'Movie added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Movie already in favorites'}, status=status.HTTP_200_OK)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, movie_id):
    """Remove movie from user's favorites"""
    try:
        favorite = FavoriteMovie.objects.get(user=request.user, movie_id=movie_id)
        favorite.delete()
        return Response({'message': 'Movie removed from favorites'}, status=status.HTTP_200_OK)
    except FavoriteMovie.DoesNotExist:
        return Response({'error': 'Movie not in favorites'}, status=status.HTTP_404_NOT_FOUND)
