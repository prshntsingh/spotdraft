from django.urls import include, path
from rest_framework import routers
from .views import MovieViewSet, PlanetViewSet, FavouriteViewSet

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'planets', PlanetViewSet, basename='planet')
router.register(r'favourites', FavouriteViewSet, basename='favourite')

urlpatterns = [
    path('', include(router.urls)),
]
