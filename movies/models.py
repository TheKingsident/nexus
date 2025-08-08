from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    """Movie genres from TMDb"""
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    """Basic movie model from TMDb API"""
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    
    # TMDb specific fields
    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    
    # Relationships
    genres = models.ManyToManyField(Genre, blank=True, related_name='movies')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-vote_average', '-vote_count']
    
    def __str__(self):
        return f"{self.title} ({self.release_date.year if self.release_date else 'TBA'})"
    
    @property
    def poster_url(self):
        """Return full poster URL"""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None

class FavoriteMovie(models.Model):
    """User's favorite movies"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class TrendingMovie(models.Model):
    """Track trending movies by day/week"""
    TRENDING_PERIOD_CHOICES = [
        ('day', 'Day'),
        ('week', 'Week'),
    ]
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='trending_periods')
    period = models.CharField(max_length=10, choices=TRENDING_PERIOD_CHOICES)
    trending_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('movie', 'period', 'trending_date')
        ordering = ['-trending_date']
    
    def __str__(self):
        return f"{self.movie.title} - Trending {self.period} ({self.trending_date})"