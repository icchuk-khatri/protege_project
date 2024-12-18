from django.contrib import admin
from django.urls import include, path
# from ontology_app import views  # Import views from ontology_app

urlpatterns = [
    # path('', views.index, name='homePage'),  # Root URL for index
    path('admin/', admin.site.urls),  # Admin site
    path('', include('ontology_app.urls')),  # Include app-specific routes
    
]
