from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)
    last_fetched = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Article(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=500)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SummaryInsight(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='summary')
    summary_text = models.TextField()
    generated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Summary for {self.country.name}"
