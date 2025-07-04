from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_items, name='search_items'),
    path('changes/', views.show_change_log, name='show_change_log'),
    path('scrape/', views.trigger_scrape, name='trigger_scrape'),
]
