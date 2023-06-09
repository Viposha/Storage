from django.urls import path
from .views import ViewNews, model_form_upload, register, user_login, user_logout, ChangeRankView, AccountView

urlpatterns = [
	path('', ViewNews.as_view(), name='home'),
	path('upload/', model_form_upload, name='upload'),
	path('register/', register, name='register'),
	path('login/', user_login, name='login'),
	path('logout/', user_logout, name='logout'),
	path('change/', ChangeRankView.as_view(), name='change_rank'),
	path('account', AccountView.as_view(), name='account')
]
