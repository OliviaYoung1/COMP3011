# Spotify Playlist Curator — Music Analytics API & Dashboard

A full‑stack music analytics project built using Django REST Framework and a custom JavaScript frontend.  
The system allows users to create and manage playlists, search for tracks, and explore a dataset of songs using advanced filtering and analytics tools.

---

## Project Overview

The Spotify Playlist Curator provides:

- A RESTful API for playlist management (CRUD)
- Endpoints for searching and filtering tracks
- Analytics endpoints for exploring popularity and genre trends
- A Track Explorer that returns the top 10 most popular songs matching user‑selected filters, which can be used by users to find songs to add to playlists 
- A fully interactive frontend dashboard styled in a Spotify‑inspired UI

The goal is to help users discover suitable songs for their playlists by filtering the dataset by genre, mood, and audio features.

The dataset used contains thousands of songs on spotify, along with information about those tracks: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

---

## Features

### Playlist Management (CRUD)
- Create playlists  
- View playlists  
- Update playlist details  
- Delete playlists  
- Add/remove tracks  

### Track Explorer
Filter by:
- Genre  
- Danceability  
- Energy  
- Valence  
- Tempo  
- Explicit content  

Returns the top 10 most popular tracks matching the filters.

### Frontend Dashboard
- Responsive UI  
- Real‑time API integration  
- Track search  
- Playlist builder  

---

## Tech Stack

### Backend
- Python 3  
- Django  
- Django REST Framework  
- SQLite (local development)

### Frontend
- HTML  
- CSS  
- JavaScript (Fetch API)

---
-
## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/OliviaYoung1/COMP3011.git
cd COMP3011/spotify_api
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
```
macOS / Linus
```bash
source venv/bin/activate
```
Windows
```bash
venv\Scripts\activate
```
### 3. Install dependencies
```bash
cd .. && pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Run the development server
```bash
python manage.py runserver
```
### API URL
The API will be available at:
```
http://127.0.0.1:8000/api/
```
### Running the Frontend
From inside the frontend folder, run:
```bash
cd frontend
python -m http.server 5500
```
Then open
```
http://127.0.0.1:5500/index.html
```

## API Documentation

Full API documentation is available in the following PDF:

📄 **[API_Documentation.pdf](docs/API_Documentation.pdf)**

