# SpotDRAFT MovieMatic

This is a Django application that [provide a brief description of what the application does].

## Prerequisites

Before running the application, ensure that you have the following prerequisites installed on your system:

- Python (version 3.8.+)
- Django (version 4.2.+)


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/prshntsingh/spotdraft.git
    ```

2. Navigate to the project directory:

    ```bash
    cd spotdraft
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv env
    ```

4. Activate the virtual environment:

    ```bash
    source env/bin/activate
    ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Perform the initial database migration:

    ```bash
    python manage.py migrate
    ```

## Configuration


1. Load planets and movies from the JSON API using this command
   ```commandline
   python manage.py load_planets_data 
   python manage.py load_movie_data
   ```
2. Add the  `.env` and add `DJANGO_SETTINGS_MODULE=spotdraft.settings` in .env.

3. Alternatively `export DJANGO_SETTINGS_MODULE=spotdraft.settings`


## Usage

To run the Django development server, use the following command:

```bash
python manage.py runserver
```

The application will be accessible at http://localhost:8000/.

## Endpoints

### Movies

- **Retrieve all movies:** `GET /api/movies/`
- **Retrieve a specific movie:** `GET /api/movies/{id}/`
- **Search movies by title:** `GET /api/movies/search/?title={search_query}`

### Planets

- **Retrieve all planets:** `GET /api/planets/`
- **Retrieve a specific planet:** `GET /api/planets/{id}/`
- **Search planets by name:** `GET /api/planets/search/?name={search_query}`

### Favorites

- **Retrieve favorite movies and planets for a user:** `GET /api/favourites/?user_id={user_id}`
- **Create a new favorite for a user:** `POST /api/favourites/`
- **Retrieve a specific favorite for a user:** `GET /api/favourites/{id}/?user_id={user_id}`
- **Update a specific favorite for a user:** `PUT /api/favourites/{id}/?user_id={user_id}`
- **Partially update a specific favorite for a user:** `PATCH /api/favourites/{id}/?user_id={user_id}`
- **Delete a specific favorite for a user:** `DELETE /api/favourites/{id}/?user_id={user_id}`

Replace `{id}` with the corresponding ID of the movie, planet, or favorite. Similarly, replace `{user_id}` with the user ID.

