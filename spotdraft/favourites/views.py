from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Movie, Planet, MovieFavourite, PlanetFavourite, Favorite
from .serializers import MovieSerializer, PlanetSerializer,  MovieFavouriteSerializer, PlanetFavouriteSerializer
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.query_params.get('user_id', None)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.query_params.get('user_id', None)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class FavouriteViewSet(viewsets.ViewSet):
    def list(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

        movie_favourites = MovieFavourite.objects.filter(user_id=user_id)
        planet_favourites = PlanetFavourite.objects.filter(user_id=user_id)

        movie_serializer = MovieFavouriteSerializer(movie_favourites, many=True, context={'user_id': user_id})
        planet_serializer = PlanetFavouriteSerializer(planet_favourites, many=True, context={'user_id': user_id})

        return Response({'movies': movie_serializer.data, 'planets': planet_serializer.data})

    def create(self, request):
        user_id = request.data.get('user_id')
        movie_id = request.data.get('movie_id')
        planet_id = request.data.get('planet_id')
        custom_title = request.data.get('custom_title')

        if not user_id or not (movie_id or planet_id):

            return Response({"error": "user_id and either movie_id or planet_id are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if movie_id:
            try:
                movie = Movie.objects.get(id=movie_id)
            except Movie.DoesNotExist:
                return Response({"error": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Check if the MovieFavourite record already exists
            try:
                favourite = MovieFavourite.objects.get(user_id=user_id, movie=movie)
                # Update the custom_title if it needs to be modified
                if custom_title:
                    favourite.custom_title = custom_title
                    favourite.save()
            except MovieFavourite.DoesNotExist:
                # Create a new MovieFavourite record
                favourite = MovieFavourite.objects.create(user_id=user_id, movie=movie, custom_title=custom_title)
        else:
            try:
                planet = Planet.objects.get(id=planet_id)
            except Planet.DoesNotExist:
                return Response({"error": "Planet does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Check if the PlanetFavourite record already exists
            try:
                favourite = PlanetFavourite.objects.get(user_id=user_id, planet=planet)
                # Update the custom_title if it needs to be modified
                if custom_title:
                    favourite.custom_title = custom_title
                    favourite.save()
            except PlanetFavourite.DoesNotExist:
                # Create a new PlanetFavourite record
                favourite = PlanetFavourite.objects.create(user_id=user_id, planet=planet, custom_title=custom_title)


        serializer = self.get_favourite_serializer(favourite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favourite = self.get_favourite_by_id(pk, user_id)
        except Favorite.DoesNotExist:
            return Response({"error": "Favourite does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_favourite_serializer(favourite)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user_id = request.data.get('user_id')
        custom_title = request.data.get('custom_title')

        if not user_id:
            return Response({"error": "user_id parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favourite = self.get_favourite_by_id(pk, user_id)
        except Favorite.DoesNotExist:
            return Response({"error": "Favourite does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if custom_title:
            favourite.custom_title = custom_title
            favourite.save()

        serializer = self.get_favourite_serializer(favourite)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favourite = self.get_favourite_by_id(pk, user_id)
        except Favorite.DoesNotExist:
            return Response({"error": "Favourite does not exist"}, status=status.HTTP_404_NOT_FOUND)

        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_favourite_by_id(self, pk, user_id):
        try:
            return Favorite.objects.get(id=pk, user_id=user_id)
        except Favorite.DoesNotExist:
            raise

    def get_favourite_serializer(self, favourite):
        if isinstance(favourite, MovieFavourite):
            return MovieFavouriteSerializer(favourite)
        elif isinstance(favourite, PlanetFavourite):
            return PlanetFavouriteSerializer(favourite)
        else:
            raise ValueError("Invalid favourite object")
