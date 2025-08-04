from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'tmdb_id', 'movie_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def movie_count(self, obj):
        return obj.movies.count()
    movie_count.short_description = 'Movies Count'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'release_date', 'vote_average', 'vote_count',
        'poster_image', 'created_at'
    )
    list_filter = ('release_date', 'genres')
    search_fields = ('title', 'overview')
    ordering = ('-vote_average', '-vote_count')
    filter_horizontal = ('genres',)
    readonly_fields = ('tmdb_id', 'poster_image', 'backdrop_image', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'tmdb_id', 'title', 'overview', 'release_date'
            )
        }),
        ('TMDb Data', {
            'fields': (
                'poster_path', 'poster_image', 'backdrop_path', 'backdrop_image',
                'vote_average', 'vote_count'
            )
        }),
        ('Categories', {
            'fields': ('genres',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def poster_image(self, obj):
        if obj.poster_path:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                obj.poster_url
            )
        return "No image"
    poster_image.short_description = 'Poster'
    
    def backdrop_image(self, obj):
        if obj.backdrop_path:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                f"https://image.tmdb.org/t/p/w1280{obj.backdrop_path}"
            )
        return "No image"
    backdrop_image.short_description = 'Backdrop'
