# Nexus - Movie Recommendation Platform (Backend)

A Django REST API backend for a movie recommendation platform that integrates with The Movie Database (TMDb) API to provide movie data, user authentication.

## Running the Application

### 1. **Start all services:**

```bash
# Start Redis (if not already running)
sudo systemctl start redis-server

# Start RabbitMQ (if not already running)
sudo systemctl start rabbitmq-server

# Verify services are running
sudo systemctl status redis-server
sudo systemctl status rabbitmq-server
```

### 2. **Start Django development server:**
```bash
# Activate virtual environment
source venv/bin/activate

# Start Django server
python manage.py runserver
```

### 3. **Start Celery worker (in separate terminal):**
```bash
# Navigate to project directory and activate venv
cd /path/to/nexus
source venv/bin/activate

# Start Celery worker
celery -A nexus worker --loglevel=info
```

### 4. **Verify everything is working:**

- **Django**: http://localhost:8000/
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
- **Swagger**: http://localhost:8000/swagger/
- **Redis**: `redis-cli ping` (should return PONG)
- **Cache test**: 
  ```bash
  python manage.py shell
  from django.core.cache import cache
  cache.set('test', 'working', 60)
  print(cache.get('test'))
  ```sonalized recommendations.

## Features

### Movies
- Fetch and store movie data from multiple TMDb endpoints
- Movie search and filtering by genre, rating, year
- Popular, top-rated, upcoming, and now-playing movies endpoints
- Trending movies by day and week
- Movie details with posters and metadata
- Advanced search and filtering capabilities

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
- Redis caching for improved API performance
- Swagger/OpenAPI documentation
- CORS support for frontend integration
- Celery task queue with RabbitMQ
- Email notifications via Zoho SMTP
- Django admin interface
- Automated daily data synchronization with TMDb

## Requirements

- Python 3.10+
- PostgreSQL
- Redis (for caching)
- RabbitMQ (for Celery tasks)
- TMDb API key

## Installation

### 1. **System Dependencies**

#### Ubuntu/Debian:
```bash
# Update system packages
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Redis
sudo apt install redis-server

# Install RabbitMQ
sudo apt install rabbitmq-server

# Start services
sudo systemctl start postgresql
sudo systemctl start redis-server
sudo systemctl start rabbitmq-server

# Enable services to start on boot
sudo systemctl enable postgresql
sudo systemctl enable redis-server
sudo systemctl enable rabbitmq-server
```

### 2. **Project Setup**

```bash
# Clone the repository
git clone git@github.com:TheKingsident/nexus.git
cd nexus

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. **Environment Configuration**

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual values
nano .env
```

### 4. **Database Setup**

```bash
# Create PostgreSQL database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE nexus_db;
CREATE USER nexus_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE nexus_db TO nexus_user;
ALTER USER nexus_user CREATEDB;
\q
```

```bash
# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Create Django superuser
python manage.py createsuperuser
```

### 5. **Redis Verification**

```bash
# Test Redis connection
redis-cli ping
# Should return: PONG

# Test Redis with Django
python manage.py shell
```

```python
from django.core.cache import cache
cache.set('test', 'hello', 60)
print(cache.get('test'))  # Should print: hello
exit()
```

### 6. **TMDb Data Population**

```bash
# Fetch movies from TMDb (all categories)
python manage.py fetch_tmdb_movies --pages=5

# This will fetch from:
# - Popular movies
# - Top rated movies  
# - Upcoming movies
# - Now playing movies
# - Trending movies (day & week)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
### Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your_very_secure_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=nexus_db
DB_USER=nexus_user
DB_PASSWORD=your_secure_database_password
DB_HOST=localhost
DB_PORT=5432

# TMDb API Configuration
TMDB_API_KEY=your_tmdb_api_key_here
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p

# Email Settings (Zoho SMTP)
DEFAULT_FROM_EMAIL=your_email@domain.com
EMAIL_HOST=smtp.zoho.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_zoho_app_password
EMAIL_USE_TLS=True

# Redis Cache Configuration
REDIS_URL=redis://127.0.0.1:6379/1
```

**Important Notes:**
- Get your TMDb API key from: https://www.themoviedb.org/settings/api
- For Zoho email, use an App Password, not your regular password
- Generate a strong SECRET_KEY using: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

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
- `GET /api/movies/` - List all movies (with filtering & search)
- `GET /api/movies/{id}/` - Movie details
- `GET /api/movies/popular/` - Popular movies
- `GET /api/movies/top-rated/` - Top rated movies
- `GET /api/movies/upcoming/` - Upcoming movies
- `GET /api/movies/now-playing/` - Currently playing movies
- `GET /api/movies/trending/day/` - Trending movies today
- `GET /api/movies/trending/week/` - Trending movies this week
- `GET /api/movies/recent/` - Recently added movies

