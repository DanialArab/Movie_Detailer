import matplotlib.pyplot as plt
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

import requests
import json


# Create your views here.

# The OMDB API returns search results in batches of 10 by default.
# To get more results, I need to use the page parameter in my API call.

def movie_search(request):
    if request.method == 'POST':
        # title = request.POST['title']
        title = request.POST.get('title', '')
        release_year = request.POST['release_year']
        genre = request.POST.get('genre')

        api_key = settings.API_KEY

        # # Build the API parameters dictionary based on user input
        # Set default values for the parameters
        params = {
            's': title,
            'apikey': api_key
        }

        # Add title and genre parameters if they have a value
        if release_year:
            params['y'] = release_year
        if genre:
            params['g'] = genre

        # Make API call to OMDBAPI.com
        response = requests.get('http://www.omdbapi.com/', params=params)

        movie_data = json.loads(response.text)

        if 'Search' in movie_data:
            for movie in movie_data['Search']:
                # Make another API call to get full plot information for each movie
                response = requests.get('http://www.omdbapi.com/', params={
                    'i': movie['imdbID'],
                    'plot': 'full',
                    'apikey': api_key
                })
                movie_info = json.loads(response.text)

                # Add plot information to each movie dictionary
                movie.update(movie_info)

        # Store movie data in session
        request.session['movie_data'] = movie_data

        # Redirect to movie_results URL
        return redirect('movies:movie_results')
    else:
        return render(request, 'movie_search.html')


def movie_results(request):
    movie_data = {}
    if 'movie_data' in request.session:
        movie_data = request.session['movie_data']
        del request.session['movie_data']
    return render(request, 'movie_results.html', {'movie_data': movie_data})

# to get the plot of metascore vs titles:

# def movie_results(request):
#     movie_data = {}
#     if 'movie_data' in request.session:
#         movie_data = request.session['movie_data']
#         del request.session['movie_data']

#         # Extract movie titles and metascores from API response
#         movie_titles = []
#         metascores = []
#         for movie in movie_data['Search']:
#             movie_titles.append(movie['Title'])
#             metascores.append(movie['Metascore'])

#         # Pass movie titles and metascores to template
#         return render(request, 'movie_results.html', {'movie_titles': movie_titles, 'metascores': metascores})
#     else:
#         return redirect('movies:movie_search')


# def movie_chart(request):
#     movie_data = {}
#     if 'movie_data' in request.session:
#         movie_data = request.session['movie_data']['Search']
#         metascores = [int(movie['Metascore']) if movie['Metascore']
#                       != 'N/A' else 0 for movie in movie_data]
#         titles = [movie['Title'] for movie in movie_data]
#         y_pos = np.arange(len(titles))

#         plt.barh(y_pos, metascores)
#         plt.yticks(y_pos, titles)
#         plt.xlabel('Metascore')
#         plt.title('Movie Metascores')
#         plt.tight_layout()

#         # Save chart to a bytes buffer
#         buffer = BytesIO()
#         plt.savefig(buffer, format='png')
#         buffer.seek(0)
#         chart_image = base64.b64encode(buffer.getvalue()).decode()
#         plt.close()

#         return render(request, 'movie_chart.html', {'chart_image': chart_image})
