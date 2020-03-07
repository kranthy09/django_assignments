from django.urls import path

from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.get_list_of_questions, name='base'),
    path('create/', views.create_question, name='create'),
    path('<int:question_id>/get/', views.get_question, name='get_question'),
    path('<int:question_id>/update/', views.update_question, name='update'),
    path('<int:question_id>/delete/', views.delete_question, name='delete'),
]
