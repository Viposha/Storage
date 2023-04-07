from django.urls import path
from .views import ViewNews, model_form_upload, register, login

urlpatterns = [
	path('', ViewNews.as_view(), name='home'),
	path('upload/', model_form_upload, name='upload'),
	path('register/', register, name='register'),
	path('login/', login, name='login'),
]