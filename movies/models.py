"""
Movie Models for Nexus Movie Recommendation Platform

Core database models for managing movies, genres, and user interactions
with TMDb API integration.

Models:
- Genre: Movie categories from TMDb
- Movie: Core movie data with TMDb sync
- FavoriteMovie: User favorites tracking
- TrendingMovie: Trending analytics data
"""

from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """Movie genres from TMDb API"""
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    """Core movie model with TMDb API integration"""
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre, blank=True, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-vote_average', '-vote_count']
    
    def __str__(self):
        year = self.release_date.year if self.release_date else 'TBA'
        return f"{self.title} ({year})"
    
    @property
    def poster_url(self):
        """Return full TMDb poster URL"""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None
    
    @property
    def backdrop_url(self):
        """Return full TMDb backdrop URL"""
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280{self.backdrop_path}"
        return None

class FavoriteMovie(models.Model):
    """Junction table for user's favorite movies"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} ♥ {self.movie.title}"

class TrendingMovie(models.Model):
    """Track trending movies by day/week for analytics"""
    TRENDING_PERIOD_CHOICES = [
        ('day', 'Daily'),
        ('week', 'Weekly'),
    ]
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='trending_periods')
    period = models.CharField(max_length=10, choices=TRENDING_PERIOD_CHOICES)
    trending_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('movie', 'period', 'trending_date')
        ordering = ['-trending_date']
    
    def __str__(self):
        return f"{self.movie.title} - Trending {self.get_period_display()} ({self.trending_date})"