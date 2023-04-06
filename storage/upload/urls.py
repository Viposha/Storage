from django.urls import path
from .views import ViewNews

urlpatterns = [
	path('', ViewNews.as_view(), name='home')
]