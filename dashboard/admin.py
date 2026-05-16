from django.contrib import admin
from .models import Country, Article, SummaryInsight

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'last_fetched')
    search_fields = ('code', 'name')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'source', 'published_at', 'fetched_at')
    list_filter = ('country', 'source', 'published_at')
    search_fields = ('title', 'description')

@admin.register(SummaryInsight)
class SummaryInsightAdmin(admin.ModelAdmin):
    list_display = ('country', 'generated_at')
    search_fields = ('country__name', 'summary_text')
