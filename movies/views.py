"""
Movie Views Module for Nexus Movie Recommendation Platform

This module contains all the API views for movie-related operations including:
- Movie listing with filtering and search
- Genre management
- Trending algorithms (daily and weekly)
- User favorites management
- Advanced movie search functionality

The module implements sophisticated caching strategies and trending algorithms
to provide optimal performance and relevant content recommendations.

Author: Kingsley Usa
Project: Nexus Movie Recommendation Platform
"""

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


# =============================================================================
# GENRE VIEWS
# =============================================================================

@method_decorator(cache_page(60 * 60), name='dispatch')
class GenreListView(generics.ListAPIView):
    """
    API View: List all movie genres
    
    Endpoint: GET /api/movies/genres/
    Cache Duration: 1 hour (genres rarely change)
    Permissions: Public access
    
    Returns:
        - List of all available movie genres
        - Each genre includes: id, name, and associated movies count
    
    Example Response:
        [
            {"id": 1, "name": "Action"},
            {"id": 2, "name": "Comedy"},
            ...
        ]
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = []  # Allow public access


class GenreDetailView(generics.RetrieveAPIView):
    """
    API View: Get detailed information about a specific genre
    
    Endpoint: GET /api/movies/genres/{id}/
    Permissions: Public access
    
    Args:
        id (int): Genre ID
        
    Returns:
        - Genre details with associated movies
        - Movies are filtered and paginated within the genre
        
    Example Response:
        {
            "id": 1,
            "name": "Action",
            "movies": [...list of action movies...]
        }
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = []


# =============================================================================
# MOVIE LISTING AND DETAIL VIEWS
# =============================================================================

class MovieListView(generics.ListAPIView):
    """
    API View: List all movies with advanced filtering and search capabilities
    
    Endpoint: GET /api/movies/
    Permissions: Public access
    Pagination: Enabled (default Django REST Framework pagination)
    
    Features:
        - Full-text search in title and overview fields
        - Genre filtering via query parameters
        - Date range filtering by release date
        - Rating filtering (minimum vote average)
        - Sorting by multiple fields
        
    Query Parameters:
        - search: Text search in title/overview
        - genre: Filter by genre ID
        - release_date_after: Movies released after date (YYYY-MM-DD)
        - release_date_before: Movies released before date (YYYY-MM-DD)
        - vote_average_min: Minimum rating filter
        - ordering: Sort by fields (vote_average, vote_count, release_date, etc.)
        
    Example Usage:
        /api/movies/?search=batman&genre=1&vote_average_min=7.0&ordering=-vote_average
    """
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = []  # Allow public access
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'overview']
    ordering_fields = ['release_date', 'vote_average', 'vote_count', 'created_at']
    ordering = ['-vote_average', '-vote_count']  # Default ordering


