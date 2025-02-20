 Spotify App

This project is a web application that displays top artists and genres from Spotify. It uses the Spotify API to fetch user data and visualize it in a user-friendly manner.

## Features

- Display top artists
- Display top genres with a transparent pie chart
- Responsive design

## Technologies Used

- Python
- Django
- Matplotlib
- HTML/CSS
- JavaScript

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/vphilavong/spotify-app.git
    cd spotify-app
    ```

2. Create a virtual environment and activate it:
    ```sh
    venv\Scripts\activate  # On Windows
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your Spotify API credentials:
    - Create a `.env` file in the root directory and add your Spotify API credentials:
      ```env
      SPOTIPY_CLIENT_ID='your_client_id'
      SPOTIPY_CLIENT_SECRET='your_client_secret'
      SPOTIPY_REDIRECT_URI='your_redirect_uri'
      ```

5. Run the Django development server:
    ```sh
    cd spotiapp
    python manage.py runserver
    ```

6. Open your browser and navigate to `http://127.0.0.1:8000/` to see the application.

## Usage

- Navigate to the homepage to see your top artists.
- Click on the "Top Genres" link to see a pie chart of your top genres.