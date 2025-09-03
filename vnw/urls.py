from django.contrib import admin
from django.urls import path, include
from people import views as people_views
from organizations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('people/', include('people.urls')),
    path('organizations/', include('organizations.urls')),
    path('scraper/', include('scraper.urls')),
    path('', people_views.home, name='home'),  # Home page view
    path("export/", include("export.urls")),
]
