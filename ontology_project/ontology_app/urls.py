from django.urls import path
from . import views

# app_name = 'ontology_app'  # Namespace for app-specific URLs

urlpatterns = [
    path('', views.index, name='homePage'),  # Homepage
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('query-data/', views.query_data, name='query_data'),  # Non-root paths
    path('get_formulas/', views.get_formulas, name='get_formulas'),
    path('get_variables/', views.get_variables, name='get_variables'),
    path('calculate_formula/', views.calculate_formula, name='calculate_formula'),
]