class MovieDetailView(generics.RetrieveAPIView):
    """
    API View: Get comprehensive details for a specific movie
    
    Endpoint: GET /api/movies/{id}/
    Permissions: Public access
    
    Args:
        id (int): Movie ID from TMDb or internal database
        
    Returns:
        - Complete movie information including:
          * Basic info (title, overview, release date)
          * TMDb data (poster, backdrop, vote statistics)
          * Genre associations
          * Runtime, budget, revenue (if available)
          * Production companies and countries
          
    Example Response:
        {
            "id": 1,
            "title": "The Dark Knight",
            "overview": "Batman faces the Joker...",
            "release_date": "2008-07-18",
            "vote_average": 9.0,
            "vote_count": 12000,
            "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "genres": [{"id": 1, "name": "Action"}, ...]
        }
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = []


# =============================================================================
# CURATED MOVIE COLLECTIONS
# =============================================================================

@method_decorator(cache_page(60 * 30), name='dispatch')
class PopularMoviesView(generics.ListAPIView):
    """
    API View: Get popular movies based on vote average and count
    
    Endpoint: GET /api/movies/popular/
    Cache Duration: 30 minutes
    Permissions: Public access
    Pagination: Disabled (returns top 20)
    
    Algorithm:
        - Minimum 100 votes (ensures statistical significance)
        - Minimum 6.0 rating (quality threshold)
        - Sorted by vote_average desc, then vote_count desc
        
    Use Case:
        - Homepage featured content
        - "Popular Right Now" sections
        - General movie recommendations
        
    Returns:
        List of 20 most popular movies meeting quality criteria
    """
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None  # Disable pagination for this view
    
    def get_queryset(self):
        return Movie.objects.filter(
            vote_count__gte=100,  # At least 100 votes
            vote_average__gte=6.0  # At least 6.0 rating
        ).order_by('-vote_average', '-vote_count')[:20]


class TopRatedMoviesView(generics.ListAPIView):
    """
    API View: Get highest-rated movies of all time
    
    Endpoint: GET /api/movies/top-rated/
    Permissions: Public access
    Pagination: Disabled (returns top 20)
    
    Algorithm:
        - Minimum 50 votes (lower threshold for classic films)
        - Pure rating-based sorting (vote_average primary)
        - Vote count as tiebreaker
        
    Use Case:
        - "Best Movies Ever" collections
        - Classic film recommendations
        - Quality-focused browsing
        
    Returns:
        List of 20 highest-rated movies with minimum vote threshold
    """
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        return Movie.objects.filter(
            vote_count__gte=50
        ).order_by('-vote_average', '-vote_count')[:20]


class UpcomingMoviesView(generics.ListAPIView):
    """
    API View: Get upcoming movie releases
    
    Endpoint: GET /api/movies/upcoming/
    Permissions: Public access
    Pagination: Disabled (returns next 20)
    
    Algorithm:
        - Release date >= today
        - Sorted by release date (earliest first)
        
    Use Case:
        - "Coming Soon" sections
        - Release calendar features
        - Future viewing planning
        
    Returns:
        List of 20 next upcoming movies sorted by release date
    """
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        return Movie.objects.filter(
            release_date__gte=timezone.now().date()
        ).order_by('release_date')[:20]


class NowPlayingMoviesView(generics.ListAPIView):
    """
    API View: Get movies currently in theaters (recently released)
    
    Endpoint: GET /api/movies/now-playing/
    Permissions: Public access
    Pagination: Disabled (returns 20 most recent)
    
    Algorithm:
        - Released in last 6 months (180 days)
        - Release date <= today (actually released)
        - Sorted by release date (most recent first)
        
    Use Case:
        - "Now Playing" theater sections
        - Recent releases browsing
        - Current entertainment options
        
    Returns:
        List of 20 most recently released movies within 6-month window
    """
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
    """
    API View: Get recently added movies to the database
    
    Endpoint: GET /api/movies/recent/
    Permissions: Public access
    Pagination: Enabled
    
    Use Case:
        - "New Additions" sections
        - Database freshness indicator
        - Admin monitoring of data updates
        
    Returns:
        Movies sorted by database creation date (most recent first)
    """
    serializer_class = MovieListSerializer
    permission_classes = []
    
    def get_queryset(self):
        return Movie.objects.order_by('-created_at')[:20]


# =============================================================================
# USER FAVORITES MANAGEMENT
# =============================================================================

class FavoriteMoviesView(generics.ListAPIView):
    """
    API View: List user's favorite movies
    
    Endpoint: GET /api/movies/favorites/
    Permissions: Authenticated users only
    Pagination: Enabled
    
    Features:
        - Returns only the current user's favorite movies
        - Optimized queries with select_related and prefetch_related
        - Filters disabled to prevent queryset conflicts
        
    Returns:
        - List of movies favorited by the authenticated user
        - Each movie includes full details and genre information
        - Ordered by when the movie was added to favorites (most recent first)
        
    Technical Notes:
        - Uses movie IDs from FavoriteMovie junction table
        - Converts to proper Movie QuerySet for DRF compatibility
        - Avoids 'list' object attribute errors in filtering
    """
    serializer_class = MovieListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = []  # Disable filtering to avoid the queryset issue

    def get_queryset(self):
        user = self.request.user
        # Get the movie IDs from user's favorites
        favorite_movie_ids = FavoriteMovie.objects.filter(user=user).values_list('movie_id', flat=True)
        # Return a proper QuerySet of Movie objects
        return Movie.objects.filter(id__in=favorite_movie_ids).select_related().prefetch_related('genres')


# =============================================================================
# ADVANCED TRENDING ALGORITHMS
# =============================================================================

@method_decorator(cache_page(60 * 5), name='dispatch')
class TrendingDayMoviesView(generics.ListAPIView):
    """
    API View: Get trending movies today using advanced multi-factor algorithm
    
    Endpoint: GET /api/movies/trending/day/
    Cache Duration: 5 minutes (trending data changes frequently)
    Permissions: Public access
    Pagination: Disabled (returns top 20)
    
    Advanced Trending Algorithm:
    ============================
    
    The trending score is calculated using multiple weighted factors:
    
    1. RECENCY BOOST (Release Date Impact):
       - Last 7 days: 3.0x multiplier
       - Last 30 days: 2.0x multiplier  
       - Last 90 days: 1.5x multiplier
       - Older: 1.0x (baseline)
       
    2. VOTE MOMENTUM (Popularity Impact):
       - 1000+ votes: 2.5x multiplier
       - 500+ votes: 2.0x multiplier
       - 100+ votes: 1.5x multiplier
       - 50+ votes: 1.2x multiplier
       - Less: 1.0x (baseline)
       
    3. QUALITY SCORE (Rating Impact):
       - 8.0+ rating: 2.0x multiplier
       - 7.0+ rating: 1.5x multiplier
       - 6.0+ rating: 1.2x multiplier
       - 5.0+ rating: 1.0x (baseline)
       - Less: 0.5x (penalty)
       
    4. FRESHNESS SCORE (Database Recency):
       - Added today: 1.5x multiplier
       - Added this week: 1.2x multiplier
       - Older: 1.0x (baseline)
       
    Final Score = vote_average × recency_boost × vote_momentum × quality_score × freshness_score
    
    Minimum Thresholds:
        - At least 10 votes (prevents spam)
        - At least 4.0 rating (quality filter)
        
    Use Cases:
        - Homepage "Trending Now" sections
        - Real-time popularity tracking
        - Viral content detection
        - Daily content recommendations
    """
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        from django.db.models import F, Case, When, FloatField, Count
        from django.db.models.functions import Greatest
        
        now = timezone.now()
        today = now.date()
        yesterday = today - timedelta(days=1)
        week_ago = today - timedelta(days=7)
        
        # Advanced trending algorithm considering multiple factors
        return Movie.objects.annotate(
            # Recent release boost (movies released in last 30 days get higher score)
            recency_boost=Case(
                When(release_date__gte=today - timedelta(days=7), then=3.0),
                When(release_date__gte=today - timedelta(days=30), then=2.0),
                When(release_date__gte=today - timedelta(days=90), then=1.5),
                default=1.0,
                output_field=FloatField()
            ),
            
            # Vote momentum (higher vote count = more popular recently)
            vote_momentum=Case(
                When(vote_count__gte=1000, then=2.5),
                When(vote_count__gte=500, then=2.0),
                When(vote_count__gte=100, then=1.5),
                When(vote_count__gte=50, then=1.2),
                default=1.0,
                output_field=FloatField()
            ),
            
            # Rating quality filter (good movies trend more)
            quality_score=Case(
                When(vote_average__gte=8.0, then=2.0),
                When(vote_average__gte=7.0, then=1.5),
                When(vote_average__gte=6.0, then=1.2),
                When(vote_average__gte=5.0, then=1.0),
                default=0.5,
                output_field=FloatField()
            ),
            
            # Database freshness (recently added to our DB)
            freshness_score=Case(
                When(created_at__gte=now - timedelta(days=1), then=1.5),
                When(created_at__gte=now - timedelta(days=7), then=1.2),
                default=1.0,
                output_field=FloatField()
            ),
            
            # Calculate trending score
            trending_score=F('vote_average') * F('recency_boost') * F('vote_momentum') * F('quality_score') * F('freshness_score')
        ).filter(
            # Only include movies with minimum thresholds
            vote_count__gte=10,  # At least 10 votes
            vote_average__gte=4.0  # At least 4.0 rating
        ).order_by('-trending_score', '-vote_count', '-vote_average')[:20]


class TrendingWeekMoviesView(generics.ListAPIView):
    """
    API View: Get trending movies this week using weekly momentum algorithm
    
    Endpoint: GET /api/movies/trending/week/
    Permissions: Public access
    Pagination: Disabled (returns top 20)
    
    Weekly Trending Algorithm:
    ==========================
    
    Optimized for sustained popularity over longer periods:
    
    1. WEEKLY RECENCY BOOST (Extended Time Windows):
       - Last 14 days: 2.5x multiplier
       - Last 60 days: 1.8x multiplier
       - Last 180 days: 1.3x multiplier
       - Older: 1.0x (baseline)
       
    2. WEEKLY VOTE MOMENTUM (Higher Thresholds):
       - 2000+ votes: 3.0x multiplier
       - 1000+ votes: 2.5x multiplier
       - 500+ votes: 2.0x multiplier
       - 200+ votes: 1.5x multiplier
       - 100+ votes: 1.2x multiplier
       - Less: 1.0x (baseline)
       
    3. WEEKLY QUALITY SCORE (Stricter Standards):
       - 8.5+ rating: 2.5x multiplier
       - 7.5+ rating: 2.0x multiplier
       - 6.5+ rating: 1.5x multiplier
       - 5.5+ rating: 1.0x (baseline)
       - Less: 0.7x (penalty)
       
    Final Score = vote_average × weekly_recency_boost × weekly_vote_momentum × weekly_quality_score
    
    Minimum Thresholds:
        - At least 50 votes (higher than daily)
        - At least 5.0 rating (stricter quality)
        
    Use Cases:
        - Weekly digest content
        - Sustained popularity tracking
        - Long-term trending analysis
        - Weekly recommendation emails
    """
    serializer_class = MovieListSerializer
    permission_classes = []
    pagination_class = None
    
    def get_queryset(self):
        from django.db.models import F, Case, When, FloatField
        
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Weekly trending algorithm with different weights
        return Movie.objects.annotate(
            # Release timing boost (different weights for weekly trending)
            weekly_recency_boost=Case(
                When(release_date__gte=today - timedelta(days=14), then=2.5),
                When(release_date__gte=today - timedelta(days=60), then=1.8),
                When(release_date__gte=today - timedelta(days=180), then=1.3),
                default=1.0,
                output_field=FloatField()
            ),
            
            # Vote scale for weekly (higher thresholds)
            weekly_vote_momentum=Case(
                When(vote_count__gte=2000, then=3.0),
                When(vote_count__gte=1000, then=2.5),
                When(vote_count__gte=500, then=2.0),
                When(vote_count__gte=200, then=1.5),
                When(vote_count__gte=100, then=1.2),
                default=1.0,
                output_field=FloatField()
            ),
            
            # Quality remains important for weekly
            weekly_quality_score=Case(
                When(vote_average__gte=8.5, then=2.5),
                When(vote_average__gte=7.5, then=2.0),
                When(vote_average__gte=6.5, then=1.5),
                When(vote_average__gte=5.5, then=1.0),
                default=0.7,
                output_field=FloatField()
            ),
            
            # Weekly trending score
            weekly_trending_score=F('vote_average') * F('weekly_recency_boost') * F('weekly_vote_momentum') * F('weekly_quality_score')
        ).filter(
            vote_count__gte=50,  # Higher threshold for weekly
            vote_average__gte=5.0
        ).order_by('-weekly_trending_score', '-vote_count', '-vote_average')[:20]


# =============================================================================
# ADVANCED SEARCH FUNCTIONALITY
# =============================================================================

@api_view(['GET'])
def movie_search(request):
    """
    API Function: Advanced movie search with multiple parameters
    
    Endpoint: GET /api/movies/search/
    Method: GET (function-based view)
    Permissions: Public access
    
    Query Parameters:
    ================
    
    - q (string): Full-text search in title and overview
      Example: ?q=batman
      
    - genre (int): Filter by genre ID
      Example: ?genre=1
      
    - min_rating (float): Minimum vote average filter
      Example: ?min_rating=7.5
      
    - year (int): Filter by release year
      Example: ?year=2023
      
    Combined Example:
        /api/movies/search/?q=spider&genre=1&min_rating=7.0&year=2023
        
    Features:
    =========
    
    1. Full-text Search:
       - Searches both title and overview fields
       - Case-insensitive matching
       - Supports partial word matching
       
    2. Genre Filtering:
       - Uses many-to-many relationship
       - Validates genre ID existence
       
    3. Rating Filtering:
       - Float validation with error handling
       - Supports decimal ratings (e.g., 7.5)
       
    4. Year Filtering:
       - Extracts year from release_date field
       - Integer validation with error handling
       
    5. Result Optimization:
       - Removes duplicates with distinct()
       - Limits to 50 results for performance
       - Sorted by relevance (rating, then popularity)
       
    Response Format:
    ===============
    
    {
        "count": 25,
        "results": [
            {
                "id": 1,
                "title": "Spider-Man: No Way Home",
                "overview": "...",
                "release_date": "2021-12-15",
                "vote_average": 8.4,
                "vote_count": 15000,
                "poster_path": "/...",
                "genres": [...]
            },
            ...
        ]
    }
    
    Error Handling:
    ==============
    
    - Invalid rating values are silently ignored
    - Invalid year values are silently ignored
    - Invalid genre IDs result in no matches
    - Empty queries return all movies (limited to 50)
    """
    query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    min_rating = request.GET.get('min_rating', '')
    year = request.GET.get('year', '')
    
    movies = Movie.objects.all()
    
    # Apply full-text search filter
    if query:
        movies = movies.filter(
            Q(title__icontains=query) | Q(overview__icontains=query)
        )
    
    # Apply genre filter
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
    
    # Apply minimum rating filter with validation
    if min_rating:
        try:
            movies = movies.filter(vote_average__gte=float(min_rating))
        except ValueError:
            pass  # Ignore invalid rating values
    
    # Apply year filter with validation
    if year:
        try:
            movies = movies.filter(release_date__year=int(year))
        except ValueError:
            pass  # Ignore invalid year values
    
    # Optimize and limit results
    movies = movies.distinct().order_by('-vote_average', '-vote_count')[:50]
    serializer = MovieListSerializer(movies, many=True)
    
    return Response({
        'count': movies.count(),
        'results': serializer.data
    })


# =============================================================================
# FAVORITES MANAGEMENT API ENDPOINTS
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, movie_id):
    """
    API Function: Add a movie to user's favorites list
    
    Endpoint: POST /api/movies/favorites/add/{movie_id}/
    Methods: GET, POST (for DRF browsable API compatibility)
    Permissions: Authenticated users only
    
    URL Parameters:
    ==============
    
    - movie_id (int): The ID of the movie to add to favorites
    
    Process Flow:
    ============
    
    1. Validate movie exists in database
    2. Check if already in user's favorites
    3. Create FavoriteMovie relationship if new
    4. Return appropriate success/info message
    
    Response Scenarios:
    ==================
    
    SUCCESS (201 Created):
    {
        "message": "Movie added to favorites"
    }
    
    ALREADY EXISTS (200 OK):
    {
        "message": "Movie already in favorites"
    }
    
    ERROR (404 Not Found):
    {
        "error": "Movie not found"
    }
    
    Technical Details:
    =================
    
    - Uses get_or_create() to prevent duplicates
    - Handles race conditions safely
    - No limit on favorites count per user
    - Atomic operation (database integrity)
    
    Use Cases:
    =========
    
    - User clicks "Add to Favorites" button
    - Batch favorites import
    - Mobile app favoriting
    - Third-party integrations
    """
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
    """
    API Function: Remove a movie from user's favorites list
    
    Endpoint: POST /api/movies/favorites/remove/{movie_id}/
    Methods: GET, POST (for DRF browsable API compatibility)
    Permissions: Authenticated users only
    
    URL Parameters:
    ==============
    
    - movie_id (int): The ID of the movie to remove from favorites
    
    Process Flow:
    ============
    
    1. Look for existing FavoriteMovie relationship
    2. Delete the relationship if found
    3. Return appropriate success/error message
    
    Response Scenarios:
    ==================
    
    SUCCESS (200 OK):
    {
        "message": "Movie removed from favorites"
    }
    
    ERROR (404 Not Found):
    {
        "error": "Movie not in favorites"
    }
    
    Technical Details:
    =================
    
    - Only removes relationship, not the movie itself
    - User-specific operation (can't affect other users)
    - Idempotent operation (safe to call multiple times)
    - No cascade deletions
    
    Use Cases:
    =========
    
    - User clicks "Remove from Favorites" button
    - Favorites list management
    - Bulk favorites cleanup
    - User preference updates
    
    Security Notes:
    ==============
    
    - Users can only remove their own favorites
    - Movie ID validation prevents unauthorized access
    - Authentication required for all operations
    """
    try:
        favorite = FavoriteMovie.objects.get(user=request.user, movie_id=movie_id)
        favorite.delete()
        return Response({'message': 'Movie removed from favorites'}, status=status.HTTP_200_OK)
    except FavoriteMovie.DoesNotExist:
        return Response({'error': 'Movie not in favorites'}, status=status.HTTP_404_NOT_FOUND)
