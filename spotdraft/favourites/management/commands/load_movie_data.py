import requests
from django.core.management.base import BaseCommand
from favourites.models import Movie, Planet
from django.core.management import execute_from_command_line

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://sw-api-rwjfuiltyq-el.a.run.app/api/films"
        response = requests.get(url)
        data = response.json()

        results = data.get("results", [])

        for result in results:
            movie = Movie(
                title=result["title"],
                episode_id=result["episode_id"],
                opening_crawl=result["opening_crawl"],
                director=result["director"],
                producer=result["producer"],
                release_date=result["release_date"],
                characters=", ".join(result["characters"]),
                planets=", ".join(result["planets"]),
                starships=", ".join(result["starships"]),
                vehicles=", ".join(result["vehicles"]),
                species=", ".join(result["species"]),
                created=result["created"],
                edited=result["edited"],
                url=result["url"]
            )
            movie.save()

        self.stdout.write(self.style.SUCCESS("Movie Data loaded successfully."))

if __name__ == "__main__":
    execute_from_command_line()