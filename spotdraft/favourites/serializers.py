from rest_framework import serializers
from .models import Movie, Planet, MovieFavourite, PlanetFavourite


class MovieSerializer(serializers.ModelSerializer):
    is_favourite = serializers.SerializerMethodField()
    updated = serializers.DateTimeField(source='edited')

    class Meta:
        model = Movie
        fields = ('title', 'release_date', 'created', 'updated', 'url', 'is_favourite')

    def get_is_favourite(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            return MovieFavourite.objects.filter(movie=obj, user_id=user_id).exists()
        return False

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        custom_title = self.context.get('custom_title')
        if custom_title:
            rep['title'] = custom_title
        return rep


class PlanetSerializer(serializers.ModelSerializer):
    is_favourite = serializers.SerializerMethodField()
    updated = serializers.DateTimeField(source='edited')

    class Meta:
        model = Planet
        fields = ('name', 'created', 'url', 'updated', 'is_favourite')

    def get_is_favourite(self, obj):
        user_id = self.context.get('user_id')
        if user_id:
            return PlanetFavourite.objects.filter(planet=obj, user_id=user_id).exists()
        return False

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        custom_title = self.context.get('custom_title')
        if custom_title:
            rep['name'] = custom_title
        return rep

class MovieFavouriteSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()

    class Meta:
        model = MovieFavourite
        fields = ('user_id', 'movie', 'custom_title')


class PlanetFavouriteSerializer(serializers.ModelSerializer):
    planet = serializers.StringRelatedField()

    class Meta:
        model = PlanetFavourite
        fields = ('user_id', 'planet', 'custom_title')


class FavouriteSerializer(serializers.Serializer):
    movie = MovieFavouriteSerializer(read_only=True)
    planet = PlanetFavouriteSerializer(read_only=True)

    class Meta:
        fields = ('user_id', 'planet', 'movie', 'custom_title')

