from django.shortcuts import render
from django.views.generic import ListView
from .models import News


class ViewNews(ListView):
	model = News
	template_name = 'upload/news_list.html'
	context_object_name = 'news'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Головна'
		return context

	def get_queryset(self):
		return News.objects.all()
