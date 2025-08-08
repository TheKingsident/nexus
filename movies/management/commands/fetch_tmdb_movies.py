import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre

TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_BASE_URL = settings.TMDB_BASE_URL

class Command(BaseCommand):
    help = 'Fetches movies from multiple TMDb endpoints and saves them to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            default=5,
            help='Number of pages to fetch from each endpoint (default: 5)'
        )

    def handle(self, *args, **options):
        pages = options['pages']
        
        # Define the endpoints to fetch from
        endpoints = [
            'movie/popular',
            'movie/top_rated', 
            'movie/upcoming',
            'movie/now_playing',
            'trending/movie/day',    # NEW: Trending today
            'trending/movie/week'    # NEW: Trending this week
        ]
        
        # First, fetch and cache genres
        self.fetch_genres()
        
        # Fetch movies from each endpoint
        for endpoint in endpoints:
            self.stdout.write(f"\nFetching movies from {endpoint}...")
            self.fetch_movies_from_endpoint(endpoint, pages)
        
        self.stdout.write(self.style.SUCCESS('\nCompleted fetching movies from all endpoints!'))

    def fetch_genres(self):
        """Fetch and store all movie genres"""
        self.stdout.write("Fetching genres...")
        url = f"{TMDB_BASE_URL}/genre/movie/list"
        params = {'api_key': TMDB_API_KEY, 'language': 'en-US'}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            genres_data = response.json().get('genres', [])
            
            for genre_data in genres_data:
                genre, created = Genre.objects.get_or_create(
                    tmdb_id=genre_data['id'],
                    defaults={'name': genre_data['name']}
                )
                if created:
                    self.stdout.write(f"Added genre: {genre.name}")
                    
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching genres: {e}"))

    def fetch_movies_from_endpoint(self, endpoint, pages):
        """Fetch movies from a specific TMDb endpoint"""
        movies_added = 0
        movies_updated = 0
        
        for page in range(1, pages + 1):
            url = f"{TMDB_BASE_URL}/{endpoint}"
            params = {
                'api_key': TMDB_API_KEY, 
                'language': 'en-US', 
                'page': page
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                for movie_data in data.get('results', []):
                    result = self.save_movie(movie_data)
                    if result == 'created':
                        movies_added += 1
                    elif result == 'updated':
                        movies_updated += 1
                        
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Error fetching {endpoint} page {page}: {e}"))
                continue
        
        self.stdout.write(
            f"From {endpoint}: {movies_added} new movies added, {movies_updated} movies updated"
        )

    def save_movie(self, movie_data):
        """Save or update a movie in the database"""
        # Get genres for this movie
        genre_objs = []
        for genre_id in movie_data.get('genre_ids', []):
            try:
                genre = Genre.objects.get(tmdb_id=genre_id)
                genre_objs.append(genre)
            except Genre.DoesNotExist:
                continue

        # Create or update movie
        movie, created = Movie.objects.update_or_create(
            tmdb_id=movie_data['id'],
            defaults={
                'title': movie_data['title'],
                'overview': movie_data.get('overview', ''),
                'release_date': movie_data.get('release_date', None) or None,
                'poster_path': movie_data.get('poster_path', ''),
                'backdrop_path': movie_data.get('backdrop_path', ''),
                'vote_average': movie_data.get('vote_average', 0.0),
                'vote_count': movie_data.get('vote_count', 0),
            }
        )
        
        # Set genres
        movie.genres.set(genre_objs)
        
        if created:
            self.stdout.write(f"Added: {movie.title}")
            return 'created'
        else:
            self.stdout.write(f"Updated: {movie.title}")
            return 'updated'
