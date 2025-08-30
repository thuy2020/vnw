from django.contrib import admin
from django.urls import path, include
from people import views as people_views
from organizations import views as org_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('people/', include('people.urls')),
    path('organizations/', include('organizations.urls')),
    path('organizations/tree/', org_views.org_tree, name='organization_tree'),
    path('scraper/', include('scraper.urls')),
    path('', people_views.home, name='home'),  # Home page view
]
