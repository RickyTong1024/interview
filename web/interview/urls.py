from django.urls import path
from interview import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login, name = "login"),
    path('logout/',  views.logout, name = "logout"),
    path('problem_update/', views.problem_update, name = 'problem_update'),
    path('problem_list/', views.problem_list, name = 'problem_list'),
    path('problem/', views.problem, name = 'problem'),
    path('problem_language/', views.problem_language, name = 'problem_language'),
    path('problem_submit/', views.problem_submit, name = 'problem_submit'),
    path('problem_view_submit/', views.problem_view_submit, name = 'problem_view_submit'),
    path('examinations/', views.examinations, name = 'examinations'),
	path('examination_update/', views.examination_update, name = 'examination_update'),
    path('users/', views.users, name = 'users'),
	path('user_update/', views.user_update, name = 'user_update'),
    path('examination/', views.examination, name = 'examination'),
]
