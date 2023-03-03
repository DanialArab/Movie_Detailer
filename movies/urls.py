from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_search, name='movie_search'),
    path('results/', views.movie_results, name='movie_results'),
    # path('chart/', views.movie_chart, name='movie_chart'), # to get the plot of metascore vs titles:
]
