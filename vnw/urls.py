from django.contrib import admin
from django.urls import path, include
from people import views as people_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('people/', include('people.urls')),
    path('', people_views.home, name='home'),  # Home page view
]