#### Genres
- `GET /api/genres/` - List all genres
- `GET /api/genres/{id}/` - Genre details with movies

#### Search
- `GET /api/search/` - Advanced movie search

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

## Data Management

### Populating Movie Data

The application fetches data from multiple TMDb endpoints:

```bash
# Fetch from all endpoints (recommended)
python manage.py fetch_tmdb_movies --pages=5

# This fetches from:
# - movie/popular
# - movie/top_rated
# - movie/upcoming  
# - movie/now_playing
# - trending/movie/day
# - trending/movie/week
```

### Automated Data Updates

For production, set up automated daily updates using cron:

```bash
# Edit crontab
crontab -e

# Add daily update at 6 AM
0 6 * * * cd /path/to/nexus && /path/to/nexus/venv/bin/python manage.py fetch_tmdb_movies --pages=5

# For more frequent trending updates
0 6,18 * * * cd /path/to/nexus && /path/to/nexus/venv/bin/python manage.py fetch_tmdb_movies --pages=3
```

### Cache Management

The application uses Redis caching for improved performance:

```bash
# Clear all cache
python manage.py shell
from django.core.cache import cache
cache.clear()

# Monitor cache usage
redis-cli info memory
redis-cli keys "*"
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

3. **Get movies (with filtering):**
```bash
# All movies
curl -X GET http://localhost:8000/api/movies/ \
  -H "Authorization: Token your_token"

# Popular movies
curl -X GET http://localhost:8000/api/movies/popular/

# Trending movies today
curl -X GET http://localhost:8000/api/movies/trending/day/

# Search movies
curl -X GET "http://localhost:8000/api/search/?q=avengers"

# Filter by genre
curl -X GET "http://localhost:8000/api/movies/?genres=28"
```

4. **Manage favorites:**
```bash
# Add to favorites
curl -X POST http://localhost:8000/api/favorites/add/123/ \
  -H "Authorization: Token your_token"

# Get user favorites
curl -X GET http://localhost:8000/api/favorites/ \
  -H "Authorization: Token your_token"
```

## Technology Stack

- **Backend:** Django 5.1, Django REST Framework
- **Database:** PostgreSQL
- **Cache:** Redis
- **Task Queue:** Celery + RabbitMQ
- **External API:** TMDb (The Movie Database)
- **Email:** Zoho SMTP
- **Documentation:** drf-yasg (Swagger/OpenAPI)
- **Dependencies:** See requirements.txt

## Project Structure

```
nexus/
├── nexus/              # Django project settings
│   ├── settings.py     # Main configuration with Redis cache
│   ├── urls.py         # URL routing
│   └── celery.py       # Celery configuration
├── movies/             # Movies app
│   ├── models.py       # Movie, Genre, FavoriteMovie models
│   ├── views.py        # API views with caching
│   ├── serializers.py  # DRF serializers
│   ├── filters.py      # Custom filters
│   ├── urls.py         # Movie API endpoints
│   └── management/     # Management commands
│       └── commands/
│           └── fetch_tmdb_movies.py  # TMDb data sync
├── users/              # Users app
│   ├── models.py       # UserProfile model
│   ├── views.py        # User authentication views
│   ├── serializers.py  # User serializers
│   ├── urls.py         # User API endpoints
│   └── tasks.py        # Celery email tasks
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── README.md          # This file
```

## Troubleshooting

### Common Issues

#### Redis Connection Issues
```bash
# Check if Redis is running
sudo systemctl status redis-server

# Test Redis connection
redis-cli ping

# Check Django cache connection
python manage.py shell
from django.core.cache import cache
cache.set('test', 'hello', 60)
print(cache.get('test'))
```

#### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -h localhost -U nexus_user -d nexus_db

# Check database settings in .env file
# Ensure DB_PASSWORD, DB_USER, DB_NAME are correct
```

#### TMDb API Issues
```bash
# Test API key
curl "https://api.themoviedb.org/3/movie/popular?api_key=YOUR_API_KEY"

# Check API key in .env file
# Ensure TMDB_API_KEY is valid
```

#### Email Issues
```bash
# Test email settings in Django shell
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'from@email.com', ['to@email.com'])
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