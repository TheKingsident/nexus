from django.urls import path
from .views import (
    GenreListView, GenreDetailView, MovieListView, MovieDetailView,
    PopularMoviesView, TopRatedMoviesView, UpcomingMoviesView, NowPlayingMoviesView,
    TrendingDayMoviesView, TrendingWeekMoviesView,  # NEW
    RecentMoviesView, FavoriteMoviesView, movie_search,
    add_favorite, remove_favorite
)

app_name = 'movies'

urlpatterns = [
    # Genres
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    
    # Movies
    path('', MovieListView.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),

    # Movie Categories
    path('popular/', PopularMoviesView.as_view(), name='popular-movies'),
    path('top-rated/', TopRatedMoviesView.as_view(), name='top-rated-movies'),
    path('upcoming/', UpcomingMoviesView.as_view(), name='upcoming-movies'),
    path('now-playing/', NowPlayingMoviesView.as_view(), name='now-playing-movies'),
    path('trending/day/', TrendingDayMoviesView.as_view(), name='trending-day-movies'),      # NEW
    path('trending/week/', TrendingWeekMoviesView.as_view(), name='trending-week-movies'),   # NEW
    path('recent/', RecentMoviesView.as_view(), name='recent-movies'),
    
    # Search & Favorites
    path('search/', movie_search, name='movie-search'),
    path('favorites/', FavoriteMoviesView.as_view(), name='favorite-movies'),
    path('favorites/add/<int:movie_id>/', add_favorite, name='add-favorite'),
    path('favorites/remove/<int:movie_id>/', remove_favorite, name='remove-favorite'),
]
