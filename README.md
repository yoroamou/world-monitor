# World Monitoring Dashboard

A full-stack Django application that provides an interactive, dark-themed world map. When you click on any country, it dynamically fetches live news articles for that region and uses natural language processing (NLP) to generate a concise AI summary of the current events.

## Features

- **Interactive World Map:** Powered by Leaflet.js and rendered with a premium dark theme. Click on any country to trigger data fetching.
- **Live News Integration:** Fetches real-time news articles using the [MediaStack API](https://mediastack.com/).
- **AI Text Summarization:** Uses `sumy` (LexRank algorithm) and `nltk` to read the descriptions of the fetched articles and extract the 3 most insightful sentences locally on the CPU (no expensive external AI API required).
- **Smart Caching:** News and summaries are temporarily cached in the database (30-minute TTL) to prevent exhausting the free-tier API limits.
- **Premium UI:** Built with Tailwind CSS, featuring glassmorphism cards, custom scrollbars, and dynamic state transitions (loading/empty states).

## Tech Stack

- **Backend:** Django 6.0, Python 3
- **Database:** SQLite (local development) / NeonDB PostgreSQL (production ready)
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
- **Map Rendering:** Leaflet.js, CartoDB Dark Matter tiles, Natural Earth GeoJSON
- **NLP Summarization:** `sumy`, `nltk`, `numpy`

## Getting Started

### Prerequisites

- Python 3.10+
- A free API key from [MediaStack](https://mediastack.com/signup/free)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd world-monitor
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory based on the provided template and add your MediaStack API key:
   ```env
   # .env
   DJANGO_SECRET_KEY=your_secret_key_here
   DEBUG=True
   MEDIASTACK_API_KEY=your_mediastack_api_key_here
   
   # Uncomment and configure if using NeonDB/PostgreSQL:
   # DATABASE_URL=postgresql://username:password@your-neon-host.neon.tech/neondb?sslmode=require
   ```

5. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create an Admin User (Optional but recommended):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

8. Open your browser and navigate to `http://127.0.0.1:8000/`.

## Project Structure

- `worldmonitor/` - Django project settings and root routing.
- `dashboard/` - Main Django application containing views, API endpoints, services (NLP & API fetching), and models.
- `dashboard/templates/` - HTML layout files.
- `static/` - Custom CSS (`style.css`) and JavaScript (`dashboard.js`).
- `requirements.txt` - Python dependencies.

## Acknowledgements

- UI design inspired by modern analytics dashboards.
- Map boundaries provided by [Natural Earth](https://www.naturalearthdata.com/) via the geo-boundaries-world-110m dataset.
