from django.urls import path
from .views import (
    GenreListView, GenreDetailView, MovieListView, MovieDetailView,
    PopularMoviesView, RecentMoviesView, movie_search,
    add_favorite, remove_favorite
)

app_name = 'movies'

urlpatterns = [
    # Genres
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    
    # Movies
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/popular/', PopularMoviesView.as_view(), name='popular-movies'),
    path('movies/recent/', RecentMoviesView.as_view(), name='recent-movies'),
    path('search/', movie_search, name='movie-search'),

    # Favorites
    path('favorites/add/<int:movie_id>/', add_favorite, name='add-favorite'),
    path('favorites/remove/<int:movie_id>/', remove_favorite, name='remove-favorite'),
]
