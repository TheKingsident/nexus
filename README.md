# Nexus - Movie Recommendation Platform (Backend)

A Django REST API backend for a movie recommendation platform that integrates with The Movie Database (TMDb) API to provide movie data, user authentication, and personalized recommendations.

## Features

### Movies
- Fetch and store movie data from TMDb API
- Movie search and filtering by genre, rating, year
- Popular and recently added movies endpoints
- Movie details with posters and metadata

### User Management
- User registration with email uniqueness validation
- Token-based authentication
- User profiles with bio and date of birth
- Async welcome email notifications via Celery

### User Interactions
- Add/remove movies to/from favorites
- User-specific favorite movies listing

### Technical Features
- PostgreSQL database integration
- Swagger/OpenAPI documentation
- CORS support for frontend integration
- Celery task queue with RabbitMQ
- Email notifications via Zoho SMTP
- Django admin interface

## Requirements

- Python 3.10+
- PostgreSQL
- RabbitMQ (for Celery tasks)
- TMDb API key

## Installation

1. **Clone the repository:**
```bash
git clone git@github.com:TheKingsident/nexus.git
cd nexus
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Environment setup:**
```bash
cp .env.example .env
# Edit .env with your actual values
```

5. **Database setup:**
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE nexus_db;
CREATE USER nexus_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE nexus_db TO nexus_user;
\q

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=db_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# TMDb API
TMDB_API_KEY=your_tmdb_api_key
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p

# Email Settings (Zoho)
DEFAULT_FROM_EMAIL=your_email@domain.com
EMAIL_HOST=smtp.zoho.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
```

## Running the Application

1. **Start Django development server:**
```bash
python manage.py runserver
```

2. **Start RabbitMQ (for Celery tasks):**
```bash
sudo systemctl start rabbitmq-server
```

3. **Start Celery worker (in separate terminal):**
```bash
celery -A nexus worker --loglevel=info
```

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
The API uses Token-based authentication. Include the token in headers:
```
Authorization: Token your_auth_token
```

### Main Endpoints

#### Movies
- `GET /api/movies/` - List movies (with filtering)
- `GET /api/movies/{id}/` - Movie details
- `GET /api/movies/popular/` - Popular movies
- `GET /api/movies/recent/` - Recently added movies
- `GET /api/search/` - Advanced movie search

#### Genres
- `GET /api/genres/` - List all genres
- `GET /api/genres/{id}/` - Genre details

#### Users
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout
- `GET /api/users/me/` - Current user info
- `GET/PUT /api/users/profile/` - User profile

#### Favorites
- `GET /api/favorites/` - User's favorite movies
- `POST /api/favorites/add/{movie_id}/` - Add to favorites
- `DELETE /api/favorites/remove/{movie_id}/` - Remove from favorites

### Interactive Documentation
- **Swagger UI:** http://localhost:8000/swagger/
- **ReDoc:** http://localhost:8000/redoc/

## 🎬 Populating Movie Data

Fetch movies from TMDb API:
```bash
python manage.py fetch_tmdb_movies
```

## Testing

### Manual API Testing

1. **Register a user:**
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

2. **Login:**
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

3. **Get movies:**
```bash
curl -X GET http://localhost:8000/api/movies/ \
  -H "Authorization: Token your_token"
```

## Technology Stack

- **Backend:** Django 5.1, Django REST Framework
- **Database:** PostgreSQL
- **Task Queue:** Celery + RabbitMQ
- **External API:** TMDb (The Movie Database)
- **Email:** Zoho SMTP
- **Documentation:** drf-yasg (Swagger/OpenAPI)

## Project Structure

```
nexus/
├── nexus/              # Django project settings
│   ├── settings.py     # Main configuration
│   ├── urls.py         # URL routing
│   └── celery.py       # Celery configuration
├── movies/             # Movies app
│   ├── models.py       # Movie, Genre, FavoriteMovie models
│   ├── views.py        # API views
│   ├── serializers.py  # DRF serializers
│   ├── filters.py      # Custom filters
│   └── management/     # Management commands
├── users/              # Users app
│   ├── models.py       # UserProfile model
│   ├── views.py        # User authentication views
│   ├── serializers.py  # User serializers
│   └── tasks.py        # Celery tasks
├── requirements.txt    # Python dependencies
└── .env               # Environment variables
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email hello@kingsleyusa.dev or create an issue on GitHub.