import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worldmonitor.settings')
django.setup()

from dashboard.services import fetch_and_update_news, generate_country_summary

try:
    c = fetch_and_update_news("US")
    summary = generate_country_summary(c)
    print("Summary Result:", summary)
except Exception as e:
    print("Error:", e)
