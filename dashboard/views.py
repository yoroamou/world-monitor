from django.shortcuts import render
from django.http import JsonResponse
from .services import fetch_and_update_news, generate_country_summary
from .models import Article, SummaryInsight, Country

def dashboard_view(request):
    """Render the main dashboard page."""
    context = {
        'total_countries': Country.objects.count(),
        'total_articles': Article.objects.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)

def country_data_api(request, country_code):
    """API endpoint to fetch data for a country when clicked on the map."""
    if not country_code:
        return JsonResponse({'error': 'Country code is required'}, status=400)
        
    country = fetch_and_update_news(country_code)
    
    # Trigger summary generation
    summary_text = generate_country_summary(country)
    
    articles = Article.objects.filter(country=country).order_by('-published_at')[:10]
    articles_data = [{
        'title': a.title,
        'description': a.description,
        'source': a.source,
        'url': a.url,
        'image_url': a.image_url,
        'published_at': a.published_at.strftime("%Y-%m-%d %H:%M") if a.published_at else "Recent"
    } for a in articles]

    return JsonResponse({
        'country_code': country.code,
        'country_name': country.name,
        'summary': summary_text,
        'articles': articles_data,
        'last_fetched': country.last_fetched.strftime("%Y-%m-%d %H:%M") if country.last_fetched else None
    })
