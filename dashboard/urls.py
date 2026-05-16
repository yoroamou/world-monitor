from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/country/<str:country_code>/', views.country_data_api, name='country_data_api'),
]
