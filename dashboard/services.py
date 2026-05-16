import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk
from .models import Country, Article, SummaryInsight
import logging

logger = logging.getLogger(__name__)

# Ensure NLTK punkt is available for sumy
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

def fetch_and_update_news(country_code):
    """
    Fetch news for a specific country from MediaStack API and update local DB.
    Returns the Country object.
    """
    country_code = country_code.lower()
    
    # Get or create the country
    country, created = Country.objects.get_or_create(
        code=country_code,
        defaults={'name': country_code.upper()} # In a real app we'd map code to actual name
    )

    # Check cache TTL (30 minutes)
    now = timezone.now()
    if country.last_fetched and (now - country.last_fetched) < timedelta(minutes=30):
        return country # Use cached data

    api_key = settings.MEDIASTACK_API_KEY
    if not api_key:
        logger.error("MEDIASTACK_API_KEY not configured.")
        return country

    url = f"http://api.mediastack.com/v1/news"
    params = {
        'access_key': api_key,
        'countries': country_code,
        'limit': 10,
        'languages': 'en'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Clear old articles to avoid infinite growth
        Article.objects.filter(country=country).delete()

        if 'data' in data and data['data']:
            for item in data['data']:
                Article.objects.create(
                    country=country,
                    title=item.get('title', 'No Title'),
                    description=item.get('description', ''),
                    source=item.get('source', 'Unknown Source'),
                    url=item.get('url', '#'),
                    image_url=item.get('image', None),
                    published_at=item.get('published_at') # MediaStack returns ISO 8601 string which Django parses
                )
        
        country.last_fetched = now
        country.save()

    except Exception as e:
        logger.error(f"Error fetching news for {country_code}: {e}")
    
    return country

def generate_country_summary(country):
    """
    Generate an AI extractive summary based on the fetched news articles using Sumy.
    """
    articles = Article.objects.filter(country=country)
    
    if not articles.exists():
        return "No recent news available to summarize."

    # Concatenate all descriptions/titles
    text_corpus = " ".join([
        (a.description or a.title) for a in articles
    ])

    if len(text_corpus) < 200:
        return "Insufficient news data to generate a meaningful summary."

    try:
        parser = PlaintextParser.from_string(text_corpus, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        
        # Extract the 3 most important sentences
        summary_sentences = summarizer(parser.document, 3)
        if not summary_sentences:
            return "Unable to extract meaningful sentences from the available news."
            
        summary_text = " ".join([str(sentence) for sentence in summary_sentences])

        # Save to DB
        insight, created = SummaryInsight.objects.update_or_create(
            country=country,
            defaults={'summary_text': summary_text}
        )
        return summary_text
    
    except Exception as e:
        logger.exception(f"Error generating summary: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Failed to generate summary: {str(e)}"

