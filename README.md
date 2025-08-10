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
  # 🎬 Nexus - Movie Recommendation Platform

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/nexus)

A production-ready Django REST API for movie recommendations, featuring real-time data from The Movie Database (TMDb), Redis caching, asynchronous email processing, and comprehensive user management.

## 🌐 Live Demo

**API Base URL**: https://nexus-kingsley.up.railway.app

- **📚 API Documentation**: https://nexus-kingsley.up.railway.app/api/docs/
- **🔧 Admin Panel**: https://nexus-kingsley.up.railway.app/admin/
- **📊 API Root**: https://nexus-kingsley.up.railway.app/api/

## ✨ Features

### 🎭 Movie Features
- **Multiple Movie Categories**: Popular, Top Rated, Upcoming, Now Playing
- **Trending Movies**: Daily and weekly trending content
- **Genre Management**: Organized movie categorization
- **Search & Filtering**: Advanced movie discovery
- **TMDb Integration**: Real-time movie data and posters
- **Caching**: Redis-powered performance optimization

### 👤 User Features  
- **Authentication**: Token-based API authentication
- **User Profiles**: Customizable user information
- **Favorites System**: Save and manage favorite movies
- **Email Notifications**: Async welcome emails via Celery
- **Admin Interface**: Full Django admin panel

### 🚀 Technical Features
- **REST API**: Comprehensive RESTful endpoints
- **Database**: PostgreSQL with optimized queries
- **Caching**: Redis for high-performance responses
- **Async Tasks**: Celery with Redis broker
- **Documentation**: Auto-generated Swagger/OpenAPI docs
- **Production Ready**: Deployed on Railway with health checks

## 🏗️ Tech Stack

