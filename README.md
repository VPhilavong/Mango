# Mango

A web application that visualizes your Spotify listening habits, displaying top artists, songs, and genres using the Spotify API.

## Features

- OAuth2 Authentication with Spotify
- Display Top Artists
- Display Top Songs
- Genre Analysis

## Tech Stack

### Backend
- Django 5.1
- Django REST Framework
- Python 3.11
- Spotify Web API

### Frontend
- Next.js
- TypeScript
- Tailwind CSS

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker and Docker Compose (optional)
- Spotify Developer Account

### Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/vphilavong/Musilytic.git
cd Musilytic
```

2. Create a `.env` file in the root directory:
```
SPOTIFY_CLIENT_ID='your_client_id'
SPOTIFY_CLIENT_SECRET='your_client_secret'
SPOTIFY_REDIRECT_URI='http://localhost:8000/api/callback/'
```

### Docker Setup

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Access the application:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000


## Contributing

1. Clone the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues
1. **Spotify Authentication Failed**
   - Verify your Spotify API credentials
   - Check REDIRECT_URI matches your Spotify app settings

2. **Docker Issues**
   - Ensure ports 3000 and 8000 are available
   - Check Docker logs: `docker-compose logs`

3. **CORS Issues**
   - Verify CORS settings in Django's settings.py
   - Check frontend API calls use correct backend URL

## Authors

- Vincent Philavong
