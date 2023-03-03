from django.db import models

# Create your models here.


# class Movie(models.Model):
#     director_name = models.CharField(max_length=255)
#     release_year = models.IntegerField()
#     ratings = models.FloatField()


# Model relationships: In your current implementation, you have defined each model
# as a separate table in the database, with no relationship between them. However,
# it might make more sense to define a single model for a movie, which includes fields
# for the director name, release year, and ratings. This will allow you to store all
# the movie data in a single table, which can make it easier to query and manage the data.


# Create models: In Django, models are used to define the structure of your app's data.
# You'll need to create a model that defines the fields you want to collect from users.
# For example, if you want users to enter a movie's director name, release year, and reviews,
# you might create a model with three fields: director_name, release_year, and reviews. You'll
# also need to set up the database connection in your Django app's settings.
