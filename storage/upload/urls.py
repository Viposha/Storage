from django.urls import path
from .views import ViewNews, model_form_upload

urlpatterns = [
	path('', ViewNews.as_view(), name='home'),
	path('upload/', model_form_upload, name='upload')
]