- **Backend**: Django 5.1 + Django REST Framework
- **Database**: PostgreSQL (Railway managed)
- **Cache**: Redis (Railway managed)
- **Task Queue**: Celery + Redis
- **Email**: SMTP (Zoho/Gmail compatible)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Deployment**: Railway with Nixpacks
- **External API**: The Movie Database (TMDb)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- TMDb API Key ([Get one here](https://www.themoviedb.org/settings/api))
- Redis (for caching and Celery)
- PostgreSQL (optional for local dev)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/TheKingsident/nexus.git
cd nexus
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
# TMDb API
TMDB_API_KEY=your_tmdb_api_key

# Database (SQLite for local dev)
DATABASE_URL=sqlite:///db.sqlite3

# Redis
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_HOST=smtp.zoho.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@example.com

# Security
SECRET_KEY=your-secret-key
DEBUG=True
```

5. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Populate Database**
```bash
python manage.py fetch_tmdb_movies
```

7. **Start Services**

Terminal 1 - Django:
```bash
python manage.py runserver
```

Terminal 2 - Celery Worker:
```bash
celery -A nexus worker --loglevel=info
```

Terminal 3 - Redis (if not system service):
```bash
redis-server
```

## 📡 API Endpoints

### 🎬 Movies
```
GET  /api/movies/                    # All movies
GET  /api/movies/{id}/               # Movie detail
GET  /api/movies/popular/            # Popular movies  
GET  /api/movies/top-rated/          # Top rated movies
GET  /api/movies/upcoming/           # Upcoming movies
GET  /api/movies/now-playing/        # Now playing movies
GET  /api/movies/trending/day/       # Daily trending
GET  /api/movies/trending/week/      # Weekly trending
GET  /api/movies/search/?q=query     # Search movies
GET  /api/movies/genres/             # All genres
```

### 👤 Users
```
POST /api/users/register/            # User registration
POST /api/users/login/               # User login
POST /api/users/logout/              # User logout
GET  /api/users/me/                  # Current user info
GET  /api/users/profile/             # User profile
PUT  /api/users/profile/             # Update profile
```

### ⭐ Favorites
```
GET  /api/movies/favorites/                    # User's favorites
POST /api/movies/favorites/add/{movie_id}/     # Add to favorites
POST /api/movies/favorites/remove/{movie_id}/  # Remove from favorites
```

### 🔧 Admin & Health
```
GET  /api/users/admin-status/        # Check superuser status
POST /api/users/create-admin/        # Create admin user
GET  /health/                        # Health check
GET  /api/                          # API root
```

## 🚀 Deployment

### Railway Deployment (Recommended)

1. **Fork this repository**

2. **Connect to Railway**
   - Visit [Railway](https://railway.app)
   - Create new project from GitHub repo
   - Select your forked nexus repository

3. **Add Environment Variables**
   ```
   TMDB_API_KEY=your_tmdb_api_key
   EMAIL_HOST=smtp.zoho.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-password
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=noreply@example.com
   ```

4. **Add Services**
   - **PostgreSQL**: Add from Railway marketplace
   - **Redis**: Add from Railway marketplace
   - Copy connection URLs to your environment

5. **Deploy**
   - Railway auto-deploys on git push
   - Database migrations run automatically
   - Superuser created automatically if env vars set

### Manual Deployment

For other platforms, ensure:
- Python 3.11+ runtime
- PostgreSQL database
- Redis instance  
- Environment variables configured
- Run: `./start.sh` or individual commands from Procfile

## 🏛️ Project Structure

```
nexus/
├── 📁 nexus/                    # Django project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # WSGI application
│   └── celery.py                # Celery configuration
├── 📁 movies/                   # Movies app
│   ├── models.py                # Movie, Genre, FavoriteMovie models
│   ├── views.py                 # Movie API views with caching
│   ├── serializers.py           # DRF serializers
│   ├── urls.py                  # Movie endpoints
│   └── 📁 management/commands/
│       └── fetch_tmdb_movies.py # TMDb data population
├── 📁 users/                    # Users app  
│   ├── models.py                # UserProfile model
│   ├── views.py                 # Authentication & profile views
│   ├── serializers.py           # User serializers
│   ├── urls.py                  # User endpoints
│   ├── tasks.py                 # Celery email tasks
│   └── 📁 management/commands/
│       └── create_admin.py      # Superuser creation
├── 📁 staticfiles/              # Static files (auto-generated)
├── 🐳 Procfile                  # Process definitions
├── 🚀 start.sh                  # Startup script with auto-setup
├── 🛠️ railway.toml              # Railway configuration  
├── 📋 requirements.txt          # Python dependencies
└── 📖 README.md                 # This file
```

## 🔧 Configuration

### Caching Strategy
- **Popular movies**: 15 minutes
- **Top rated movies**: 1 hour  
- **Trending movies**: 5 minutes
- **Movie details**: 30 minutes
- **Search results**: 10 minutes

### Email Configuration
- **Welcome emails**: Sent asynchronously via Celery
- **Retry logic**: 3 attempts with exponential backoff
- **Fallback**: Synchronous sending if Celery unavailable

### Database Optimization
- **Connection pooling**: Optimized for Railway PostgreSQL
- **Query optimization**: Select related for foreign keys
- **Indexing**: Optimized for common queries

## 🧪 Testing

### API Testing
```bash
# Test popular movies endpoint
curl https://nexus-kingsley.up.railway.app/api/movies/popular/

# Test user registration
curl -X POST https://nexus-kingsley.up.railway.app/api/users/register/ 
  -H "Content-Type: application/json" 
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

# Test admin status
curl https://nexus-kingsley.up.railway.app/api/users/admin-status/
```

### Health Checks
```bash
# Basic health check
curl https://nexus-kingsley.up.railway.app/health/

# Database and cache status
curl https://nexus-kingsley.up.railway.app/api/
```

## 🐛 Troubleshooting

### Common Issues

**1. TMDb API Errors**
```bash
# Verify API key
curl "https://api.themoviedb.org/3/movie/popular?api_key=YOUR_API_KEY"
```

**2. Email Not Sending**
- Check SMTP credentials in environment variables
- Verify Celery worker is running
- Check Railway logs for email errors

**3. Caching Issues**
```bash
# Test Redis connection
redis-cli -u $REDIS_URL ping
```

**4. Database Connection**
- Verify DATABASE_URL in environment
- Check Railway PostgreSQL service status

### Logs
```bash
# Railway logs
railway logs

# Local development
python manage.py runserver --verbosity=2
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`  
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Ensure all tests pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Email**: hello@kingsleyusa.dev
- **Issues**: [GitHub Issues](https://github.com/TheKingsident/nexus/issues)
- **Documentation**: [API Docs](https://nexus-kingsley.up.railway.app/api/docs/)

## 🙏 Acknowledgments

- **The Movie Database (TMDb)** for providing movie data
- **Railway** for hosting infrastructure
- **Django REST Framework** for the excellent API framework
- **Redis** for caching and task queue capabilities

---

⭐ **Star this repository if you found it helpful!**sonalized recommendations.

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
- **Swagger UI:** http://localhost:8000/swagger/, http://localhost:8000/api/docs/
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