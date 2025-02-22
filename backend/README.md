# Mango Backend

Django backend for Mango, a Spotify analytics application that visualizes your music preferences and listening habits.

## This README includes:
1. All your API endpoints from urls.py
2. Your project structure
3. The SpotifyToken model details
4. Setup instructions for both local and Docker environments

## Features

- Spotify OAuth Authentication
- Top Artists Analysis
- Top Tracks Analysis
- Genre Distribution
- Recently Played Tracks
- User Session Management

## Tech Stack

- Django 5.1
- Django REST Framework
- Python 3.11
- Spotify Web API

## API Endpoints

### Authentication
- `GET /login/` - Initiates Spotify OAuth flow
- `GET /callback/` - Handles Spotify OAuth callback

### Dashboard Endpoints

## Setup Instructions

### Prerequisites
- Python 3.11+
- Spotify Developer Account
- pip

### Development Setup

1. Set up environment variables:
Create a `.env` file in the root directory:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/callback
```

2. Run migrations:
```sh
python manage.py migrate
```
3. Run the development server:
```sh
python manage.py runserver
```

## Backend Structure

```
backend/
├── api/ # API endpoints
├── config/ # Django settings
├── dashboard/ # Main application views
├── spotify/ # Spotify integration
│ ├── migrations/ # Database migrations
│ ├── models.py # Data models
│ └── views.py # View logic
├── manage.py # Django management script
└── requirements.txt # Python dependencies
```


## Models

### SpotifyToken
- `user`: CharField, unique user identifier
- `created_at`: DateTimeField, token creation timestamp
- `refresh_token`: CharField, Spotify refresh token
- `access_token`: CharField, Spotify access token
- `expires_in`: DateTimeField, token expiration time
- `token_type`: CharField, token type identifier

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Run tests
5. Submit a pull request