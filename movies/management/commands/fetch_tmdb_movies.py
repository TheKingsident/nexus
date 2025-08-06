import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie, Genre
import os

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_BASE_URL = os.environ.get('TMDB_BASE_URL')

class Command(BaseCommand):
    help = 'Fetches popular movies from TMDb and saves them to the database'

    def handle(self, *args, **options):
        url = f"{TMDB_BASE_URL}/movie/popular"
        params = {'api_key': TMDB_API_KEY, 'language': 'en-US', 'page': 1}
        response = requests.get(url, params=params)
        data = response.json()

        for movie_data in data.get('results', []):
            genre_objs = []
            for genre_id in movie_data.get('genre_ids', []):
                genre_url = f"{TMDB_BASE_URL}/genre/movie/list"
                genre_resp = requests.get(genre_url, params={'api_key': TMDB_API_KEY, 'language': 'en-US'})
                genres = genre_resp.json().get('genres', [])
                for g in genres:
                    if g['id'] == genre_id:
                        genre_obj, _ = Genre.objects.get_or_create(tmdb_id=g['id'], name=g['name'])
                        genre_objs.append(genre_obj)

            movie, created = Movie.objects.get_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'overview': movie_data.get('overview', ''),
                    'release_date': movie_data.get('release_date', None),
                    'poster_path': movie_data.get('poster_path', ''),
                    'backdrop_path': movie_data.get('backdrop_path', ''),
                    'vote_average': movie_data.get('vote_average', 0.0),
                    'vote_count': movie_data.get('vote_count', 0),
                }
            )
            if created:
                movie.genres.set(genre_objs)
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Added movie: {movie.title}"))
            else:
                self.stdout.write(f"Movie already exists: {movie.title}")
