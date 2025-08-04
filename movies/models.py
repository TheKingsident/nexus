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
    backdrop_path = models.CharField(max_length=255, blank=True)
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
