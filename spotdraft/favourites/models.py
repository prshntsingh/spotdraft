from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField()
    director = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    release_date = models.DateField()
    characters = models.TextField()
    planets = models.TextField()
    starships = models.TextField()
    vehicles = models.TextField()
    species = models.TextField()
    created = models.DateTimeField()
    edited = models.DateTimeField()
    url = models.URLField()

    def __str__(self):
        return self.title


class Planet(models.Model):
    name = models.CharField(max_length=255)
    rotation_period = models.CharField(max_length=255)
    orbital_period = models.CharField(max_length=255)
    diameter = models.CharField(max_length=255)
    climate = models.CharField(max_length=255)
    gravity = models.CharField(max_length=255)
    terrain = models.CharField(max_length=255)
    surface_water = models.CharField(max_length=255)
    population = models.CharField(max_length=255)
    residents = models.TextField()
    films = models.TextField()
    created = models.DateTimeField()
    edited = models.DateTimeField()
    url = models.URLField()

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user_id = models.IntegerField()
    custom_title = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"User: {self.user_id}, {self.get_favorited_object()}"

    def get_favorited_object(self):
        raise NotImplementedError("Subclasses must implement get_favorited_object()")


class MovieFavourite(Favorite):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def get_favorited_object(self):
        return f"Movie: {self.movie.title}"

class PlanetFavourite(Favorite):
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)

    def get_favorited_object(self):
        return f"Planet: {self.planet.name}"

