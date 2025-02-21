 Spotify App

This project is a web application that displays top artists and genres from Spotify. It uses the Spotify API to fetch user data and visualize it in a user-friendly manner.

## Features

- Display top artists
- Display top songs

## Technologies Used

- Django
- Next.js


## Windows Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/vphilavong/Musilytic.git
    cd Musilytic
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your Spotify API credentials:
    - Create a `.env` file in the `app/` directory and add your Spotify API credentials:
      ```env
      SPOTIPY_CLIENT_ID='your_client_id'
      SPOTIPY_CLIENT_SECRET='your_client_secret'
      SPOTIPY_REDIRECT_URI='your_redirect_uri'
      ```

5. Run start.py from root:
    ```sh
    # Ensure you are in app directory
    python start.py
    ```

6. Open your browser and navigate to `http://127.0.0.1:3000/` to see the application.


