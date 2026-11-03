# MovieHub 🎬

A Python-based movie search and recommendation application that uses the OMDb API to search for movies and display essential movie information through a modern web interface.

## Problem Statement

Develop a movie search and recommendation application that allows users to search for movies and view relevant movie information using an external movie API.

## Assigned Feature Set

**Feature Set A**

The assigned features are:

* Search movies
* Display movie title
* Display movie poster
* Display movie rating
* Display basic movie details

## Features Implemented

MovieHub currently implements the assigned Feature Set A:

* 🔎 Search movies by title
* 🎬 Display movie titles
* 🖼️ Display movie posters
* ⭐ Display IMDb ratings
* 📋 Display basic movie information
* 🔍 Open detailed information for a selected movie
* 🌐 Fetch movie information dynamically using the OMDb API
* 📱 Responsive web interface
* 🎨 Modern cinematic user interface

## Technologies Used

### Backend

* Python
* Flask
* Requests
* python-dotenv

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite

### API

* OMDb API

### Development Tools

* Visual Studio Code
* Git
* GitHub

## Project Architecture

```text
User
  ↓
HTML / CSS / JavaScript
  ↓
Flask Backend
  ↓
OMDb API
  ↓
Movie Data
  ↓
Web Interface
```

SQLite is included in the project for application data storage and future extensibility.

## Project Structure

```text
MovieHub/
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
│
├── services/
│   ├── __init__.py
│   └── omdb.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── templates/
    └── index.html
```

## AI Tools Used

AI tools were used as learning and development assistants during the project.

AI assistance was used for:

* Understanding the problem statement
* Planning the application architecture
* Understanding Flask routes and API communication
* Generating and improving code
* Debugging errors
* Testing application functionality
* Improving the user interface
* Understanding Git and GitHub workflow
* Preparing project documentation

The generated or suggested code was reviewed, tested, understood, and modified during development.

## Important AI Prompts / AI Usage

Examples of AI assistance used during development include:

* Planning the architecture for a Python Flask movie search application.
* Understanding how to integrate the OMDb API with Flask.
* Creating Flask API routes for movie search and movie details.
* Debugging Python and Flask errors.
* Designing and improving the MovieHub frontend.
* Understanding Git initialization, commits, branches, and GitHub remote repositories.
* Preparing project documentation and README structure.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/sarvesh6401/MovieHub.git
cd MovieHub
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On Windows:

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the OMDb API key

Create a `.env` file in the project root:

```text
OMDB_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own OMDb API key.

### 6. Initialize the database

```cmd
python database.py
```

### 7. Start the Flask application

```cmd
python app.py
```

Open the local application in a browser:

```text
http://127.0.0.1:5000
```

## Testing

The application was tested during development for:

* Flask server startup
* OMDb API connectivity
* Movie search
* Movie poster display
* Movie rating display
* Movie details retrieval
* Error handling for invalid searches
* Frontend interaction
* Database initialization

## Security

The OMDb API key is stored in the `.env` file and is excluded from Git using `.gitignore`.

The `.env` file is **not included in the GitHub repository**.

## Screenshots

Screenshots of the working application can be added here.

Example:

```text
![MovieHub Home Page](screenshots/home.png)
```

## Future Improvements

Possible future improvements include:

* User authentication
* Favorites
* Watchlist
* Advanced filtering
* Genre-based recommendations
* Movie history
* Improved recommendation algorithms

These features are outside the currently assigned Feature Set A.

## Author

**Sarvesh**

BCA Student

## Repository

[MovieHub GitHub Repository](https://github.com/sarvesh6401/MovieHub.git?utm_source=chatgpt.com)
