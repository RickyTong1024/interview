from django.urls import path
from interview import views

urlpatterns = [
    path('problem_update/', views.problem_update, name = 'problem_update'),
    path('problem_list/', views.problem_list, name = 'problem_list'),
    path('problem/', views.problem, name = 'problem'),
    path('problem_language/', views.problem_language, name = 'problem_language'),
    path('problem_submit/', views.problem_submit, name = 'problem_submit'),
]
